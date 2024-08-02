import unittest
from unittest import mock
from io import StringIO

from shopping_list import recommend_recipe
from shopping_list.database import recipe_database

class TestReccomendRecipe(unittest.TestCase):

    def test_recipe_search(self):
        ingredient_list = ['Apples', 'Bananas', 'Cucumber', 'dark chocolate']
        test_ingredient = ingredient_list[0]
        recipes = recipe_database.RecipeDatabase()
        recipes.insert('Fruit Salad', ['Apples', 'Bananas'])
        recipes.insert('Apple pie', ['Apples', 'Flour', 'dark chocolate'])

        with mock.patch('builtins.input', return_value=test_ingredient), mock.patch('sys.stdout', new=StringIO()) as mock_stdout:
            actual_list = recommend_recipe.recipe_search(ingredient_list, recipes)
            actual_stdout = mock_stdout.getvalue().strip()

        expected_list = ['Fruit Salad', 'Apple pie']
        expected_stdout = 'known ingredients: Apples, Bananas, Cucumber, dark chocolate\nsearching for ' + test_ingredient

        self.assertEqual(actual_list, expected_list)
        self.assertEqual(actual_stdout, expected_stdout)

    def test_recipe_search(self):
        ingredient_list = ['Apples', 'Bananas', 'Cucumber', 'dark chocolate']
        test_ingredient = ingredient_list[0]
        recipes = recipe_database.RecipeDatabase()
        recipes.insert('Fruit Salad', ['Apples', 'Bananas'])
        recipes.insert('Apple pie', ['Apples', 'Flour', 'dark chocolate'])

        with mock.patch('builtins.input', return_value=test_ingredient), mock.patch('sys.stdout', new=StringIO()) as mock_stdout:
            actual_list = recommend_recipe.recipe_search(ingredient_list, recipes)
            actual_stdout = mock_stdout.getvalue().strip()

        expected_list = ['Fruit Salad', 'Apple pie']
        expected_stdout = 'known ingredients: Apples, Bananas, Cucumber, dark chocolate\nsearching for ' + test_ingredient

        self.assertEqual(actual_list, expected_list)
        self.assertEqual(actual_stdout, expected_stdout)

        # TODO self.assertRaises(SystemExit)
        # https://stackoverflow.com/questions/15672151/is-it-possible-for-a-unit-test-to-assert-that-a-method-calls-sys-exit
