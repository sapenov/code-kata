@echo off

if "%1" == "install" goto install
if "%1" == "format" goto format
if "%1" == "lint" goto lint
if "%1" == "test" goto test
if "%1" == "all" goto all

echo Usage: make [install^|format^|lint^|test^|all]
goto :eof

:install
pip install -r requirements.txt
goto :eof

:format
black .
goto :eof

:lint
pylint par_parser.py tests\test_par_parser.py
goto :eof

:test
pytest tests
goto :eof

:all
call :install
call :format
call :lint
call :test
goto :eof