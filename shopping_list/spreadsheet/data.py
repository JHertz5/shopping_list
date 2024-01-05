from ..database import ingredient_database
from ..database import recipe_database


def get_ingredient_list(ingredients_data):
    return [x['Name'] for x in ingredients_data]


def get_ingredient_grouping_options(ingredients_data):
    grouping_options = list(ingredients_data[0].keys())[1:]
    return grouping_options


def get_ingredient_sheet_data(ingredients_data, grouping_selection):
    # Get data from the sheet.

    # Construct the ingredients dict.
    ingredients = ingredient_database.ingredientDatabase()
    for record in ingredients_data:
        # The record holds the name of the ingredient and all of the groupings. The name and the groupings must be
        # provided separately to the ingredient class, so extract the name from the record and construct an instance of
        # the ingredient object.
        ingredient_name = record.pop('Name')
        ingredients.add_new_ingredient(ingredient_name, record[grouping_selection])

    return ingredients


def get_recipe_sheet_data(recipe_data):
    # Construct recipes dict.
    recipes = recipe_database.RecipeDatabase()
    for recipe_row in recipe_data:
        # The row holds the name of the recipe in the first column and all of the ingredients in subsequent columns.
        # Parse the name and the ingredients from the row to construct an instance of the recipe object.
        recipe_name = recipe_row[0]
        recipe_ingredients = [x for x in recipe_row[1:] if x != '']
        recipes.add_new_recipe(recipe_name, recipe_ingredients)

    return recipes


def get_input_sheet_data(input_sheet_data):
    meals_to_buy_list = input_sheet_data['Meals To Buy']
    exclusions_list = input_sheet_data['Exclusions']
    inclusions_list = input_sheet_data['Inclusions']

    return meals_to_buy_list, exclusions_list, inclusions_list
