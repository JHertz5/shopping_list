import gspread
from oauth2client.service_account import ServiceAccountCredentials

def openWorksheets():
    #use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('Shopping List-32ab969084cf.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open sheets
    return client.open("Shopping List").worksheets()

def selectGrouping(groupingOptions_minusUnordered):

    inputValid = False
    while not inputValid:
        # print grouping options
        print('\nsort options:')
        groupingOptions = ['Unordered'] + groupingOptions_minusUnordered
        for index,groupingOption in enumerate(groupingOptions):
            print('\t{}({})'.format(groupingOption,index))

        groupingSelection = int(input('Pick sort method: ')) # input selection

        # check validity of selection
        if 0 < groupingSelection < len(groupingOptions):
            inputValid = True
        else:
            print('input must be in range [{}-{}]'.format(0,len(groupingOptions)-1))

    print('{} selected\n'.format(groupingOptions[groupingSelection]))
    return groupingSelection

def getData_ItemGroup(sheets):
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

def getAndProcess_ItemGroup(sheets):
    itemGroupingRecords, groupingSelection = getData_ItemGroup(sheets)
    return processData_ItemGroup(itemGroupingRecords, groupingSelection)

def getAndProcessData_Recipes(sheets):
    recipesRaw = sheets[1].get_all_values()
    recipes = {}
    for recipe in recipesRaw:
        # create dict entry of recipe name : recipe ingredients
        recipes[recipe[0]] = [x for x in recipe if x != '']
    return recipes

def getAndProcessData_Input(sheets):
    inputRaw = sheets[2].get_all_values()
    # process each input set
    inputSets = []
    for listIndex in range(1,4):
        # pull column data into set
        inputSets.append(set(sheets[2].col_values(listIndex)[1:]))
    return inputSets #(mealsToBuy, exclusions, extras)
