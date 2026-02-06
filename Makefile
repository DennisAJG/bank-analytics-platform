.PHONY: lint test fmt

lint:
	cd api && poetry run ruff check .

fmt:
	cd api && poetry run ruff format .

fmt-check:
	cd api && poetry run ruff format --check .

test:
	cd api && poetry run pytest
