# Contains basic auxiliary commands for working with restaurant order service.

# run linters
lint:
	ruff check . --config=pyproject.toml --fix

# run tests
test:
	pytest -vv -p no:warnings

# run API
api:
	python -m src

# run development server with reload
dev:
	uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# run alembic migrations
migrate:
	alembic upgrade head

# create new migration
migration:
	alembic revision --autogenerate -m "$(message)" 