import os
import logging

logger = logging.getLogger(__name__)

from datetime import datetime
from datetime import timedelta

import random
random.seed(666)

import redis

from iv8 import broker
from iv8.socketio import socketio

def update(units, db=0, publish=True):
  r = redis.Redis.from_url(
    os.environ.get("REDIS_URL", "redis://localhost"),
    db=db
  )
  step = timedelta(days=1)
  keys   = []
  values = []
  with r.pipeline() as pipe:
    for unit in units:
      start = datetime.strptime(unit["start"], "%Y%m%d")
      end   = datetime.strptime(unit["end"], "%Y%m%d")
      while start <= end:
        day = start.strftime("%Y%m%d")
        key = ":".join([unit["supplier"], unit["component"], unit["unit"], day])
        # TODO non-default partitions
        keys.append(key)
        pipe.hincrby(key, "default", unit["amount"])
        start += step
    values = pipe.execute()

  if any(v <= 0 for v in values):
    with r.pipeline() as pipe:
      for key, value in zip(keys, values):
        if value <= 0: pipe.delete(key)
        if value < 0 and publish:
          broker.publish("NegativeInventoryDetected", key)
      pipe.execute()
  if publish:
    for unit in units:
      broker.publish("InventoryTransactionCreated", unit)  

def apply(transaction, db=0):
  update([transaction], db=db, publish=False)

def get(db=0):
  r = redis.StrictRedis.from_url(
    os.environ.get("REDIS_URL", "redis://localhost"),
    db=db, charset="utf-8", decode_responses=True
  )
  i = {}
  for key in r.keys("supplier*"):
    i[key] = r.hgetall(key)
  return i

def reset():
  r = redis.Redis.from_url(os.environ.get("REDIS_URL", "redis://localhost"))
  r.flushall()

def populate(db=0, suppliers=2, components=2500, units=10, days=1000, partitions=10):
  r = redis.Redis.from_url(
    os.environ.get("REDIS_URL", "redis://localhost"),
    db=db
  )
  now = datetime.now()
  dates = [ (now + timedelta(days=i)).strftime("%Y%m%d") for i in range(days) ]

  for component in range(components):
    print(component)
    ckey = ":component" + str(component)
    with r.pipeline() as pipe:
      for supplier in range(suppliers):
        skey = "supplier" + str(supplier) + ckey
        for unit in range(units):
          ukey = skey + ":unit" + str(unit)
          for date in dates:
            value = {}
            for partition in range(partitions):
              value["partition"+str(partition)] = int(10 * random.random()) 
            pipe.hmset(ukey + ":" + date, value)
      pipe.execute()

def process_unit_acquired_event(msg):
    supplier = msg["supplier"]
    units = []
    for unit in msg["units"]:
      units.append({
        "supplier" : "supplier"  + str(supplier),
        "component": "component" + str(unit["component"]),
        "unit"     : "unit"      + str(unit["unit"]),
        "start"    : unit["from"],
        "end"      : unit["to"],
        "amount"   : unit["amount"]
      })
    update(units)

def process_product_sold_event(msg):
  units = []
  for unit in msg["units"]:
    units.append({
      "supplier" : "supplier"  + str(unit["supplier"]),
      "component": "component" + str(unit["component"]),
      "unit"     : "unit"      + str(unit["unit"]),
      "start"    : msg["from"],
      "end"      : msg["to"],
      "amount"   : -1
    })
  update(units)

def process_events():
  while True:
    socketio.sleep(0.1)
    event, msg = broker.get("inventory")
    logger.info("received {0}".format(event))
    {
      "UnitsAcquired" : process_unit_acquired_event,
      "ProductSold"   : process_product_sold_event
    }[event](msg)

socketio.start_background_task(target=process_events)

if __name__ == "__main__":
  populate()
