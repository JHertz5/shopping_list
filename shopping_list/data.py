from .database import item_database
from .database import recipe_database

import gspread
from oauth2client.service_account import ServiceAccountCredentials

items_sheet_name = 'Items'
recipes_sheet_name = 'Recipes'
input_sheet_name = 'Input'


class Data:
    '''
    sheet interface functions shared between other files
    TODO better comments.
    '''

    def __init__(self, spreadsheet):
        self.download_ingredients_data(spreadsheet)
        self.download_recipes_data(spreadsheet)
        self.download_input_data(spreadsheet)

    def download_ingredients_data(self, spreadsheet):
        '''
        Pull data from the ingredients sheet into a list of dicts.
        '''
        self._ingredients_sheet_data = spreadsheet.worksheet(items_sheet_name).get_all_records()
        print('ingredients retrieved')
        return

    def download_recipes_data(self, spreadsheet):
        '''
        Pull data from the recipes sheet into a list of lists.
        '''
        self._recipes_sheet_data = spreadsheet.worksheet(recipes_sheet_name).get_values()
        print('recipes retrieved')
        return

    def download_input_data(self, spreadsheet):
        '''
        Pull data from the inputs sheet into a list of lists.
        '''
        self.input_list = spreadsheet.worksheet(input_sheet_name).get_values(major_dimension="COLUMNS")
        # Get input config data.
        self._input_sheet_data = {}
        for column in self.input_list:
            column_heading = column[0]
            # Remove any empty strings with list comprehension.
            column_data = list(filter(None, column[1:]))
            self._input_sheet_data[column_heading] = column_data
        print('input retrieved')
        return

    def add_new_recipe_to_buy(self, recipes_to_buy_list, new_recipe_name):
        new_recipe_row = len(recipes_to_buy_list) + 1
        # TODO magic number
        new_recipe_col = 1
        self._input_sheet.update_cell(new_recipe_row, new_recipe_col, new_recipe_name)

    def get_ingredient_list(self):
        return [x['Name'] for x in self._ingredients_sheet_data]

    def get_ingredient_grouping_options(self):
        grouping_options = list(self._ingredients_sheet_data[0].keys())[1:]
        return grouping_options

    def get_ingredient_sheet_data(self, grouping_selection):
        # Construct the ingredients database.
        ingredients = item_database.ItemDatabase()
        for record in self._ingredients_sheet_data:
            # The record holds the name of the ingredient and all of the groupings. The name and the groupings must be
            # provided separately to the ingredient class, so extract the name from the record and construct an instance of
            # the ingredient object.
            ingredient_name = record.pop('Name')
            if grouping_selection == 'Unordered':
                group = 0
            else:
                group = record[grouping_selection]
            ingredients.insert(ingredient_name, group)

        return ingredients

    def get_recipe_sheet_data(self):
        # Construct recipes database.
        recipes = recipe_database.RecipeDatabase()
        for recipe_row in self._recipes_sheet_data:
            # The row holds the name of the recipe in the first column and all of the ingredients in subsequent columns.
            # Parse the name and the ingredients from the row to construct an instance of the recipe object.
            recipe_name = recipe_row[0]
            recipe_ingredients = [x for x in recipe_row[1:] if x != '']
            recipes.insert(recipe_name, recipe_ingredients)

        return recipes

    def get_input_sheet_data(self):
        recipes_to_buy_list = self._input_sheet_data['Meals To Buy']
        exclusions_list = self._input_sheet_data['Exclusions']
        inclusions_list = self._input_sheet_data['Inclusions']

        return recipes_to_buy_list, exclusions_list, inclusions_list


def open_spreadsheet(token_filename, sheet_name):
    # use creds to create a client to interact with the Google Drive API
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    # TODO put filename in config file
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        token_filename, scope)
    client = gspread.authorize(creds)


    # Find a spreadsheet by name and open it.
    spreadsheet = client.open(sheet_name)
    print('data connected')
    return spreadsheet
