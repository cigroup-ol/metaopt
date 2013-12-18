.PHONY: clean-pyc clean-build docs

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "install - install orges and all dependencies"
	@echo "isort - sanititize imports with isort"
	@echo "lint - check style with flake8"	
	@echo "release - package and upload a release"
	@echo "sdist - package"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "venv - create and activate virtual environment"

clean: clean-build clean-pyc clean-patchfiles clean-backupfiles

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info
	rm -fr *.egg

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +

clean-patchfiles:
	find . -name '*.orig' -exec rm -f {} +
	find . -name '*.rej' -exec rm -f {} +

clean-backupfiles:
	find . -name '*~' -exec rm -f {} +
	find . -name '*.bak' -exec rm -f {} +

coverage:
	coverage run --source orges setup.py nosetests
	coverage report -m
	coverage html
	open htmlcov/index.html

docs:
	sphinx-apidoc -o docs/ orges
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html &> /dev/null || echo "";  # works under MacOS
	start docs/_build/html/index.html &> /dev/null || echo "";  # works under Windows
	xdg-open docs/_build/html/index.html &> /dev/null || echo "";  # works under Linux

install:
	python setup.py install
	find . -wholename "./requirements_*.txt" -exec pip install -r {} \;

isort:
	find examples -name "*.py" -exec isort {} &> /dev/null +
	find orges -name "*.py" -exec isort {} &> /dev/null +
	find tests -name "*.py" -exec isort {} &> /dev/null +

lint:
	find orges -name '*.py' -exec flake8 {} +
	python3 setup.py flake8
	pylint orges

reindent:
	find orges -name "*.py" -exec python `locate reindent.py` {} +

release: clean
	python setup.py sdist upload

sdist: clean
	python setup.py sdist
	ls -l dist

test:
	python setup.py test

test-all:
	tox

venv:
	virtualenv venv
	source venv/bin/activate
