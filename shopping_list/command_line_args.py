import argparse
import glob
import sys
import os


# TODO use/modify
def __is_valid_file(value: str) -> str:
    '''
    Check an argument in argparse to be a path to an existing file
    :param value: String path to analyze.
    :return:
    '''
    # TODO
    lFileNames = glob.glob(os.path.expanduser(os.path.expandvars(value)), recursive=True)
    if len(lFileNames) == 0:
        if '*' in value:
            raise argparse.ArgumentTypeError(f"The file glob {value} did not match any files.")
        else:
            raise argparse.ArgumentTypeError(f"The file {value} does not exist.")
    return lFileNames


def parse_command_line_args():
    '''
    Parse the command line arguments using argparse.
    '''
    parser = argparse.ArgumentParser(
        prog='Shopping List',
        description='''
            Pulls data from a Google Sheet spreadsheet, processes it, and produces a shopping list in todo.txt format
            '''
    )

    exclsuive_group = parser.add_mutually_exclusive_group()
    exclsuive_group.add_argument('-g', '--generate_list', default=False, action='store_true', help='Generate a shopping list.')
    exclsuive_group.add_argument('-s', '--suggest_recipe', default=False, action='store_true', help='Suggest a recipe.')
    exclsuive_group.add_argument('-r', '--recipe_url', default=False, action='store_true', help='Get the URL of a recipe.')
    exclsuive_group.add_argument('-v', '--version', default=False, action='store_true', help='Display version information.')

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_usage()
        sys.exit()
    else:
        return args
