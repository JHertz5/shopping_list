import gspread
from oauth2client.service_account import ServiceAccountCredentials

from . import data


class Wrapper:
    '''
    sheet interface functions shared between other files
    TODO better comments.
    '''

    def __init__(self):
        self._workbook = self._open_spreadsheet()
        # Open the ingredient sheet.
        self._ingredients_sheet = self._workbook.worksheet('Items')
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

    def download_ingredients_data(self):
        '''
        Pull data from the ingredients sheet into a list of dicts.
        '''
        self._ingredients_sheet_data = self._ingredients_sheet.get_all_records()

    def download_recipe_data(self):
        '''
        Pull data from the recipes sheet into a list of lists.
        '''
        self.recipes_sheet_data = self._recipes_sheet.get_values()

    def download_input_data(self):
        '''
        Pull data from the inputs sheet into a list of lists.
        '''
        self.input_list = self._input_sheet.get_values(major_dimension="COLUMNS")
        # Get input config data.
        self.input_sheet_data = {}
        for column in self.input_list:
            column_heading = column[0]
            # Remove any empty strings with list comprehension.
            column_data = list(filter(None, column[1:]))
            self.input_sheet_data[column_heading] = column_data

    def add_new_recipe_to_buy(self, recipes_to_buy_list, new_recipe_name):
        new_recipe_row = len(recipes_to_buy_list) + 1
        # TODO magic number
        new_recipe_col = 1
        self._input_sheet.update_cell(new_recipe_row, new_recipe_col, new_recipe_name)

    def get_ingredient_list(self):
        return data.get_ingredient_list(self._ingredients_sheet_data)

    def get_ingredient_grouping_options(self):
        return data.get_ingredient_grouping_options(self._ingredients_sheet_data)

    def get_ingredient_sheet_data(self, grouping_selection):
        return data.get_ingredient_sheet_data(self._ingredients_sheet_data, grouping_selection)

    def get_recipe_sheet_data(self):
        return data.get_recipe_sheet_data(self.recipes_sheet_data)

    def get_input_sheet_data(self):
        return data.get_input_sheet_data(self.input_sheet_data)
