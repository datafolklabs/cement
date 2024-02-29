.PHONY: dev test test-core comply-fix docs clean dist dist-upload docker docker-push

dev:
	docker-compose up -d
	docker-compose exec cement pip install -r requirements-dev.txt
	docker-compose exec cement python setup.py develop
	docker-compose exec cement /bin/bash

test: comply
	python -m pytest -v --cov=cement --cov-report=term --cov-report=html:coverage-report --capture=sys tests/

test-core: comply
	python -m pytest -v --cov=cement.core --cov-report=term --cov-report=html:coverage-report --capture=sys tests/core

virtualenv:
	virtualenv --prompt '|> cement <| ' env
	env/bin/pip install -r requirements-dev.txt
	env/bin/python setup.py develop
	@echo
	@echo "VirtualENV Setup Complete. Now run: source env/bin/activate"
	@echo

virtualenv-windows:
	virtualenv --prompt '|> cement <| ' env-windows
	env-windows\\Scripts\\pip.exe install -r requirements-dev-windows.txt
	env-windows\\Scripts\\python.exe setup.py develop
	@echo
	@echo "VirtualENV Setup Complete. Now run: .\env-windows\Scripts\activate.ps1"
	@echo

comply:
	flake8 cement/ tests/

comply-fix:
	autopep8 -ri cement/ tests/

comply-typing:
	mypy ./cement

docs:
	python setup.py build_sphinx
	@echo
	@echo DOC: "file://"$$(echo `pwd`/docs/build/html/index.html)
	@echo

clean:
	find . -name '*.py[co]' -delete
	rm -rf doc/build

dist: clean
	rm -rf dist/*
	python setup.py sdist
	python setup.py bdist_wheel

dist-upload:
	twine upload dist/*

docker:
	docker build -t datafolklabs/cement:latest .

docker-push:
	docker push datafolklabs/cement:latest

remove-merged-branches:
	git branch --merged | grep -v -e 'main\|stable/*\|dev/*' | xargs git branch -d
