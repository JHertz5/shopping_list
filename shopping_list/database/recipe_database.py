from . import recipe


class RecipeDatabase:
    '''
    TODO comment
    '''

    def __init__(self, recipe_dict={}):
        # Validate and assign initial attribute values.
        assert isinstance(recipe_dict, dict)
        self._recipe_dict = recipe_dict

    def incr_quantities_for_list_of_irecipes(self, recipe_list):
        assert isinstance(recipe_list, list)

        for recipe_name in recipe_list:
            self.incr_recipe_quantity(recipe_name)

    def incr_recipe_quantity(self, recipe_name):
        assert isinstance(recipe_name, str)

        if not recipe_name in self._recipe_dict.keys():
            self.add_new_recipe(recipe_name)

        self._recipe_dict[recipe_name].incr_quantity()

    def add_new_recipe(self, recipe_name, recipe_ingredients=[]):
        self._recipe_dict[recipe_name] = recipe.Recipe(recipe_name, recipe_ingredients)

    def get_non_zero_quantity_recipe_name_list(self):
        recipe_name_list = []
        for recipe_name, recipe_obj in self._recipe_dict.items():
            if recipe_obj.get_quantity() > 0:
                recipe_name_list.append(recipe_name)
        return recipe_name_list

    def get_non_zero_quantity_recipe_ingredient_list(self):
        recipe_ingredient_list = []
        for recipe_name in self.get_non_zero_quantity_recipe_name_list():
            recipe_ingredient_list += self._recipe_dict[recipe_name].get_ingredients_list()
        return recipe_ingredient_list

    def get_non_zero_quantity_recipe_quanitity_dict(self):
        # TODO I think this method is too specific. Replace with a dict of just the non-zero recipes?
        # TODO I feel like this would be simpler if each recipe was just a dict rather than an object.
        recipe_name_list = self.get_non_zero_quantity_recipe_name_list()
        recipe_quantity_dict = {}
        for recipe_name in recipe_name_list:
            recipe_quantity_dict[recipe_name] = self._recipe_dict[recipe_name].get_quantity()
        return recipe_quantity_dict

    def get_recipes_containing_ingredient(self, ingredient):
        # TODO if this was a dict of dicts, we would just do
        # return [x for x in recipes.keys() if search_ingredient in recipes[x]]
        recipe_list = [x for x in self._recipe_dict.keys() if self._recipe_dict[x].is_ingredient_in_recipe(ingredient)]
        return recipe_list
