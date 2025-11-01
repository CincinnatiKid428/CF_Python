

class ShoppingList(object):
    def __init__(self, list_name):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
        self.list_name = list_name
        self.shopping_list = []

    def add_item(self, item):
        if not item in self.shopping_list:
            self.shopping_list.append(item)
            print(f" + Added {item}")

    def remove_item(self, item):
        if item in self.shopping_list:
            self.shopping_list.remove(item)
            print(f" - Removed {item}")

    def view_list(self):
        print(f"\n--------------------\nCurrent {self.list_name}:")
        for item in self.shopping_list:
            print(f"  {item}")

# ---Main--------------------

# Testing class with instance below:
pet_store_list = ShoppingList("Pet Store Shopping List")

# Add items
pet_store_list.add_item("dog food")
pet_store_list.add_item("frisbee")
pet_store_list.add_item("dog bowl")
pet_store_list.add_item("collars")
pet_store_list.add_item("flea collars")

# Remove item
pet_store_list.remove_item("flea collars")

# View list
pet_store_list.view_list()