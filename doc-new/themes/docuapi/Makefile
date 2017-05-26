

#
# Makefile to perform rebuilds after changes to asset files.
#
# n.b. you must install fswatch (OS X: `brew install fswatch`)
#
# To start live live rebuilds, use the following command:
# $ make serve
#

# TODO: Figure a way to watch recursive
SLATE_DIR := /Users/bep/dev/clone/slate
WATCH_PATHS = ./assets/*.* ./assets/javascripts/*.* ./assets/javascripts/app/*.*
WATCH_PATHS := ${WATCH_PATHS} ./assets/stylesheets/*.*

build:
	go run bundler.go -slate=${SLATE_DIR}

serve:
	@make build 
	@fswatch -o ${WATCH_PATHS} | xargs -n1 -I{} make build

release:
	git tag -a ${version} -m "Release ${version}"
	git push --follow-tags
