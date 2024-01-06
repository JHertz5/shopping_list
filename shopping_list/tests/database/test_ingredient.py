import unittest

from shopping_list.database import ingredient

test_group_int = 1


class TestIngredient(unittest.TestCase):

    def test_ingredient_exists(self):
        test_ingredient = ingredient.Ingredient()
        self.assertTrue(test_ingredient)

    def test_ingredient_group_default(self):
        test_ingredient = ingredient.Ingredient()
        self.assertIsInstance(test_ingredient.group, str)
        self.assertEqual(test_ingredient.group, 'none')

    def test_ingredient_group_int(self):
        test_ingredient = ingredient.Ingredient(group=test_group_int)
        self.assertIsInstance(test_ingredient.group, int)
        self.assertEqual(test_ingredient.group, test_group_int)
