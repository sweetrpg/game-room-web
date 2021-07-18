#!/bin/bash

set -e

scriptdir="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
${scriptdir}/build-and-tag.sh
${scriptdir}/push-to-registry.sh
${scriptdir}/deploy-to-k8s.sh
