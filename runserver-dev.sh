#!/bin/bash
set -e
ROOT=`dirname "${BASH_SOURCE[0]}"`
exec ${ROOT}/manage.sh runserver 0:7892
