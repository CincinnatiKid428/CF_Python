#File: recipe_mysql.py

#This file will connect the CLI app to a MySQL database and provide an interface for recipe SQL operations.

import os
import textwrap
from dotenv import load_dotenv
import mysql.connector

# This function will print out the recipe dictionary with difficulty.
def display_recipe(recipe_dict):

    print(f'🍴 Recipe: {recipe_dict['name']}')
    print(f'  🕑 Cooking Time (mins): {recipe_dict['cooking_time']}')
    print(f'  🍳 Difficulty Level: {recipe_dict['difficulty']}')
    print('  🥕 Ingredients:')
    ingredients = ", ".join(recipe_dict['ingredients'])
    for line in textwrap.wrap(ingredients, width=60):
        print(f'        {line}')
    print("\n")

# Converts a recipe row from the database into a recipe dictionary.
def get_recipe_dict_from_row(recipe_row):
    recipe_id= recipe_row[0]
    name = recipe_row[1]
    ingredients = recipe_row[2].split(", ")
    cooking_time = recipe_row[3]
    difficulty = recipe_row[4]

    #Create recipe dictionary (4, 'Chicken Noodle Soup', 'Carrots, Celery, Chicken, Chicken Broth, Garlic, Noodles, Onion, Oregano, Parsley, Pepper, Salt, Water', 25, 'Hard')
    recipe = {
        'id':recipe_id,
        'name':name, 
        'cooking_time':cooking_time, 
        'ingredients':ingredients,
        'difficulty':difficulty
        }   
    return recipe

#SELECTS one row given id param and prints the recipe.
def verify_recipe_by_id(cursor, id):
    cursor.execute(f"SELECT * FROM Recipes WHERE id={id};")
    update = cursor.fetchall()
    updated_recipe = get_recipe_dict_from_row(update[0])
    display_recipe(updated_recipe)

# Displays main menu and calls functions according to user choice
def main_menu(conn, cursor):

    while True:
        print("\n✴️ ✴️ ✴️ Main Menu ✴️ ✴️ ✴️\n")
        print("Choose from the following:")
        print("     1. Create a new recipe")
        print("     2. Search for recipes by ingredient")
        print("     3. Update an existing recipe")
        print("     4. Delete a recipe")
        print("     Type 'Quit' to exit the program\n")
        choice = str(input("✴️ Enter 1-4 or 'quit': "))

        try:
            if choice == '1':
                create_recipe(conn, cursor)
            elif choice == '2':
                search_recipe(conn, cursor)
            elif choice == '3':
                update_recipe(conn, cursor)
            elif choice == '4':
                delete_recipe(conn, cursor)
            elif choice.lower() == 'quit': #Exit loop condition
                break
            else:
                print(f"❌ Invalid selection {choice}")
                continue
        except Exception as e:
            print(f"\n     ❌ Error with database operation: {e}")
            
# Takes input from the user for a new recipe, gathering name, cooking time and ingredient list.
def create_recipe(conn, cursor):

    print("\n🟢 🟢 🟢 Create Recipe 🟢 🟢 🟢\n")

    name = ''

    while True:
        name = str(input("🟢 Enter the name of the recipe: "))
        if name != '':
            name = name.title()
            break
        else:
            print("❌ Recipe name cannot be empty...")


    cooking_time = 'a'
    
    while True:
        cooking_time = input(f'🟢 Enter the cooking time in minutes: ')
        if cooking_time.isdigit():  #Checks that input is only digits
            cooking_time = int(cooking_time)
            break
        else:
            print("❌ Please enter a valid number of minutes (digits only).")

    ingredients = []

    #Loop to get all ingredients
    print('🟢 Enter an ingredient or "Done" to finish: ')
    while True:
        ingredient = str(input('  - '))
        if ingredient.lower() == "":
            print("❌ Ingredients cannot be empty...")
            continue
            
        elif ingredient.lower() != "done":
            ingredients.append(ingredient.title())
        
        elif len(ingredients) < 1:
            print("❌ Please enter at least 1 ingredient...")
            continue
        
        else: #Exit loop, input must be 'done' and >0 ingredient
            break

    ingredients.sort()
    difficulty = calc_difficulty(cooking_time, len(ingredients))

    #Create recipe dictionary
    recipe = {'name':name, 
              'cooking_time':cooking_time, 
              'ingredients':ingredients,
              'difficulty':difficulty
              }   

    #Insert new recipe into DB
    cursor.execute(f'''INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (
    '{name}', '{", ".join(ingredients)}', '{cooking_time}', '{difficulty}');''')
    conn.commit()

    print("\n     ✅ Finished insert for recipe:\n")
    display_recipe(recipe)

#Assigns a difficulty rating based on the parameters.
def calc_difficulty(cooking_time, ingredient_count):

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

#SELECTS recipes from database containing a search ingredient.
def search_recipe(conn, cursor):
    print("\n🔹🔹🔷🔹🔹 Search Recipe 🔹🔹🔷🔹🔹\n")

    #SELECT list of all ingredients in database
    cursor.execute("SELECT ingredients FROM Recipes;")
    results = cursor.fetchall()

    all_ingredients = []
    search_ingredient = 'none'

    for row in results:
        ingred_list = row[0].split(", ")
        for i in ingred_list:
            if not i in all_ingredients:
                all_ingredients.append(i)

    all_ingredients.sort()
    num_ingredients = len(all_ingredients)
    
    #Show list to user with numbers to select an ingredient
    for i in range(0,num_ingredients):
        print(f'     {i+1}. {all_ingredients[i]}') #Display list starting from 1. for user (i+1)

    choice = str(input("🔹Enter ingredient number or 'Back' to go to the Main Menu: "))
    
    while choice.lower() != 'back':
        if choice.isdigit():
            if 1 <= int(choice) <= num_ingredients:
                break
        choice = str(input(f"     ❌ Invalid choice {choice}\n🔹Enter ingredient number or 'Back' to go to the Main Menu: "))

    if choice.lower() == 'back':
        return #Do nothing, go back to Main Menu
    else:
        search_ingredient = all_ingredients[int(choice)-1]

    #SELECT all recipes containing this search ingredient
    cursor.execute(f"SELECT * FROM Recipes WHERE ingredients LIKE '%{search_ingredient}%';")
    results = cursor.fetchall()
    print(f"\n===== Found {search_ingredient} in {len(results)} Recipes : =====\n")
    for row in results:
        display_recipe(get_recipe_dict_from_row(row))

#UPDATES an existing recipe's name, cooking time or ingredients.
def update_recipe(conn, cursor):
    print("\n🔸🔸🔶🔸🔸 Update Recipe 🔸🔸🔶🔸🔸\n")

    while True:
        print("Select the Recipe to Update:")

        #SELECT all recipes id & name
        cursor.execute("SELECT id, name FROM Recipes;")
        all_recipe_ids_names = cursor.fetchall()
        valid_ids = []

        #Show all recipes to user with id, name
        for row in all_recipe_ids_names:
            print(f'     {row[0]}. {row[1]}')
            valid_ids.append(str(row[0]))

        choice = str(input("\n🔸Enter recipe number or 'Back' to go to the Main Menu: "))
        selected_recipe = {}

        #Ensure valid recipe selection
        while not choice in valid_ids and choice.lower() != 'back':
            choice = str(input(f"❌ Invalid choice {choice}\n🔸Enter recipe number or 'Back' to go to the Main Menu: "))

        if choice.lower() == 'back': #Exit loop & go back
            break
        else:  
            print("\n")
            query = "SELECT * FROM Recipes WHERE id=%s;"
            values = (choice,)
            cursor.execute(query, values)
            result = cursor.fetchall()
            selected_recipe = get_recipe_dict_from_row(result[0])

        #Print entire recipe selected and ask which column to update
        display_recipe(selected_recipe)
        print("Please enter a choice to update the recipe :")
        print("     1. Update Name\n     2. Update Cooking Time\n     3. Update Ingredients")
        update_choice = str(input("\n🔸Select an option above or enter 'Back' to pick a different recipe: "))
    
        #Ensure valid update choice made
        valid_choices = ['1','2','3','back']
        while not update_choice.lower() in valid_choices:
            update_choice = str(input(f"❌ Invalid choice {choice}\n🔸Enter an option above or enter 'Back' to pick a different recipe: "))

        if update_choice.lower() == 'back': #Go back to update a recipe loop
            print("\n")
            continue
        
        #Get new name column input and UPDATE
        elif update_choice == '1':
            new_name = ''

            while True:
                new_name = str(input(f'🔸Enter a new name for "{selected_recipe['name']}" : '))
                if new_name != '':
                    new_name = new_name.title()
                    break
                else:
                    print("❌ Recipe name cannot be empty...")

            query = "UPDATE Recipes SET name = %s WHERE id = %s;"
            values = (new_name, selected_recipe['id'])
            cursor.execute(query, values)
            conn.commit()
            print(f"\n     ✅ Updated {selected_recipe['name']}\n")

            #Verify row back to user with SELECT
            verify_recipe_by_id(cursor, selected_recipe['id'])
        
        #Get new cooking time input and UPDATE
        elif update_choice == '2':
            new_cooking_time = ''
            while True:
                new_cooking_time = input(f'🔸Enter a new cooking time for "{selected_recipe["name"]}" in minutes: ')
                if new_cooking_time.isdigit():  #Checks that input is only digits
                    new_cooking_time = int(new_cooking_time)
                    break
                else:
                    print("❌ Please enter a valid number of minutes (digits only).")        
                        
            #Recalculate difficulty based on new igredients list length
            difficulty = calc_difficulty(int(new_cooking_time), len(selected_recipe['ingredients']))

            query = "UPDATE Recipes SET cooking_time = %s, difficulty = %s WHERE id = %s;"
            values = (new_cooking_time, difficulty, selected_recipe['id'])
            cursor.execute(query, values)
            conn.commit()
            print(f"\n     ✅ Updated {selected_recipe['name']}\n")

            #Verify row back to user with SELECT
            verify_recipe_by_id(cursor, selected_recipe['id'])

        #Get new ingredients input and UPDATE
        elif update_choice == '3':
            ingredients = []

            #Loop to get all ingredients
            print(f'\n🔸Enter new ingredients for "{selected_recipe['name']}" or "Done" to finish: ')
            while True:
                ingredient = str(input('  - '))
                if ingredient.lower() == "":
                    print("❌ Ingredients cannot be empty...")
                    continue

                elif ingredient.lower() != "done":
                    ingredients.append(ingredient.title())

                elif len(ingredients) < 1:
                    print("❌ Please enter at least 1 ingredient...")
                    continue
                
                else: #Exit loop, input must be 'done' and >0 ingredient
                    print("\n")
                    break

            ingredients.sort()

            #Recalculate difficulty based on new igredients list length
            difficulty = calc_difficulty(int(selected_recipe['cooking_time']), len(ingredients))

            query = "UPDATE Recipes SET ingredients = %s, difficulty = %s WHERE id = %s;"
            values = (", ".join(ingredients), difficulty, selected_recipe['id'])
            cursor.execute(query, values)
            conn.commit()
            print(f"\n     ✅ Updated {selected_recipe['name']}\n")

            #Verify row back to user with SELECT
            verify_recipe_by_id(cursor, selected_recipe['id'])

#DELETES an existing recipe.
def delete_recipe(conn, cursor):
    print("\n🔺🔺🔺🔺🔺 Delete Recipe 🔺🔺🔺🔺🔺\n")

    while True:
        print("Select the Recipe to Delete:")

        cursor.execute("SELECT id, name FROM Recipes;")
        all_recipe_ids_names = cursor.fetchall()
        valid_ids = []

        for row in all_recipe_ids_names:
            print(f'     {row[0]}. {row[1]}')
            valid_ids.append(str(row[0]))

        valid_ids.append('back')

        choice = str(input("\n🔺Enter recipe number or 'Back' to go to the Main Menu: "))

        #Ensure valid input
        while not choice.lower() in valid_ids:
            choice = str(input(f"❌ Invalid choice {choice}\n🔺Enter recipe number or 'Back' to go to the Main Menu: "))

        if choice.lower() == 'back': #Exit loop & go back
            break
        else:       
            cursor.execute(f"DELETE FROM Recipes WHERE (id='{choice}');")
            conn.commit()
            for recipe_id, recipe_name in all_recipe_ids_names:
                if str(recipe_id) == choice:
                    print(f"\n     ✅ Deleted {recipe_name}\n")
                    break 

#=====MAIN===========================================================

#Load the .env file
load_dotenv()

#Pull values from .env
host = os.getenv("MYSQL_HOST")
port = int(os.getenv("MYSQL_PORT",3306))
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASS")
db = os.getenv("MYSQL_DB")

#Open database connection & get cursor
conn = mysql.connector.connect(
  host=host, 
  port=port, 
  user=user, 
  password=password,
  database=db
  )
cursor = conn.cursor()

#Create database if neccessary
cursor.execute("CREATE DATABASE IF NOT EXISTS task_database;")
cursor.execute("USE task_database;")

#Create table if neccessary
cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
id INT PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(50) NOT NULL,
ingredients VARCHAR(255) NOT NULL,
cooking_time INT NOT NULL,
difficulty VARCHAR(20)
);
''')

#Run main menu for app
main_menu(conn, cursor)

#Close database connection
conn.close()
