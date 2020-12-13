#!/usr/bin/env bash
# startup script for wuestbot on gunicorn

# Project Name
NAME="wuestbot"

# Host to listen on
HOST=127.0.0.1

# Port to listen on
PORT=5000

# Number of gunicorn Workers
NUM_WORKERS=1

# Databank directory
DB_DIR=app/database

# create database
# source $DB_DIR/db_create.py

# create venv
source venv/bin/activate

# startup server
exec gunicorn $NAME:app \
    -b $HOST:$PORT \
    -w $NUM_WORKERS \