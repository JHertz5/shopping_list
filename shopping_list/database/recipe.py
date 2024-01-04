class Recipe:
    '''
    A class representing a recipe.
    TODO better comments, remove args.

    Args:
    - name (str): The name of the recipe.
    - url (str): The URL of the recipe.
    - ingredients_list (list[str]): A list of ingredients (i.e. ingredients) for the recipe.
    '''

    def __init__(self, name, ingredients_list, url=''):
        # Validate and assign initial attribute values.
        assert isinstance(name, str)
        # TODO name unused?
        self._name = name
        assert isinstance(ingredients_list, list)
        self._ingredients_list = ingredients_list
        # TODO url is currently unused. Remove?
        assert isinstance(url, str)
        self._url = url
        self._quantity = 0

    def get_name(self):
        return self._name

    def get_url(self):
        return self._url

    def get_ingredients_list(self):
        return self._ingredients_list

    def is_ingredient_in_recipe(self, ingredient):
        return ingredient in self._ingredients_list

    def incr_quantity(self):
        self._quantity += 1

    def get_quantity(self):
        return self._quantity
