# shopping_list
Python script to automate shopping list creation

This is a python script to automate the process of creating a shopping list. The script pulls shopping list data from a [Google Sheets spreadsheet in this format](https://docs.google.com/spreadsheets/d/1B3kR0sYUVmMu2IA-XWe45FsB8voRAKXCzPxGnjfMUiI/edit?usp=sharing). This data consists of Ingredients, Recipes, and Input. These are pretty self explanatory if you look at the spreadsheet. Once the data has been collected and processed, the shopping list used to create a [todo.txt](https://github.com/todotxt/todo.txt) file in a location local to your device.

## Setup
1. Install python dependencies - in the root of the repository, run `make init`.
2. Setup Sheet access. Here are some [instructions to get credentials for spreadsheet API access](https://github.com/burnash/gspread/blob/master/docs/oauth2.rst). The oauth token generated should be stored on the same device from which shopping_list will be run from. The path to the token should be provided as the `-t` argument, while the name of the spreadsheet should be provided as the `-s` argument.
3. Install SimpleTask (or other todo.txt compatible app). Open the file (provided with the `-g` argument) within the app to use.
