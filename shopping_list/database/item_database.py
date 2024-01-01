from . import item


class ItemDatabase:
    '''
    TODO comment
    '''

    def __init__(self, item_dict={}):
        # Validate and assign initial attribute values.
        assert isinstance(item_dict, dict)
        self._item_dict = item_dict

    def get_item_dict(self):
        return self._item_dict

    def reset_quantities_for_list_of_items(self, item_list):
        assert isinstance(item_list, list)
        for item_name in item_list:
            self.reset_item_quantity(item_name)

    def incr_quantities_for_list_of_items(self, item_list):
        '''
        TODO comment
        Duplicates are allowed and will increment the quantity of the item once for each occurrence.
        '''
        assert isinstance(item_list, list)
        for item_name in item_list:
            self.incr_item_quantity(item_name)

    def reset_item_quantity(self, item_name):
        assert isinstance(item_name, str)
        assert item_name in self._item_dict.keys()
        self._item_dict[item_name].reset_quantity()

    def incr_item_quantity(self, item_name):
        assert isinstance(item_name, str)

        if not item_name in self._item_dict.keys():
            self.add_new_item(item_name)

        self._item_dict[item_name].incr_quantity()

    def add_new_item(self, item_name, groups_dict={}):
        self._item_dict[item_name] = item.Item(item_name, groups_dict)

    def get_non_zero_quantity_item_name_list(self):
        item_name_list = []
        for item_name, item_obj in self._item_dict.items():
            if item_obj.get_quantity() > 0:
                item_name_list.append(item_name)
        return item_name_list

    def get_non_zero_quantity_item_quanitity_dict(self):
        # TODO I feel like this would be simpler if each item was just a dict rather than an object.
        item_name_list = self.get_non_zero_quantity_item_name_list()
        item_quantity_dict = {}
        for item_name in item_name_list:
            item_quantity_dict[item_name] = self._item_dict[item_name].get_quantity()
        return item_quantity_dict

    def get_non_zero_quantity_item_dict(self):
        non_zero_quantity_item_dict = {
            x: self._item_dict[x] for x in self._item_dict if self._item_dict[x].get_quantity() > 0
        }
        return non_zero_quantity_item_dict
