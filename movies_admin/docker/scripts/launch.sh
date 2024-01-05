#!/bin/bash

./wait-for-it.sh db:"${DB_PORT}" --timeout=-60
./wait-for-it.sh elasticsearch:"${ELASTIC_PORT}" --timeout=-60

./index_creation.sh
./migrations.sh
