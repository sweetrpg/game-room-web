#!/bin/bash

set -x
set -e
set -o pipefail

cat > .$$.sql <<EOF
INSERT INTO "user_roles"
("user_id", "role_id", "enabled")
VALUES
((SELECT "id" FROM users WHERE "email" = 'paul@schifferers.net'),
 (SELECT "id" FROM roles WHERE "name" = 'admin'),
 true)
;
EOF
psql -d postgres -f .$$.sql
rm -f .$$.sql
