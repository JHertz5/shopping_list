import unittest

from shopping_list.report import checklist
from shopping_list.database import item


class TestChecklist(unittest.TestCase):

    def test_generate_line_with_no_tags(self):
        test_text = 'I hope that the test passes'
        test_group = '1'
        actual_string = checklist._generate_line(test_text, test_group)

        expected_string = '{} @{}\n'.format(test_text, test_group)

        self.assertEqual(actual_string, expected_string)

    def test_generate_line_with_tags(self):
        test_text = 'I hope that the test passes'
        test_group = '1'
        test_tag_list = ['Green', 'Red']
        actual_string = checklist._generate_line(test_text, test_group, test_tag_list)

        expected_string = '{} @{} +{} +{}\n'.format(test_text, test_group, test_tag_list[0], test_tag_list[1])

        self.assertEqual(actual_string, expected_string)

    def test_generate_report(self):
        test_recipe_dict = {
            'recipe1': 1,
            'recipe2': 2,
            'recipe3': 3
        }
        test_ingredient_dict = {
            'ingredient1': item.Item(quantity=1, group='a'),
            'ingredient2': item.Item(quantity=2, group='none'),
            'ingredient3': item.Item(quantity=3, group=1)
        }
        actual_list = checklist._generate_report(test_recipe_dict, test_ingredient_dict)

        expected_list = [
            'recipe1 (1) @recipes\n',
            'recipe2 (2) @recipes\n',
            'recipe3 (3) @recipes\n',
            'ingredient1 (1) @a\n',
            'ingredient2 (2) @none\n',
            'ingredient3 (3) @1\n',
        ]

        self.assertEqual(actual_list, expected_list)
