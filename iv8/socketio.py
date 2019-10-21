import eventlet
eventlet.monkey_patch()

import logging

logger = logging.getLogger(__name__)

from flask import request

import json

import redis

from flask_socketio import SocketIO, emit, join_room, leave_room

from iv8 import server, broker

socketio = SocketIO(server)

@socketio.on('connect')
def on_connect():
  logger.info("connect: {0})".format(request.sid))

@socketio.on('disconnect')
def on_disconnect():
  logger.info("disconnect: {0}".format(request.sid))

def emit_to_browser():
  while True:
    socketio.sleep(0.1)
    event, msg = broker.get("browser")
    socketio.emit("incoming", json.dumps({ "event" : event, "msg" : msg }))
    logger.info("emitted {0}".format(msg))

socketio.start_background_task(target=emit_to_browser)
