''' function will get all recipes from the input recipes column and present them
    to the user. The user will select a recipe and the script will get the url
    associated with this recipe '''

import re
import webbrowser

from .spreadsheet import wrapper


def get_all_recipe_urls(sheet):
    recipe_headers_raw = sheet.col_values(1, value_render_option='FORMULA')
    recipe_url_dict = {}
    for recipe_formula in recipe_headers_raw:
        if "HYPERLINK" in recipe_formula:
            # parse url and recipe from google sheets HYPERLINK formula format
            match_result = re.match(r'.*\("(.*)","(.*)"\)', recipe_formula)
            recipe_url = match_result.group(1)
            recipe_name = match_result.group(2)
        else:
            # no url in cell, treat as plaintext name
            recipe_name = recipe_formula
            recipe_url = ""
        # create dict entry of recipe name:recipe url
        recipe_url_dict[recipe_name] = recipe_url
    return recipe_url_dict


def select_recipe(input_recipes):
    # get user to select recipe from input recipes
    input_valid = False
    while not input_valid:

        print('recipes on input list:')
        for index, recipe in enumerate(input_recipes):
            print('\t{} - {}'.format(index, recipe))

        recipe_selection_raw = input('pick recipe: ')
        # check validity of selection
        try:
            recipe_selection_int = int(recipe_selection_raw)
            if 0 <= recipe_selection_int < len(input_recipes):
                input_valid = True
            else:
                print('input must be in range [{}-{}]'.format(
                    0, len(input_recipes) - 1))
        except BaseException:
            print('recipe selection must be int')

    return recipe_selection_int


def get_recipe_urls():
    sheets = wrapper._open_spreadsheet()
    print('data connected')

    # get list of input recipes
    input_sheet = sheets.worksheet('Input')
    input_recipes = input_sheet.col_values(1)[1:]
    print('input data retrieved')

    # get user selected recipe
    recipe_selection_int = select_recipe(input_recipes)
    # convert result from int to string to use as key
    recipe_selection = input_recipes[recipe_selection_int]
    print('\t{} selected'.format(recipe_selection))

    # get recipe url data
    recipes_sheet = sheets.worksheet('Recipes')
    recipe_url_dict = get_all_recipe_urls(recipes_sheet)
    print('recipe urls retrieved')

    # get url of selected recipe
    recipe_url = recipe_url_dict[recipe_selection]

    if recipe_url == "":
        print("no url available")
    else:
        print('{} -> {}'.format(recipe_selection, recipe_url))

        input_valid = False
        while not input_valid:
            option_input = input('[o]pen url or [q]uit?: ')
            if option_input == 'o':  # open url
                input_valid = True
                print('\topen url selected')
                webbrowser.open(recipe_url, new=2)
            elif option_input == 'q':  # quit
                input_valid = True
                print('\tquit selected')
            else:
                print('{} is not valid input {}'.format(option_input, option_responses))
                option_input = input(option_question)


if __name__ == "__main__":
    get_recipe_urls()
