export FLASK_APP=app.py
export FLASK_ENV=development

default:
	./ve flask run

install:
	python3 -m venv .virtualenv
	./ve pip install --upgrade pip
	./ve pip install --upgrade -r requirements.txt
