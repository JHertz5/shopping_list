'''
A class representing an item.

Attributes:
- name (str): The name of the item.
- group (str): The group of the item.
- quantity (int): The quantity of the item.
'''

class Item:
    def __init__(self, name, group, quantity):
        # Validate and assign initial attribute values.
        if not isinstance(name, str):
            raise ValueError('name must be a string.', name)
        self._name = name
        if not isinstance(group, str):
            raise ValueError('group must be a string.', group)
        self._group = group
        if not isinstance(quantity, int):
            raise ValueError('quantity must be an integer.', quantity)
        self._quantity = quantity

    def get_name(self):
        return self._name

    def set_group(self, group):
        self._group = group

    def get_group(self):
        return self._group

    def set_quantity(self, quantity):
        self._quantity = quantity

    def get_quantity(self):
        return self._quantity
