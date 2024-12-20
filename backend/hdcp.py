from flask import Flask, jsonify, request, Response, json, Blueprint, current_app, make_response
from flask_cors import cross_origin
from bson.json_util import dumps
from bson.objectid import ObjectId
from database import *
import logging

module_hdcp = Blueprint('hdcp', __name__)
FRONTEND = os.getenv("FRONTEND_URL")


@module_hdcp.route('/api/download', methods=["GET"])
@cross_origin(origins=[FRONTEND, "http://localhost:8003/"], methods=["GET"])
def download():
    response = make_response()
    client = database().connect_db()
    members = client["score"]["members"]
    items = members.find()
    return dumps(items, default=str), 200
