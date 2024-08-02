# Install all required python packages.
init:
	pip install -r requirements.txt

# Run a suite of unit tests.
test:
	python -m unittest

# Make a list in a deafult location, using any available JSON file as the token and assuming the name of the shopping
# list.
list:
	./bin/shopping_list -g test.txt -t *.json -s "Shopping List"
