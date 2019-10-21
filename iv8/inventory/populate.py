import os

import random
random.seed(666)

from datetime import datetime
from datetime import timedelta

import redis

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


if __name__ == "__main__":
  populate()
