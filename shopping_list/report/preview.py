'''
TODO comment
'''


def print_report(recipe_quantity_dict, ingredient_quantity_dict):
    print_string = _generate_report(recipe_quantity_dict, ingredient_quantity_dict)
    print(print_string)


def _generate_report(recipe_quantity_dict, ingredient_quantity_dict):
    recipe_strings = ['{} ({})'.format(x, recipe_quantity_dict[x]) for x in recipe_quantity_dict.keys()]
    ingredient_strings = ['{} ({})'.format(x, ingredient_quantity_dict[x]) for x in ingredient_quantity_dict.keys()]

    return_string = '\nRecipes:\n\t' \
        + '\n\t'.join(recipe_strings) \
        + '\ningredients:\n\t' \
        + '\n\t'.join(ingredient_strings) \
        + '\n'
    return return_string
