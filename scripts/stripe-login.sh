#!/bin/bash

set -x
set -e
set -o pipefail

export $(cat .env | xargs)

stripe login --api-key "$STRIPE_API_KEY"
