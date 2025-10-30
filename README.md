# 🍲🍝 Recipe Application 🥗🥞

## 🎯 Objective
Achievement 1 : Build a command line version of a recipe application using Python.

## 📋 User Goals
Users should be able to create and modify recipes with ingredients, cooking time, and a difficulty parameter that would be automatically calculated by the app. Users should also be able to search for recipes by their ingredients.

## ✅ Key Features
- Create and manage the user’s recipes on a locally hosted MySQL database.
- Option to search for recipes that contain a set of ingredients specified by the user.
- Automatically rate each recipe by their difficulty level.
- Display more details on each recipe if the user prompts it, such as the ingredients, cooking time and difficulty of the recipe.

## 🧩 Technical Requirements
- The app should handle any common exceptions or errors that may pop up either during user input, database access, for example, and display user-friendly error messages.
- The app must connect to a MySQL database hosted locally on your system.
- The app must provide an easy-to-use interface, supported by simple forms of input and concise instructions that any user can follow—always assume that they aren’t as technically proficient as you may be. For instance, if the program requires that the user picks an option from a list, instead of having them manually type in the option, list the options with numbers, and have them enter the number corresponding to their choice.
- The app should work on Python 3.6+ installations.
- App code must be well-formatted according to standardized guidelines
- App code should also be supported by concise, helpful comments that illustrate the flow of the program.

## 🛠 Setting Up the Command Line Application
1. You will need the following to begin setting up this application:
   - [Python](https://www.python.org/downloads/) 3.12 or later installed.
   - MySQL database and access. *If you would like to use another relational database, you will need to update the `create_engine()` arguments in `recipe_app.py` for the database type.*<br><br>
2. Copy `recipe_app.py` and `requirements.txt` from https://github.com/CincinnatiKid428/CF_Python/tree/main/Exercise1.7/ into your project folder.<br><br>
3. Create a virtual environment using Python:
   ```bash
    # Create a virtual environment
    python -m venv myenv
    
    # Activate it (Windows)
    myenv\Scripts\activate
    
    # Activate it (macOS/Linux)
    source myenv/bin/activate
    
    # Deactivate when done
    deactivate
   ```
   Or `pip install virtualenvwrapper` and use `mkvirtualenv myenv` to create the virtual environment.  If it does not automatically activate it, use `workon myenv` to activate it.
   Use `deactivate` to deactivate the virtual environment when finished.<br><br>
4. Install dependencies with `pip install -r requirements.txt`.<br><br>
5. Create a `.env` file in the project root containing the following values:
   ```
     MYSQL_HOST=hostname
     MYSQL_PORT=3306 #default
     MYSQL_USER=your_username
     MYSQL_PASS=your_password
     MYSQL_DB=database_name
   ```
   <br>
6. Run the application using `ipython recipe_app.py` (iPython will be installed as a dependency)
<hr>

## Achievement 1 - Exercise Goals

### Exercise 1.1: Intro to Python Programming
- ☑ Install Python on macOS, Windows, or Linux
- ☑ Create and manage virtual environments
- ☑ Use `pip` to install and manage packages

### Exercise 1.2: Data Types in Python
- ☑ Use data types and methods to execute Python commands that store recipes containing their own internal data
- ☑ Enter a number of these recipes into another linear data structure

### Exercise 1.3: Functions and Other Operations in Python
- ☑ Create your first script on a `.py` script file
- ☑ Build a script that uses `if-elif-else` statements, `for` loops, and functions to take recipes from the user then display them

### Exercise 1.4: 
- ☑ Create a Python script that takes recipes from the user and writes the data in a binary file
- ☑ Create another script that reads the binary file and lists out the available ingredients. The user chooses an ingredient and the script displays all recipes which contain it
- ☑ Use Python’s exception handling features to handle common errors

### Exercise 1.5: 
- ☑ Build a custom class for your recipes, which contains its own data attributes for name, ingredients, cooking time, and difficulty, as well as other custom methods to interact with this data

### Exercise 1.6: 
- ☑ Set up a MySQL database and connect your scripts to it (created locally in a container with Docker)
- ☑ Build an application that creates, reads, updates, and deletes recipes, as well as searching for
them by a single ingredient

### Exercise 1.7: 
- ☑ Use an Object Relational Mapper from SQLAlchemy to manage the contents of your database from your application
- ☑ Build a user-friendly menu for entering and searching recipes and ingredients
- ☑ Store recipe and ingredient data in a MySQL database
- ☑ Implement recipe search according to user-defined ingredients
- ☑ Implement a detailed display of the recipe selected by the user

