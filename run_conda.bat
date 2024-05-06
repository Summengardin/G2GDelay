echo Running Glass to Glass latency measurement
set VENV_NAME=conda_env
set SCRIPT_PATH=G2GDelay.py

echo Activating Conda environment...
call conda activate ./envs/%VENV_NAME%

echo Running Python script...
echo python %SCRIPT_PATH%
python %SCRIPT_PATH%

echo Script execution completed.

echo Deactivating Conda environment...
conda deactivate