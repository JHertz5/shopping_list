from datetime import datetime
from shopping_list import item_database
from shopping_list import recipe_database


def generate_timestamp_filename():
    now = datetime.now()
    return_string = "shoppinglist_" + now.strftime('%Y%m%d%H%M%S') + ".txt"
    return return_string


def write_report(filename, recipe_quantity_dict, item_dict, item_grouping_method):
    write_string_list = []

    # Add recipes to file.
    for recipe_name, recipe_quantity in recipe_quantity_dict.items():
        recipe_str = '{} ({})'.format(recipe_name, recipe_quantity)
        line_string =_generate_line(recipe_str, 'recipes')
        write_string_list.append(line_string)

    # Add items to the file.
    for item_name, item_obj in item_dict.items():
        item_str = '{} ({})'.format(item_name, item_obj.get_quantity())
        item_group = item_obj.get_group(item_grouping_method)
        line_string =_generate_line(item_str, item_group)
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


class Checklist:

    def __init__(self, filename=''):
        if filename == '':
            # generate filename
            generate_timestamp_filename()
        else:
            self._filename = filename

    def get_filename(self):
        return self._filename

    def generate_file(self, recipe_quantity_dict, item_dict, item_grouping_method):

        self.file = open(self._filename, 'w')

        # Add recipes to file.
        for recipe_name, recipe_quantity in recipe_quantity_dict.items():
            recipe_str = '{} ({})'.format(recipe_name, recipe_quantity)
            self.write_line(recipe_str, 'recipes')

        # Add items to the file.
        for item_name, item_obj in item_dict.items():
            item_str = '{} ({})'.format(item_name, item_obj.get_quantity())
            item_group = item_obj.get_group(item_grouping_method)
            self.write_line(item_str, item_group)

        self.file.close()

    def write_line(self, text, group, tag_list=[]):
        # Validate inputs.
        assert isinstance(text, str)
        assert isinstance(group, str)
        assert isinstance(tag_list, list)

        tag_list_formatted = [' +' + tag for tag in tag_list]
        line = text + " @" + group + "".join(tag_list_formatted) + '\n'
        self.file.write(line)
