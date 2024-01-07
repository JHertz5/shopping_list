
from . import spreadsheet
from . import report


def generate_shopping_list(checklist_filename):
    sheets = spreadsheet.wrapper.Wrapper()
    print('data connected')

    sheets.download_ingredients_data()
    grouping_options = sheets.get_ingredient_grouping_options()

    # Get user's grouping selection.
    input_valid = False
    while not input_valid:
        # print grouping options
        print('\nsort options:')
        grouping_options = ['Unordered'] + grouping_options
        for index, grouping_option in enumerate(grouping_options):
            print('\t{}({})'.format(grouping_option, index))

        grouping_selection_raw = input('pick sort method: ')
        # check validity of selection
        try:
            grouping_selection_int = int(grouping_selection_raw)
            if 0 <= grouping_selection_int < len(grouping_options):
                input_valid = True
            else:
                print('input must be in range [{}-{}]'.format(
                    0, len(grouping_options) - 1)
                )
        except BaseException:
            print('grouping selection must be int')

    # Convert result from int to string to use as key.
    grouping_selection = grouping_options[grouping_selection_int]
    print('\t{} selected\n'.format(grouping_selection))

    # Extract data from ingredients sheet and construct ingredients database
    ingredients = sheets.get_ingredient_sheet_data(grouping_selection)
    print('ingredients retrieved')

    # Extract data from recipes sheet.
    sheets.download_recipe_data()
    recipes = sheets.get_recipe_sheet_data()
    print('recipes retrieved')

    # TODO change this to a function rather than a loop, with top-level control?
    user_input_finalised = False
    while not user_input_finalised:

        # Extract data from the input sheet.
        sheets.download_input_data()
        recipes_to_buy_list, exclusions_list, inclusions_list = sheets.get_input_sheet_data()
        print('input retrieved')

        # Update the quantities in the recipe database, based on the recipes to be bought.
        for recipe_name in recipes_to_buy_list:
            recipes.incr_quantity(recipe_name)

        # Update the quantities in the ingredients database, based on the recipe quantities.
        recipe_ingredient_list = recipes.get_ingredient_list_of_selected()
        for ingredient_name in recipe_ingredient_list:
            ingredients.incr_quantity(ingredient_name)
        # Update the quantities in the ingredients database, based on the exclusions.
        for ingredient_name in exclusions_list:
            ingredients.reset_quantity(ingredient_name)
        # Update the quantities in the ingredients database, based on the inclusions.
        for ingredient_name in inclusions_list:
            ingredients.incr_quantity(ingredient_name)

        report.preview.print_report(
            recipes.get_quantity_dict_of_selected(),
            ingredients.get_quantity_dict_of_selected()
        )
        print('shopping list generated')

        input_valid = False
        while not input_valid:
            write_list_input = input('[w]rite list, [r]efresh list or [q]uit?: ')

            # Write file.
            if write_list_input == 'w':
                input_valid = True
                print('\twrite file selected')

                # Generate checklist file.
                report.checklist.write_report(
                    checklist_filename,
                    recipes.get_quantity_dict_of_selected(),
                    ingredients.get_dict_of_selected()
                )
                print('\tshopping list written to ' + checklist_filename)

                # End script.
                user_input_finalised = True

            # Refresh file.
            elif write_list_input == 'r':
                input_valid = True
                print('\trefresh file selected')
                # Restart script.
                user_input_finalised = False

            # Quit.
            elif write_list_input == 'q':
                input_valid = True
                print('\tquit selected')
                # End script.
                user_input_finalised = True
            else:
                print('{} is not valid input'.format(write_list_input))
