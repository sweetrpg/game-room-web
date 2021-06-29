#!/bin/bash

set -e

version=$(git tag -l | head -1)
if [ -z "${version}" ]; then
    version=0.0.0
fi

docker build \
    -t registry.sweetrpg.com/sweetrpg-library-web:latest \
    -t registry.sweetrpg.com/sweetrpg-library-web:$(semver -i patch ${version}) \
    --ssh default \
    .
