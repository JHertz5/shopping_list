class Recipe:
    '''
    A class representing a recipe.
    TODO better comments, remove args.

    Args:
    - name (str): The name of the recipe.
    - url (str): The URL of the recipe.
    - items_list (list[str]): A list of items (i.e. ingredients) for the recipe.
    '''

    def __init__(self, name, items_list, url=''):
        # Validate and assign initial attribute values.
        assert isinstance(name, str)
        # TODO name unused?
        self._name = name
        assert isinstance(items_list, list)
        self._items_list = items_list
        # TODO url is currently unused. Remove?
        assert isinstance(url, str)
        self._url = url
        self._quantity = 0

    def get_name(self):
        return self._name

    def get_url(self):
        return self._url

    def get_items_list(self):
        return self._items_list

    def is_item_in_recipe(self, item):
        return item in self._items_list

    def incr_quantity(self):
        self._quantity += 1

    def get_quantity(self):
        return self._quantity
