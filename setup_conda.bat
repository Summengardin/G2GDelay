@echo off
set VENV_NAME=conda_env
set SCRIPT_PATH=G2GDelay.py

echo Creating Conda environment...
call conda create --prefix ./envs/%VENV_NAME% python=3.11 -y

echo Activating Conda environment...
call conda activate ./envs/%VENV_NAME%

echo Installing requirements...
call conda install pip -y
pip install -r requirements.txt

echo Conda environment and requirements installation completed.
call conda deactivate
pause