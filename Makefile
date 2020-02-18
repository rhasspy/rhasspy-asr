PYTHON_FILES = rhasspyasr/*.py *.py
PIP_INSTALL ?= install

.PHONY: reformat check test dist venv

reformat:
	scripts/format-code.sh $(PYTHON_FILES)

check:
	scripts/check-code.sh $(PYTHON_FILES)

venv:
	scripts/create-venv.sh

dist:
	python3 setup.py sdist
