install:
	pip install -r requirements.txt

lint:
	ruff check .

format:
	ruff format .

black:
	black .

typecheck:
	mypy --config-file mypy.ini .

qa:
	ruff check .
	mypy --config-file mypy.ini .
