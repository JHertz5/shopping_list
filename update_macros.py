''' script to calculate macros in meals based with google sheets as database '''

import sheet_interface

sheets = sheet_interface.openSpreadsheet()

ingredientMacrosSheet = sheets.worksheet('Items-Macros')
mealIngredientsSheet = sheets.worksheet('Recipes')
recipeMacrosSheet = sheets.worksheet('Recipes-Macros')


# get ingredients data into dict of dicts
ingredientMacrosRaw = ingredientMacrosSheet.get_all_records()
ingredientMacros = {}
for ingredient in ingredientMacrosRaw:
    ingredientName = ingredient.pop('Item')
    ingredientMacros[ingredientName] = ingredient

# get meal ingredients into dict of lists
mealIngredientsRaw = mealIngredientsSheet.get_all_values()
mealIngredients = {}
for meal in mealIngredientsRaw:
    mealName = meal.pop(0)
    mealIngredients[mealName] = [ x for x in meal if x != '' ]

# get headings for table fo meal macros
arbitraryIngredient = next(iter(ingredientMacros))
macroHeadingsRaw = ingredientMacros[arbitraryIngredient].keys()
macroHeadings = [ x for x in macroHeadingsRaw if '/Serving' in x ]

print('data retrieved')

# get list of meals
mealNames = sorted(list(mealIngredients.keys()))

# get cells from recipeMacrosSheet
cellRange = 'A1:E' + str(len(mealNames)+1)
cellList = recipeMacrosSheet.range(cellRange)

cellList[0].value = 'Meal'
cellCounter = 0

for index,cell in enumerate( cellList[ 1 : 1+len(macroHeadings) ]):
    cellCounter += 1
    cell.value = macroHeadings[index]

for meal in mealNames:
    # fill in name of meal
    cellCounter += 1
    cellList[cellCounter].value = meal

    # find total of all ingredients for each heading and write to cell
    for heading in macroHeadings:
        cellCounter += 1
        ingredientMacroList = [ int(ingredientMacros[x][heading]) for x in mealIngredients[meal] if x in ingredientMacros]
        mealMacroTotal = sum(ingredientMacroList)
        cellList[cellCounter].value = mealMacroTotal

print('totals calculated')

recipeMacrosSheet.update_cells(cellList)

print('new data written')
print('macro update complete')
