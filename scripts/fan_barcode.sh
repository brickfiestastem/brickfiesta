#!/bin/bash
set -e
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $SCRIPT_DIR
cd ../
mkdir -p ./tmp
. venv/bin/activate
echo "Enter Fan ID: "
read FAN_ID
echo "Enter Fan Full Name: "
read FAN_NAME
python manage.py fan_barcode "$FAN_ID" "$FAN_NAME"
brother_ql_create --model QL-800 --label-size 29x90 --rotate 90 ./tmp/label-$FAN_ID.png > ./tmp/$FAN_ID.bin
# brother_ql_create --model QL-800 --label-size 62 --rotate 90 ./tmp/label-$FAN_ID.png > ./tmp/$FAN_ID.bin
cat ./tmp/$FAN_ID.bin > /dev/usb/lp3
rm -rf ./tmp
set +e