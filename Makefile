.PHONY: clean-pyc clean-build docs

IMPORT_TO_ADD = "from __future__ import division, print_function, with_statement"

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "install - install metaopt and all dependencies"
	@echo "isort - sanititize imports with isort"
	@echo "lint - check style with flake8"	
	@echo "release - package and upload a release"
	@echo "sdist - package"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "venv - create and activate virtual environment"

check-manifest:
	 check-manifest

clean: clean-backup clean-build clean-patch clean-pyc clean-reverse clean-release

clean-backup:
	find . -name '*~' -exec rm -f {} +
	find . -name '*.bak' -exec rm -f {} +

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info
	rm -fr *.egg

clean-patch:
	find . -name '*.orig' -exec rm -f {} +
	find . -name '*.rej' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +

clean-reverse:
	rm classes_MetaOpt.png packages_MetaOpt.png &> /dev/null || exit 0

coverage:
	coverage run --source metaopt setup.py nosetests
	coverage report -m
	coverage html
	open htmlcov/index.html

docs:
	sphinx-apidoc -o docs/ metaopt
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html &> /dev/null || echo "";  # works under MacOS
	start docs/_build/html/index.html &> /dev/null || echo "";  # works under Windows
	xdg-open docs/_build/html/index.html &> /dev/null || echo "";  # works under Linux

install:
	python setup.py install
	find . -wholename "./requirements_*.txt" -exec pip install -r {} \;

isort:
	find examples -name "*.py" -exec isort -a $(IMPORT_TO_ADD) {} &> /dev/null +
	find metaopt -name "*.py" -exec isort -a $(IMPORT_TO_ADD) {} &> /dev/null +

lint:
	find metaopt -name '*.py' -exec flake8 {} +
	python3 setup.py flake8
	pylint metaopt

reindent:
	find metaopt -name "*.py" -exec python `locate reindent.py` {} +

release: clean
	python setup.py sdist upload

reverse: clean-reverse
	pyreverse --ignore tests -o png -p MetaOpt metaopt
	open ./classes_MetaOpt.png &> /dev/null || echo "";  # works under MacOS
	open ./packages_MetaOpt.png &> /dev/null || echo "";  # works under MacOS
	start ./classes_MetaOpt.png &> /dev/null || echo "";  # works under Windows
	start ./packages_MetaOpt.png &> /dev/null || echo "";  # works under Windows
	xdg-open ./classes_MetaOpt.png &> /dev/null || echo "";  # works under Linux
	xdg-open ./packages_MetaOpt.png &> /dev/null || echo "";  # works under Linux

sdist: clean
	python setup.py sdist
	ls -l dist

test:
	python setup.py nosetests

test-all:
	tox
