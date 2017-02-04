.PHONY: all init doc test comply clean

all: init test doc clean

init:
	pip install --upgrade -r requirements-dev.txt

test:
	python setup.py nosetests

comply:
	flake8 cement/ tests/

doc:
	python setup.py build_sphinx
	@echo
	@echo DOC: "file://"$$(echo `pwd`/doc/build/html/index.html)
	@echo

clean:
	find . -name '*.py[co]' -delete
	rm -rf doc/build
