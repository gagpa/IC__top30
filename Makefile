# Vars
CODE_DIR = server
TESTS_DIR = tests
COV_LEVEL=95
PYTHONPATH = PYTHONPATH=./:$(CODE_DIR)

# Executables
PYTHON = $(PYTHONPATH) python3
POETRY = $(PYTHONPATH) poetry run
ALEMBIC = $(PYTHONPATH) alembic -c $(CODE_DIR)/database/alembic.ini
TEST =  $(POETRY) pytest --verbosity=2 --showlocals --strict

# Params
DOWNGRADE_DEFAULT = -1

.PHONY: run-script migrations db_upgrade db_downgrade pretty help lint test test-failed test-cov validate

run-script:  ## Запустить скрипты
	${PYTHON} -m scripts

migrations:  ## Создать миграции
	$(ALEMBIC) revision --autogenerate -m "$(message)"

db_upgrade:  ## Запуск миграций
	$(ALEMBIC) upgrade head

db_downgrade:  ## Откат до предыдущей (по умолчанию) миграции
	$(ALEMBIC) downgrade $(DOWNGRADE_DEFAULT)

test:  ## Прогон тестов
	$(TEST) --cov --cov-fail-under=$(COV_LEVEL)

test-failed:  ## Запуск только тестов, упавших в прошлый раз
	$(TEST) --last-failed

test-cov:  ## Запуск тестов с подробным сбором покрытия
	$(TEST) --cov-report html

pretty:  ## "Причесать" код - isort, black, пр.
	isort .
	black .
	autoflake --in-place --verbose -r .

lint:  ## Линтинг
	black --check $(CODE_DIR) tests
	pylint --jobs 4 --rcfile=pyproject.toml $(CODE_DIR)
	mypy $(CODE_DIR)

help:  ## Показать это сообщение
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

validate: lint test
