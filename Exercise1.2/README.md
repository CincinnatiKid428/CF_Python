# Task 1.2

## `recipe_N` Structure
I chose a dictionary for the recipe structure due to its flexibility with key-value pairs to store information about the recipe. New pairs can be added (such as instructions) or existing pairs can be modified as needed due to the mutable property of the dictionary. Thinking ahead, ingredients is currently defined as a list but would be better suited as a dictionary as well so you can assign each ingredient a key-value pair for name, quantity, substitutions, etc.

## `all_recipes` Structure
I chose a list for the all_recipes structure because it again is a sequential, mutable structure allowing modifying elements, adding or removing elements, and the ability to sort the list. This will be useful if the user has options such as sorting by name of the recipe, or if the cooking time were restricted to an int in minutes they could sort by lowest cooking times to show the quickest recipes first by providing the `key=` parameter in the `sort()` function.