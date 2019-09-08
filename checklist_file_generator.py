from datetime import datetime

def generate_filename():
    filename_base = "shoppinglist_"
    filename_tag  = datetime.now().strftime('%Y%m%d%H%M%S')
    return filename_base + filename_tag

def generate_file(shopping_list_grouped, filename):
    with open(filename,'w') as checklist_file:
        groups = list(shopping_list_grouped.keys())

        # add recipes to file
        groups.remove('recipes')
        for recipe in shopping_list_grouped['recipes']:
            line = generate_checklist_line(recipe,'recipes')
            checklist_file.write(line)

        # add unknown groups to file
        groups.remove('unknown')
        for item in shopping_list_grouped['unknown']:
            line = generate_checklist_line(item['name'],'none')
            checklist_file.write(line)

        # add items to the file
        for group_idx,group in enumerate(groups):
            for item in shopping_list_grouped[group]:
                entry = '{} ({})'.format(item['name'], item['num_portions'])
                line = generate_checklist_line(entry, str(group_idx))
                checklist_file.write(line)

# TODO function to write whole group in default format and remove from list

# TODO write line in function
def generate_checklist_line(text,group):
    line = text + " @" + group + '\n'
    return line
