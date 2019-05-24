export FLASK_APP=app.py
export FLASK_ENV=development

default:
	./ve flask run

install:
	python3 -m venv .virtualenv
	./ve pip install --upgrade pip --trusted-host mirrors.aliyun.com -i https://mirrors.aliyun.com/pypi/simple/
	./ve pip install --upgrade -r requirements.txt --trusted-host mirrors.aliyun.com -i https://mirrors.aliyun.com/pypi/simple/
