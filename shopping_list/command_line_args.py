import argparse
import glob
import sys
import os


def parse_command_line_args():
    '''
    Parse the command line arguments using argparse.
    '''
    parser = argparse.ArgumentParser(
        prog='Shopping List',
        description='A tool for generating shopping lists from a Google Sheet.'''
    )

    exclsuive_group = parser.add_mutually_exclusive_group(required=True)
    exclsuive_group.add_argument(
        '-g',
        '--generate_list',
        type=str,
        metavar='FILENAME',
        help='Generate a shopping list in file FILENAME.')
    exclsuive_group.add_argument(
        '-s',
        '--suggest_recipe',
        default=False,
        action='store_true',
        help='Suggest a recipe.')
    exclsuive_group.add_argument(
        '-r',
        '--recipe_url',
        default=False,
        action='store_true',
        help='Get the URL of a recipe.')
    exclsuive_group.add_argument(
        '-v',
        '--version',
        default=False,
        action='store_true',
        help='Display version information.')

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_usage()
        sys.exit()
    else:
        return args
