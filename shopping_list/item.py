class Item:
    '''
    A class representing an item.
    TODO better comments, remove args.

    Args:
    - name (str): The name of the item.
    - groups_dict (dict[str]): The group value for each possible grouping method.
    '''

    def __init__(self, name, groups_dict):
        # Validate and assign initial attribute values.
        assert isinstance(name, str)
        self._name = name
        assert isinstance(groups_dict, dict)
        self._groups_dict = groups_dict
        self._quantity = 0

    def __str__(self):
        return "TODO"

    # TODO name unused?
    def get_name(self):
        return self._name

    def get_group(self, grouping_method):
        return self._groups_dict[grouping_method]

    def incr_quantity(self, incr_num):
        self._quantity += incr_num

    def reset_quantity(self):
        self._quantity = 0

    def get_quantity(self):
        return self._quantity
