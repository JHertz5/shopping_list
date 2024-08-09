# Install all required python packages.
init:
	pip install -r requirements.txt

# Run a suite of unit tests.
test:
	python -m unittest

ENTRY_SCRIPT_PATH=./bin/shopping_list
DEFAULT_CONFIG_VALUES=-t *.json -s "Shopping List"

# Make a list in a default location, using any available JSON file as the token and assuming the name of the shopping
# list.
list:
	${ENTRY_SCRIPT_PATH} -g test.txt ${DEFAULT_CONFIG_VALUES}

# Start recommendation, using any available JSON file as the token and assuming the name of the shopping list.
recommend:
	${ENTRY_SCRIPT_PATH} -r ${DEFAULT_CONFIG_VALUES}
