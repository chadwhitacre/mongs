.tox/python:
	python3 -m venv .tox/python
	.tox/python/bin/pip install -r requirements.txt

clean:
	rm -rf .tox

run: .tox/python
	ASPEN_WWW_ROOT=www PORT=8080 .tox/python/bin/python -m pando
