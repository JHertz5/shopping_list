#!/usr/bin/env python

''' main script for user interface '''

import sys

from . import command_line_args
from . import generate_shopping_list
from . import get_recipe_urls
from . import suggest_recipe
from . import version


def print_help_message(options_dict):
    help_string = "usage: " + __package__ + " "
    options_strings = ["[" + " | ".join(options_dict[key]) + "] " for key in options_dict.keys()]
    print(help_string + "".join(options_strings))


def main():

    args = command_line_args.parse_command_line_args()

    if args.generate_list:
        generate_shopping_list.generate_shopping_list()
    elif args.suggest_recipe:
        suggest_recipe.suggest_recipe()
    elif args.recipe_url:
        get_recipe_urls.get_recipe_urls()
    elif args.version:
        version.print_version_info()


if __name__ == "__main__":
    main()
