# shopping_list
python script to generate shopping list from Google Sheets spreadsheet

This is a python script to automate the process of creating a shopping list. The script pulls shopping list data from my [Google Sheets spreadsheet](https://docs.google.com/spreadsheets/d/17Rz_LtAQ1LwB1cfCZZSNrlJu1g-M5W7wxDtt7iOh0yY/edit?usp=sharing). This data consists of Ingredients, Recipes, and Input. These are pretty self explanatory if you look at the spreadsheet. Once the data has been collected and processed, the shopping list used to create a [todo.txt](https://github.com/todotxt/todo.txt) file which is pushed to mobile via PushBullet.

## Setup
1. Install the following python dependencies
  * gspread
  * oauth2client
  * cryptography
2. Setup Sheet access
  * [Instruction to get credentials for spreadsheet API access](https://github.com/burnash/gspread/blob/master/docs/oauth2.rst)
  * Edit line 7 in database_interface.py so that the filename matches that of your .json file
3. Get your PushBullet API key
  * Get PushBullet auth key. Save it in file called '.pb'
4. Install SimpleTask (or other todo.txt compatible app)
  * Open the file within the app to use
