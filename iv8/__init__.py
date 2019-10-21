import os
import logging

LOG_LEVEL = os.environ.get("LOG_LEVEL") or "DEBUG"

logger = logging.getLogger(__name__)

FORMAT  = "[%(asctime)s] [%(name)s] [%(process)d] [%(levelname)s] %(message)s"
DATEFMT = "%Y-%m-%d %H:%M:%S %z"

logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt=DATEFMT)
formatter = logging.Formatter(FORMAT, DATEFMT)

# silence requests logger a bit
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

# adjust gunicorn logger to global level and formatting 
gunicorn_logger = logging.getLogger("gunicorn.error")
gunicorn_logger.handlers[0].setFormatter(formatter)
gunicorn_logger.setLevel(logging.getLevelName(LOG_LEVEL))

logging.getLogger("gunicorn.error").setLevel(logging.INFO)
logging.getLogger("engineio.client").setLevel(logging.WARN)
logging.getLogger("engineio.server").setLevel(logging.WARN)
logging.getLogger("socketio.client").setLevel(logging.WARN)

from flask import Flask
import flask_restful
from flask import make_response

import json

def output_json(data, code, headers=None):
  resp = make_response(json.dumps(data), code)
  resp.headers.extend(headers or {})
  return resp

server = Flask(__name__)

api = flask_restful.Api(server)
api.representations = { 'application/json': output_json }

import iv8.interface
import iv8.socketio

import iv8.broker.rest

import iv8.inventory
import iv8.inventory.rest

import iv8.shop
import iv8.shop.rest

logger.info("web/api server is ready.")
