import unittest

from shopping_list.report import preview


class TestPreview(unittest.TestCase):

    def test_generate_report(self):
        test_recipe_dict = {
            'recipe1': 1,
            'recipe2': 2,
            'recipe3': 3
        }
        test_ingredient_dict = {
            'ingredient1': 1,
            'ingredient2': 2,
            'ingredient3': 3
        }
        expected_string = '\nRecipes:\n\t' \
            + 'recipe1 (1)\n\t' \
            + 'recipe2 (2)\n\t' \
            + 'recipe3 (3)' \
            + '\ningredients:\n\t' \
            + 'ingredient1 (1)\n\t' \
            + 'ingredient2 (2)\n\t' \
            + 'ingredient3 (3)' \
            + '\n'
        actual_string = preview._generate_report(test_recipe_dict, test_ingredient_dict)
        self.assertEqual(actual_string, expected_string)
