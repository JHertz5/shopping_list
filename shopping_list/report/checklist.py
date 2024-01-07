'''
TODO comment
'''

from datetime import datetime


def write_report(filename, recipe_quantity_dict, ingredient_dict):
    line_list = _generate_report(recipe_quantity_dict, ingredient_dict)

    # Write the lines to the file.
    file = open(filename, 'w')
    file.writelines(line_list)
    file.close()


def _generate_report(recipe_quantity_dict, ingredient_dict):
    return_list = []

    # Add recipes to file.
    for recipe_name, recipe_quantity in recipe_quantity_dict.items():
        recipe_str = '{} ({})'.format(recipe_name, recipe_quantity)
        # TODO get group from recipe instance
        line_string = _generate_line(recipe_str, 'recipes')
        return_list.append(line_string)

    # Add ingredients to the file.
    for ingredient_name, ingredient_obj in ingredient_dict.items():
        ingredient_str = '{} ({})'.format(ingredient_name, ingredient_obj.quantity)
        ingredient_group = ingredient_obj.group
        line_string = _generate_line(ingredient_str, str(ingredient_group))
        return_list.append(line_string)

    return return_list


def _generate_line(text, group, tag_list=[]):
    # Validate inputs.
    assert isinstance(text, str)
    assert isinstance(group, str)
    assert isinstance(tag_list, list)

    tag_list_formatted = [' +' + tag for tag in tag_list]
    return_string = text + " @" + group + "".join(tag_list_formatted) + '\n'
    return return_string
