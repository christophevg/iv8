all: requirements
	. venv/bin/activate; gunicorn -w 1 -k eventlet iv8:server

venv:
	virtualenv -p python3 $@

requirements: venv requirements.txt
	. venv/bin/activate; pip install --upgrade -r requirements.txt > /dev/null

upgrade: requirements
	. venv/bin/activate; pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U
