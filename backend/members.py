from flask import Flask, jsonify, request, Response, json, Blueprint, current_app
from flask_cors import cross_origin
from bson.json_util import dumps
from bson.objectid import ObjectId
from database import *
import logging


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
    payload = request.json["members"]
    client = database().connect_db()
    db = client["score"]
    members = db["members"]

    try:
        # TODO: transaction
        for member in payload:
            members.update_one({"_id": ObjectId(member["_id"]["$oid"])},
                               {"$set": {"hdcp": member["hdcp"]}})
    except Exception as e:
        return dumps([], default=str), 500
        pass

    return dumps([], default=str), 200


@module_api.route('/api/members/add', methods=["POST"])
@cross_origin(origins=[FRONTEND, "http://localhost:8003/"], methods=["POST"])
def add():
    payload = request.json["member"]
    logger = current_app.logger

    client = database().connect_db()
    members = client["score"]["members"]
    payload["name"] = payload["name"].strip().replace(" ", "").replace("　", "")

    try:
        result = members.insert_one(payload)
    except Exception as e:
        return dumps([], default=str), 500
        pass

    return dumps({"_id": {"$oid": str(result.inserted_id)}, "name": payload["name"], "hdcp": payload["hdcp"]}, default=str), 200


@module_api.route('/api/members/remove', methods=["POST"])
@cross_origin(origins=[FRONTEND, "http://localhost:8003/"], methods=["POST"])
def remove():
    payload = request.json["member"]
    id = payload["id"]
    logger = current_app.logger
    client = database().connect_db()
    members = client["score"]["members"]

    try:
        members.delete_one({"_id": ObjectId(id)})
    except Exception as e:
        return dumps([], default=str), 500
        pass

    return dumps({"remove": True}, default=str), 200
