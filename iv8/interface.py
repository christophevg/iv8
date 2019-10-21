import os

import logging

logger = logging.getLogger(__name__)

from flask  import render_template, send_from_directory
from flask  import request, redirect, abort
from jinja2 import TemplateNotFound

from iv8 import server

@server.route("/")
@server.route("/<string:name>.html")
def render_landing(name="index"):
  try:
    return render_template(name+".html")
  except TemplateNotFound:
    abort(404)
