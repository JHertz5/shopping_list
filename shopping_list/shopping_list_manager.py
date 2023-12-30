class ShoppingList:

    def __init__(self):
        self.recipes = []
        self.items = {}

    # add item to shopping list
    def add_item(self, item):
        if item in self.items.keys():
            self.items[item]['num_portions'] += 1
        else:
            self.items[item] = {
                'num_portions' : 1,
                'group' : 0
                }

    # add dict with list of items to shopping list
    def add_recipe(self, recipe_name, ingredients):
        self.recipes.append(recipe_name)
        for item in ingredients:
            self.add_item(item)

    def exclude_items(self, excluded_items):
        for item in excluded_items:
            # use pop to avoid errors when item is not on list
            self.items.pop(item, None)

    def include_items(self, included_items):
        current_items = self.items.keys()
        new_items = included_items.difference(current_items)

        for item in new_items:
            self.add_item(item)

    def set_item_groups(self, item_groups):
        group_known_items = item_groups.keys()
        for item in self.items.keys():
            if item in group_known_items:
                self.items[item]['group'] = item_groups[item]
            else:
                self.items[item]['group'] = 'unknown'

    def generate_grouped_list(self):
        grouped_list = {}

        # add recipes group
        grouped_list['recipes'] = self.recipes

        # add items to groups
        for item, data in self.items.items():
            group = data['group']
            group_item = {
            'name' : item,
            'num_portions' : data['num_portions']
            }
            if group in grouped_list:
                grouped_list[group].append(group_item)
            else:
                grouped_list[group] = [ group_item ]

        return grouped_list

    def preview_list(self):
        # convert group setss to strings with newline seperation
        item_strings = ['{} ({})'.format(x,self.items[x]['num_portions'])
            for x in self.items.keys()]

        preview = '\nRecipes:\n\t' \
        + '\n\t'.join(self.recipes) \
        + '\nItems:\n\t' \
        + '\n\t'.join(item_strings) \
        + '\n'
        print(preview)
