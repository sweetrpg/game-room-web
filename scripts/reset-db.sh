#!/bin/bash

set -x
set -e
set -o pipefail

export $(cat .env | xargs)

cat > .$$.sql <<EOF
DROP DATABASE $PGDATABASE;
CREATE DATABASE $PGDATABASE OWNER $PGUSER;
EOF
psql -d postgres -f .$$.sql
rm -f .$$.sql
