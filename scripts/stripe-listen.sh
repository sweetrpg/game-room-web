#!/bin/bash

set -x
set -e
set -o pipefail

export $(cat .env | xargs)

stripe listen --forward-to localhost:5000/billing/stripe/webhook
