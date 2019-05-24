import database_interface
import checklist_file_generator
import push_file

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

sheets = database_interface.openWorksheets()
print('data connected')

aisleGroupItems,itemNames = database_interface.getAndProcess_ItemGroup(sheets)
print('items retrieved')
# extract data from recipe sheet
recipes = database_interface.getAndProcessData_Recipes(sheets)
print('recipes retrieved')
# extract data from input sheet
(mealsToBuy, exclusions, extras) = database_interface.getAndProcessData_Input(sheets)
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

# ask user whether to push shopping list to phone
sendList_question = 'send list? (y/n)\n'
sendList_input = input(sendList_question)
while sendList_input not in ['y','n']:
    print('{} is not valid input, input y or n'.format(sendList_input))
    sendList_input = input(sendList_question)
sendList = sendList_input == "y"

if sendList:
    checklist_filename = checklist_file_generator.generate(mealsToBuy,shoppingList_grouped)
    print('file generated')
    authKey = push_file.get_pb_authKey()
    push_file.push_file(checklist_filename, authKey)
    print('file pushed')

print('exiting script')
