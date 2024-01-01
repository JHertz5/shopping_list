from datetime import datetime

class Checklist:

    def __init__(self, filename=''):
        if filename == '':
            # generate filename
            now = datetime.now()
            self.filename = "shoppinglist_" + now.strftime('%Y%m%d%H%M%S') + ".txt"
        else:
            self.filename = filename

        self.file = open(self.filename,'w')

    def generate_file(self, shopping_list_grouped):
        groups = list(shopping_list_grouped.keys())

        # add recipes to file
        if 'recipes' in groups:
            groups.remove('recipes')
            for recipe in shopping_list_grouped['recipes']:
                self.add_line(recipe,'recipes')

        # add unknown groups to file
        if 'unknown' in groups:
            groups.remove('unknown')
            for item in shopping_list_grouped['unknown']:
                self.add_line(item['name'],'none')

        # add items to the file
        for group_idx,group in enumerate(sorted(groups)):
            for item in shopping_list_grouped[group]:
                entry = '{} ({})'.format(item['name'], item['num_portions'])
                self.add_line(entry, str(group_idx))

        self.file.close()

    def add_line(self, text, group, tag_list=[]):
        # Validate inputs.
        assert isinstance(text, str)
        assert isinstance(group, str)
        assert isinstance(tag_list, list)

        tag_list_formatted = [' +' + tag for tag in tag_list]
        line = text + " @" + group + "".join(tag_list_formatted) + '\n'
        self.file.write(line)
