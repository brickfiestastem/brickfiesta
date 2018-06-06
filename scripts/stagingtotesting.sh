#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

DEPLOYMENT=testing
FROM=staging_brickfiesta_com

echo "Running clean database"
cd $SCRIPT_DIR
cd ../
find . -path "./afol/migrations/*.py" -delete -print
find . -path "./event/migrations/*.py" -delete -print
find . -path "./mocs/migrations/*.py" -delete -print
find . -path "./news/migrations/*.py" -delete -print
find . -path "./planning/migrations/*.py" -delete -print
find . -path "./referral/migrations/*.py" -delete -print
find . -path "./shop/migrations/*.py" -delete -print
find . -path "./vendor/migrations/*.py" -delete -print
find . -path "*/migrations/*.pyc"  -delete -print

cp --verbose ../$FROM/afol/migrations/*.py ./afol/migrations/
cp --verbose ../$FROM/event/migrations/*.py ./event/migrations/
cp --verbose ../$FROM/mocs/migrations/*.py ./mocs/migrations/
cp --verbose ../$FROM/news/migrations/*.py ./news/migrations/
cp --verbose ../$FROM/planning/migrations/*.py ./planning/migrations/
cp --verbose ../$FROM/referral/migrations/*.py ./referral/migrations/
cp --verbose ../$FROM/shop/migrations/*.py ./shop/migrations/
cp --verbose ../$FROM/vendor/migrations/*.py ./vendor/migrations/

python manage.py makemigrations afol --settings=brickfiesta.$DEPLOYMENT
python manage.py makemigrations admin --settings=brickfiesta.$DEPLOYMENT
python manage.py makemigrations auth --settings=brickfiesta.$DEPLOYMENT
python manage.py makemigrations contenttypes --settings=brickfiesta.$DEPLOYMENT
python manage.py makemigrations event --settings=brickfiesta.$DEPLOYMENT
python manage.py makemigrations flatpages --settings=brickfiesta.$DEPLOYMENT
python manage.py makemigrations mocs --settings=brickfiesta.$DEPLOYMENT
python manage.py makemigrations news --settings=brickfiesta.$DEPLOYMENT
python manage.py makemigrations planning --settings=brickfiesta.$DEPLOYMENT
python manage.py makemigrations referral --settings=brickfiesta.$DEPLOYMENT
python manage.py makemigrations sessions --settings=brickfiesta.$DEPLOYMENT
python manage.py makemigrations shop --settings=brickfiesta.$DEPLOYMENT
python manage.py makemigrations sites --settings=brickfiesta.$DEPLOYMENT
python manage.py makemigrations vendor --settings=brickfiesta.$DEPLOYMENT

