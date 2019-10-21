from flask_restful import Resource

from iv8 import api, inventory

class Inventory(Resource):
  def get(self):
    return inventory.get(db=0)

api.add_resource(Inventory, "/api/inventory/inventory")


class Reset(Resource):
  def delete(self):
    return inventory.reset()

api.add_resource(Reset, "/api/inventory/reset")
