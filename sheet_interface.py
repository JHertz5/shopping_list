import gspread
from oauth2client.service_account import ServiceAccountCredentials

def openSpreadsheet():
    #use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    #TODO put filename in config file
    creds = ServiceAccountCredentials.from_json_keyfile_name('Shopping List-32ab969084cf.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open sheets
    return client.open("Shopping List")

def selectGrouping(groupingOptions_minusUnordered):

    inputValid = False
    while not inputValid:
        # print grouping options
        print('\nsort options:')
        groupingOptions = ['Unordered'] + groupingOptions_minusUnordered
        for index,groupingOption in enumerate(groupingOptions):
            print('\t{}({})'.format(groupingOption,index))

        groupingSelection = input('Pick sort method: ') # input selection
#int
        # check validity of selection
        try:
            groupingSelection_int = int(groupingSelection)
            if 0 < groupingSelection_int < len(groupingOptions):
                inputValid = True
            else:
                print('input must be in range [{}-{}]'.format(0,len(groupingOptions)-1))
        except:
            print('Grouping selection must be int')


    print('{} selected\n'.format(groupingOptions[groupingSelection_int]))
    return groupingSelection_int

def getData_ItemGroup(sheet):
    # extract data from item group sheet
    itemGroupingRecords = sheet.get_all_records() # get data from sheet

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

def getAndProcess_ItemGroup(sheet):
    itemGroupingRecords, groupingSelection = getData_ItemGroup(sheet)
    return processData_ItemGroup(itemGroupingRecords, groupingSelection)

def getAndProcessData_Recipes(sheet):
    recipesRaw = sheet.get_all_values()
    recipes = {}
    for recipe in recipesRaw:
        # create dict entry of recipe name : recipe ingredients
        recipes[recipe[0]] = [x for x in recipe[1:] if x != '']
    return recipes

def getAndProcessData_Input(sheet):
    inputRaw = sheet.get_all_values()
    # process each input set
    inputSets = []
    for listIndex in range(1,4):
        # pull column data into set
        columnData = set(sheet.col_values(listIndex)[1:])
        columnData.discard('') # remove any empty strings
        inputSets.append(columnData)

    return inputSets #(mealsToBuy, exclusions, extras)
