
.PHONY : clean


lint: install-dev
	python -m black pychadwicklib/ tests/ ./setup.py
	python -m flake8 pychadwicklib


test: install
	pytest tests/

clean:
	rm -fr pychadwicklib.egg-info
	rm -fr build
	rm -fr dist
	python setup.py clean
	cd src && make clean

dist: clean
	python setup.py bdist_wheel
	python setup.py sdist


install-dev:
	pip install --quiet -r requirements-dev.txt

install: install-dev
	pip install --quiet -r requirements.txt
	python setup.py install
