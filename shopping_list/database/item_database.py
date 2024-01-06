from . import item


class ItemDatabase:
    '''
    TODO comment
    '''

    def __init__(self):
        self._item_dict = {}

    def reset_quantity(self, item_name):
        assert isinstance(item_name, str)
        assert item_name in self._item_dict.keys()
        self._item_dict[item_name].reset_quantity()

    def incr_quantity(self, item_name):
        assert isinstance(item_name, str)

        if not item_name in self._item_dict.keys():
            self.insert(item_name)

        self._item_dict[item_name].incr_quantity()

    def insert(self, item_name, group='none'):
        self._item_dict[item_name] = item.Item(group=group)

    def get_names_of_selected(self):
        return_list = []
        for name, obj in self._item_dict.items():
            if obj.quantity > 0:
                return_list.append(name)
        return return_list

    def get_quantity_dict_of_selected(self):
        name_list = self.get_names_of_selected()
        return_dict = {}
        for name in name_list:
            return_dict[name] = self._item_dict[name].quantity
        return return_dict

    def get_dict_of_selected(self):
        return_dict = {x: self._item_dict[x] for x in self._item_dict if self._item_dict[x].quantity > 0}
        return return_dict
