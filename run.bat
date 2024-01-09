@echo off
echo Running Glass to Glass latency measurement 
set VENV_NAME=.venv
set SCRIPT_PATH=G2GDelay.py

echo Activating virtual environment...
call %VENV_NAME%\Scripts\activate

echo Running Python script...
echo python %SCRIPT_PATH% -c -n 30
python %SCRIPT_PATH% -c -n 30

echo Script execution completed.
pause