''' sheet interface functions shared between other files '''

import gspread
from oauth2client.service_account import ServiceAccountCredentials

def open_spreadsheet():
    #use creds to create a client to interact with the Google Drive API
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
        ]
    #TODO put filename in config file
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'Shopping List-32ab969084cf.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open sheets
    return client.open("Shopping List")

def get_data_recipes(sheet):
    recipes_raw = sheet.get_all_values()
    recipes = {}
    for recipe in recipes_raw:
        # create dict entry of recipe name : recipe ingredients
        recipes[recipe[0]] = [x for x in recipe[1:] if x != '']
    return recipes
