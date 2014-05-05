#!/bin/sh

ME=$(basename $0)
DATABASE_DIR="$(dirname $(realpath ${ME}))/database"
TEMPLATE_DIR="${DATABASE_DIR}/templates"

rm -r ${TEMPLATE_DIR}
mkdir -p ${TEMPLATE_DIR}

pushd ../game_engine
GOPATH=$(pwd) go run templater.go -filepath=${TEMPLATE_DIR}
popd

rm database/db.sqlite3
./database/sql_scripts/create_db.py
./database/sql_scripts/seed_db.py
