#!/bin/bash

scripts/reset-db.sh
rm -rf migrations
scripts/setup-db.sh
scripts/seed-db.sh
