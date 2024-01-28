import unittest
from unittest import mock

from shopping_list import data

# Testing lower case (dark chocolate)
test_ingredients_sheet_data = [
    {'Name': 'Apples', 'aldi': 1, 'lidl': 2},
    {'Name': 'Bananas', 'aldi': 0, 'lidl': 2},
    {'Name': 'Cucumber', 'aldi': 0, 'lidl': 1},
    {'Name': 'dark chocolate', 'aldi': 0, 'lidl': 1},
]

# Testing not title case (Apple pie)
test_recipes_sheet_data = [
    ['Fruit Salad', 'Apples', 'Bananas'],
    ['Apple pie', 'Apples', 'Flour', 'dark chocolate']
]

# Testing unknown recipe (Steak and Chips)
# Testing unknown item in exclusions (Oranges)
# Testing unknown item in inclusions (Beef)
# Testing inlusions/exclusions conflict (Bananas)
test_input_sheet_data_raw = [
    ['Meals To Buy', 'Fruit Salad', 'Apple pie', 'Steak and Chips'],
    ['Exclusions', 'Bananas', 'Oranges'],
    ['Inclusions', 'Cucumber', 'Bananas', 'Beef']
]
test_input_sheet_data = {
    'Meals To Buy': ['Fruit Salad', 'Apple pie', 'Steak and Chips'],
    'Exclusions': ['Bananas', 'Oranges'],
    'Inclusions': ['Cucumber', 'Bananas', 'Beef']
}

test_ingredients = {
    'Apples': {'aldi': 1, 'lidl': 2},
    'Bananas': {'aldi': 0, 'lidl': 2},
    'Cucumber': {'aldi': 0, 'lidl': 1}
}

test_recipes = {
    'Fruit salad': ['Apples', 'Bananas']
}

test_input = {
    'Meals to buy': ['Fruit Salad', 'Apple pie', 'Steak and Chips'],
    'Exclusions': ['Oranges'],
    'Inclusions': ['Cucumber'],
}


@mock.patch('sys.stdout')
@mock.patch('gspread.Spreadsheet')
class TestData(unittest.TestCase):

    def test_download_ingredients_data(self, mock_spreadsheet, mock_stdout):
        mock_spreadsheet.worksheet().get_all_records.return_value = test_ingredients_sheet_data
        test_data_obj = data.Data(mock_spreadsheet)
        test_data_obj.download_ingredients_data(mock_spreadsheet)
        actual = test_data_obj._ingredients_sheet_data

        expected = test_ingredients_sheet_data

        self.assertEqual(actual, expected)

        expected_stdout = []
        expected_stdout.append(mock.call('ingredients retrieved'))
        expected_stdout.append(mock.call('\n'))
        expected_stdout.append(mock.call('recipes retrieved'))
        expected_stdout.append(mock.call('\n'))
        expected_stdout.append(mock.call('input retrieved'))
        expected_stdout.append(mock.call('\n'))
        expected_stdout.append(mock.call('ingredients retrieved'))
        expected_stdout.append(mock.call('\n'))

        mock_stdout.write.assert_has_calls(expected_stdout)


    def test_download_recipes_data(self, mock_spreadsheet, mock_stdout):
        mock_spreadsheet.worksheet().get_values.return_value = test_recipes_sheet_data
        test_data_obj = data.Data(mock_spreadsheet)
        test_data_obj.download_recipes_data(mock_spreadsheet)
        actual = test_data_obj._recipes_sheet_data

        expected = test_recipes_sheet_data

        self.assertEqual(actual, expected)


        expected_stdout = []
        expected_stdout.append(mock.call('ingredients retrieved'))
        expected_stdout.append(mock.call('\n'))
        expected_stdout.append(mock.call('recipes retrieved'))
        expected_stdout.append(mock.call('\n'))
        expected_stdout.append(mock.call('input retrieved'))
        expected_stdout.append(mock.call('\n'))
        expected_stdout.append(mock.call('recipes retrieved'))
        expected_stdout.append(mock.call('\n'))

        mock_stdout.write.assert_has_calls(expected_stdout)



    def test_download_input_data(self, mock_spreadsheet, mock_stdout):
        mock_spreadsheet.worksheet().get_values.return_value = test_input_sheet_data_raw
        test_data_obj = data.Data(mock_spreadsheet)
        test_data_obj.download_input_data(mock_spreadsheet)
        actual = test_data_obj._input_sheet_data

        expected = test_input_sheet_data

        self.assertEqual(actual, expected)


        expected_stdout = []
        expected_stdout.append(mock.call('ingredients retrieved'))
        expected_stdout.append(mock.call('\n'))
        expected_stdout.append(mock.call('recipes retrieved'))
        expected_stdout.append(mock.call('\n'))
        expected_stdout.append(mock.call('input retrieved'))
        expected_stdout.append(mock.call('\n'))
        expected_stdout.append(mock.call('input retrieved'))
        expected_stdout.append(mock.call('\n'))

        mock_stdout.write.assert_has_calls(expected_stdout)


    def test_add_new_recipe_to_buy(self, mock_spreadsheet, mock_stdout):
        new_recipe = 'Stir-fry'

        test_data_obj = data.Data(mock_spreadsheet)
        test_data_obj._input_sheet_data = test_input_sheet_data

        test_data_obj.add_new_recipe_to_buy(mock_spreadsheet, new_recipe)
        mock_spreadsheet.worksheet().update_cell.assert_called_with(4, 1, new_recipe)

    def test_get_ingredient_list(self, mock_spreadsheet, mock_stdout):
        test_data_obj = data.Data(mock_spreadsheet)
        test_data_obj._ingredients_sheet_data = test_ingredients_sheet_data
        actual = test_data_obj.get_ingredient_list()

        expected = ['Apples', 'Bananas', 'Cucumber', 'dark chocolate']

        self.assertEqual(actual, expected)

    def test_get_ingredient_grouping_options(self, mock_spreadsheet, mock_stdout):
        test_data_obj = data.Data(mock_spreadsheet)
        test_data_obj._ingredients_sheet_data = test_ingredients_sheet_data
        actual = test_data_obj.get_ingredient_grouping_options()

        expected = ['aldi', 'lidl']

        self.assertEqual(actual, expected)

    def test_get_ingredient_sheet_data(self, mock_spreadsheet, mock_stdout):
        test_data_obj = data.Data(mock_spreadsheet)
        test_data_obj._ingredients_sheet_data = test_ingredients_sheet_data
        actual_dict = test_data_obj.get_ingredient_sheet_data('aldi')._item_dict

        expected_dict = {
            'Apples': {'quantity': 0, 'group': 1},
            'Bananas': {'quantity': 0, 'group': 0},
            'Cucumber': {'quantity': 0, 'group': 0},
            'dark chocolate': {'quantity': 0, 'group': 0}
        }

        self.assertEqual(actual_dict.keys(), expected_dict.keys())
        for key in expected_dict.keys():
            self.assertEqual(actual_dict[key].__dict__, expected_dict[key])

    def test_get_recipes_sheet_data(self, mock_spreadsheet, mock_stdout):
        test_data_obj = data.Data(mock_spreadsheet)
        test_data_obj._recipes_sheet_data = test_recipes_sheet_data
        actual_dict = test_data_obj.get_recipes_sheet_data()._item_dict

        expected_dict = {
            'Fruit Salad': {
                'quantity': 0,
                'group': 'recipes',
                'ingredient_list': ['Apples', 'Bananas']
            },
            'Apple pie': {
                'quantity': 0,
                'group': 'recipes',
                'ingredient_list': ['Apples', 'Flour', 'dark chocolate']
            }
        }

        self.assertEqual(actual_dict.keys(), expected_dict.keys())
        for key in expected_dict.keys():
            self.assertEqual(actual_dict[key].__dict__, expected_dict[key])

    def test_get_input_sheet_data(self, mock_spreadsheet, mock_stdout):
        test_data_obj = data.Data(mock_spreadsheet)
        for key in test_input_sheet_data.keys():
            test_data_obj._input_sheet_data[key] = test_input_sheet_data[key]

        actual_recipes_to_buy, actual_exclusions_list, actual_inclusions_list = test_data_obj.get_input_sheet_data()

        expected_recipes_to_buy = test_input_sheet_data['Meals To Buy']
        expected_exclusions_list = test_input_sheet_data['Exclusions']
        expected_inclusions_list = test_input_sheet_data['Inclusions']

        self.assertEqual(actual_recipes_to_buy, expected_recipes_to_buy)
        self.assertEqual(actual_exclusions_list, expected_exclusions_list)
        self.assertEqual(actual_inclusions_list, expected_inclusions_list)
