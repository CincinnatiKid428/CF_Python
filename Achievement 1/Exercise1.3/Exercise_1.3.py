#Create master lists for all recipes and all ingredients in all recipes
recipes_list, ingredients_list = [],[]

# This function takes input from the user for a new recipe, gathering
# name, cooking time and ingredient list.
def take_recipe():
    name = str(input("\nEnter the name of the recipe: "))
    cooking_time = int(input("Enter the cooking time in minutes: "))
    
    ingredients = []
    ingredient = "next"

    #Loop to get all ingredients
    print('Enter an ingredient or "Done" to finish: ')
    while ingredient.lower() != "done":
        ingredient = str(input('  - '))
        if ingredient.lower() != "done":
            ingredients.append(ingredient)

    #Create recipe dictionary
    recipe = {'name':name, 
              'cooking_time':cooking_time, 
              'ingredients':ingredients
              }   
    return recipe

# This function assigns a difficulty rating based on the recipe parameter's
# cooking time and ingredient count.
def get_difficulty(recipe_dict):
    cooking_time = recipe_dict['cooking_time']
    ingredient_count = len(recipe_dict['ingredients'])

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

# This function will print out the recipe dictionary with difficulty
def print_recipe(recipe_dict):
    print(f'Recipe: {recipe_dict['name']}')
    print(f'Cooking Time (mins): {recipe_dict['cooking_time']}')
    print('Ingredients:')
    for i in recipe_dict['ingredients']:
        print(f'  - {i}')
    print(f'Difficulty Level: {get_difficulty(recipe_dict)}\n')

# -----Main---------------------------------------------------

n = int(input("\nHow many recipes would you like to add? "))

# I left this in just to show I tried to originally do the master list using the
# list comprehension method, but with the additional checks (and the lesson said do a for-loop)
# I changed it.  It did take the values and create the list properly though!

#recipes_list = [take_recipe() for i in range(0,n)]

#Get n recipes
for i in range(0, n):
    recipe = take_recipe()
    #Check if each ingredient is stored in master list, if not add it
    for ingredient in recipe['ingredients']:
        if ingredient.title() not in ingredients_list:
            ingredients_list.append(ingredient.title())
    #Add recipe to master list
    recipes_list.append(recipe)

print("====================================================================\n")

print(" All Recipes:\n=-=-=-=-=-=-=-")
for recipe in recipes_list:
    print_recipe(recipe)

print(" Ingredients Available Across All Recipes:\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
ingredients_list.sort()
for i in ingredients_list:
    print(f'  - {i}')