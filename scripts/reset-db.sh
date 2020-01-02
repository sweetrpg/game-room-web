#!/bin/bash

set -x
set -e
set -o pipefail

export $(cat .env | xargs)

cat > .$$.sql <<EOF
DROP DATABASE $POSTGRES_DB;
CREATE DATABASE $POSTGRES_DB OWNER $POSTGRES_USER;
EOF
psql -d postgres -f .$$.sql
rm -f .$$.sql
