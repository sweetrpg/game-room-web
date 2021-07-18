#!/bin/bash

set -e

export DOCKER_BUILDKIT=1
registry=registry.sweetrpg.com
name=sweetrpg-library-web

docker push \
    ${registry}/${name}
