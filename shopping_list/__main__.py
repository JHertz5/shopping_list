#!/usr/bin/env python

''' main script for user interface '''

import sys

from . import generate_shopping_list
from . import get_recipe_urls
from . import suggest_recipe

def print_help_message(options_dict):
    help_string = "usage: jeffrey.py "
    for key in options_dict.keys():
        help_string += "[" + " | ".join(options_dict[key]) + "] "
    print(help_string)

def main():

    # Get user input.
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
    else:
        user_input = ""

    options_dict = {
        'generate_list'  : ['-g', '--generate_list', ''],
        'recipe_url'     : ['-r', '--recipe_url'],
        'suggest_recipe' : ['-s', '--suggest_recipe'],
        'help'           : ['-h', '--help']
    }

    if user_input in options_dict['generate_list']:
        generate_shopping_list.generate_shopping_list()
    elif user_input in options_dict['recipe_url']:
        get_recipe_urls.get_recipe_urls()
    elif user_input in options_dict['suggest_recipe']:
        suggest_recipe.suggest_recipe()
    else:
        print('unknown option: {}'.format(user_input))
        print_help_message(options_dict)

if __name__ == "__main__":
    main()
