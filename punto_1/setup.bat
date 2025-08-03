@echo off
cd /d "%~dp0"
call .\venv\Scripts\activate.bat
pip install -r requirements.txt
python -m ipykernel install --user --name=venv --display-name "Python (venv)"
echo Instalación finalizada, presione cualquier tecla para finalizar...
pause