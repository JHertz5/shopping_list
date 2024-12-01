from . import item


class ItemDatabase:
    '''
    A database of items on a shopping list.
    '''

    def __init__(self):
        self._item_dict = {}

    def reset_quantity(self, item_name):
        assert isinstance(item_name, str)
        assert item_name in self._item_dict.keys()
        self._item_dict[item_name].reset_quantity()

    def reset_quantities(self):
        for item_name in self._item_dict.keys():
            self._item_dict[item_name].reset_quantity()

    def incr_quantity(self, item_name, incr_num=1):
        assert isinstance(item_name, str)

        if not item_name in self._item_dict.keys():
            self.insert(item_name)

        self._item_dict[item_name].incr_quantity(incr_num)

    def insert(self, item_name, group='none'):
        self._item_dict[item_name] = item.Item(group=group)

    def get_names_of_selected(self):
        return [name for name, obj in self._item_dict.items() if obj.quantity > 0]

    def get_quantity_dict_of_selected(self):
        name_list = self.get_names_of_selected()
        return {name: self._item_dict[name].quantity for name in name_list}

    def get_dict_of_selected(self):
        return {x: self._item_dict[x] for x in self._item_dict if self._item_dict[x].quantity > 0}
