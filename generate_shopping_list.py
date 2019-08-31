import sheet_interface
import shopping_list_manager
import checklist_file_generator
import push_file
import os # for deleting file

sheets = sheet_interface.openSpreadsheet()
print('data connected')

items_sheet = sheets.worksheet('Items')
item_groups = sheet_interface.getData_ItemGroup(items_sheet)
print('items retrieved')

# extract data from recipe sheet
recipes_sheet = sheets.worksheet('Recipes')
recipes = sheet_interface.getData_Recipes(recipes_sheet)
print('recipes retrieved')

generateList = True
while generateList:
    # extract data from input sheet
    input_sheet = sheets.worksheet('Input')
    (mealsToBuy, exclusions, inclusions) = sheet_interface.getData_Input(input_sheet)
    print('input data retrieved')
    print('data retrieved')

    # create subset of recipes containing only recipes to go in shopping list
    recipes_to_buy = { x:recipes[x] for x in recipes.keys() if x in mealsToBuy }

    shopping_list = shopping_list_manager.ShoppingList()
    for recipe_name, ingredients in recipes_to_buy.items():
        shopping_list.add_recipe(recipe_name, ingredients)

    # inclusions overrides exclusions
    excluded_items = exclusions.difference(inclusions)
    shopping_list.exclude_items(excluded_items)

    # assigning groups to shopping list items
    shopping_list.set_item_groups(item_groups)

    shopping_list.preview_list()
    print('shopping list generated')

    sendList_question = '[s]end list, [r]efresh list or [q]uit?\n'
    sendList_responses = ['s','r','q']
    # ask user whether to push shopping list
    sendList_input = input(sendList_question)
    while sendList_input not in sendList_responses:
        print('{} is not valid input {}'.format(sendList_input, sendList_responses))
        sendList_input = input(sendList_question)

    if sendList_input == 's': # send file
        print('send file selected')

        # generate grouped list
        shopping_list_grouped = shopping_list.generate_grouped_list()

        # generate checklist file
        checklist_filename = checklist_file_generator.generate_filename()
        checklist_file_generator.generate_file(shopping_list_grouped, checklist_filename)
        print('{} generated'.format(checklist_filename))

        # push file
        push_file.push_file(checklist_filename)
        print('file pushed')

        os.remove(checklist_filename) # delete file

        generateList = False; # end script

    elif sendList_input == 'r': # refresh file
        print('refresh file selected')
        generateList = True; # restart script

    else:
        print('quit selected')
        generateList = False; # end script
print('exiting script')
