''' function to suggest recipe and add it to input '''

from . import spreadsheet


def recipe_search(item_list, recipes):
    # get item to search for from user input
    input_recognised = False
    while not input_recognised:
        print('known items: ' + ', '.join(item_list))
        user_input_item = input('input item: ')
        search_item = user_input_item.title()  # items are in Title Case

        if search_item not in item_list:
            print('{} not in items list'.format(search_item))
        else:
            input_recognised = True

    # get recipes containing search_item
    print('searching for {}'.format(search_item))
    return recipes.get_recipes_containing_item(search_item)


def select_recipe(search_results):
    search_complete = False  # default value
    new_recipe = ''    # default value
    input_valid = False
    while not input_valid:

        print('recipes containing item:')
        for index, recipe in enumerate(search_results):
            print('\t{} - {}'.format(index, recipe))

        user_input_raw = input('select recipe to add to list or [q]uit or [n]ew search: ')
        # check user input
        if user_input_raw == 'q':
            print('quit selected')
            search_complete = True
            input_valid = True
        elif user_input_raw == 'n':
            print('new seach selected')
            search_complete = False
            input_valid = True
        else:
            try:
                recipe_selection_int = int(user_input_raw)
                if 0 <= recipe_selection_int < len(search_results):
                    input_valid = True
                else:
                    print('input must be in range [{}-{}]'.format(
                        0, len(search_results) - 1))
            except BaseException:
                print('recipe selection must be int')

            search_complete = True
            new_recipe = search_results[recipe_selection_int]
            print('{} selected'.format(new_recipe))
    return new_recipe, search_complete


def suggest_recipe():
    sheets = spreadsheet.Spreadsheet()
    print('data connected')

    # Extract data from item sheet.
    item_list = sheets.get_item_list()
    print('items retrieved')

    # Extract data from recipes sheet.
    recipes = sheets.get_recipe_sheet_data()
    print('recipes retrieved')

    # Extract data from the input sheet.
    meals_to_buy_list = sheets.get_input_sheet_data()
    print('input retrieved')

    search_complete = False
    while not search_complete:
        search_results = recipe_search(item_list, recipes)
        if search_results == []:
            print('no recipes containing item')
        else:
            (new_recipe, search_complete) = select_recipe(search_results)

    if new_recipe != '':
        sheets.add_new_meal_to_buy(meals_to_buy_list, new_recipe)
        print('{} written to spreadsheet'.format(new_recipe))
