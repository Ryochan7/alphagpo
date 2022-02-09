all: help

help:
	@echo 'make test            run tests and show coverage report'
	@echo 'make clean           clean up files'

dev-config:
	mkdir -p envs/dev
	echo django.core.mail.backends.console.EmailBackend > envs/dev/EMAIL_BACKEND
	echo secret > envs/dev/SECRET_KEY
	echo postgres://mygpo:mygpo@localhost/mygpo > envs/dev/DATABASE_URL
	echo True > envs/dev/DEBUG
	echo "127.0.0.1" > envs/dev/INTERNAL_IPS

prod-skel:
	# Create empty skeleton for a production config. Need to fill in
	# files with applicable values manually. Focusing on items not
	# covered by settings module
	mkdir -p envs/prod
	echo "False" > envs/prod/DEBUG
	touch envs/prod/ADMINS
	touch envs/prod/DATABASE_URL
	touch envs/prod/DEFAULT_FROM_EMAIL
	touch envs/prod/SECRET_KEY
	touch envs/prod/SERVER_EMAIL

test: envs/dev/MEDIA_ROOT
	# assume defined media root directory, empty before running tests
	rm -rf $(shell cat envs/dev/MEDIA_ROOT)
	mkdir -p $(shell cat envs/dev/MEDIA_ROOT)
	envdir envs/dev/ python -Wd -m pytest --cov=mygpo/ --cov-branch
	coverage report --show-missing

update-po:
	envdir envs/dev/ python manage.py makemessages \
		--ignore=doc/* --ignore=envs/* --ignore=media/* --ignore=venv/* \
		--ignore=res/* --ignore=tools/* --ignore=mygpo/*/migrations/* \
		--ignore=static/*

compilemessages:
	envdir envs/dev/ python manage.py compilemessages

notebook:
	envdir envs/dev/ python manage.py shell_plus --notebook

clean:
	git clean -fX

install-deps:
	sudo apt-get install libpq-dev libjpeg-dev zlib1g-dev libwebp-dev \
		build-essential python3-dev virtualenv libffi-dev redis postgresql

format-code:
	black --target-version py38 --skip-string-normalization mygpo/

check-code-format:
	black --check --target-version py38 --skip-string-normalization mygpo/

start-project:
	# Start new screen session for mygpo project
	screen -dmS mygpo ./startapp_mygpo.sh

stop-project:
	# Add ^C to session console. Causes shell script to kill subprocesses
	screen -X -S mygpo stuff "^C"

.PHONY: all help test clean unittest coverage install-deps format-code start-project stop-project
