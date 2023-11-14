VENV=.venv
SHELL=/bin/bash

python=$(VENV)/bin/python3
pip=$(python) -m pip

# Utility scripts to prettify echo outputs
bold := '\033[1m'
sgr0 := '\033[0m'


.PHONY: bootstrap
bootstrap: venv develop


.PHONY: clean
clean:
	@echo -e $(bold)Clean up old virtualenv and cache$(sgr0)
	rm -rf $(VENV) *.egg-info


.PHONY: venv
venv: clean
	@echo -e $(bold)Create virtualenv$(sgr0)
	python3 -m venv $(VENV)
	$(pip) install --upgrade pip pip-tools


.PHONY: develop
develop:
	@echo -e $(bold)Install and update requirements$(sgr0)
	$(pip) install -r requirements.txt 
	$(pip) install --editable .[develop]
	$(pip) install --editable .[testing]
	$(pip) install --editable .

.PHONY: requirements
requirements:
	$(python) -m piptools compile --upgrade \
				--resolver backtracking \
				--output-file requirements.txt \
				pyproject.toml
				
.PHONY: tests
tests:
	$(python) -m pytest