import pickle

recipe = {
  'name':'Tea',
  'ingredients':['Tea leaves','Water','Sugar'],
  'cooking_time':5,
  'difficulty':'Easy'
}

#Open file, write with pickle.dump(), close file
recipe_file = open('recipe_binary.bin','wb')
pickle.dump(recipe, recipe_file)
recipe_file.close()

#Open file again with read access, pickle.load(), close file
recipe_file = open('recipe_binary.bin','rb')
loaded_recipe = pickle.load(recipe_file)
recipe_file.close()

print("Recipe loaded from pickle:")
print(f"Name: {loaded_recipe['name']}")
print("Ingredients:")
for ingredient in loaded_recipe['ingredients']:
    print(f" - {ingredient}")
print(f"Cooking Time: {loaded_recipe['cooking_time']}")
print(f"Difficulty: {loaded_recipe['difficulty']}")