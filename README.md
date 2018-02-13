# Brick Fiesta Site

## Developer Notes

Setup Virtual Environment
```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Set Environment Variables
```bash
. ./script/development.sh l
```

Clear the migrations if there is a major problem but this should NOT happen after deployment.
```bash
find . -path "./afol/migrations/*.py" -delete -print
find . -path "./event/migrations/*.py" -delete -print
find . -path "./mocs/migrations/*.py" -delete -print
find . -path "./news/migrations/*.py" -delete -print
find . -path "./planning/migrations/*.py" -delete -print
find . -path "./referral/migrations/*.py" -delete -print
find . -path "./shop/migrations/*.py" -delete -print
find . -path "./vendor/migrations/*.py" -delete -print
find . -path "*/migrations/*.pyc"  -delete -print
rm *.sqlite3
```

Make and migrate the migrations
```bash
python manage.py makemigrations afol event mocs news planning referral shop vendor
python manage.py migrate
```

Load the fixtures
```bash
python manage.py loaddata event/fixtures/locations.json
python manage.py loaddata event/fixtures/events.json
python manage.py loaddata shop/fixtures/products.json

```

Create super user
```bash
python manage.py createsuperuser
```
