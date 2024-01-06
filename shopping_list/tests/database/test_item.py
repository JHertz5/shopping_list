import unittest

from shopping_list.database import item


class TestItem(unittest.TestCase):

    def test_item_exists(self):
        test_item = item.Item()
        self.assertTrue(test_item)

    def test_item_quantity(self):
        test_item = item.Item()
        self.assertIsInstance(test_item.quantity, int)
        self.assertEqual(test_item.quantity, 0, 'default is incorrect')
        test_item.quantity = 5
        self.assertEqual(test_item.quantity, 5)

    def test_incr_quantity_method(self):
        test_item = item.Item()

        # Test from initial value.
        pre_incr_value = test_item.quantity
        test_item.incr_quantity()
        self.assertEqual(test_item.quantity, pre_incr_value + 1)

        # Test from a higher value.
        test_item.quantity = 5
        pre_incr_value = test_item.quantity
        test_item.incr_quantity()
        self.assertEqual(test_item.quantity, pre_incr_value + 1)

    def test_reset_quantity_method(self):
        test_item = item.Item()
        test_item.reset_quantity()
        self.assertEqual(test_item.quantity, 0)

        test_item.quantity = 5
        test_item.reset_quantity()
        self.assertEqual(test_item.quantity, 0)
