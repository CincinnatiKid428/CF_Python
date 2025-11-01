#File: recipe_app.py

# This is a command line recipe application that can store, recall and manage
# recipes in a MySQL database.

import os
import textwrap
from dotenv import load_dotenv
from datetime import datetime, timezone #For formatting date timestamps

#SQLAlchemy Imports
from sqlalchemy import create_engine, Column, select, update, bindparam
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.types import Integer, String, DateTime

#=====CLASSES========================================================

#Create Base class for a recipe
Base = declarative_base()
class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))
    last_update = Column(DateTime, default=lambda: datetime.now(timezone.utc)) #lambda suggested by ChatGPT

    #Assigns difficulty rating based on cooking time & number of ingredients.
    def calculate_difficulty(self):

        ingredient_count = len(self.ingredients.split(","))
        cooking_time = int(self.cooking_time)

        if cooking_time < 10 and ingredient_count < 4:
            self.difficulty = 'Easy'
        elif cooking_time < 10 and ingredient_count >= 4:
            self.difficulty = 'Medium'
        elif cooking_time >= 10 and ingredient_count < 4:
            self.difficulty = 'Intermediate'
        elif cooking_time >= 10 and ingredient_count >= 4:
            self.difficulty = 'Hard'
        else:
            self.difficulty = 'Undetermined'

    #Returns ingredients as list, or emtpy list if no ingredients
    def return_ingredients_as_list(self):
        if len(self.ingredients) == 0:
            return []
        else:
            return self.ingredients.split(",")

    def __repr__(self):
        return f"<Recipe ID: {str(self.id)} Name: {self.name} Difficulty: {self.difficulty}>"

    def __str__(self):
        recipe_lines = []
        date_str = self.last_update.strftime("%m/%d/%Y %H:%M UTC") if self.last_update else "Unknown"

        recipe_lines.append(f"🍴 {self.name}\t(Last updated {date_str})")
        recipe_lines.append(f"   🕑 Cooking Time (mins): {self.cooking_time}")
        recipe_lines.append(f"   🍳 Difficulty Level: {self.difficulty}")
        recipe_lines.append(f"   🥕 Ingredients:")

        for line in textwrap.wrap(self.ingredients, width=60):
            recipe_lines.append(f'\t{line}')
        recipe_lines.append("\n")

        return "\n".join(recipe_lines)

#=====[FUNCTIONS]======================================================

#Takes recipe name input, validates input and returns name.
def input_recipe_name(menu_marker):

    name = ''
    while True:
        name = str(input(f"{menu_marker} Enter the name of the recipe: "))
        cleaned_name = name.replace(" ","").replace("-","").replace("'","")
        #Validate name input
        if name == '':
            print(" ❌ Recipe names cannot be empty.")
        elif not cleaned_name.isalpha():
            print(" ❌ Recipe names can only contain letters, hypens or aphostrophes.")
        elif len(name) > 50:
            print(" ❌ Recipe names can be no longer than 50 characters.")
        else:
            name = name.title()
            return name
    

#Takes recipe cooking time input, validates and returns it.
def input_recipe_cooking_time(menu_marker):

    cooking_time = 'a'
    while True:
        cooking_time = input(f'{menu_marker} Enter the cooking time in minutes: ')
        #Validate cooking time input is only digits
        if not cooking_time.isdigit():  #isdigit() is more strict than isnumeric() 
            print(" ❌ Please enter a valid number of minutes (digits only).")
            continue
        else:
            return int(cooking_time)


#Takes recipe ingredients input and returns them in a list.
def input_recipe_ingredients(menu_marker):

    ingredients = []
    char_count = 0
    #Loop to get all ingredients
    print(f'{menu_marker} Enter an ingredient or "Done" to finish: ')
    while True:
        ingredient = str(input('\t- '))
        cleaned_ingredient = ingredient.replace(" ","").replace("-","").replace("'","")
        
        #Validate ingredient name
        if ingredient == "":
            print(" ❌ Ingredients cannot be blank.")

        elif not cleaned_ingredient.isalpha():
            print(" ❌ Ingredients can only contain letters, spaces, hypens or aphostrophes.")
        
        elif ingredient.lower() != "done":

            if char_count == 0:
                char_count += len(ingredient)
            else:
                char_count += 2 + len(ingredient) #Account for join() with ", " separator between
            
            #Check if there is room to add this ingredient
            if char_count < 256:
                #print(f'(char count : {char_count})')
                ingredients.append(ingredient.title())
            else:
                print(' ❌ Max character count for ingredients reached.')
                char_count -= len(ingredient) + 2 #Remove last ingredient & separator ", "
                remaining_chars = 255 - char_count - 2
                print(f' ❌ You may use {remaining_chars} more charaters or enter "Done" to finish.')
        elif len(ingredients) < 1:
            print(" ❌ Please enter at least 1 ingredient.")
        else: 
            #Exit loop, input must be 'done' and >0 ingredient
            ingredients.sort() 
            return ingredients


#SELECTS recipe with primary key "id" and prints it.
def verify_recipe_by_id(session, id):
    recipe = session.get(Recipe, id)
    print(f"\n{recipe}")


#Prints a recipe without the difficulty rating or timestamp, used in edit_recipe().
def print_recipe_no_diff_timestamp(name, cooking_time, ingredients):
    recipe_lines = []

    recipe_lines.append(f"\n\n🍴 {name}")
    recipe_lines.append(f"   🕑 Cooking Time (mins): {cooking_time}")
    recipe_lines.append(f"   🥕 Ingredients:")

    for line in textwrap.wrap(ingredients, width=60):
        recipe_lines.append(f'\t{line}')

    print("\n".join(recipe_lines))


#Creates new recipe and adds it to database.
def create_recipe(session):
    print("\n🟩 🟩 🟩 🟩 🟩 Create Recipe 🟩 🟩 🟩 🟩 🟩\n")

    #Get all the user inputs for a recipe
    name = input_recipe_name('🟩').title()     
    cooking_time = input_recipe_cooking_time('🟩')   
    ingredients = input_recipe_ingredients('🟩')

    #Create recipe object
    new_recipe = Recipe(
      name = name,
      cooking_time = cooking_time,
      ingredients = ", ".join(ingredients)
    )
    new_recipe.calculate_difficulty()

    #Insert new recipe into DB
    session.add(new_recipe)
    session.commit()

    print(f"\n\t✅ Successfully added recipe:\n\n{str(new_recipe)}")


#Prints a list of all stored recipes.
def view_all_recipes(session):
    print("\n🟪 🟪 🟪 🟪 🟪  All Recipes  🟪 🟪 🟪 🟪 🟪\n")

    #Get all recipes from database
    all_recipes = session.execute(select(Recipe)).scalars().all()

    if len(all_recipes) == 0:
        print("\n🟪 There are currently no stored recipes.\n")
    else:
        for r in all_recipes:
            print(f"{r}")


#Prints recipes containing user-selected ingredients.
def search_by_ingredients(session):
    print("\n🟦 🟦 🟦 🟦 🟦 Search by Ingredients 🟦 🟦 🟦 🟦 🟦\n")

    all_ingredients = []
    search_ingredients = []

    #Get all ingredients from database
    results = ", ".join(session.execute(select(Recipe.ingredients)).scalars().all() )
    results_list = results.split(", ")
    
    for i in results_list:
        if not i in all_ingredients:
            all_ingredients.append(i)
    all_ingredients.sort()

    #Print list of ingredients with indices (start at 1 for user-friendly numbering)
    index = 1
    for i in all_ingredients:
        print(f'\t{index}. {i}')
        index += 1

    #User chooses ingredients
    while True:
        choice = str(input('\n🟦 Choose ingredients by number separated by spaces,\n   or enter "Back" for the Main Menu: '))

        #Validate input
        choice_cleaned = choice.replace(" ", "")
        if choice == "":
            print("❌ Choice cannot be blank.\n")
        elif choice.lower() == 'back':
            break
        elif not choice_cleaned.isdigit():
            print(f" ❌ Invalid characters entered '{choice}', use digits/spaces only).\n")
        else:
            choice_list = choice.split(" ")

            #Get actual ingredient names
            for i in choice_list:
                search_ingredients.append(all_ingredients[int(i)-1]) #Subtract 1 for proper index

            #Build condition list
            conditions = []
            for like_term in search_ingredients:
                conditions.append(Recipe.ingredients.like(f'%{like_term}%'))

            #Search for recipes with condition list
            results = session.execute(select(Recipe).filter(*conditions)).scalars().all()
            print(f'\n🟦 Found {len(results)} recipe(s) with {", ".join(search_ingredients)}:\n')
            for r in results:
                print(str(r))
            break


#Updates a recipe selected by the user.
def edit_recipe(session):
    print("\n🟨 🟨 🟨 🟨 🟨 Edit a Recipe 🟨 🟨 🟨 🟨 🟨\n")

    #Get all recipe id & name values from database
    results = session.execute(select(Recipe.id, Recipe.name, Recipe.cooking_time, Recipe.ingredients)).all()
    valid_ids = []
    recipe_to_edit = None
    edit_option = ""

    if len(results) == 0:
        print("\n🟨 There are currently no stored recipes.\n")
        return None
    else:
        for r in results:
            print(f"\t{r.id}. {r.name}")
            valid_ids.append(r.id)
        print()

        #User selects a recipe
        while True:
            choice = str(input('🟨 Choose a recipe to edit by number or\n    enter "Back" to return to the Main Menu: '))

            #Validate choice
            if choice.lower() == 'back':
                return None
            elif choice == "":
                print(f" ❌ Choice cannot be blank.\n")
                continue
            elif not choice.isdigit():
                print(f" ❌ Invalid choice : {choice}\n")
                continue
            elif int(choice) not in valid_ids:
                print(f" ❌ Invalid choice : {choice}\n")
                continue
            else:
                break #We have good input

        #Display chosen recipe's name, cooking time and ingredients
        for recipe in results:
            if recipe.id == int(choice):
                recipe_to_edit = recipe
        print_recipe_no_diff_timestamp(recipe_to_edit.name, recipe_to_edit.cooking_time, recipe_to_edit.ingredients)
        
        #User selects what part to edit
        while True:
            print("\n🟨 Recipe Edit Options:\n\t1. Change name\n\t2. Change cooking time\n\t3. Change ingredients\n")
            edit_option = str(input('🟨 Choose an option above or enter "Back"\n    to return to the Main Menu: '))
            
            #Validate edit_option
            if edit_option.lower() == 'back':
                return None
            elif edit_option == "":
                print(f" ❌ Choice cannot be blank.\n")
                continue
            elif not edit_option.isdigit():
                print(f" ❌ Invalid input, must be a digit : {edit_option}\n")
                continue
            elif edit_option not in ['1','2','3']:
                print(f" ❌ Invalid choice : {edit_option}\n")
                continue
            else: 
                break #We have good input

        #Get new values & build update statement
        update_stmt = ""
        new_value = ""

        if edit_option == '1':
            new_value = input_recipe_name('🟨')
            update_stmt = update(Recipe).where(Recipe.id == recipe_to_edit.id).values(name=bindparam("new_value"), last_update=datetime.now(timezone.utc))

        elif edit_option == '2':
            new_value = input_recipe_cooking_time('🟨')
            update_stmt = update(Recipe).where(Recipe.id == recipe_to_edit.id).values(cooking_time=bindparam("new_value"), last_update=datetime.now(timezone.utc))

        else:
            new_value = ", ".join(input_recipe_ingredients('🟨'))
            update_stmt = update(Recipe).where(Recipe.id == recipe_to_edit.id).values(ingredients=bindparam("new_value"), last_update=datetime.now(timezone.utc))

        #Execute update
        session.execute(update_stmt, {"new_value":new_value})
        session.commit()

        #Get updated record to verify changes
        verify_recipe_by_id(session, recipe_to_edit.id)
        print(f"\t✅ Updated!\n")
        

#Deletes a recipe selected by the user.
def delete_recipe(session):
    print("\n🟥 🟥 🟥 🟥 🟥 Delete Recipe 🟥 🟥 🟥 🟥 🟥\n")

    #Get all recipes from database
    all_recipes = session.execute(select(Recipe.id, Recipe.name)).all()

    valid_ids = []

    for r in all_recipes:
        print(f"\t{r.id}.  {r.name}")
        valid_ids.append(str(r.id))
    print()
    
    while True:
        choice = str(input("🟥 Enter the number of the recipe to delete\n  or 'Back' to return to the Main Menu: "))
        #Validate choice
        if choice.lower() == 'back':
            break
        elif choice == "":
            print(f" ❌ Choice cannot be blank.\n")
        elif choice not in valid_ids:
            print(f" ❌ Invalid choice : {choice}\n")
        else:
            delete_recipe = session.execute(select(Recipe).filter(Recipe.id == int(choice))).scalar_one()
            session.delete(delete_recipe)
            session.commit()
            print(f"\n\t✅ Deleted {delete_recipe.name}\n")
            break


#Presents main menu and handles errors.
def main_menu(session):

    while True:
        print("\n🟧 🟧 🟧 🟧 🟧  Main  Menu  🟧 🟧 🟧 🟧 🟧\n")
        print("Choose From the Following:")
        print("\t1. Create a New Recipe")
        print("\t2. View All Recipes")
        print("\t3. Search for Recipes by Ingredient")
        print("\t4. Update an Existing Recipe")
        print("\t5. Delete a Recipe")
        print("\tType 'Quit' to Exit\n")
        choice = str(input("🟧 Enter 1-5 or 'Quit': "))

        try:
            if choice == '1':
                create_recipe(session)
            elif choice == '2':
                view_all_recipes(session)
            elif choice == '3':
                search_by_ingredients(session)
            elif choice == '4':
                edit_recipe(session)
            elif choice == '5':
                delete_recipe(session)
            elif choice.lower() == 'quit': #Exit loop condition
                break
            else:
                print(f" ❌ Invalid selection {choice}")

        except Exception as e:
            print(f"\n\t❌ Error with database operation: {e}")
           
#=====[MAIN]===========================================================

#Load .env file settings
load_dotenv()

host = os.getenv("MYSQL_HOST")
port = int(os.getenv("MYSQL_PORT",3306))
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASS")
db = os.getenv("MYSQL_DB")

#Create SQL Alchemy engine & test conenction
database_ok = False
engine = create_engine(f"mysql://{user}:{password}@{host}:{port}/{db}")
try:
    engine.connect().close()
    database_ok = True
except Exception as e:
    print("\n\n  ❌ Error connecting to database:")
    print(e)

if database_ok:
    #Create Session class bound to engine, and Session instance
    Session = sessionmaker(bind=engine)
    session = Session()

    #Create the table with ORM
    Base.metadata.create_all(engine)

    #Start Main Menu
    main_menu(session)

    #Cleanup connection after quitting Main Menu
    session.close()
else:
    print("\n  ⚠️ Exiting application")