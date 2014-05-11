.PHONY: clean-pyc clean-build docs

IMPORT_TO_ADD = "from __future__ import absolute_import, division, print_function, unicode_literals, with_statement"

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "install - install metaopt and all dependencies"
	@echo "isort - sanititize imports with isort"
	@echo "lint - check style with flake8"	
	@echo "release - package and upload a release"
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

clean-release: clean-build
	rm -rf venv-27-sdist  # virtualenv for py27-sdist
	rm -rf venv-27-wheel # virtualenv for py27-wheel
	rm -rf metaopt-pypi-test  # install for packages from PyPI's test server

clean-reverse:
	rm classes_MetaOpt.png packages_MetaOpt.png &> /dev/null || exit 0

coverage:
	nosetests
	coverage report -m
	coverage html
	open htmlcov/index.html

coding-comment:
	find metaopt examples -name "*.py" -exec python3 -c "import sys;[tuple[1].\
	write(''.join(['# -*- coding: utf-8 -*-\n'] + tuple[0])) for tuple in [(op\
	en(filepath, 'r').readlines()[:], open(filepath, 'w')) for filepath in sys\
	.argv[1:] if open(filepath).readlines() and not open(filepath).readlines()\
	[0] == '# -*- coding: utf-8 -*-\n']]" {} + 

docs:
	#sphinx-apidoc -o docs/ metaopt
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

release-build: clean-release release-build-sdist release-build-wheel

release-build-sdist:
	python setup.py sdist
	virtualenv venv-27-sdist
	venv-27-sdist/bin/pip install --no-index dist/metaopt-*.tar.gz
	venv-27-sdist/bin/python -c "import metaopt; print metaopt.__version__"

release-build-wheel:
	python setup.py bdist_wheel
	virtualenv venv-27-wheel
	venv-27-wheel/bin/pip install --use-wheel --no-index dist/metaopt-*.whl
	venv-27-wheel/bin/python -c "import metaopt; print metaopt.__version__"

release-test: release-build
	python setup.py register -r test
	python setup.py sdist upload -r test
	python setup.py bdist_wheel upload -r test
	pip install --target metaopt-pypi-test -i https://testpypi.python.org/pypi metaopt
	pip install --use-wheel --target metaopt-pypi-test -i https://testpypi.python.org/pypi metaopt

release: release-build release-test
	python setup.py register -r pypi
	python setup.py sdist upload -r pypi
	python setup.py bdist_wheel upload -r pypi

reverse: clean-reverse
	pyreverse --ignore tests -o png -p MetaOpt metaopt
	open ./classes_MetaOpt.png &> /dev/null || echo "";  # works under MacOS
	open ./packages_MetaOpt.png &> /dev/null || echo "";  # works under MacOS
	start ./classes_MetaOpt.png &> /dev/null || echo "";  # works under Windows
	start ./packages_MetaOpt.png &> /dev/null || echo "";  # works under Windows
	xdg-open ./classes_MetaOpt.png &> /dev/null || echo "";  # works under Linux
	xdg-open ./packages_MetaOpt.png &> /dev/null || echo "";  # works under Linux

test:
	coverage run --source=metaopt setup.py nosetests

test-all:
	tox
