#!/bin/sh

pip install --no-install -r requirements.txt

cp -r src/django-autoload/autoload ./autoload
cp -r src/django-dbindexer/dbindexer ./dbindexer
cp -r src/django-nonrel/django ./django
cp -r src/djangoappengine/djangoappengine ./djangoappengine
cp -r src/djangotoolbox/djangotoolbox ./djangotoolbox

rm -rf src/
