import unittest

from shopping_list.database import ingredient


class TestIngredient(unittest.TestCase):

    def test_ingredient_exists(self):
        test_ingredient = ingredient.Ingredient()
        self.assertTrue(test_ingredient)

    def test_ingredient_group_default(self):
        test_ingredient = ingredient.Ingredient()
        self.assertEqual(test_ingredient.group, 'none')

    def test_ingredient_group_int(self):
        test_int = 1
        test_ingredient = ingredient.Ingredient(test_int)
        self.assertEqual(test_ingredient.group, test_int)
