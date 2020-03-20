SH := /bin/sh
PY := $(shell which python3)
MULTIPROC_DIR ?= $(shell pwd)/.multiproc_dir
CONFFILE = devconf.py

.PHONY: help
## help: prints this help message
help:
	@echo "Usage: \n"
	@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ':' |  sed -e 's/^/ /'

.PHONY: test
## test: run unit tests
test:
	cd src/ && $(PY) -m pytest -s -v

.PHONY: run
## run: calls run/dev to start the API locally
run: run/dev

.PHONY: run/dev
## run/dev: start via the Flask development server
run/dev:
	CONFFILE=$(CONFFILE) \
	FLASK_APP=./src/run.py \
	ENVIRONMENT=development \
	FLASK_ENV=development \
	FLASK_DEBUG=True \
		flask run

.PHONY: run/prod
## run/prod: start via gunicorn
run/prod:
	CONFFILE=$(CONFFILE) \
	ENVIRONMENT=production \
	./gunicorn.sh $(MULTIPROC_DIR)

.PHONY: clean
## clean: cleans .multiproc_dir
clean:
	find $(MULTIPROC_DIR) -type f -not -regex ".*gitkeep$$" -exec rm "{}" \;
