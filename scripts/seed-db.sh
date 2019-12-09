#!/bin/bash

set -x
set -e
set -o pipefail

env=$1

export $(cat .env | xargs)
export PGHOST=$POSTGRES_HOST
export PGPORT=$POSTGRES_PORT
export PGDATABASE=$POSTGRES_DB
export PGUSER=$POSTGRES_USER
export PGPASSWORD=$POSTGRES_PW

psql -f seed-data/users.sql
psql -f seed-data/game-systems.sql
