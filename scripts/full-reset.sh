#!/bin/bash

set -x
set -e
set -o pipefail

env_file=${1:.env}

scripts/reset-db.sh $env_file
rm -rf migrations
scripts/setup-db.sh $env_file
scripts/seed-db.sh $env_file
