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
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open sheets
sheets = client.open("Shopping List").worksheets()

print('data connected')

# extract and display order options
print('Categorisation Options')
categoryOptions = ['Unordered'] + sheets[0].row_values(1)[1:] # skip Item column
for index,categoryOption in enumerate(categoryOptions):
    print('\t{}({})'.format(categoryOption,index))
# input selection
categorySelection = int(input('Pick order: '))
# check validity of selection
if categorySelection < 0:
    raise ValueError('categorySelection must be >= 0')
elif categorySelection > len(categoryOptions):
    raise ValueError('categorySelection must be <= len(categoryOptions)')

print('{} selected'.format(categoryOptions[categorySelection]))

# extract data from 1st sheet - items to sort order dictionary
items = sheets[0].col_values(1)[1:] # get items, skip header row
if categorySelection == 0: # if unordered
    order = [1]*len(items) # equal order category for every item
else:
    order = sheets[0].col_values(categorySelection+1)[1:] # get order values, skip header row
# order items in dict
itemOrder = {}
for index,item in enumerate(items):
    itemOrder[item] = order[index]

# extract data from 2nd sheet - recipe to items dictionary
recipes = {}
rowIndex = 2; # skip header row
while True:
    row = sheets[1].row_values(rowIndex)
    if row == []: # end of table reached
        break
    else:
        recipes[row[0]] = row[2:] # use header column as key for list, skip recipe link
        rowIndex += 1

# extract data from 3rd sheet - input data lists
mealsToBuy = sheets[2].col_values(1)[1:] # get meals        , skip header row
exclusions = sheets[2].col_values(2)[1:] # get exclusions   , skip header row
extras     = sheets[2].col_values(3)[1:] # get extras       , skip header row

print('data retrieved')

# combine meal recipes into items list (using set to avoid duplication)
shoppingList = set()
for meal in mealsToBuy:
    shoppingList = shoppingList.union(recipes[meal])

# removing excluded items and add extras
for exclusion in exclusions:
    shoppingList.discard(exclusion)
shoppingList = shoppingList.union(extras)

# sorting according to mapping value and combining into one string
shoppingList = sorted(list(shoppingList),key=lambda x:itemOrder[x])

# copy items to new list while adding seperators
currentOrder = 0
shoppingList_seperated = []
for item in shoppingList:
    if itemOrder[item] != currentOrder:
        shoppingList_seperated.append('\n'+item) # move item to new list with seperator
        currentOrder = itemOrder[item] # update order
    else:
        shoppingList_seperated.append(item) # move item to new list

print('shopping list generated')

date = time.strftime("%d/%m/%Y-%H:%M:%S") # get date for subject line
subject = 'Shopping List ' + date # create subject for email

message = '\n'.join([
                '\nMeals:\n',
                '\n'.join(mealsToBuy),
                '\nItems:',
                '\n'.join(shoppingList_seperated)
                ])

send_email.sendEmail(subject,message)

print('email sent')
#print('NOTE - email suppressed')
