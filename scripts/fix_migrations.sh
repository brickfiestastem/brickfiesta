#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $SCRIPT_DIR
cd ../
echo $(pwd)
echo "Environment [testing, staging, production]: "
read DEPLOYMENT

find . -path "./afol/migrations/*.py" -delete -print
find . -path "./event/migrations/*.py" -delete -print
find . -path "./games/migrations/*.py" -delete -print
find . -path "./mocs/migrations/*.py" -delete -print
find . -path "./news/migrations/*.py" -delete -print
find . -path "./planning/migrations/*.py" -delete -print
find . -path "./referral/migrations/*.py" -delete -print
find . -path "./shop/migrations/*.py" -delete -print
find . -path "./vendor/migrations/*.py" -delete -print
find . -path "*/migrations/*.pyc"  -delete -print

touch ./afol/migrations/__init__.py
touch ./event/migrations/__init__.py
touch ./games/migrations/__init__.py
touch ./mocs/migrations/__init__.py
touch ./news/migrations/__init__.py
touch ./planning/migrations/__init__.py
touch ./referral/migrations/__init__.py
touch ./shop/migrations/__init__.py
touch ./vendor/migrations/__init__.py

python manage.py makemigrations --settings=brickfiesta.$DEPLOYMENT

python manage.py migrate --settings=brickfiesta.$DEPLOYMENT