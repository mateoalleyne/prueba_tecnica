@echo off
cd /d "%~dp0"
echo API Key en entorno: %OPENAI_API_KEY%
call .\venv\Scripts\activate.bat
streamlit run app.py
start http://localhost:8501/
echo Presione cualquier tecla para finalizar...
pause