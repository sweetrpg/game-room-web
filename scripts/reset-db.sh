#!/bin/bash

set -x
set -e
set -o pipefail

export $(cat .env | xargs)

export PGPASSWORD=$POSTGRES_PASSWORD
cat > .$$.sql <<EOF
DROP DATABASE $POSTGRES_DB;
CREATE DATABASE $POSTGRES_DB OWNER $POSTGRES_USER;
EOF
psql -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER -d postgres -f .$$.sql
rm -f .$$.sql
