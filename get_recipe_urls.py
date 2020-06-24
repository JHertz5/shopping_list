''' function will get all recipes from the input recipes column and present them
    to the user. The user will select a recipe and the script will get the url
    associated with this recipe '''

import webbrowser
import sheet_interface

def get_recipe_urls():
    sheets = sheet_interface.open_spreadsheet()
    print('data connected')

    # get list of input recipes
    input_sheet = sheets.worksheet('Input')
    input_recipes = sheet_interface.get_data_input(input_sheet)[0]
    print('input data retrieved')

    # get user to select recipe from input recipes
    input_valid = False
    while not input_valid:

        print('recipes on input list:')
        for index,recipe in enumerate(input_recipes):
            print('\t{} - {}'.format(index,recipe))

        recipe_selection_raw = input('pick recipe: ')
        # check validity of selection
        try:
            recipe_selection_int = int(recipe_selection_raw)
            if 0 <= recipe_selection_int < len(input_recipes):
                input_valid = True
            else:
                print('input must be in range [{}-{}]'.format(
                        0, len(input_recipes)-1)
                    )
        except:
            print('recipe selection must be int')

    # convert result from int to string to use as key
    recipe_selection = input_recipes[recipe_selection_int]
    print('\t{} selected'.format(recipe_selection))

    # get recipe url data
    recipes_sheet = sheets.worksheet('Recipes')
    recipe_url_dict = sheet_interface.get_data_recipe_headers(recipes_sheet)
    print('recipe urls retrieved')

    # get url of selected recipe
    recipe_url = recipe_url_dict[recipe_selection]

    if recipe_url == "":
        print("no url available")
    else:
        print('{} -> {}'.format(recipe_selection,recipe_url))

        option_question = '[o]pen url or [q]uit?\n'
        option_responses = ['o','q']
        # ask user whether to open url or quit
        option_input = input(option_question)
        while option_input not in option_responses:
            print('{} is not valid input {}'.format(option_input,option_responses))
            option_input = input(option_question)

        if option_input == 'o': # open url
            print('open url selected')
            webbrowser.open(recipe_url,new=2)
        else:
            print('quit selected')

if __name__ == "__main__":
    get_recipe_urls()
