.PHONY: clean virtualenv test docker dist dist-upload

clean:
	find . -name '*.py[co]' -delete

virtualenv:
	pdm venv create
	pdm install
	@echo
	@echo "VirtualENV Setup Complete. Now run: eval \$$(pdm venv activate)"
	@echo

test:
	pdm run pytest \
		-v \
		--cov={{ label }} \
		--cov-report=term \
		--cov-report=html:coverage-report \
		tests/

docker: clean
	docker build -t {{ label }}:latest .

dist: clean
	rm -rf dist/*
	pdm build

dist-upload:
	twine upload dist/*
