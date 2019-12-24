#!/bin/bash

set -x
set -e
set -o pipefail

scripts/reset-db.sh
rm -rf migrations
scripts/setup-db.sh
scripts/seed-db.sh
