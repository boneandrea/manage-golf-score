from flask import Flask, jsonify
from flask_cors import cross_origin
import os
from database import *
from igolf import *
from marshalI import *
from golfweb import *

app = Flask(__name__)

# .envの`PORT`は勝手に読まれる


@app.route('/')
@cross_origin(origins=["http://localhost:5173"], methods=["GET"])
def index():
    readdata()
    try:
        print("fetching.....")
        x = golfweb()
        scores = x.get_scores(
            "https://v2anegasaki.igolfshaper.com/anegasaki/score/2nf6slre#/landscape-a")
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
    for i in items:
        print(i)
    print(f"num of data: {score.count_documents({})}")


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
