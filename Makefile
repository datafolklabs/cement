.PHONY: dev test test-core comply-fix docs clean dist dist-upload docker docker-push

dev:
	docker-compose up -d
	docker-compose exec cement pip install -r requirements-dev.txt
	docker-compose exec cement python setup.py develop
	docker-compose exec cement /bin/bash

test: comply
	pdm run pytest --cov=cement tests

test-core: comply
	pdm run pytest --cov=cement.core tests/core

virtualenv:
	pdm venv create
	pdm install
	virtualenv --prompt '|> cement <| ' env
	env/bin/pip install -r requirements-dev.txt
	env/bin/python setup.py develop
	@echo
	@echo "VirtualENV Setup Complete. Now run: eval $(pdm venv activate)"
	@echo

comply:
	pdm run ruff check cement/ tests/

comply-fix:
	pdm run ruff check --fix cement/ tests/

comply-typing:
	pdm run mypy

docs:
	cd docs; pdm run sphinx-build ./source ./build; cd ..
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
