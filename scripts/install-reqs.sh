#!/bin/bash

set -x
set -e
set -o pipefail

$(pyenv which python) -m pip install -r requirements.txt
