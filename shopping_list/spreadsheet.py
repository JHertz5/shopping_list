import gspread
from oauth2client.service_account import ServiceAccountCredentials

from .database import ingredient_database
from .database import recipe_database


class Spreadsheet:
    '''
    sheet interface functions shared between other files
    TODO better comments.
    '''

    def __init__(self):
        self._workbook = self._open_spreadsheet()
        # Open the ingredient sheet.
        self._ingredients_sheet = self._workbook.worksheet('ingredients')
        # Open the recipes sheet.
        self._recipes_sheet = self._workbook.worksheet('Recipes')
        # Open the input sheet.
        self._input_sheet = self._workbook.worksheet('Input')

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

    def get_ingredient_list(self):
        # Extract the first column data from the ingredients sheet excluding header row.
        ingredient_list = self._ingredients_sheet.col_values(1)[1:]
        return ingredient_list

    def get_ingredient_sheet_data(self):
        # Get data from the sheet.
        ingredient_dicts_list = self._ingredients_sheet.get_all_records()

        grouping_options = list(ingredient_dicts_list[0].keys())[1:]

        # Construct the ingredients dict.
        ingredients = ingredient_database.ingredientDatabase()
        for record in ingredient_dicts_list:
            # The record holds the name of the ingredient and all of the groupings. The name and the groupings must be
            # provided separately to the ingredient class, so extract the name from the record and construct an instance of
            # the ingredient object.
            ingredient_name = record.pop('Name')
            ingredients.add_new_ingredient(ingredient_name, record)

        return ingredients, grouping_options

    def get_recipe_sheet_data(self):
        # Get data from the sheet.
        recipe_rows = self._recipes_sheet.get_values()

        # Construct recipes dict.
        recipes = recipe_database.RecipeDatabase()
        for recipe_row in recipe_rows:
            # The row holds the name of the recipe in the first column and all of the ingredients in subsequent columns.
            # Parse the name and the ingredients from the row to construct an instance of the recipe object.
            recipe_name = recipe_row[0]
            recipe_ingredients = [x for x in recipe_row[1:] if x != '']
            recipes.add_new_recipe(recipe_name, recipe_ingredients)

        return recipes

    def get_input_sheet_data(self):
        # Get input config data.
        input_sheet_data_dict = {}
        number_of_columns = 4
        # TODO surely this can be improved? Use get, or get_values instead? Issue #32.
        for column_index in range(1, number_of_columns):
            # Pull column data into list.
            column = self._input_sheet.col_values(column_index)
            column_heading = column[0]
            # Remove any empty strings with list comprehension.
            column_data = [x for x in column[1:] if x]
            input_sheet_data_dict[column_heading] = column_data

        meals_to_buy_list = input_sheet_data_dict['Meals To Buy']
        exclusions_list = input_sheet_data_dict['Exclusions']
        inclusions_list = input_sheet_data_dict['Inclusions']

        return meals_to_buy_list, exclusions_list, inclusions_list

    def add_new_meal_to_buy(self, meals_to_buy_list, new_recipe_name):
        new_recipe_row = len(meals_to_buy_list) + 1
        # TODO magic number
        new_recipe_col = 1
        self._input_sheet.update_cell(new_recipe_row, new_recipe_col, new_recipe_name)
