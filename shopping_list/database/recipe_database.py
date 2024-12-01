from . import recipe
from .item_database import ItemDatabase


class RecipeDatabase(ItemDatabase):
    '''
    A database of recipes on a shopping list.
    '''

    def insert(self, recipe_name, ingredient_list=[]):
        self._item_dict[recipe_name] = recipe.Recipe(ingredient_list=ingredient_list)

    def get_recipes_containing_ingredient(self, ingredient):
        return_list = [x for x in self._item_dict.keys() if self._item_dict[x].ingredient_is_in_recipe(ingredient)]
        return return_list
