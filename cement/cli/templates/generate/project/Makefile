.PHONY: clean setup test docker dist dist-upload

clean:
	find . -name '*.py[co]' -delete

setup:
	pdm install

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
