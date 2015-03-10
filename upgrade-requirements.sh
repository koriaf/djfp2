#!/bin/bash
set -e
ROOT=`dirname "${BASH_SOURCE[0]}"`
source ${ROOT}/venv.sh
pip3 install -r ${ROOT}/system/requirements.txt --upgrade
