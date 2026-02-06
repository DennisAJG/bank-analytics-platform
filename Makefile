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

unit-ci:
	cd api && poetry run pytest -m "not integration" \
		--cov=bank_api \
		--cov-report=term-missing \
		--cov-report=xml:coverage.xml \
		--cov-fail-under=70 \
		--junitxml=junit.xml

integration-ci:
	cd api && INTEGRATION_BASE_URL=http://localhost:8001 poetry run pytest -m integration \
		--junitxml=junit-integration.xml
