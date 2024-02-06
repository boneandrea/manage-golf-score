from flask import Flask, jsonify
from flask_cors import cross_origin
from flask import request

import os
from database import *
from igolf import *
from marshalI import *
from golfweb import *

# from logging.config import dictConfig

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

# .envの`PORT`は勝手に読まれる


@app.route('/get', methods=["POST"])
@cross_origin(origins=["http://localhost:5173"], methods=["GET", "POST"])
def get():
    readdata()
    try:
        url = request.json["url"]
        print(url)
        x = golfweb()
        scores = x.get_scores(url)
        return jsonify(scores)

    except ValueError as e:
        return jsonify({
            "status": "error",
            "reason": str(e)
        })

    except Exception as e:
        print(e)
        return jsonify({
            "status": "error",
            "reason": e
        })


def readdata():
    print("read mongodb....")
    client = database().connect_db()
    db = client["score"]
    score = db["score"]
    items = score.find()
    print(f"num of data: {score.count_documents({})}")


@app.route('/store', methods=["POST"])
@cross_origin(origins=["http://localhost:5173"], methods=["POST"])
def store():
    try:
        readdata()
        print("sending.....")
        store_score(request.json)
        print("sent")
        return jsonify({"status": "success"})

    except ValueError as e:
        return jsonify({
            "status": "error",
            "reason": str(e)
        })

    except Exception as e:
        print(e)
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

    score.insert_one(result)


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
