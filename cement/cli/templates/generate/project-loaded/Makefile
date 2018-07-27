.PHONY: clean dev test docker dist dist-upload

clean:
	find . -name '*.py[co]' -delete
	rm -rf docs/build

dev:
	docker-compose up -d
	docker-compose exec {{ label }} pip install -r requirements-dev.txt
	docker-compose exec {{ label }} python setup.py develop
	docker-compose exec {{ label }} /bin/bash

test:
	python -m pytest \
		-v \
		--cov={{ label }} \
		--cov-report=term \
		--cov-report=html:coverage-report \
		tests/

docker: clean
	docker build -t {{ label }}:latest .

dist: clean
	rm -rf dist/*
	python setup.py sdist
	python setup.py bdist_wheel

dist-upload:
	twine upload dist/*
