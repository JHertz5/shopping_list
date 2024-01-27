import argparse
import glob
import sys
import os

from . import version


def parse_command_line_args():
    '''
    Parse the command line arguments using argparse.
    '''
    parser = argparse.ArgumentParser(
        prog='shopping_list',
        description='A tool for generating shopping lists from a Google Sheet.'''
    )

    parser.add_argument(
        '-v',
        '--version',
        default=False,
        action='version',
        version=version.string_version_info())

    script_selection_group = parser.add_mutually_exclusive_group(required=True)
    script_selection_group.add_argument(
        '-g',
        '--generate_list',
        metavar='LIST_FILENAME',
        type=str,
        help='generate a shopping list file with the given filename'
    )
    script_selection_group.add_argument(
        '-r',
        '--recommend_recipe',
        action='store_true',
        help='recommend recipes'
    )

    parser.add_argument(
        '-t',
        '--token_filename',
        metavar='TOKEN_FILENAME',
        type=__is_valid_file,
        help='the relative path of the file that holds the oauth token',
        required=True
    )

    parser.add_argument(
        '-s',
        '--sheet_name',
        metavar='SHEET_NAME',
        type=str,
        help='the relative name of the spreadsheet file.',
        required=True
    )

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_usage()
        sys.exit()
    else:
        return args


def __is_valid_file(value: str) -> str:
    '''
    Check an argument in argparse to be a path to an existing file
    :param value: String path to analyze.
    :return:
    '''
    # TODO
    filenames_list = glob.glob(os.path.expanduser(os.path.expandvars(value)), recursive=True)
    if len(filenames_list) == 0:
        if '*' in value:
            raise argparse.ArgumentTypeError(f"The file glob {value} did not match any files.")
        else:
            raise argparse.ArgumentTypeError(f"The file {value} does not exist.")
    return filenames_list[0]
