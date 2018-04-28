.PHONY: all init doc test clean dist dist-upload

all: init test doc clean

init:
	pip install --upgrade -r requirements-dev.txt

test:
	python setup.py nosetests

doc:
	python setup.py build_sphinx
	@echo
	@echo DOC: "file://"$$(echo `pwd`/doc/build/html/index.html)
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

