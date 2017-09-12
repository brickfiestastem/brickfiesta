#!/bin/bash
# Simple script to setup development for this project.

# Use factumproject/scripts/python3_setup.sh

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

setup_virtualenv() {
    echo "Setting up local virtualenv"
    cd $SCRIPT_DIR
    cd ../
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
}

setup_local_settings() {
    echo "Setting up local settings."
    cd $SCRIPT_DIR
    cd ../brickfiesta
    NEW_UUID=$(tr -dc '[:alnum:]' < /dev/urandom | head -c 48)
    echo '""" Do not commit to version control.' > local_settings.py
    echo '"""' >> local_settings.py
    echo "SECRET_KEY = '$NEW_UUID'" >> local_settings.py
}

usage () {
    echo "f Full Install"
    echo "v Just virtualenv"
    echo "l Just local_settings.py"
    echo "Usage $0 [f] [v] [l]"
    exit 1
}

case "$1" in
    f)
        setup_virtualenv
        setup_local_settings
        ;;
    l)
        setup_local_settings
        ;;
    v)
        setup_virtualenv
        ;;
    *)
        usage
        ;;
esac
