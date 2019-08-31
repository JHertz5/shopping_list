import sheet_interface
import checklist_file_generator
import push_file
import os # for deleting file

def preview_list(shoppingList_grouped):
    # convert group setss to strings with newline seperation
    shoppingList_stringList = ['\n'.join(x) for x in shoppingList_grouped]

    preview = '\n'.join([
    '\nMeals:\n',
    '\n'.join(mealsToBuy),
    '\nItems:\n',
    '\n\n'.join(shoppingList_stringList),
    '\n'
    ])
    print(preview)

sheets = sheet_interface.openSpreadsheet()
print('data connected')

items_sheet = sheets.worksheet('Items')
aisleGroupItems,itemNames = sheet_interface.getAndProcess_ItemGroup(items_sheet)
print('items retrieved')

# extract data from recipe sheet
recipes_sheet = sheets.worksheet('Recipes')
recipes = sheet_interface.getAndProcessData_Recipes(recipes_sheet)
print('recipes retrieved')

generateList = True
while generateList:
    # extract data from input sheet
    input_sheet = sheets.worksheet('Input')
    (mealsToBuy, exclusions, extras) = sheet_interface.getAndProcessData_Input(input_sheet)
    print('input data retrieved')
    print('data retrieved')

    # combine meal recipes into items list (using set to avoid duplication)
    shoppingList = set()
    for meal in mealsToBuy:
        shoppingList = shoppingList.union(recipes[meal])

    # removing excluded items and add extras
    shoppingList = shoppingList.difference(exclusions) # remove excluded items
    shoppingList = shoppingList.union(extras)

    # create shoppingList_grouped, dict[aisle number] = item list
    aisleGroupList = sorted(aisleGroupItems.keys())
    shoppingList_grouped = [
        aisleGroupItems[x].intersection(shoppingList) for x in aisleGroupList
        ]
    # remove empty groups from shoppingList_grouped
    shoppingList_grouped = [x for x in shoppingList_grouped if x != set()]

    # Add any extras without item groups to group 0
    unorderdExtras = extras.difference(itemNames)
    if len(unorderdExtras) > 0:
        shoppingList_grouped.append(unorderdExtras)

    print('shopping list generated')

    preview_list(shoppingList_grouped)

    sendList_question = '[s]end list, [r]efresh list or [q]uit?\n'
    sendList_responses = ['s','r','q']

    # ask user whether to push shopping list to phone
    sendList_input = input(sendList_question)
    while sendList_input not in sendList_responses:
        print('{} is not valid input {}'.format(sendList_input, sendList_responses))
        sendList_input = input(sendList_question)
    # sendList = ( sendList_input == "y" )

    if sendList_input == 's': # send file
        print('send file selected')

        # generate checklist file
        checklist_filename = checklist_file_generator.generate_filename()
        checklist_file_generator.generate_file(mealsToBuy, shoppingList_grouped, checklist_filename)
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
