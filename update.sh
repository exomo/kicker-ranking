#!/bin/bash

cd "$(dirname "$0")"

mkdir -p backup
cp kicker_scores.db backup/$(date -Iseconds)_kicker_scores.db.bkp

git pull
python3 src/database/update_database.py