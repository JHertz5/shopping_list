import os

from . import spreadsheet
from . import push_file
from . import report


def generate_shopping_list():
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
        recipes.incr_quantities_for_list_of_irecipes(recipes_to_buy_list)

        # Update the quantities in the ingredients database, based on the recipe quantities.
        recipe_ingredient_list = recipes.get_non_zero_quantity_recipe_ingredient_list()
        ingredients.incr_quantities_for_list_of_ingredients(recipe_ingredient_list)
        # Update the quantities in the ingredients database, based on the exclusions.
        ingredients.reset_quantities_for_list_of_ingredients(exclusions_list)
        # Update the quantities in the ingredients database, based on the inclusions.
        ingredients.incr_quantities_for_list_of_ingredients(inclusions_list)

        report.preview.print_report(
            recipes.get_non_zero_quantity_recipe_quanitity_dict(),
            ingredients.get_non_zero_quantity_ingredient_quanitity_dict()
        )
        print('shopping list generated')

        input_valid = False
        while not input_valid:
            send_list_input = input('[s]end list, [r]efresh list or [q]uit?: ')

            if send_list_input == 's':  # send file
                input_valid = True
                print('\tsend file selected')

                # generate checklist file
                checklist_filename = report.checklist.generate_timestamp_filename()
                report.checklist.write_report(
                    checklist_filename,
                    recipes.get_non_zero_quantity_recipe_quanitity_dict(),
                    ingredients.get_non_zero_quantity_ingredient_dict(),
                    grouping_selection
                )
                print('\t{} generated'.format(checklist_filename))

                # push file
                push_file.push_file(checklist_filename)
                print('\tfile pushed')

                os.remove(checklist_filename)  # delete file

                user_input_finalised = True  # end script

            elif send_list_input == 'r':  # refresh file
                input_valid = True
                print('\trefresh file selected')
                user_input_finalised = False  # restart script

            elif send_list_input == 'q':  # quit
                input_valid = True
                print('\tquit selected')
                user_input_finalised = True  # end script
            else:
                print('{} is not valid input'.format(send_list_input))
