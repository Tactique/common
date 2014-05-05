#!/bin/sh

rm database/db.sqlite3
./database/sql_scripts/create_db.py
./database/sql_scripts/seed_db.py
