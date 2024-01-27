
import sys

from . import spreadsheet
from . import report
from . import utils


def generate_shopping_list(output_filename : str, token_filename : str, sheet_name : str):
    sheets = spreadsheet.wrapper.Wrapper(token_filename,  sheet_name)
    print('data connected')

    sheets.download_ingredients_data()
    grouping_options = sheets.get_ingredient_grouping_options()

    # Get user's grouping selection.
    grouping_selection = get_user_grouping_selection(grouping_options)
    print('\t{} selected\n'.format(grouping_selection))

    # Extract data from ingredients sheet and construct ingredients database
    ingredients = sheets.get_ingredient_sheet_data(grouping_selection)
    print('ingredients retrieved')

    # Extract data from recipes sheet.
    sheets.download_recipe_data()
    recipes = sheets.get_recipe_sheet_data()
    print('recipes retrieved')

    user_input_finalised = False
    while not user_input_finalised:

        # Extract data from the input sheet.
        sheets.download_input_data()
        recipes_to_buy_list, exclusions_list, inclusions_list = sheets.get_input_sheet_data()
        print('input retrieved')
        recipes, ingredients = generate_shopping_list_data(
            recipes_to_buy_list, exclusions_list, inclusions_list, recipes, ingredients
        )

        write_list_input = get_user_action_selection()
        user_input_finalised = write_list_input in ['w', 'q']

        match write_list_input:
            # Write file.
            case'w':
                print('\twrite list selected')
                # Generate checklist file.
                report.checklist.write_report(
                    output_filename,
                    recipes.get_quantity_dict_of_selected(),
                    ingredients.get_dict_of_selected()
                )
                print('shopping list written to ' + output_filename)

            # Refresh file.
            case 'r':
                print('\trefresh list selected')
                # Reset the quantities of each shopping list item.
                recipes.reset_quantites()
                ingredients.reset_quantites()

            # Quit.
            case 'q':
                print('\tquit selected')

    print('exiting')
    return


def get_user_grouping_selection(grouping_options):

    grouping_options = ['Unordered'] + grouping_options
    max_grouping_selection = len(grouping_options) - 1

    user_input_is_valid = False
    while not user_input_is_valid:

        # Print grouping options.
        print('\nsort options:')
        for index, grouping_option in enumerate(grouping_options):
            print('\t{} - {}'.format(index, grouping_option))

        grouping_selection_str = input('pick sort method: ')
        # Check validity of selection.
        user_input_is_valid = utils.string_is_valid_int(grouping_selection_str, max=max_grouping_selection)

    # Convert result from int to string to use as key.
    grouping_selection = grouping_options[int(grouping_selection_str)]

    return grouping_selection


def generate_shopping_list_data(recipes_to_buy_list, exclusions_list, inclusions_list, recipes, ingredients):

    # Update the quantities in the recipe database, based on the recipes to be bought.
    recipes = update_recipe_quantities(recipes, recipes_to_buy_list)
    recipe_ingredient_list = recipes.get_ingredient_list_of_selected()

    # Update the quantities in the recipe database, based on the recipes to be bought.
    ingredients = update_ingredient_quantities(
        ingredients, recipe_ingredient_list, exclusions_list, inclusions_list
    )

    report.preview.print_report(
        recipes.get_quantity_dict_of_selected(),
        ingredients.get_quantity_dict_of_selected()
    )
    print('shopping list generated')
    return recipes, ingredients


def update_recipe_quantities(recipes, recipes_to_buy_list):
    # Update the quantities in the recipe database, based on the recipes to be bought.
    for recipe_name in recipes_to_buy_list:
        recipes.incr_quantity(recipe_name)
    return recipes


def update_ingredient_quantities(ingredients, recipe_ingredient_list, exclusions_list, inclusions_list):
    # Update the quantities in the ingredients database, based on the recipe quantities.
    for ingredient_name in recipe_ingredient_list:
        ingredients.incr_quantity(ingredient_name)
    # Update the quantities in the ingredients database, based on the exclusions.
    for ingredient_name in exclusions_list:
        ingredients.reset_quantity(ingredient_name)
    # Update the quantities in the ingredients database, based on the inclusions.
    for ingredient_name in inclusions_list:
        ingredients.incr_quantity(ingredient_name)
    return ingredients


def get_user_action_selection():

    user_input_is_valid = False
    while not user_input_is_valid:
        write_list_input = input('[w]rite list, [r]efresh list or [q]uit?: ')
        user_input_is_valid = write_list_input in ['w', 'r', 'q']
        if not user_input_is_valid:
            print('Error: invalid input ' + write_list_input)

    return write_list_input
