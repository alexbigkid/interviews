.PHONY:	upgrade_setuptools install_test install_dev test settings help
.SILENT: coverage

upgrade_setuptools:
	pip install --upgrade setuptools

install_test: upgrade_setuptools
	pip install --requirement requirements_test.txt

install_dev: upgrade_setuptools
	pip install --requirement requirements_test.txt

test:
	python -m unittest discover --start-directory .

test_ff:
	python -m unittest discover --start-directory . --failfast

test_v:
	python -m unittest discover --start-directory . --verbose

test_vff:
	python -m unittest discover --start-directory . --verbose --failfast

%:
	@:

test_1:
	python -m unittest $(filter-out $@,$(MAKECMDGOALS))


coverage:
	coverage run --source ../aai-list-devices-by-project --omit="./*" -m unittest discover --start-directory .
	@echo
	coverage report
	coverage xml

settings:
	@echo "HOME             = ${HOME}"
	@echo "PWD              = ${PWD}"
	@echo "SHELL            = ${SHELL}"

help:
	@echo "Targets:"
	@echo "-----------------------------------------------------------------------------"
	@echo "  install_test             - installs test required packages"
	@echo "  install_dev              - installs dev required packages"
	@echo "  test                     - runs all tests"
	@echo "  test_ff                  - runs all tests and stops at 1st failed test"
	@echo "  test_v                   - runs all tests with verbose messaging"
	@echo "  test_vff                 - runs all tests with fail fast verbose messaging"
	@echo "  test_1 <file.class.test> - runs a single test"
	@echo "  coverage                 - runs test, produces coverage and displays it"
	@echo "-----------------------------------------------------------------------------"
	@echo "  settings                 - outputs current settings"
	@echo "  help                     - outputs this info"
