''' function to suggest recipe and add it to input '''

import sheet_interface

def recipe_search(item_list, recipes):
    # get item to search for from user input
    input_recognised = False
    while not input_recognised:
        print('known items: ' + ', '.join(item_list))
        user_input_item = input('input item: ')
        search_item     = user_input_item.title() # items are in Title Case

        if search_item not in item_list:
            print('{} not in items list'.format(search_item))
        else:
            input_recognised = True

    # get recipes containing search_item
    print('searching for {}'.format(search_item))
    return [ x for x in recipes.keys() if search_item in recipes[x] ]

def select_recipe(search_results):
    search_complete = False # default value
    new_recipe      = ''    # default value
    input_valid     = False
    while not input_valid:

        print('recipes containing item:')
        for index,recipe in enumerate(search_results):
            print('\t{} - {}'.format(index,recipe))

        user_input_raw = input('select recipe to add to list or [q]uit or [n]ew search: ')
        # check user input
        if user_input_raw == 'q':
            print('quit selected')
            search_complete = True
            input_valid     = True
        elif user_input_raw == 'n':
            print('new seach selected')
            search_complete = False
            input_valid     = True
        else:
            try:
                recipe_selection_int = int(user_input_raw)
                if 0 <= recipe_selection_int < len(search_results):
                    input_valid = True
                else:
                    print('input must be in range [{}-{}]'.format(
                            0, len(search_results)-1) )
            except:
                print('recipe selection must be int')

            search_complete = True
            new_recipe      = search_results[recipe_selection_int]
            print('{} selected'.format(new_recipe))
    return new_recipe, search_complete

def suggest_recipe():
    sheets = sheet_interface.open_spreadsheet()
    print('data connected')

    # extract data from recipe sheet
    items_sheet = sheets.worksheet('Items')
    item_list = sheet_interface.get_data_items_list(items_sheet)
    print('items retrieved')

    # extract data from recipe sheet
    recipes_sheet = sheets.worksheet('Recipes')
    recipes = sheet_interface.get_data_recipes(recipes_sheet)
    print('recipes retrieved')

    input_sheet = sheets.worksheet('Input')
    input_recipes_col = input_sheet.col_values(1)
    print('input retrieved')

    search_complete = False
    while not search_complete:
        search_results = recipe_search(item_list, recipes)
        if search_results == []:
            print('no recipes containing item')
        else:
            (new_recipe, search_complete) = select_recipe(search_results)

    if new_recipe != '':
        # append new recipe onto input recipes column
        new_recipe_row = len(input_recipes_col) + 1
        new_recipe_col = 1
        input_sheet.update_cell(new_recipe_row, new_recipe_col, new_recipe)
        print('{} written to spreadsheet'.format(new_recipe))

if __name__ == '__main__':
    suggest_recipe()
