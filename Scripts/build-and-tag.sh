#!/bin/bash

set -e

scriptdir="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

version=$(semver -i patch $(git tag -l | head -1))
if [ -z "${version}" ]; then
    version=0.0.0
fi

${scriptdir}/build-docker-image.sh ${version}

git tag -m "${version}" ${version}
git push origin --tags
