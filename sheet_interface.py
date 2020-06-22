import gspread
from oauth2client.service_account import ServiceAccountCredentials

def open_spreadsheet():
    #use creds to create a client to interact with the Google Drive API
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
        ]
    #TODO put filename in config file
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'Shopping List-32ab969084cf.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open sheets
    return client.open("Shopping List")

def get_data_item_group(sheet):
    # extract data from item group sheet
    item_grouping_records = sheet.get_all_records() # get data from sheet

    table_headers = list(item_grouping_records[0].keys())
    items_header = table_headers[0]
    grouping_options = table_headers[1:] # get names of grouping options

    # get user to select grouping
    input_valid = False
    while not input_valid:
        # print grouping options
        print('\nsort options:')
        grouping_options = ['Unordered'] + grouping_options
        for index,grouping_option in enumerate(grouping_options):
            print('\t{}({})'.format(grouping_option,index))

        grouping_selection_raw = input('pick sort method: ')
        # check validity of selection
        try:
            grouping_selection_int = int(grouping_selection_raw)
            if 0 <= grouping_selection_int < len(grouping_options):
                input_valid = True
            else:
                print('input must be in range [{}-{}]'.format(
                        0, len(grouping_options)-1)
                    )
        except:
            print('grouping selection must be int')

    # convert result from int to string to use as key
    grouping_selection = grouping_options[grouping_selection_int]
    print('{} selected\n'.format(grouping_selection))

    item_groups = {}
    for record in item_grouping_records:
        if grouping_selection == 'Unordered':
            item_groups[record[items_header]] = 0
        else:
            item_groups[record[items_header]] = record[grouping_selection]

    return item_groups

def get_data_recipes(sheet):
    recipes_raw = sheet.get_all_values()
    recipes = {}
    for recipe in recipes_raw:
        # create dict entry of recipe name : recipe ingredients
        recipes[recipe[0]] = [x for x in recipe[1:] if x != '']
    return recipes

def get_data_input(sheet):
    # process each input set
    inputSets = []
    for listIndex in range(1,4):
        # pull column data into list
        columnData = sheet.col_values(listIndex)[1:]
        # columnData.remove('') # remove any empty strings
        inputSets.append(columnData)

    return inputSets #(mealsToBuy, exclusions, extras)
