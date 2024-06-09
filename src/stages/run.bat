@echo off

REM Activate the Poetry shell
call poetry shell
if %ERRORLEVEL% neq 0 (
    echo Failed to activate Poetry shell
    pause
    exit /b %ERRORLEVEL%
)


REM Run stage_prepare_data_folders.py
poetry run python 00_stage_prepare_data_folders.py
REM Check if the script ran successfully
if %ERRORLEVEL% neq 0 (
    echo 00_stage_prepare_data_folders.py failed
    pause
    exit /b %ERRORLEVEL%
)

REM Run stage_pre_process.py
poetry run python 01_stage_pre_process.py
REM Check if the script ran successfully
if %ERRORLEVEL% neq 0 (
    echo 01_stage_pre_process.py failed
    pause
    exit /b %ERRORLEVEL%
)

REM Run stage_thin_occurences.py
poetry run python 02_stage_thin_occurences.py
REM Check if the script ran successfully
if %ERRORLEVEL% neq 0 (
    echo 02_stage_thin_occurences.py failed
    pause
    exit /b %ERRORLEVEL%
)

REM Run stage_create_background_points.py
poetry run python 03_stage_create_background_points.py
REM Check if the script ran successfully
if %ERRORLEVEL% neq 0 (
    echo 03_stage_create_background_points.py failed
    pause
    exit /b %ERRORLEVEL%
)

REM Run stage_crop_files.py
poetry run python 04_stage_crop_files.py
REM Check if the script ran successfully
if %ERRORLEVEL% neq 0 (
    echo 04_stage_crop_files.py failed
    pause
    exit /b %ERRORLEVEL%
)

REM Run stage_feature_selection.py
poetry run python 05_stage_feature_selection.py
REM Check if the script ran successfully
if %ERRORLEVEL% neq 0 (
    echo 05_stage_feature_selection.py failed
    pause
    exit /b %ERRORLEVEL%
)

REM Run stage_create_models.py
poetry run python 06_stage_create_models.py
REM Check if the script ran successfully
if %ERRORLEVEL% neq 0 (
    echo 06_stage_create_models.py failed
    pause
    exit /b %ERRORLEVEL%
)

REM Run stage_create_models.py
poetry run python 07_stage_generate_models_results_output.py
REM Check if the script ran successfully
if %ERRORLEVEL% neq 0 (
    echo 07_stage_generate_models_results_output.py failed
    pause
    exit /b %ERRORLEVEL%
)

REM Run stage_create_models.py
poetry run python 08_stage_generate_models_results_output.py
REM Check if the script ran successfully
if %ERRORLEVEL% neq 0 (
    echo 08_stage_generate_models_results_output.py failed
    pause
    exit /b %ERRORLEVEL%
)

REM Run stage_create_models.py
poetry run python 09_stage_generate_reports.py
REM Check if the script ran successfully
if %ERRORLEVEL% neq 0 (
    echo 09_stage_generate_reports.py failed
    pause
    exit /b %ERRORLEVEL%
)

REM Run stage_create_models.py
poetry run python 10_stage_generate_prob.py
REM Check if the script ran successfully
if %ERRORLEVEL% neq 0 (
    echo 10_stage_generate_prob.py failed
    pause
    exit /b %ERRORLEVEL%
)
echo All scripts ran successfully
pause
