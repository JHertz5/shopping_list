'''
TODO comment
'''

from datetime import datetime


def generate_timestamp_filename():
    now = datetime.now()
    return_string = "shoppinglist_" + now.strftime('%Y%m%d%H%M%S') + ".txt"
    return return_string


def write_report(filename, recipe_quantity_dict, ingredient_dict, ingredient_grouping_method):
    write_string_list = []

    # Add recipes to file.
    for recipe_name, recipe_quantity in recipe_quantity_dict.items():
        recipe_str = '{} ({})'.format(recipe_name, recipe_quantity)
        line_string = _generate_line(recipe_str, 'recipes')
        write_string_list.append(line_string)

    # Add ingredients to the file.
    for ingredient_name, ingredient_obj in ingredient_dict.items():
        ingredient_str = '{} ({})'.format(ingredient_name, ingredient_obj.quantity)
        ingredient_group = ingredient_obj.group
        line_string = _generate_line(ingredient_str, str(ingredient_group))
        write_string_list.append(line_string)

    # Write the lines to the file.
    file = open(filename, 'w')
    file.writelines(write_string_list)
    file.close()


def _generate_line(text, group, tag_list=[]):
    # Validate inputs.
    assert isinstance(text, str)
    assert isinstance(group, str)
    assert isinstance(tag_list, list)

    tag_list_formatted = [' +' + tag for tag in tag_list]
    return_string = text + " @" + group + "".join(tag_list_formatted) + '\n'
    return return_string
