PY ?= python3
export PYTHONPATH := src:$(PYTHONPATH)

.PHONY: setup lint test eval eval-regression demo check secretscan

setup:
	$(PY) -m pip install -e ".[dev]"

lint:
	$(PY) -m ruff check src tests exercises solutions
	$(PY) -m ruff format --check src tests exercises solutions
	$(PY) -m mypy

test:
	$(PY) -m pytest

eval:
	$(PY) -m workshop eval

# Healthy outcome: non-zero exit. The gate found the bad lab agent.
eval-regression:
	$(PY) -m workshop eval-regression

demo:
	$(PY) -m workshop demo

check:
	$(PY) -m workshop check all --impl solution

secretscan:
	$(PY) -m workshop secretscan .

# Plain equivalents, if make is not installed:
#   PYTHONPATH=src python -m ruff check src tests exercises solutions
#   PYTHONPATH=src python -m ruff format --check src tests exercises solutions
#   PYTHONPATH=src python -m mypy
#   PYTHONPATH=src python -m pytest
#   PYTHONPATH=src python -m workshop eval
#   PYTHONPATH=src python -m workshop eval-regression
#   PYTHONPATH=src python -m workshop demo
#   PYTHONPATH=src python -m workshop check all --impl solution
#   PYTHONPATH=src python -m workshop secretscan .
