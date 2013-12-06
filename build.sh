#!/bin/sh

mkdir build

pip install --download='./build' --no-install -r requirements.txt

unzip -q build/django-autoload-*.zip -d build
unzip -q build/django-dbindexer-*.zip -d build
unzip -q build/django-nonrel-*.zip -d build
unzip -q build/djangoappengine-*.zip -d build
unzip -q build/djangotoolbox-*.zip -d build

cp -r build/django-autoload/autoload ./autoload
cp -r build/django-dbindexer/dbindexer ./dbindexer
cp -r build/django-nonrel/django ./django
cp -r build/djangoappengine/djangoappengine ./djangoappengine
cp -r build/djangotoolbox/djangotoolbox ./djangotoolbox

#rm -rf build/
