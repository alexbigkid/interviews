.PHONY:	upgrade_setuptools install install_dev test test_verbose my_dish settings help
.SILENT: my_dish coverage
SRC_HOME = src

my_dish:
	cd $(SRC_HOME) && python main.py

# -----------------------------------------------------------------------------
# Dependency installation Makefile rules
# -----------------------------------------------------------------------------
upgrade_setuptools:
	pip install --upgrade pip setuptools wheel

install: upgrade_setuptools
	pip install --requirement requirements.txt

install_test: upgrade_setuptools
	pip install --requirement requirements_test.txt

install_dev: upgrade_setuptools
	pip install --requirement requirements_dev.txt


# -----------------------------------------------------------------------------
# Running tests Makefile rules
# -----------------------------------------------------------------------------
test:
	python -m unittest discover --start-directory tests

test_v:
	python -m unittest discover --start-directory tests --verbose

test_ff:
	python -m unittest discover --start-directory tests --failfast

test_vff:
	python -m unittest discover --start-directory tests --verbose --failfast

%:
	@:

test_1:
	python -m unittest "tests.$(filter-out $@,$(MAKECMDGOALS))"

coverage:
	coverage run --source src --omit src/__init__.py -m unittest discover --start-directory tests
	@echo
	coverage report
	coverage xml


# -----------------------------------------------------------------------------
# Clean up Makefile rules
# -----------------------------------------------------------------------------
clean:
	@echo "deleting log files:"
	@echo "___________________"
	@if [ -f logs/* ]; then ls -la logs/*; fi;
	@if [ -f logs/* ]; then rm -rf logs/*; fi;
	@echo
	@echo "deleting dist files:"
	@echo "___________________"
	@if [ -d dist ]; then ls -la dist; fi;
	@if [ -d dist ]; then rm -rf dist; fi;
	@echo
	@echo "deleting build files:"
	@echo "___________________"
	@if [ -d build ]; then ls -la build; fi;
	@if [ -d build ]; then rm -rf build; fi;
	@echo
	@echo "deleting egg-info files:"
	@echo "___________________"
	@if [ -d *.egg-info ]; then ls -la *.egg-info; fi
	@if [ -d *.egg-info ]; then rm -rf *.egg-info; fi
	@echo
	@echo "deleting __pycache__ directories:"
	@echo "___________________"
	find . -name "__pycache__" -type d -prune
	rm -rf  $(find . -name "__pycache__" -type d -prune)


# -----------------------------------------------------------------------------
# Display info Makefile rules
# -----------------------------------------------------------------------------
settings:
	@echo "HOME             = ${HOME}"
	@echo "PWD              = ${PWD}"
	@echo "SHELL            = ${SHELL}"

help:
	@echo "Targets:"
	@echo "-----------------------------------------------------------------------------"
	@echo "  my_dish            - executes the main program"
	@echo "-----------------------------------------------------------------------------"
	@echo "  install            - installs required packages"
	@echo "  install_test       - installs required packages for test"
	@echo "  install_dev        - installs required development packages"
	@echo "-----------------------------------------------------------------------------"
	@echo "  test               - runs test"
	@echo "  test_v             - runs test with verbose messaging"
	@echo "  test_ff            - runs test fast fail"
	@echo "  test_vff           - runs test fast fail with verbose messaging"
	@echo "  test_1 <file.class.test> - runs a single test"
	@echo "  coverage           - runs test, produces coverage and displays it"
	@echo "-----------------------------------------------------------------------------"
	@echo "  clean              - cleans some auto generated build files"
	@echo "  settings           - outputs current settings"
	@echo "  help               - outputs this info"
