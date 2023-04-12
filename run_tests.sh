#!/bin/sh

docker-compose -f docker-compose.test.yml pull
docker-compose -f docker-compose.test.yml build
docker-compose -f docker-compose.test.yml up --force-recreate

exit $?
