#!/bin/bash

set -x
set -e
set -o pipefail

env=$1

export $(cat .env | xargs)

psql -f seed-data/users.sql
psql -f seed-data/game-systems.sql
