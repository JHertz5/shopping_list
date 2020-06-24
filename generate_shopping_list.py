''' function to generate shopping list '''

import sheet_interface
import shopping_list_manager
import checklist_manager
import push_file
import os # for deleting file

def generate_shopping_list():
    sheets = sheet_interface.open_spreadsheet()
    print('data connected')

    items_sheet = sheets.worksheet('Items')
    item_groups = sheet_interface.get_data_item_group(items_sheet)
    print('items retrieved')

    # extract data from recipe sheet
    recipes_sheet = sheets.worksheet('Recipes')
    recipes = sheet_interface.get_data_recipes(recipes_sheet)
    print('recipes retrieved')

    generate_list = True
    while generate_list:
        # extract data from input sheet
        input_sheet = sheets.worksheet('Input')
        (meals_to_buy, exclusions_list, inclusions_list) = sheet_interface.get_data_input(input_sheet)
        exclusions = set(exclusions_list)
        inclusions = set(inclusions_list)
        print('input data retrieved')
        print('data retrieved')

        # create list of recipes containing only recipes to go in shopping list
        recipes_to_buy = [ recipes[x] for x in meals_to_buy ]

        # instantiate shopping list and add recipes
        shopping_list = shopping_list_manager.ShoppingList()
        for recipe, ingredients in zip(meals_to_buy,recipes_to_buy):
            shopping_list.add_recipe(recipe, ingredients)

        # inclusions overrides exclusions
        excluded_items = exclusions.difference(inclusions)
        shopping_list.exclude_items(excluded_items)
        shopping_list.include_items(inclusions)

        # assigning groups to shopping list items
        shopping_list.set_item_groups(item_groups)

        shopping_list.preview_list()
        print('shopping list generated')

        send_list_question = '[s]end list, [r]efresh list or [q]uit?\n'
        send_list_responses = ['s','r','q']
        # ask user whether to push shopping list
        send_list_input = input(send_list_question)
        while send_list_input not in send_list_responses:
            print('{} is not valid input {}'.format(
                send_list_input, send_list_responses))
            send_list_input = input(send_list_question)

        if send_list_input == 's': # send file
            print('send file selected')

            # generate grouped list
            shopping_list_grouped = shopping_list.generate_grouped_list()

            # generate checklist file
            checklist = checklist_manager.checklist_manager()
            checklist.generate_file(shopping_list_grouped)
            checklist_filename = checklist.filename
            print('{} generated'.format(checklist_filename))

            # push file
            push_file.push_file(checklist_filename)
            print('file pushed')

            os.remove(checklist_filename) # delete file

            generate_list = False; # end script

        elif send_list_input == 'r': # refresh file
            print('refresh file selected')
            generate_list = True; # restart script

        else:
            print('quit selected')
            generate_list = False; # end script

if __name__ == "__main__":
    generate_shopping_list()
