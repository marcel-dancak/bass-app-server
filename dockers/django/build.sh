#!/bin/sh

mkdir -p tmp

cp ../../server/requirements.txt tmp/
cp ../../server/dist/basscloud-dev.tar.gz tmp/

docker build -t dancakm/basscloud-django .

# rm -r tmp/

# rm -r server clients