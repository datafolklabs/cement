ROOT_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

ifneq ($(CURDIR),$(patsubst %/,%,$(ROOT_DIR)))
$(error Must run make from the project root: $(ROOT_DIR))
endif

.PHONY: init dev up down test test-core cli-smoke-test comply-fix commit docs clean superclean dist dist-upload docker docker-push

init:
	devbox install
	devbox run pdm install

dev:
	docker compose up -d
	docker compose exec cement pdm install
	docker compose exec cement-py310 pdm install
	docker compose exec cement-py311 pdm install
	docker compose exec cement-py312 pdm install
	docker compose exec cement-py313 pdm install
	docker compose exec cement /bin/bash

up:
	process-compose up

down:
	process-compose down

test: comply
	pdm run pytest --cov=cement tests

test-core: comply
	pdm run pytest --cov=cement.core tests/core

cli-smoke-test:
	bash scripts/cli-smoke-test.sh

virtualenv:
	pdm venv create
	pdm install
	@echo
	@echo "VirtualENV Setup Complete. Now run: eval $(pdm venv activate)"
	@echo

comply: comply-ruff comply-mypy

comply-ruff:
	pdm run ruff check cement/ tests/

comply-ruff-fix:
	pdm run ruff check --fix cement/ tests/

comply-mypy:
	pdm run mypy

commit:
	pdm run cz commit

docs:
	cd docs; pdm run sphinx-build ./source ./build; cd ..
	@echo
	@echo DOC: "file://"$$(echo `pwd`/docs/build/html/index.html)
	@echo

clean:
	find . -name '*.py[co]' -delete
	find . -name '__pycache__' -type d -delete
	rm -rf docs/build
	rm -rf coverage-report .coverage*
	rm -rf .pytest_cache
	rm -rf *.egg-info dist
	rm -rf dump.rdb

superclean: clean
	rm -rf .devbox/ .venv/
	rm -rf .mypy_cache .ruff_cache .pdm-build
	rm -rf tmp/*
	@echo "Must run 'direnv allow' and 'make init' again"

dist:
	pdm build

docker:
	docker build -t datafolklabs/cement:latest .

docker-push:
	docker push datafolklabs/cement:latest

remove-merged-branches:
	git branch --merged | grep -v -e 'main\|stable/*\|dev/*' | xargs git branch -d
