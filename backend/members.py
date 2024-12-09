from flask import Flask, jsonify, request, Response, json, Blueprint
from flask_cors import cross_origin
from bson.json_util import dumps
from bson.objectid import ObjectId
from database import *


module_api = Blueprint('members', __name__)
FRONTEND = os.getenv("FRONTEND_URL")


@module_api.route('/api/members/', methods=["GET"])
@cross_origin(origins=[FRONTEND, "http://localhost:8003/"], methods=["GET"])
def index():
    items = readAll()
    return dumps(items, default=str)


def readAll():
    client = database().connect_db()
    db = client["score"]
    members = db["members"]
    items = []
    for member in members.find():
        print(members)

    return list(members.find())


@module_api.route('/api/members/update', methods=["POST"])
@cross_origin(origins=[FRONTEND, "http://localhost:8003/"], methods=["POST"])
def update():
    items = readAll()
    return dumps(items, default=str)
