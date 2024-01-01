import gspread
from oauth2client.service_account import ServiceAccountCredentials

from . import item_database
from . import recipe_database


class Spreadsheet:
    '''
    sheet interface functions shared between other files
    TODO better comments.
    '''

    def __init__(self):
        self.workbook = self._open_spreadsheet()

    def _open_spreadsheet(self):
        # use creds to create a client to interact with the Google Drive API
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        # TODO put filename in config file
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            'Shopping List-32ab969084cf.json', scope)
        client = gspread.authorize(creds)

        # Find a workbook by name and open sheets
        return client.open("Shopping List")

    def get_item_database(self):
        # Open the item sheet.
        items_sheet = self.workbook.worksheet('Items')
        # Get data from the sheet.
        item_dicts_list = items_sheet.get_all_records()

        # Construct the items dict.
        items = item_database.ItemDatabase()
        for record in item_dicts_list:
            # The record holds the name of the item and all of the groupings. The name and the groupings must be
            # provided separately to the item class, so extract the name from the record and construct an instance of
            # the item object.
            item_name = record.pop('Name')
            items.add_new_item(item_name, record)

        return items

    def get_recipe_database(self):
        # Open the recipes sheet.
        recipes_sheet = self.workbook.worksheet('Recipes')
        # Get data from the sheet.
        recipe_rows = recipes_sheet.get_all_values()

        # Construct recipes dict.
        recipes = recipe_database.RecipeDatabase()
        for recipe_row in recipe_rows:
            # The row holds the name of the recipe in the first column and all of the ingredients in subsequent columns.
            # Parse the name and the ingredients from the row to construct an instance of the recipe object.
            recipe_name = recipe_row[0]
            recipe_ingredients = [x for x in recipe_row[1:] if x != '']
            recipes.add_new_recipe(recipe_name, recipe_ingredients)

        return recipes

    def get_input_sheet_config(self):
        # Open the input sheet.
        input_sheet_config_sheet = self.workbook.worksheet('Input')
        # Get input config data.
        input_sheet_config_data_dict = {}
        number_of_columns = 4
        # TODO surely this can be improved? Use get, or get_values instead? Issue #32.
        for column_index in range(1, number_of_columns):
            # Pull column data into list.
            column = input_sheet_config_sheet.col_values(column_index)
            column_heading = column[0]
            # Remove any empty strings with list comprehension.
            column_data = [x for x in column[1:] if x]
            input_sheet_config_data_dict[column_heading] = column_data

        meals_to_buy_list = input_sheet_config_data_dict['Meals To Buy']
        exclusions_list = input_sheet_config_data_dict['Exclusions']
        inclusions_list = input_sheet_config_data_dict['Inclusions']

        return meals_to_buy_list, exclusions_list, inclusions_list
