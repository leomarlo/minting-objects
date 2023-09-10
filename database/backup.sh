#!/bin/bash

TIMESTAMP=$(date +"%F")
BACKUP_DIR="./backup/$TIMESTAMP"
mkdir -p $BACKUP_DIR
docker exec -t your_project_name_database_1 pg_dumpall -c -U $DB_USER > $BACKUP_DIR/dump_"$TIMESTAMP".sql
