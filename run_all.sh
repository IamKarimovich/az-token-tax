#!/usr/bin/env bash
set -e
python3 prep.py
node measure.mjs
python3 measure_mistral.py
python3 analyze.py
python3 charts.py
echo "Done. See the results folder."
