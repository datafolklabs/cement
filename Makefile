.PHONY: all init api-doc test comply clean

all: init test test-coverage comply api-docs clean

init:
	pip install --upgrade -r requirements-dev.txt

test:
	python -m pytest -v tests/	

test-coverage:
	python -m pytest -v --cov=cement --cov-report=term --cov-report=html:coverage-report tests/	

comply:
	flake8 cement/ tests/

api-docs:
	python setup.py build_sphinx
	@echo
	@echo DOC: "file://"$$(echo `pwd`/doc/build/html/index.html)
	@echo

clean:
	find . -name '*.py[co]' -delete
	rm -rf doc/build

