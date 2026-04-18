# Place your local stuff in Makefile.local
-include .env
-include vendors/deps-pipelines/shared/Makefile
-include Makefile.local

CI_PIPELINE_ID ?= latest
APP_NAME=$(REPOSITORY_URL)/deps-ci/deps_lil_chyn:$(CI_PIPELINE_ID)
PROJECT_DIRECTORY_NAME=deps_lil_chyn
HOST_UID=$(shell id -u ${USER})
HOST_GID=$(shell id -g ${USER})
HOST_UGID=$(HOST_UID):$(HOST_GID)

NO_DEV_DOCKER_IMAGE = lil-chyn
DEV_DOCKER_IMAGE=$(APP_NAME)
# Redefined variables for container_exec function from Makefile.poetry
PYPROJECT_TOML_VOLUME_PASSING = -v '$(shell pwd)/pyproject.toml:/app/pyproject.toml'
POETRY_LOCK_VOLUME_PASSING = -v '$(shell pwd)/poetry.lock:/app/poetry.lock'
REQUIREMENTS_TXT_VOLUME_PASSING = -v '$(shell pwd)/requirements.txt:/app/requirements.txt'


.PHONY: build-tests
build-tests:
	@#@ Build project for tests
	docker build --target develop --build-arg REPOSITORY_URL=$(REPOSITORY_URL) -t $(APP_NAME) .

.PHONY: poetry-bash
poetry-bash:
	@#@ Run poetry environment
	docker build --target develop --build-arg REPOSITORY_URL=$(REPOSITORY_URL) -t $(APP_NAME) .
	docker run -v $(PWD):/app --rm -i -t $(APP_NAME) bash

.PHONY: mypy-check
mypy-check:
	@#@ Run typechecking using mypy
	docker run -t --rm $(APP_NAME) mypy $(PROJECT_DIRECTORY_NAME)

.PHONY: lint
lint:
	@#@ Run linter
	docker run -t --rm $(APP_NAME) flake8 $(PROJECT_DIRECTORY_NAME)

.PHONY: format
format:
	@#@ Run formatting using black and isort
	docker run -u $(HOST_UGID) -v $(PWD)/$(PROJECT_DIRECTORY_NAME):/app/$(PROJECT_DIRECTORY_NAME) --rm -i -t $(APP_NAME) sh -c "black $(PROJECT_DIRECTORY_NAME) && isort $(PROJECT_DIRECTORY_NAME)"

.PHONY: format-check
format-check:
	@#@ Run formatting using black and isort
	docker run -t --rm $(APP_NAME) sh -c "black $(PROJECT_DIRECTORY_NAME) --check && isort $(PROJECT_DIRECTORY_NAME) --check"

.PHONY: tests
tests: | build-tests
	docker run --env-file .test.env -t --rm $(APP_NAME) coverage run -m pytest tests/

.PHONY: tests-with-coverage
tests-with-coverage:
	@#@ Test coverage
	docker run --env-file .test.env -t --rm $(APP_NAME) \
	 sh -c "coverage run -m pytest tests/ && coverage report"

.PHONY: shell
shell:
	@#@ Open poetry shell
	docker run --env-file .test.env -v "$(CURDIR)":/app --rm -i -t $(APP_NAME) bash

.PHONY: ci
ci: | build-tests format-check lint mypy-check tests-with-coverage
	@#@ Run CI checks
	@echo "Done"

.PHONY: build-no-dev
build-no-dev:
	docker build --cache-from $(APP_NAME) --target build --build-arg REPOSITORY_URL=$(REPOSITORY_URL) -t $(NO_DEV_DOCKER_IMAGE):latest .
