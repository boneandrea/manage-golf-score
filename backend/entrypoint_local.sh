#!/bin/bash

pip install -U pip && pip install -r requirements.txt
gunicorn main:app -b 0.0.0.0:8000 --reload
