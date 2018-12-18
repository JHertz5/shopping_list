'''
ShoppingList v2.0
This script :
    extracts data from google sheets file
    manipulates data to generate shopping list
    emails shopping list to me
'''

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import send_email

#use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('Shopping List-32ab969084cf.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open sheets
sheets = client.open("Shopping List").worksheets()

print('data connected')

# extract and display sort options
print('Sort Options')
categoryOptions = ['Unordered'] + sheets[0].row_values(1)[1:] # skip Item column
for index,categoryOption in enumerate(categoryOptions):
    print('\t{}({})'.format(categoryOption,index))
# input selection
categorySelection = int(input('Pick sort method: '))
# check validity of selection
if categorySelection < 0:
    raise ValueError('categorySelection must be >= 0')
elif categorySelection > len(categoryOptions):
    raise ValueError('categorySelection must be <= len(categoryOptions)')

print('{} selected'.format(categoryOptions[categorySelection]))

# extract data from 1st sheet - items to sort aisle dictionary
items = sheets[0].col_values(1)[1:] # get items, skip header row
if categorySelection == 0: # if unordered
    aisleGroups = [1]*len(items) # equal aisleGroup category for every item
else:
    # get aisleGroup values, skip header row
    aisleGroups = list(map(int,sheets[0].col_values(categorySelection+1)[1:]))

aisleGroupItems = {x:set() for x in set(aisleGroups)}
for (aisleGroup,item) in zip(aisleGroups,items):
    aisleGroupItems[aisleGroup].add(item)

# extract data from 2nd sheet - recipe to items dictionary
recipes = {}
rowIndex = 2; # skip header row
while True:
    row = sheets[1].row_values(rowIndex)
    if row == []: # end of table reached
        break
    else:
        recipes[row[0]] = row[1:] # use header column as key for list
        rowIndex += 1

# extract data from 3rd sheet - input data lists
# store data in sets to remove duplicates
mealsToBuy = set(sheets[2].col_values(1)[1:]) # get meals      , skip header row
exclusions = set(sheets[2].col_values(2)[1:]) # get exclusions , skip header row
extras     = set(sheets[2].col_values(3)[1:]) # get extras     , skip header row

print('data retrieved')

# discard empty values from input data
mealsToBuy.discard('')
exclusions.discard('')
extras.discard('')

# combine meal recipes into items list (using set to avoid duplication)
shoppingList = set()
for meal in mealsToBuy:
    shoppingList = shoppingList.union(recipes[meal])

# removing excluded items and add extras
shoppingList = shoppingList.difference(exclusions) # remove excluded items
shoppingList = shoppingList.union(extras)

# dict with aisle number as key and item list as value
aisleGroupList = sorted(aisleGroupItems.keys())
shoppingList_seperatedByAisle = [aisleGroupItems[x].intersection(shoppingList) for x in
                                 aisleGroupList]
shoppingList_seperatedByAisle = [x for x in shoppingList_seperatedByAisle if x != set()]

# Add any unsupported extras
unorderdExtras = extras.difference(items)
shoppingList_seperatedByAisle[0] = shoppingList_seperatedByAisle[0].union(unorderdExtras)

# convert groups to string with newline seperation
shoppingList_stringList = ['\n'.join(x) for x in shoppingList_seperatedByAisle]
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
