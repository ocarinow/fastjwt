#!/bin/bash

# Install poetry
export POETRY_HOME=/opt/poetry
python3 -m venv $POETRY_HOME
$POETRY_HOME/bin/pip install poetry==1.4.0
$POETRY_HOME/bin/poetry --version
# Install dependencies
$POETRY_HOME/bin/poetry config virtualenvs.in-project true 
$POETRY_HOME/bin/poetry install --no-interaction --no-root --with dev
# Run Commands
$POETRY_HOME/bin/poetry run pytest tests/
$POETRY_HOME/bin/poetry run flake8 fastjwt --statistics --tee --output-file ./reports/flake8stats.txt
$POETRY_HOME/bin/poetry run genbadge tests -i reports/junit.xml -o - > reports/tests-badge.svg
$POETRY_HOME/bin/poetry run genbadge coverage -i reports/coverage.xml -o - > reports/coverage-badge.svg
$POETRY_HOME/bin/poetry run genbadge flake8 -i reports/flake8stats.txt -o - > reports/flake8-badge.svg
$POETRY_HOME/bin/poetry run docstr-coverage