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
        actual_string = preview._generate_report(test_recipe_dict, test_ingredient_dict)

        expected_string = '\nRecipes:\n' \
            + '\trecipe1 (1)\n' \
            + '\trecipe2 (2)\n' \
            + '\trecipe3 (3)\n' \
            + 'ingredients:\n' \
            + '\tingredient1 (1)\n' \
            + '\tingredient2 (2)\n' \
            + '\tingredient3 (3)\n'

        self.assertEqual(actual_string, expected_string)
