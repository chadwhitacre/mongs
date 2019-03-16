.tox/python:
	python3 -m venv .tox/python
	.tox/python/bin/pip install -r requirements.txt

clean:
	rm -rf .tox

run: .tox/python
	.tox/python/bin/python -m launch
