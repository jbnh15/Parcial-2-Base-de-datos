PY = .venv/bin

.PHONY: install check run seed

install:
	uv pip install --python $(PY)/python -r requirements-dev.txt

check:
	$(PY)/ruff check .
	$(PY)/pytest -q

seed:
	$(PY)/python -m seed.seed

run:
	$(PY)/flask --app app run --debug
