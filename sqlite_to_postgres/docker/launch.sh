#!/bin/bash

./wait-for-it.sh db:"${DB_PORT}" --timeout=-60

python3 main.py