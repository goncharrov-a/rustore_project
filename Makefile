install:
	pip install -r requirements.txt

lint:
	ruff check .

format:
	ruff format .

black:
	black .

typecheck:
	mypy .

qa:
	ruff check .
	mypy .
