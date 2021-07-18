#!/bin/bash

set -e

scriptdir="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
env=${1:-dev}

kubectl apply -k ${scriptdir}/../kubernetes/overlays/${env}
