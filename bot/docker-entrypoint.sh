#!/bin/sh

echo "install dependencies"
python -m  pip install -r /app/requirements.txt 

echo "start server"
gunicorn wuestbot:app -b 0.0.0.0:8443 -w 1 --access-logfile -

exec "$@"