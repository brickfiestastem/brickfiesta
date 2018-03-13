#!/bin/bash
# Simple script to setup development for this project.

# Use factumproject/scripts/python3_setup.sh

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

setup_virtualenv() {
    echo "Setting up local virtualenv"
    cd $SCRIPT_DIR
    cd ../
    sudo apt install virtualenv
    virtualenv -p python3 venv
    pip install --upgrade virtualenv
    source venv/bin/activate
    pip install -r requirements.txt
}

run_virtualenv() {
    echo "Run local virtualenv"
    cd $SCRIPT_DIR
    cd ../
    source venv/bin/activate
}

setup_local_settings() {
    echo "Setting up local settings"
    cd $SCRIPT_DIR
    cd ../
    NEW_UUID=$(tr -dc '[:alnum:]' < /dev/urandom | head -c 48)
    echo "Enter Google Recaptcha Key: "
    read GOOGLE_RECAPTCHA_KEY
    echo "Enter Google Recaptcha Site Key: "
    read GOOGLE_RECAPTCHA_SITE_KEY
    echo "Enter Google Map Key: "
    read GOOGLE_MAP_KEY
    echo "Enter Square Cart Key: "
    read SQUARE_CART_KEY
    echo "Enter Square Location Key: "
    read SQUARE_LOCATION_KEY
    echo "{" > settings.json
    echo "  \"SECRET_KEY\": \"$NEW_UUID\", " >> settings.json
    echo "  \"GOOGLE_RECAPTCHA_KEY\": \"$GOOGLE_RECAPTCHA_KEY\", " >> settings.json
    echo "  \"GOOGLE_RECAPTCHA_SITE_KEY\": \"$GOOGLE_RECAPTCHA_SITE_KEY\", " >> settings.json
    echo "  \"GOOGLE_MAP_KEY\": \"$GOOGLE_MAP_KEY\", " >> settings.json
    echo "  \"SQUARE_CART_KEY\": \"$SQUARE_CART_KEY\", " >> settings.json
    echo "  \"SQUARE_LOCATION_KEY\": \"$SQUARE_LOCATION_KEY\" " >> settings.json
    echo "}" >> settings.json
}

run_autopep8() {
    echo "Running autopep8"
    cd $SCRIPT_DIR
    cd ../
    find . -path ./venv -prune -o -name '*.py' -print -exec autopep8 -i {} \;
}

clean_database() {
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
    rm *.sqlite3
    python manage.py makemigrations afol event mocs news planning referral shop vendor sessions
    python manage.py migrate
}

load_fixtures() {
    echo "Load fixtures"
    cd $SCRIPT_DIR
    cd ../
    python manage.py loaddata event/fixtures/locations.json
    python manage.py loaddata event/fixtures/events.json
}

optimize_images() {
    echo "Optimize Images"
    find ./static/ -type f -name "*.png" -printf '%p\n' -exec convert {} -strip {} \;
    find ./static/ -type f -name "*.gif" -printf '%p\n' -exec convert {} -strip {} \;
    find ./static/ -type f -name "*.jpg" -printf '%p\n' -exec convert {} -sampling-factor 4:2:0 -strip -quality 85 -interlace JPEG -colorspace sRGB {} \;
}

usage() {
    echo "c Clean database"
    echo "f Full Install"
    echo "l Just local_settings.py"
    echo "L Load fixtures"
    echo "r run virtualenv"
    echo "v Just virtualenv"
    echo "8 Run autopep8"
    echo "Usage $0 [c] [f] [l] [L] [r] [v] [8]"
    exit 1
}

case "$1" in
    c)
        clean_database
        ;;
    cL)
        clean_database
        load_fixtures
        ;;
    f)
        setup_virtualenv
        setup_local_settings
        ;;
    l)
        setup_local_settings
        ;;
    L)
        load_fixtures
        ;;
    r)
        run_virtualenv
        ;;
    v)
        setup_virtualenv
        ;;
    8)
        run_autopep8
        ;;
    *)
        usage
        ;;
esac
