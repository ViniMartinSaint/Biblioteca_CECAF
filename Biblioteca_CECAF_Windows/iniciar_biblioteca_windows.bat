@echo off
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
    set PYTHON=py
) else (
    set PYTHON=python
)

if not exist ".venv\Scripts\python.exe" (
    echo Criando ambiente virtual...
    %PYTHON% -m venv .venv
    if errorlevel 1 goto erro
)

echo Instalando/verificando dependencias...
".venv\Scripts\python.exe" -m pip install --disable-pip-version-check -r requirements_windows.txt
if errorlevel 1 goto erro

echo.
echo Abrindo Biblioteca CECAF em http://127.0.0.1:8050
start "" http://127.0.0.1:8050
".venv\Scripts\python.exe" main_windows.py
goto fim

:erro
echo.
echo ERRO: nao foi possivel iniciar o sistema.
echo Verifique se o Python 3 esta instalado e marcado no PATH.
pause

:fim
