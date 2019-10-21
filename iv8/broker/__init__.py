import os
import logging

logger = logging.getLogger(__name__)

import json

import redis

broker = redis.StrictRedis.from_url(
  os.environ.get("REDIS_URL", "redis://localhost"),
  db=0, charset="utf-8", decode_responses=True
)

distribution = {
  "UnitsAcquired"               : [ "inventory" ],
  "ProductSold"                 : [ "inventory" ],
  "InventoryTransactionCreated" : [ "shop" ]
}

def publish(event, payload):
  try:
    msg = json.dumps( (event, payload), default=str)
    broker.lpush("browser", msg)
    for consumer in distribution[event]:
      logger.info("delivering to {0}: {1} = {2}".format(consumer, event, payload))
      broker.lpush(consumer, msg)
  except KeyError:
    logging.error("no consumers for {}".format(event))

def get(queue):
  _, msg = broker.blpop(queue)
  return json.loads(msg)
