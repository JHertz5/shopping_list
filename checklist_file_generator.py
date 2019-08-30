from datetime import datetime

def generate_filename():
    filename_base = "shoppinglist_"
    filename_tag  = datetime.now().strftime('%Y%m%d%H%M%S')
    return filename_base + filename_tag

def generate_file(mealsToBuy,shoppingList_grouped, filename):
    with open(filename,'w') as checklist_file:
        for meal in mealsToBuy:
            line = generate_checklist_line(meal,'meals')
            checklist_file.write(line)

        for (group_id,group) in enumerate(shoppingList_grouped):
            for item in group:
                line = generate_checklist_line(item,str(group_id))
                checklist_file.write(line)

def generate_checklist_line(text,group):
    return text + " @" + group + '\n'
