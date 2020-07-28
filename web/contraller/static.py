# -*- coding: utf-8 -*-  ##这个只是临时用  在部署的时候就用不上了
from flask import Blueprint,send_from_directory
from application import app


route_static = Blueprint('static', __name__)
@route_static.route("/<path:filename>")
def index( filename ):
    return send_from_directory(  app.root_path + "/web/static/" ,filename )