from flask import Flask, jsonify
from flask_cors import cross_origin
from flask import request
from bson.json_util import dumps

from datetime import datetime

import os

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
app.logger.setLevel(logging.INFO)

# .envの`PORT`は勝手に読まれる

FRONTEND = os.getenv("FRONTEND_URL")
print(FRONTEND)
app.logger.debug("HELLO")


# 過去データ読み取り
@app.route('/api/find', methods=["GET"])
@cross_origin(origins=[FRONTEND, "http://localhost:8003/"], methods=["GET", "POST"])
def find():
    data = readOne()
    app.logger.debug(data)
    return data


# 過去データupdate
@app.route('/api/update', methods=["POST"])
@cross_origin(origins=[FRONTEND, "http://localhost:8003/"], methods=["GET", "POST"])
def update():
    return jsonify({"fe": FRONTEND})


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


def readOne():
    app.logger.debug("read mongodb....")
    client = database().connect_db()
    db = client["score"]
    score = db["score"]
    items = list(score.find())
    return dumps(items, default=str)


@ app.route('/api/store', methods=["POST"])
@ cross_origin(origins=[FRONTEND, "http://localhost:8003"], methods=["GET", "POST"])
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

    import dateutil.parser
    result["date"] = dateutil.parser.parse(
        result["date"])  # from string to ISODate
    result["created_at"] = datetime.now()
    score.insert_one(result)


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
