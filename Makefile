.PHONY: dev test test-core comply-fix docs clean dist dist-upload

dev:
	docker-compose up -d
	docker-compose exec cement pip install -r requirements-dev.txt
	docker-compose exec cement python setup.py develop
	docker-compose exec cement /bin/bash

test: comply
	python -m pytest -v --cov=cement --cov-report=term --cov-report=html:coverage-report tests/

test-core: comply
	python -m pytest -v --cov=cement.core --cov-report=term --cov-report=html:coverage-report tests/core

comply:
	flake8 cement/ tests/

comply-fix:
	autopep8 -ri cement/ tests/

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
