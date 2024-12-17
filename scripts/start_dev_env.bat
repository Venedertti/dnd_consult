cd ..

python -m venv .venv

timeout /t 10

call .venv\Scripts\activate.bat

pip install -r requirements.txt

pip freeze

pause
