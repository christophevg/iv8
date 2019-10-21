import logging

logger = logging.getLogger(__name__)

from iv8          import broker, inventory
from iv8.socketio import socketio

# simulating a read-cache on db instance 5, applying transactions to our copy

def process_inventory_transaction_created_event(transaction):
  inventory.apply(transaction, db=5)

# handle events delivered to our queue

def process_events():
  while True:
    socketio.sleep(0.1)
    event, msg = broker.get("shop")
    logger.info("received {0}".format(event))
    {
      "InventoryTransactionCreated" : process_inventory_transaction_created_event
    }[event](msg)

socketio.start_background_task(target=process_events)
