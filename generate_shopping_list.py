''' function to generate shopping list '''

import sheet_interface
import shopping_list_manager
import checklist_manager
import push_file
import os # for deleting file

def get_data_item_group(sheet):
    # extract data from item group sheet
    item_grouping_records = sheet.get_all_records() # get data from sheet

    table_headers    = list(item_grouping_records[0].keys())
    items_header     = table_headers[0]
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
    print('\t{} selected\n'.format(grouping_selection))

    item_groups = {}
    for record in item_grouping_records:
        if grouping_selection == 'Unordered':
            item_groups[record[items_header]] = 0
        else:
            item_groups[record[items_header]] = record[grouping_selection]

    return item_groups

def get_data_input(sheet):
    input_data_dict = {}
    for column_index in range(1,4):
        # pull column data into list
        column         = sheet.col_values(column_index)
        column_heading = column[0]
        column_data    = set(column[1:])
        column_data.discard('') # remove any empty strings
        input_data_dict[column_heading] = column_data

    return input_data_dict

def generate_shopping_list():
    sheets = sheet_interface.open_spreadsheet()
    print('data connected')

    items_sheet = sheets.worksheet('Items')
    item_groups = get_data_item_group(items_sheet)
    print('items retrieved')

    # extract data from recipe sheet
    recipes_sheet = sheets.worksheet('Recipes')
    recipes       = sheet_interface.get_data_recipes(recipes_sheet)
    print('recipes retrieved')

    generate_list = True
    while generate_list:
        # extract data from input sheet
        input_sheet     = sheets.worksheet('Input')
        input_data_dict = get_data_input(input_sheet)
        exclusions      = input_data_dict['Exclusions']
        inclusions      = input_data_dict['Inclusions']
        meals_to_buy    = input_data_dict['Meals To Buy']
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

        input_valid = False
        while not input_valid:
            send_list_input = input('[s]end list, [r]efresh list or [q]uit?: ')

            if send_list_input == 's': # send file
                input_valid = True
                print('\tsend file selected')

                # generate grouped list
                shopping_list_grouped = shopping_list.generate_grouped_list()

                # generate checklist file
                checklist = checklist_manager.checklist_manager()
                checklist.generate_file(shopping_list_grouped)
                checklist_filename = checklist.filename
                print('\t{} generated'.format(checklist_filename))

                # push file
                push_file.push_file(checklist_filename)
                print('\tfile pushed')

                os.remove(checklist_filename) # delete file

                generate_list = False; # end script

            elif send_list_input == 'r': # refresh file
                input_valid = True
                print('\trefresh file selected')
                generate_list = True; # restart script

            elif send_list_input == 'q': # quit
                input_valid = True
                print('\tquit selected')
                generate_list = False; # end script
            else:
                print('{} is not valid input'.format(send_list_input))

if __name__ == "__main__":
    generate_shopping_list()
