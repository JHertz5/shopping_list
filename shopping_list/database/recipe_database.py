from . import recipe
from .item_database import ItemDatabase


class RecipeDatabase(ItemDatabase):
    '''
    TODO comment
    '''

    def insert(self, recipe_name, ingredient_list=[]):
        self._item_dict[recipe_name] = recipe.Recipe(ingredient_list=ingredient_list)

    def get_ingredient_list_of_selected(self):
        return_list = []
        for name in self.get_names_of_selected():
            return_list += self._item_dict[name].ingredient_list
        return return_list

    def get_recipes_containing_ingredient(self, ingredient):
        return_list = [x for x in self._item_dict.keys() if self._item_dict[x].ingredient_is_in_recipe(ingredient)]
        return return_list
