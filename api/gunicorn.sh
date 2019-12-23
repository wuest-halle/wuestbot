#!/usr/bin/env bash

ENVIRONMENT=production prometheus_multiproc_dir=${1} gunicorn --config gunicorn.conf.py run:app
