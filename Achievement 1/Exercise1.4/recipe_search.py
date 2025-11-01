import pickle

# This function will print out the recipe dictionary with difficulty
def display_recipe(recipe_dict):

    print(f'Recipe: {recipe_dict['name']}')
    print(f'Cooking Time (mins): {recipe_dict['cooking_time']}')
    print('Ingredients:')
    for i in recipe_dict['ingredients']:
        print(f'  - {i}')
    print(f'Difficulty Level: {recipe_dict['difficulty']}\n')

# This function displays all ingredients and lets user choose one.
def search_ingredient(data):

    # Display all ingredients from data w/indicies
    print('\n========== All Ingredients: ==========\n')
    for index, ingredient in enumerate(data['all_ingredients']):
        print(f' {index}. {ingredient}')

    try:
        ingredient_selected = int(input('Please enter the number for an ingredient above: '))
    except:
        print(f"❌ Invalid input : {ingredient_selected}")
    else:
        chosen_ingredient = data['all_ingredients'][ingredient_selected]

        # Filter the recipes to only include ones with the selected ingredient
        filtered_recipes = [recipe for recipe in data['recipes_list'] if chosen_ingredient in recipe['ingredients']]
        
        print(f'\n========== {len(filtered_recipes)} Recipes Containing {chosen_ingredient} ==========\n')
        for recipe in filtered_recipes:
            print('-------------------------')
            display_recipe(recipe)

# ----------Main------------------------------------------------------------------------------

# Try to open & load data from the binary file---------------

filename = str(input('\nEnter the filename storing the binary application data: '))

try:
    datafile = open(filename, 'rb') #❓Use 'with' here for temp open and auto close stream on error?
    data = pickle.load(datafile)
except FileNotFoundError:
    print(f"❌ Error: {filename} was not found.")
except EOFError:
    # Added this block due initially to empty file causing EOFError on pickle.load() and not closing stream
    #  with the logic setup in the task.
    print(f"❌ Error: {filename} was empty.")
    datafile.close()
except:
    print("❌ Unexpected error trying to open/load data.")
else:
    datafile.close()
    search_ingredient(data)
