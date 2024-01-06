import unittest

from shopping_list.database import recipe

test_ingredient_list = ['Apples', 'Bananas', 'Orange']
test_ingredient_str = test_ingredient_list[0]


class TestRecipe(unittest.TestCase):

    def test_recipe_exists(self):
        test_recipe = recipe.Recipe()
        self.assertTrue(test_recipe)

    def test_recipe_ingredient_list_default(self):
        test_recipe = recipe.Recipe()
        self.assertIsInstance(test_recipe.ingredient_list, list)
        self.assertEqual(test_recipe.ingredient_list, [])

    def test_recipe_ingredient_list(self):
        test_recipe = recipe.Recipe(ingredient_list=test_ingredient_list)
        self.assertIsInstance(test_recipe.ingredient_list, list)
        self.assertEqual(test_recipe.ingredient_list, test_ingredient_list)

    def test_recipe_ingredient_is_in_recipe_method(self):
        test_recipe = recipe.Recipe(ingredient_list=test_ingredient_list)
        self.assertTrue(test_recipe.ingredient_is_in_recipe(test_ingredient_str))
