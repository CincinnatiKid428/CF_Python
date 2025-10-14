import pickle

#Holds bin file data object
data = {}

#Create master lists for all recipes and all ingredients in all recipes
recipes_list, all_ingredients = [],[]

# Takes input from the user for a new recipe, gathering name, cooking time and ingredient list.
def take_recipe():

    name = str(input("\nEnter the name of the recipe: "))
    cooking_time = int(input("Enter the cooking time in minutes: "))
    
    ingredients = []
    ingredient = "not done"

    #Loop to get all ingredients
    print('Enter an ingredient or "Done" to finish: ')
    while ingredient.lower() != "done":
        ingredient = str(input('  - '))
        if ingredient.lower() != "done":
            ingredients.append(ingredient.title())

    ingredients.sort()

    #Create recipe dictionary
    recipe = {'name':name, 
              'cooking_time':cooking_time, 
              'ingredients':ingredients,
              'difficulty':calc_diffficulty(cooking_time, len(ingredients))
              }   
    return recipe

# Sssigns a difficulty rating based on the parameters.
def calc_diffficulty(cooking_time, ingredient_count):

    if cooking_time < 10 and ingredient_count < 4:
        return 'Easy'
    elif cooking_time < 10 and ingredient_count >= 4:
        return 'Medium'
    elif cooking_time >= 10 and ingredient_count < 4:
        return 'Intermediate'
    elif cooking_time >= 10 and ingredient_count >= 4:
        return 'Hard'
    else:
        return 'Unable to determine difficulty'

# Prints out the recipe dictionary with difficulty
def display_recipe(recipe_dict):
    print(f'Recipe: {recipe_dict['name']}')
    print(f'Cooking Time (mins): {recipe_dict['cooking_time']}')
    print('Ingredients:')
    for i in recipe_dict['ingredients']:
        print(f'  - {i}')
    print(f'Difficulty Level: {recipe_dict['difficulty']}\n')

# Sets the global data object to a dictionary with empty lists for recipes_list & all_ingredients.
def set_default_data():
    global data
    data = {
        'recipes_list':[],
        'all_ingredients':[]
    }
    print("ℹ  Default data has been set")

# Prints lists written in pickle.dump() for debugging
def print_dump_data():
    print("\n💾 Recipes & Ingredients Data :\n")

    print("=-=-=-=-=-=-=-All Recipes:=-=-=-=-=-=-=-\n")
    for recipe in recipes_list:
        display_recipe(recipe)

    print("=-=-=-=-=-=-=-Ingredients Across All Recipes:=-=-=-=-=-=-=-\n")
    for i in all_ingredients:
        print(f'  - {i}')

# -----Main---------------------------------------------------

# Try to open & load data from the binary file---------------

filename = str(input('\nEnter the filename storing the binary application data: '))

try:
    datafile = open(filename, 'rb') #❓Use 'with' here for temp open and auto close stream on error?
    data = pickle.load(datafile)
except FileNotFoundError:
    print(f"❌ Error: {filename} was not found.")
    set_default_data()
except EOFError:
    # Added this block due initially to empty file causing EOFError on pickle.load() and not closing stream
    #  with the logic setup in the task.
    print(f"❌ Error: {filename} was empty.")
    datafile.close()
    set_default_data()
except:
    print("❌ Unexpected error trying to open/load data.")
    set_default_data()
else:
    datafile.close()
finally:
    recipes_list = data['recipes_list']
    all_ingredients = data['all_ingredients']



# Ask the user to add new recipes-------------------------

n = int(input("\nHow many recipes would you like to add? "))

#Get n recipes
for i in range(0, n):
    recipe = take_recipe()
    #Check if each ingredient is stored in master list, if not add it
    for ingredient in recipe['ingredients']:
        if ingredient.title() not in all_ingredients:
            all_ingredients.append(ingredient.title())
    #Add recipe to master list
    recipes_list.append(recipe)

all_ingredients.sort()

# Update data object with new lists and write out to binary file----------

data = {
    'recipes_list':recipes_list,
    'all_ingredients':all_ingredients
}

try:
    datafile = open(filename, 'wb')
    pickle.dump(data, datafile)
except:
    print(f"❌ Unexpected error encountered while writing binary data to {filename}")
    #❓Is it possible to reach this block with an error from pickle.dump() and yet still have open file stream?
else:
    datafile.close()

print_dump = str(input('Would you like to see the current lists of recipes & all ingredients? (Y/N): '))
if print_dump.lower() == 'y':
    print_dump_data()