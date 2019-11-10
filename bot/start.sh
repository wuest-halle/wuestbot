#!/usr/bin/env sh
# startup script for wuestbot on gunicorn

# Project Name
NAME="wuestbot"

# Host to listen on
HOST=127.0.0.1

# Port to listen on
PORT=8443

# Number of gunicorn Workers
NUM_WORKERS=2

# Databank directory
DB_DIR=app/database

# start venv
source venv/bin/activate

# create database
source $DB_DIR/db_create.py

# startup server
exec gunicorn $NAME:app \
    -b $HOST:$PORT \
    -w $NUM_WORKERS \