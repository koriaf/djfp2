#!/bin/bash
set -e
ROOT=`dirname "${BASH_SOURCE[0]}"`
exec ${ROOT}/manage.sh runserver 127.0.0.1:7892