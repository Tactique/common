#!/bin/bash

ME=$(basename $0)
TEMPLATE_DIR="${ROOTIQUE}/common/database/templates"

function usage() {
	echo "Usage: ${ME} [ deps | sync ]"
}

function setup_database() {
	rm database/db.sqlite3
	./database/sql_scripts/create_db.py
	sync_database
}

function sync_database() {
	./database/sql_scripts/seed_db.py game_engine
	generate_templates
	./database/sql_scripts/seed_db.py template
}

function generate_templates() {
	rm -r ${TEMPLATE_DIR}
	mkdir -p ${TEMPLATE_DIR}

	pushd ../game_engine
	GOPATH=$(pwd) go run engine.go -write_templates=true -template_out_dir=${TEMPLATE_DIR}
	popd
}

function install_deps() {
	sudo pip install -r requirements.txt
}

function main() {
	if [ $# -lt 1 ]; then
			setup_database
	else
		if [ $1 == 'deps' ]; then
			install_deps
		elif [ $1 == 'sync' ]; then
			sync_database
		else
			usage
		fi
	fi
}

main $@
