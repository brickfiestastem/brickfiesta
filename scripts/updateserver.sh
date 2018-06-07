#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $SCRIPT_DIR
cd ../
echo "Environment [testing, staging, production]: "
read DEPLOYMENT
git pull
python manage.py makemigrations afol --settings=brickfiesta.$DEPLOYMENT
python manage.py makemigrations admin --settings=brickfiesta.$DEPLOYMENT
python manage.py makemigrations event --settings=brickfiesta.$DEPLOYMENT
python manage.py makemigrations mocs --settings=brickfiesta.$DEPLOYMENT
python manage.py makemigrations news --settings=brickfiesta.$DEPLOYMENT
python manage.py makemigrations planning --settings=brickfiesta.$DEPLOYMENT
python manage.py makemigrations referral --settings=brickfiesta.$DEPLOYMENT
python manage.py makemigrations sessions --settings=brickfiesta.$DEPLOYMENT
python manage.py makemigrations shop --settings=brickfiesta.$DEPLOYMENT
python manage.py makemigrations vendor --settings=brickfiesta.$DEPLOYMENT

python manage.py migrate --settings=brickfiesta.$DEPLOYMENT
python manage.py collectstatic --settings=brickfiesta.$DEPLOYMENT
