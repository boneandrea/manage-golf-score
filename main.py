from flask import Flask, jsonifyin
from flask_cors import cross_origin

import os

app = Flask(__name__)


@app.route('/')
@cross_origin(origins=["http://localhost:5173"], methods=["GET"])
def index():
    data = [
        {
            "name": "上條栄子",
            "gross": 95
        },
        {
            "name": "北村友成",
            "gross": 88
        },
        {
            "name": "飯沼茂",
            "gross": 75
        },
        {
            "name": "高田由美子",
            "gross": 101
        },
        {
            "name": "高田由美子",
            "gross": 101
        },
        {
            "name": "高田由美子",
            "gross": 101
        },
        {
            "name": "高田由美子",
            "gross": 101
        },
        {
            "name": "高田由美子",
            "gross": 101
        },
        {
            "name": "高田由美子",
            "gross": 101
        },
        {
            "name": "高田由美子",
            "gross": 101
        },
        {
            "name": "高田由美子",
            "gross": 101
        },
        {
            "name": "高田由美子",
            "gross": 101
        },
        {
            "name": "高田由美子",
            "gross": 101
        },
        {
            "name": "高田由美子",
            "gross": 101
        },
        {
            "name": "高田由美子",
            "gross": 101
        },
        {
            "name": "高田由美子",
            "gross": 101
        },
    ]

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
