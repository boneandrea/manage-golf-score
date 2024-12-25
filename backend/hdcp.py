from flask import Flask, jsonify, request, Response, json, Blueprint, current_app, make_response
import io as cStringIO
import codecs
import csv
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
    sjis = map(lambda x: {"name": x["name"].encode(
        "shift_jis"), "hdcp": x["hdcp"]}, items)

    csv_file = cStringIO.StringIO()
    writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
    x = []
    x.append(("あああ", "1"))
    writer.writerows(x)

    response.data = csv_file.getvalue().encode("shift_jis")
    current_app.logger.debug(response.data)
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = u'attachment; filename=a.csv'
    return response
    # return dumps(items, default=str), 200
