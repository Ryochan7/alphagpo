#!/bin/bash

DIR=$(dirname "${BASH_SOURCE[0]}")
DIR=$(realpath "${DIR}")

cd $DIR
source $DIR/venv/bin/activate

envdir envs/prod celery -A mygpo beat --pidfile=/tmp/celerybeat.pid -S django &
envdir envs/prod celery -A mygpo worker --concurrency=3 -l info -Ofair &
envdir envs/prod gunicorn mygpo.wsgi -c conf/gunicorn.conf.py &

wait
pkill -P $$

