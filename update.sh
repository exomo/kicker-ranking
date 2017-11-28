#!/bin/bash

cp kicker_scores.db kicker_scores.db.bkp
git pull
cp kicker_scores.db.bkp kicker_scores.db
python3 GUI/gui_test.py