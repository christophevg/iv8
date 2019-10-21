from flask_restful import Resource

from iv8 import api, inventory

class InventoryCache(Resource):
  def get(self):
    return inventory.get(db=5)

api.add_resource(InventoryCache, "/api/shop/inventory")
