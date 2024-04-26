@echo off

echo Running Glass to Glass latency measurement 
set VENV_NAME=.venv
set SCRIPT_PATH=G2GDelay.py


echo Activating virtual environment...
call %VENV_NAME%\Scripts\activate

echo Running Python script...
echo python %SCRIPT_PATH%
python %SCRIPT_PATH%

echo Script execution completed.

echo Deactivating virtual environment...
deactivate