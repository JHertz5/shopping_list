from shopping_list import item_database
from shopping_list import recipe_database

def print_report(recipe_quantity_dict, item_quantity_dict):
    print_string = _generate_report(recipe_quantity_dict, item_quantity_dict)
    print(print_string)

def _generate_report(recipe_quantity_dict, item_quantity_dict):
    recipe_strings = ['{} ({})'.format(x, recipe_quantity_dict[x]) for x in recipe_quantity_dict.keys()]
    item_strings = ['{} ({})'.format(x, item_quantity_dict[x]) for x in item_quantity_dict.keys()]

    return_string = '\nRecipes:\n\t' \
        + '\n\t'.join(recipe_strings) \
        + '\nItems:\n\t' \
        + '\n\t'.join(item_strings) \
        + '\n'
    return return_string
