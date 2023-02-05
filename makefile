VENV=.venv
SHELL=/bin/bash

python=$(VENV)/bin/python3
pip=$(VENV)/bin/pip3

# Utility scripts to prettify echo outputs
bold := '\033[1m'
sgr0 := '\033[0m'


.PHONY: bootstrap
bootstrap: venv develop


.PHONY: clean
clean:
	@echo -e $(bold)Clean up old virtualenv and cache$(sgr0)
	rm -rf $(VENV)


.PHONY: venv
venv: clean
	@echo -e $(bold)Create virtualenv$(sgr0)
	/usr/bin/python3 -m venv $(VENV)
	$(pip) install --upgrade pip pip-tools


.PHONY: develop
develop:
	@echo -e $(bold)Install and update requirements$(sgr0)
	$(python) -m pip install -r requirements.dev.txt --editable .

.PHONY: freeze
freeze:
	$(python) -m piptools compile --upgrade --resolver backtracking -o requirements.txt pyproject.toml
	$(python) -m piptools compile --upgrade --resolver backtracking -o requirements.dev.txt --extra dev --extra test pyproject.toml

.PHONY: tests
tests:
	$(python) -m pytest