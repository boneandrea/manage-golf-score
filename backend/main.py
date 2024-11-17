from flask import Flask, jsonify, request, Response, json
from flask_cors import cross_origin
from bson.json_util import dumps
from bson.objectid import ObjectId

from datetime import datetime

import os
import dateutil.parser

from database import *
from igolf import *
from marshalI import *
from golfweb import *

# from logging.config import dictCjjjjonfig
import logging
# dictConfig({
#     'version': 1,
#     'formatters': {'default': {
#         'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
#     }},
#     'handlers': {'wsgi': {
#         'class': 'logging.StreamHandler',
#         'stream': 'ext://flask.logging.wsgi_errors_stream',
#         'formatter': 'default'
#     }},
#     'root': {
#         'level': 'INFO',
#         'handlers': ['wsgi']
#     }
# })


app = Flask(__name__)
# app.logger.setLevel(logging.INFO)
app.logger.setLevel(logging.DEBUG)

# .envの`PORT`は勝手に読まれる

FRONTEND = os.getenv("FRONTEND_URL")
print(FRONTEND)
app.logger.debug("HELLO")


# 過去データindex
@app.route('/api/find', methods=["GET"])
@cross_origin(origins=[FRONTEND, "http://localhost:8003/"], methods=["GET"])
def find():
    items = readAll()
    return dumps(items, default=str)


# 過去データdownload
@app.route('/api/download', methods=["GET"])
@cross_origin(origins=[FRONTEND, "http://localhost:8003/"], methods=["GET"])
def download():
    items = readAll()
    json_str = dumps(items, default=str, ensure_ascii=False)
    # レスポンスを作成してContent-Dispositionヘッダーを設定し、ダウンロードさせる
    # jsでファイル名つけるのも可能
    response = Response(json_str, content_type='application/json')
    # response.headers['Content-Disposition'] = "golf.json"
    return response


# 過去データ読み取り
@app.route('/api/findOne/<id>', methods=["GET"])
@cross_origin(origins=[FRONTEND, "http://localhost:8003/"], methods=["GET"])
def findOne(id):
    item = readOne(id)
    return dumps(item, default=str)


# 過去データupdate
@app.route('/api/update', methods=["POST"])
@cross_origin(origins=[FRONTEND, "http://localhost:8003/"], methods=["POST"])
def update():
    try:
        app.logger.debug("sending.....")
        updateOne(request.json)
        app.logger.debug("sent")
        return jsonify({"status": "success"})

    except ValueError as e:
        return jsonify({
            "status": "error",
            "reason": str(e)
        })

    except Exception as e:
        app.logger.debug(e)
        return jsonify({
            "status": "error",
            "reason": e
        })

    return jsonify({"fe": FRONTEND})

# 過去データ読み取り


@app.route('/api/remove/<id>', methods=["POST"])
@cross_origin(origins=[FRONTEND, "http://localhost:8003/"], methods=["POST"])
def remove(id):
    deleteOne(id)
    return dumps({}, default=str)


@app.route('/api/get', methods=["POST"])
@cross_origin(origins=[FRONTEND, "http://localhost:8003/"], methods=["GET", "POST"])
def get():
    # readdata()
    try:
        url = request.json["url"]
        app.logger.debug(f"fetching {url}....")
        x = golfweb()
        scores = x.get_scores(url)
        return jsonify(scores)

    except ValueError as e:
        return jsonify({
            "status": "error",
            "reason": str(e)
        })

    except Exception as e:
        app.logger.debug(e)
        return jsonify({
            "status": "error",
            "reason": e
        })


def readdata():
    app.logger.debug("read mongodb....")
    client = database().connect_db()
    db = client["score"]
    score = db["score"]
    items = score.find()
    return json.dumps(arr, default=str)
    app.logger.debug(f"num of data: {score.count_documents({})}")


def readAll():
    app.logger.debug("read mongodb....")
    client = database().connect_db()
    db = client["score"]
    score = db["score"]
    return list(score.find())


def readOne(id):
    app.logger.debug("read one; mongodb....")
    app.logger.debug(id)
    client = database().connect_db()
    db = client["score"]
    score = db["score"]
    item = score.find_one({"_id": ObjectId(id)})
    return item


def updateOne(json):
    app.logger.debug("update one; mongodb....")
    client = database().connect_db()
    db = client["score"]
    score = db["score"]
    app.logger.debug(json)
    id = json["id"]
    del json["id"]
    json["date"] = dateutil.parser.parse(
        json["date"])  # from string to ISODate
    score.update_one({"_id": ObjectId(id)}, {"$set": json})
    return {}


def deleteOne(id):
    client = database().connect_db()
    db = client["score"]
    score = db["score"]
    score.delete_one({"_id": ObjectId(id)})
    return {}


@app.route('/api/store', methods=["POST"])
@cross_origin(origins=[FRONTEND, "http://localhost:8003"], methods=["GET", "POST"])
def store():
    try:
        app.logger.debug("sending.....")
        store_score(request.json)
        app.logger.debug("sent")
        return jsonify({"status": "success"})

    except ValueError as e:
        return jsonify({
            "status": "error",
            "reason": str(e)
        })

    except Exception as e:
        app.logger.debug(e)
        return jsonify({
            "status": "error",
            "reason": e
        })


def store_score(result):
    client = database().connect_db()
    db = client["score"]
    score = db["score"]

    result["date"] = dateutil.parser.parse(
        result["date"])  # from string to ISODate
    result["created_at"] = datetime.now()
    score.insert_one(result)


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
