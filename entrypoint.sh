#!/bin/bash

cd backend
echo $PORT
gunicorn main:app
