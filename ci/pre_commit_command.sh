#!/bin/bash
poetry run pytest tests/
poetry run flake8 fastjwt --statistics --tee --output-file ./reports/flake8stats.txt
poetry run genbadge tests -i reports/junit.xml -o - > reports/tests-badge.svg
poetry run genbadge coverage -i reports/coverage.xml -o - > reports/coverage-badge.svg
poetry run genbadge flake8 -i reports/flake8stats.txt -o - > reports/flake8-badge.svg
poetry run docstr-coverage