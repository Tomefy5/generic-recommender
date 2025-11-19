.PHONY: test lint format

test:
	pytest

lint:
	ruff check src tests

format:
	ruff format src tests

lint-fix:
	ruff check src tests --fix

