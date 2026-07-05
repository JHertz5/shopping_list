# Install all required python packages.
init:
	pip install -r requirements.txt --prefer-binary

# Run a suite of unit tests.
test:
	python -m unittest

ENTRY_SCRIPT_PATH=./bin/shopping_list
DEFAULT_CONFIG_VALUES=-t *.json -s "Shopping List"

DEFAULT_LIST_FILE=list.txt
CB_SCRIPT_NAME=../jeffrey.sh

# Create a script which will generate a shopping list and then set the Android clipboard to the contents of the list so
# that it can be copied into a todo.txt app.
cb_script:
	@echo "#!/bin/bash \n\
	cd shopping_list \n\
	make list \n\
	cat ${DEFAULT_LIST_FILE} | termux-clipboard-set \n\
	" > ${CB_SCRIPT_NAME}
	@chmod u+x ${CB_SCRIPT_NAME}

# Make a list in a default location, using any available JSON file as the token and assuming the name of the shopping
# list.
list:
	${ENTRY_SCRIPT_PATH} -g ${DEFAULT_LIST_FILE} ${DEFAULT_CONFIG_VALUES}

# Start recommendation, using any available JSON file as the token and assuming the name of the shopping list.
recommend:
	${ENTRY_SCRIPT_PATH} -r ${DEFAULT_CONFIG_VALUES}
