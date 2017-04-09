clean:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm db.sqlite

setup:
	pip install pipenv
	pipenv lock
	pipenv install --dev

setup-dev: setup
	pipenv run python setup.py develop

install:
	pipenv install
	pipenv run python setup.py install

test:
	pipenv run pytest
