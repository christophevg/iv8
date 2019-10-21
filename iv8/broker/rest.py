import logging

logger = logging.getLogger(__name__)

from flask import request
from flask_restful import Resource

import json

from iv8 import api, inventory, broker

# event publication end points

class UnitsAcquired(Resource):
  def post(self):
    msg = json.loads(request.get_json())
    logger.info("received UnitsAcquired event")
    logger.debug(msg)
    broker.publish("UnitsAcquired", msg)
    return True

api.add_resource(UnitsAcquired, "/api/broker/UnitsAcquired")

class ProductSold(Resource):
  def post(self):
    msg = json.loads(request.get_json())
    logger.info("received ProductSold event")
    logger.debug(msg)
    broker.publish("ProductSold", msg)

api.add_resource(ProductSold, "/api/broker/ProductSold")
