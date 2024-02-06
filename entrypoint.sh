#!/bin/bash

service nginx start
cd backend
gunicorn main:app
