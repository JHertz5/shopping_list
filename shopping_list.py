'''
ShoppingList v3.0
This script :
    extracts data from google sheets file
    manipulates data to generate shopping list
    emails shopping list to me
'''

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import send_email

index_skipHeader = 1

def openWorksheets():
    #use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('Shopping List-32ab969084cf.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open sheets
    return client.open("Shopping List").worksheets()

def selectGrouping(groupingOptions_minusUnordered):
    print('\nsort options:')
    groupingOptions = ['Unordered'] + groupingOptions_minusUnordered
    for index,groupingOption in enumerate(groupingOptions):
        print('\t{}({})'.format(groupingOption,index))
    # input selection
    groupingSelection = int(input('Pick sort method: '))
    # check validity of selection
    if groupingSelection < 0:
        raise ValueError('groupingSelection must be >= 0')
    elif groupingSelection > len(groupingOptions):
        raise ValueError('groupingSelection must be <= len(groupingOptions)')

    print('{} selected\n'.format(groupingOptions[groupingSelection]))
    return groupingSelection

def getData_ItemGroup():
    # extract data from item group sheet
    itemGroupingRecords = sheets[0].get_all_records() # get data from sheet

    groupingOptions = list(itemGroupingRecords[0].keys())[1:] # get names of grouping options
    groupingSelection = selectGrouping(groupingOptions)
    return itemGroupingRecords, groupingSelection

def processData_ItemGroup(itemGroupingRecords, groupingSelection):
    recordKeys = list(itemGroupingRecords[0].keys())
    itemNamesKey = recordKeys[0]
    groupingSelectionKey = recordKeys[groupingSelection]

    # extract data into lists
    itemNames = [x[itemNamesKey] for x in itemGroupingRecords]
    if groupingSelection == 0: # if unordered
        aisleGroups = [1]*len(itemNames) # equal aisleGroup for every item
    else:
        # convert group values into list of ints
        aisleGroups = [x[groupingSelectionKey] for x in itemGroupingRecords]

    # arrange data into list of sets
    aisleGroupItems = {x:set() for x in set(aisleGroups)}
    for (aisleGroup,itemName) in zip(aisleGroups,itemNames):
        aisleGroupItems[aisleGroup].add(itemName)
    return aisleGroupItems, itemNames

def getAndProcess_ItemGroup():
    itemGroupingRecords, groupingSelection = getData_ItemGroup()
    return processData_ItemGroup(itemGroupingRecords, groupingSelection)

def getAndProcessData_Recipes():
    recipesRaw = sheets[1].get_all_values()
    recipes = {}
    for recipe in recipesRaw:
        # create dict entry of recipe name : recipe ingredients
        recipes[recipe[0]] = [x for x in recipe if x != '']
    return recipes

def getAndProcessData_Input():
    inputRaw = sheets[2].get_all_values()
    # process each input set
    inputSets = []
    for listIndex in range(1,4):
        # pull column data into set
        inputSets.append(set(sheets[2].col_values(listIndex)[index_skipHeader:]))
    return inputSets #(mealsToBuy, exclusions, extras)

def convertRecordsToDict(records): #TODO remove? unused?
    """ converts records (list of dicts) to single dict """
    headings = list(records[0].keys())
    dict = {}
    for heading in headings:
        dict[heading] = [x[heading] for x in records]
    return dict

sheets = openWorksheets()
print('data connected')

aisleGroupItems,itemNames = getAndProcess_ItemGroup()

# extract data from recipe sheet
recipes = getAndProcessData_Recipes()

# extract data from input sheet
(mealsToBuy, exclusions, extras) = getAndProcessData_Input()

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
shoppingList_grouped[0] = shoppingList_grouped[0].union(unorderdExtras)

# convert groups to string with newline seperation
shoppingList_stringList = ['\n'.join(x) for x in shoppingList_grouped]
print('shopping list generated')

date = time.strftime("%d/%m/%Y-%H:%M:%S") # get date for subject line
subject = 'Shopping List ' + date # create subject for email

message = '\n'.join([
                '\nMeals:\n',
                '\n'.join(mealsToBuy),
                '\nItems:\n',
                '\n\n'.join(shoppingList_stringList)
                ])

send_email.sendEmail(subject,message)

print('email sent')
print(message)
