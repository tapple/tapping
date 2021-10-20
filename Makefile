.PHONY: install mypy

install:
	pip install .

mypy:
	pip install mypy
	mypy pingdiscover