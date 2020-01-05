#!/bin/bash

set -x
set -e
set -o pipefail

env_file=${1:.env}

export $(cat $env_file | xargs)

python3 manage.py db migrate
python3 manage.py db upgrade
