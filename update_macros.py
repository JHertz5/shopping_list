''' function to calculate macros in each recipe '''

import sheet_interface

def update_macros():
    sheets = sheet_interface.open_spreadsheet()

    # get ingredients data into dict of dicts
    ingredient_macros_sheet = sheets.worksheet('Items-Macros')
    ingredient_macros_raw = ingredient_macros_sheet.get_all_records()
    ingredient_macros = {}
    for ingredient in ingredient_macros_raw:
        ingredient_name = ingredient.pop('Item')
        ingredient_macros[ingredient_name] = ingredient

    # get meal ingredients into dict of lists
    meal_ingredients_sheet = sheets.worksheet('Recipes')
    meal_ingredients_raw = meal_ingredients_sheet.get_all_values()
    meal_ingredients = {}
    for meal in meal_ingredients_raw:
        meal_name = meal.pop(0)
        meal_ingredients[meal_name] = [ x for x in meal if x != '' ]

    # get headings for table fo meal macros
    arbitrary_ingredient = next(iter(ingredient_macros))
    macro_headings_raw = ingredient_macros[arbitrary_ingredient].keys()
    macro_headings = [ x for x in macro_headings_raw if '/Serving' in x ]

    print('data retrieved')

    # get list of meals
    meal_names = sorted(list(meal_ingredients.keys()))

    # get cells from recipe_macros_sheet
    recipe_macros_sheet = sheets.worksheet('Recipes-Macros')
    cell_range = 'A1:F' + str(len(meal_names)+1)
    cell_list = recipe_macros_sheet.range(cell_range)

    # fill in heading names
    cell_counter = 0
    cell_list[cell_counter].value = 'Meal'
    for index,cell in enumerate( cell_list[ 1 : 1+len(macro_headings) ]):
        cell_counter += 1
        cell.value = macro_headings[index]
    cell_counter += 1
    cell_list[cell_counter].value = 'Skipped Items'

    for meal in meal_names:
        # fill in name of meal
        cell_counter += 1
        cell_list[cell_counter].value = meal

        # find total of all ingredients for each heading and write to cell
        for heading in macro_headings:
            cell_counter += 1
            ingredient_macroList = [ int(ingredient_macros[x][heading])
                for x in meal_ingredients[meal] if x in ingredient_macros]
            mealMacroTotal = sum(ingredient_macroList)
            cell_list[cell_counter].value = mealMacroTotal

        cell_counter += 1
        skipped_ingredients = [ x for x in meal_ingredients[meal]
            if x not in ingredient_macros ]
        cell_list[cell_counter].value = ', '.join(skipped_ingredients)


    print('totals calculated')

    recipe_macros_sheet.update_cells(cell_list)

    print('new data written')
    print('macro update complete')

if __name__ == "__main__":
    update_macros()
