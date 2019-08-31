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

def selectGrouping(groupingOptions_data):

    inputValid = False
    while not inputValid:
        # print grouping options
        print('\nsort options:')
        groupingOptions = ['Unordered'] + groupingOptions_data
        for index,groupingOption in enumerate(groupingOptions):
            print('\t{}({})'.format(groupingOption,index))

        groupingSelection_raw = input('Pick sort method: ') # input selection
#int
        # check validity of selection
        try:
            groupingSelection_int = int(groupingSelection_raw)
            if 0 < groupingSelection_int < len(groupingOptions):
                inputValid = True
            else:
                print('input must be in range [{}-{}]'.format(0,len(groupingOptions)-1))
        except:
            print('Grouping selection must be int')

    grouping_selection = groupingOptions[groupingSelection_int]
    print('{} selected\n'.format(grouping_selection))
    return grouping_selection

def getData_ItemGroup(sheet):
    # extract data from item group sheet
    itemGroupingRecords = sheet.get_all_records() # get data from sheet

    table_headers = list(itemGroupingRecords[0].keys())
    items_header = table_headers[0]
    groupingOptions = table_headers[1:] # get names of grouping options
    groupingSelection = selectGrouping(groupingOptions)

    item_groups = {}
    for record in itemGroupingRecords:
        if groupingSelection == 'Unordered':
            item_groups[record[items_header]] = 0
        else:
            item_groups[record[items_header]] = record[groupingSelection]

    return item_groups

def getData_Recipes(sheet):
    recipesRaw = sheet.get_all_values()
    recipes = {}
    for recipe in recipesRaw:
        # create dict entry of recipe name : recipe ingredients
        recipes[recipe[0]] = [x for x in recipe[1:] if x != '']
    return recipes

def getData_Input(sheet):
    inputRaw = sheet.get_all_values()
    # process each input set
    inputSets = []
    for listIndex in range(1,4):
        # pull column data into set
        columnData = set(sheet.col_values(listIndex)[1:])
        columnData.discard('') # remove any empty strings
        inputSets.append(columnData)

    return inputSets #(mealsToBuy, exclusions, extras)
