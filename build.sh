#!/bin/bash

set -e

version=$(git tag -l | head -1)
if [ -z "${version}" ]; then
    version=0.0.0
fi

export DOCKER_BUILDKIT=1
registry=registry.sweetrpg.com
name=sweetrpg-library-web

ssh-add ~/.ssh/id_rsa
docker build \
    -t ${registry}/${name}:latest \
    -t ${registry}/${name}:$(semver -i patch ${version}) \
    --ssh default \
    .
