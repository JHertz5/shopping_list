def generate(mealsToBuy,shoppingList_grouped):
    filename = 'checklist.txt'
    with open(filename,'w') as checklist_file:
        for meal in mealsToBuy:
            line = generate_checklist_line(meal,'meals to buy')
            checklist_file.write(line)

        for (group_id,group) in enumerate(shoppingList_grouped):
            for item in group:
                line = generate_checklist_line(item,str(group_id))
                checklist_file.write(line)
    return filename

def generate_checklist_line(text,group):
    return text + " @" + group + '\n'
