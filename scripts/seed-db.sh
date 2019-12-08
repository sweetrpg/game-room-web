#!/bin/bash

set -x
set -e
set -o pipefail

env=$1

export $(cat configs/${env}.env | xargs)
export PGHOST=$POSTGRES_HOST
export PGPORT=$POSTGRES_PORT
export PGDATABASE=$POSTGRES_DB
export PGUSER=$POSTGRES_USER
export PGPASSWORD=$POSTGRES_PW

python manage.py db init
python manage.py db migrate
python manage.py db upgrade

psql -f seed-data/users.sql
psql -f seed-data/game-systems.sql
