#!/usr/bin/env python

''' main script for user interface '''

from . import command_line_args
from . import generate_shopping_list
from . import recommend_recipe


def print_help_message(options_dict):
    help_string = "usage: " + __package__ + " "
    options_strings = ["[" + " | ".join(options_dict[key]) + "] " for key in options_dict.keys()]
    print(help_string + "".join(options_strings))


def main():

    args = command_line_args.parse_command_line_args()

    if args.generate_list is not None:
        generate_shopping_list.generate_shopping_list(args.generate_list, args.token_filename, args.sheet_name)
    elif args.recommend_recipe:
        recommend_recipe.recommend_recipe(args.token_filename, args.sheet_name)
