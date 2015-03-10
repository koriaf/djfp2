#!/bin/bash
ROOT=`dirname "${BASH_SOURCE[0]}"`
act="${ROOT}/system/venv/bin/activate"
export PYTHONDONTWRITEBYTECODE='dontwrite'

if [ ! -f "${act}" ]; then
    set -e
    mkdir -p ${ROOT}/system/
    pyvenv ${ROOT}/system/venv
    source ${act}
    wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py -O - | python
    wget https://bootstrap.pypa.io/get-pip.py -O - | python
    ${ROOT}/upgrade-requirements.sh
    set +e
else
    source ${act}
fi

ARGS="$@"
if [ -n "${ARGS}" ]; then
    cd ${ROOT}
    exec $@
fi
