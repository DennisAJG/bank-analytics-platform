.PHONY: lint test fmt

lint:
	cd api && poetry run ruff check .

fmt:
	cd api && poetry run ruff format .

fmt-check:
	cd api && poetry run ruff format --check .

test:
	cd api && poetry run pytest

unit:
	cd api && poetry run pytest -m "unit or not integration"

integration:
	cd api && INTEGRATION_BASE_URL=http://localhost:8001 poetry run pytest -m integration
