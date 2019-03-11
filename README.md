# shopping_list
python script to generate shopping list from Google Sheets spreadsheet

This is a python script to automate the process of creating a shopping list. The script pulls shopping list data from my [Google Sheets spreadsheet](https://docs.google.com/spreadsheets/d/17Rz_LtAQ1LwB1cfCZZSNrlJu1g-M5W7wxDtt7iOh0yY/edit?usp=sharing). This data consists of Ingredients, Recipes, and Input. These are pretty self explanatory if you look at the spreadsheet. Once the data has been collected and processed, the shopping list is emailed to a specified email address. 

## Setup
1. Install the following python dependencies
  * gspread
  * oauth2client
  * cryptography
2. Setup Sheet access
  * [Instruction to get credentials for spreadsheet API access](https://github.com/burnash/gspread/blob/master/docs/oauth2.rst)
3. Setup email account
  * Create file 'email_addresses.txt' containing the to and from email addresses as follows:
    ```
    from@address.com
    to@address.com
    ```
  * Run  `python3 encrypt.py` and enter the password for the from email address when prompted for input
