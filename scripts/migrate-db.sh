#!/bin/bash

set -x
set -e
set -o pipefail

export $(cat .env | xargs)

python3 manage.py db migrate
python3 manage.py db upgrade
