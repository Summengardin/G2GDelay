@echo off
set VENV_NAME=.venv
set SCRIPT_PATH=G2GDelay.py

echo Creating virtual environment...
python -m venv %VENV_NAME%

echo Activating virtual environment...
call %VENV_NAME%\Scripts\activate

echo Installing requirements...
pip install setuptools
pip install -r requirements.txt

echo Virtual environment and requirements installation completed.
