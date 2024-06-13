.PHONY: dev test test-core comply-fix docs clean dist dist-upload docker docker-push

dev:
	docker-compose up -d
	docker-compose exec cement pdm install
	docker-compose exec cement-py38 pdm install
	docker-compose exec cement-py39 pdm install
	docker-compose exec cement-py310 pdm install
	docker-compose exec cement-py311 pdm install
	docker-compose exec cement-py312 pdm install
	docker-compose exec cement-py313 pdm install
	docker-compose exec cement /bin/bash

test: comply
	pdm run pytest --cov=cement tests

test-core: comply
	pdm run pytest --cov=cement.core tests/core

virtualenv:
	pdm venv create
	pdm install
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

dist:
	pdm build

docker:
	docker build -t datafolklabs/cement:latest .

docker-push:
	docker push datafolklabs/cement:latest

remove-merged-branches:
	git branch --merged | grep -v -e 'main\|stable/*\|dev/*' | xargs git branch -d
