.PHONY: all dev test comply docs clean

all: test comply comply-test api-docs clean

dev:
	docker-compose up -d
	docker-compose exec cement /bin/ash

test:
	python -m pytest -v --cov=cement --cov-report=term --cov-report=html:coverage-report tests/

comply:
	flake8 cement/ tests/

comply-fix:
	autopep8 -ri cement/ tests/

docs:
	python setup.py build_sphinx
	@echo
	@echo DOC: "file://"$$(echo `pwd`/doc/build/html/index.html)
	@echo

clean:
	find . -name '*.py[co]' -delete
	rm -rf doc/build
