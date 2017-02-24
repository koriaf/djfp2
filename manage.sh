#!/bin/bash
set -e

ROOT=`dirname "${BASH_SOURCE[0]}"`
export PYTHONDONTWRITEBYTECODE='dontwrite'

export DJANGO_SETTINGS_MODULE=djfp2.settings
export AB_DEBUG="True"

${ROOT}/venv.sh ./src/manage.py $@
