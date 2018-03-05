#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $SCRIPT_DIR
cd ../
echo "Environment [testing, staging, production]: "
read DEPLOYMENT
git pull
python manage.py makemigrations afol admin auth contenttypes event flatpages mocs news planning referral sessions shop sites vendor --settings=brickfiesta.$DEPLOYMENT
python manage.py migrate --settings=brickfiesta.$DEPLOYMENT
python manage.py collectstatic --settings=brickfiesta.$DEPLOYMENT
