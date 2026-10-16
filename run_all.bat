@echo off
python prep.py || exit /b 1
node measure.mjs || exit /b 1
python measure_mistral.py || exit /b 1
python analyze.py || exit /b 1
python charts.py || exit /b 1
echo Done. See the results folder.
