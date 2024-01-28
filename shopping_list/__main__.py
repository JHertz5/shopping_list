#!/usr/bin/env python

''' main script for user interface '''

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from . import command_line_args
from . import generate_shopping_list
from . import recommend_recipe
from . import data


def print_help_message(options_dict):
    help_string = "usage: " + __package__ + " "
    options_strings = ["[" + " | ".join(options_dict[key]) + "] " for key in options_dict.keys()]
    print(help_string + "".join(options_strings))


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

def main():

    args = command_line_args.parse_command_line_args()

    spreadsheet = open_spreadsheet(args.token_filename, args.sheet_name)
    data_obj = data.Data(spreadsheet)

    if args.generate_list is not None:
        generate_shopping_list.generate_shopping_list(spreadsheet, data_obj, args.generate_list)
    elif args.recommend_recipe:
        recommend_recipe.recommend_recipe(spreadsheet, data_obj)
