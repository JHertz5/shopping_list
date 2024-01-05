from . import ingredient


class ingredientDatabase:
    '''
    TODO comment
    '''

    def __init__(self, ingredient_dict={}):
        # Validate and assign initial attribute values.
        assert isinstance(ingredient_dict, dict)
        self._ingredient_dict = ingredient_dict

    def get_ingredient_dict(self):
        return self._ingredient_dict

    def reset_quantities_for_list_of_ingredients(self, ingredient_list):
        assert isinstance(ingredient_list, list)
        for ingredient_name in ingredient_list:
            self.reset_ingredient_quantity(ingredient_name)

    def incr_quantities_for_list_of_ingredients(self, ingredient_list):
        '''
        TODO comment
        Duplicates are allowed and will increment the quantity of the ingredient once for each occurrence.
        '''
        assert isinstance(ingredient_list, list)
        for ingredient_name in ingredient_list:
            self.incr_ingredient_quantity(ingredient_name)

    def reset_ingredient_quantity(self, ingredient_name):
        assert isinstance(ingredient_name, str)
        assert ingredient_name in self._ingredient_dict.keys()
        self._ingredient_dict[ingredient_name].reset_quantity()

    def incr_ingredient_quantity(self, ingredient_name):
        assert isinstance(ingredient_name, str)

        if not ingredient_name in self._ingredient_dict.keys():
            self.add_new_ingredient(ingredient_name)

        self._ingredient_dict[ingredient_name].incr_quantity()

    def add_new_ingredient(self, ingredient_name, group='none'):
        self._ingredient_dict[ingredient_name] = ingredient.Ingredient(ingredient_name, group=group)

    def get_non_zero_quantity_ingredient_name_list(self):
        ingredient_name_list = []
        for ingredient_name, ingredient_obj in self._ingredient_dict.items():
            if ingredient_obj.quantity > 0:
                ingredient_name_list.append(ingredient_name)
        return ingredient_name_list

    def get_non_zero_quantity_ingredient_quanitity_dict(self):
        # TODO I feel like this would be simpler if each ingredient was just a dict rather than an object.
        ingredient_name_list = self.get_non_zero_quantity_ingredient_name_list()
        ingredient_quantity_dict = {}
        for ingredient_name in ingredient_name_list:
            ingredient_quantity_dict[ingredient_name] = self._ingredient_dict[ingredient_name].quantity
        return ingredient_quantity_dict

    def get_non_zero_quantity_ingredient_dict(self):
        non_zero_quantity_ingredient_dict = {
            x: self._ingredient_dict[x] for x in self._ingredient_dict if self._ingredient_dict[x].quantity > 0
        }
        return non_zero_quantity_ingredient_dict
