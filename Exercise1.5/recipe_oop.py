

class Recipe(object):

    # Class variable sharing all ingredients across all Recipe objects
    all_ingredients = []

    def __init__(self, name):
        self.name = name
        self.cooking_time = 0
        self.ingredients = []
        self.difficulty = 'NA'

    def __str__(self):
        return f"Recipe Name: {self.name}\n\
 - Cooking Time (minutes): {self.cooking_time}\n\
 - Ingredients: {', '.join(self.ingredients)}\n\
 - Difficulty: {self.difficulty}"

    def get_name(self):
        return self.name
    
    def set_name(self, new_name):
        self.name = new_name

    def get_cooking_time(self):
        return self.cooking_time

    def set_cooking_time(self, new_cooking_time):
        self.cooking_time = new_cooking_time
        self.calculate_difficulty(self.cooking_time, len(self.ingredients))

    def get_ingredients(self):
        return self.ingredients

    def get_difficulty(self):
        if self.difficulty == 'NA':
            self.calculate_difficulty(self.cooking_time, len(self.ingredients))
        return self.difficulty

    # Assigns instance variable self.difficulty a rating based on the parameters.
    def calculate_difficulty(self, cooking_time, ingredient_count):
        if cooking_time < 10 and ingredient_count < 4:
            self.difficulty = 'Easy'
        elif cooking_time < 10 and ingredient_count >= 4:
            self.difficulty = 'Medium'
        elif cooking_time >= 10 and ingredient_count < 4:
            self.difficulty = 'Intermediate'
        elif cooking_time >= 10 and ingredient_count >= 4:
            self.difficulty = 'Hard'
        else:
            self.difficulty = 'Unable to determine difficulty'

    # Takes a tuple with one or more ingredients as str and adds to the
    #  instance self.ingredients as well as updating all ingredients.
    def add_ingredients(self, ingredients_tuple = () ):
        if len(ingredients_tuple) == 0:
            return # Nothing to add
        
        for item in ingredients_tuple:
            # Standardize the formatting of igredients for comparison
            item = item.title()
            self.ingredients.append(item)

        # Ingredients added, recalculate difficulty
        self.calculate_difficulty(self.cooking_time, len(self.ingredients))
        
        # Update all ingredients
        self.update_all_ingredients()
                
    # Returns True/False if ingredient is in the instance variable self.ingredients
    def search_ingredient(self, ingredient):
        return ingredient.title() in self.ingredients
        
    # Returns recipes that contain specified ingredient
    def recipe_search(data, search_term):
        found_recipes = []
        for recipe in data:
            if recipe.search_ingredient(search_term):
                found_recipes.append(recipe)
        if len(found_recipes) > 0:
            print(f" * * Found '{search_term.title()}' in {len(found_recipes)} Recipes:")
            print("--------------------")
            for recipe in found_recipes:
                print(f"{recipe}")
                print("--------------------")

    # Adds any new ingredients to collective class variable all_ingredients
    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            if not ingredient in Recipe.all_ingredients:
                Recipe.all_ingredients.append(ingredient)
        Recipe.all_ingredients.sort()

    # Prints list of collective all_ingredients list
    def print_all_ingredients():
        for ingredient in Recipe.all_ingredients:
            print(f" - {ingredient}")

# -----Main-------------------------------------------------

# Testing class
tea = Recipe("Tea")
tea.add_ingredients(("Tea leaves","Water","Sugar"))
tea.set_cooking_time(5)
print("Displaying str representation of 'Tea' recipe:")
print(tea)

# Adding more recipes
coffee = Recipe("Coffee")
coffee.add_ingredients(("Ground Coffee","Water","Cream","Sugar"))
coffee.set_cooking_time(5)

cake = Recipe("Cake")
cake.add_ingredients(("sugar","butter","eggs","vanilla extract","flour","baking powder","milk"))
cake.set_cooking_time(50)

banana_smoothie = Recipe("Banana Smoothie")
banana_smoothie.add_ingredients(("bananas","milk","peanut butter","sugar","ice cubes"))
banana_smoothie.set_cooking_time(5)

recipes_list = [tea, coffee, cake, banana_smoothie]

print("\n *** Searching for 'Water'")
Recipe.recipe_search(recipes_list, "Water")

print("\n *** Searching for 'Sugar'")
Recipe.recipe_search(recipes_list, "Sugar")

print("\n *** Searching for 'Bananas")
Recipe.recipe_search(recipes_list, "Bananas")

# Test printing all ingredients
print("\n-----All Ingredients-----\n")
Recipe.print_all_ingredients()