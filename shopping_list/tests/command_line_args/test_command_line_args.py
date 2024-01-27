import unittest
import os
import sys

from shopping_list import command_line_args

test_list_filename = 'test_list.txt'
test_token_filename = 'test_token.json'
test_sheet_name = 'Google Sheet Title'

token_path = os.path.join(os.path.dirname(__file__), test_token_filename)


class testCommandLineArgs(unittest.TestCase):

    def test_valid_recommend(self):
        '''
        Test a valid set of arguments for the recipe recommendation behaviour.
        '''
        sys.argv = ['shopping_list', '-r', '-t', token_path, '-s', test_sheet_name]
        actual_dict = command_line_args.parse_command_line_args().__dict__

        expected_dict = {
            'generate_list': None,
            'recommend_recipe': True,
            'token_filename': token_path,
            'sheet_name': test_sheet_name,
            'version': False
        }

        self.assertEqual(actual_dict, expected_dict)

    def test_valid_generate(self):
        '''
        Test a valid set of arguments for the list generation behaviour.
        '''
        sys.argv = ['shopping_list', '-g', test_list_filename, '-t', token_path, '-s', test_sheet_name]
        actual_dict = command_line_args.parse_command_line_args().__dict__

        expected_dict = {
            'generate_list': test_list_filename,
            'recommend_recipe': False,
            'token_filename': token_path,
            'sheet_name': test_sheet_name,
            'version': False
        }

        self.assertEqual(actual_dict, expected_dict)
