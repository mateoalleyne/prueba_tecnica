@echo off
cd /d "%~dp0"
call .\venv\Scripts\activate.bat
pip install -r requirements.txt
echo Instalación finalizada, presione cualquier tecla para finalizar...
pause