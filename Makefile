# Copyright 2016 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

VIRTUALENV=virtualenv
ENV=env
PIP = $(ENV)/bin/pip
PYTHON = $(ENV)/bin/python


build:
	$(VIRTUALENV) $(ENV)
	$(PIP) install -e .
	$(PIP) install -e .[test]

test:
	$(PYTHON) -m testtools.run discover


dist:
	$(PYTHON) setup.py egg_info -r sdist


clean:
	rm -rf txSSE.egg-info
	rm -rf dist
	rm -rf env


.PHONY: dist clean
