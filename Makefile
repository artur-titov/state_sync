# ---------------------------------------------------------------------+
# Call to 'help' section with 'make' command
help:
	@echo "\nSupported commands             Description\n"
	@echo "--------------------------------------------------------"
	@echo "make test                      Run Python unit tests."
	@echo "make sync FROM=<file>          Lint Ansible files."
	@echo "--------------------------------------------------------\n"


# ---------------------------------------------------------------------+
# Dev commands:
test:
	python3 -m unittest discover -s tests


# ---------------------------------------------------------------------+
# StateSync start command:
# FROM - path to config yml file.
sync:
	python3 start.py "${FROM}"
