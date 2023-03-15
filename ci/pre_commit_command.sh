#!/bin/bash

# Install poetry
export POETRY_HOME=/opt/poetry
python3 -m venv $POETRY_HOME
$POETRY_HOME/bin/pip install poetry==1.4.0
$POETRY_HOME/bin/poetry --version
# Install dependencies
poetry install --no-interaction --no-root --with dev
# Run Commands
poetry run pytest tests/
poetry run flake8 fastjwt --statistics --tee --output-file ./reports/flake8stats.txt
poetry run genbadge tests -i reports/junit.xml -o - > reports/tests-badge.svg
poetry run genbadge coverage -i reports/coverage.xml -o - > reports/coverage-badge.svg
poetry run genbadge flake8 -i reports/flake8stats.txt -o - > reports/flake8-badge.svg
poetry run docstr-coverage