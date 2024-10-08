.PHONY: install format lint test

install:
	pip install -r requirements.txt

format:
	black .

lint:
	pylint par_parser.py tests/test_par_parser.py

test:
	pytest tests/

all: install format lint test