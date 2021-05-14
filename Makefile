SHELL := /bin/bash


ifeq ($(uname_S), Windows)
    venv\Scripts\activate.bat
endif

ifeq ($(uname_S), Linux)
    . venv/bin/activate
endif

test:
	python3 -m unittest discover tests
.PHONY: test

lint:
	pylint *.py --ignore-patterns=test_.*?py,__init*
.PHONY: lint