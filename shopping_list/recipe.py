'''
A class representing a recipe.

Args:
- name (str): The name of the recipe.
- url (str): The URL of the recipe.
- ingredients_list (list): A list of ingredients for the recipe.
'''


class Recipe:
    def __init__(self, name, url, ingredients_list):
        # Validate and assign initial attribute values.
        if not isinstance(name, str):
            raise ValueError('name must be a string.', name)
        self._name = name
        if not isinstance(url, str):
            raise ValueError('url must be a string.', url)
        self._url = url
        if not isinstance(ingredients_list, list):
            raise ValueError('ingredients_list must be a list.', ingredients_list)
        self._ingredients_list = ingredients_list

    def get_name(self):
        return self._name

    def get_url(self):
        return self._url

    def get_ingredients_list(self):
        return self._ingredients_list

    def is_ingredient_in_recipe(self, ingredient):
        return ingredient in self._ingredients_list

    def __str__(self):
        return "TODO"
