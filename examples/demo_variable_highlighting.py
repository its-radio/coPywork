#!/usr/bin/env python3
"""
Demo file to showcase variable highlighting in practice mode

This file demonstrates that ALL text now gets the washed-out treatment
in practice mode, including variable names and other non-highlighted text.
"""

# Variables with different naming styles
user_name = "Alice"
userAge = 25
MAX_ATTEMPTS = 3
_private_var = "secret"

# Function with parameters and local variables
def calculate_total(price, tax_rate, discount):
    """Calculate total price with tax and discount"""
    
    # Local variables
    tax_amount = price * tax_rate
    discounted_price = price - discount
    final_total = discounted_price + tax_amount
    
    # Variable in f-string
    result_message = f"Total: ${final_total:.2f}"
    
    return final_total

# Class with instance variables
class ShoppingCart:
    def __init__(self):
        self.items = []
        self.total_cost = 0.0
        self.item_count = 0
    
    def add_item(self, item_name, item_price):
        """Add an item to the cart"""
        new_item = {
            "name": item_name,
            "price": item_price,
            "quantity": 1
        }
        
        self.items.append(new_item)
        self.total_cost += item_price
        self.item_count += 1
        
        print(f"Added {item_name} for ${item_price}")

# Dictionary and list with variable names
product_catalog = {
    "laptop": 999.99,
    "mouse": 29.99,
    "keyboard": 79.99
}

shopping_list = ["laptop", "mouse"]

# Loop with iterator variables
for product_name in shopping_list:
    if product_name in product_catalog:
        product_price = product_catalog[product_name]
        print(f"{product_name}: ${product_price}")

# List comprehension with variables
expensive_items = [item for item, price in product_catalog.items() if price > 50]

# Lambda with parameter variables
calculate_discount = lambda original_price, discount_percent: original_price * (1 - discount_percent / 100)

# Exception handling with variable
try:
    result = calculate_total(100, 0.08, 10)
    print(f"Calculation result: {result}")
except Exception as error:
    print(f"Error occurred: {error}")

# Instructions for testing:
# 
# 1. Run: python coPywork.py demo_variable_highlighting.py
# 2. Press Ctrl+M to enter Practice mode
# 3. Notice that ALL text is now washed out, including:
#    - Variable names (user_name, userAge, price, tax_rate, etc.)
#    - Parameter names in function definitions
#    - Local variable names
#    - Instance variable names (self.items, self.total_cost)
#    - Dictionary keys and values when they're variables
#    - Loop iterator variables (product_name, item, price)
#    - Exception variable names (error)
# 
# 4. Start typing and watch ALL text restore to normal colors when typed correctly
# 
# Before this fix:
# - Only syntax-highlighted elements (keywords, strings, numbers) were washed out
# - Variable names kept their normal color, making them stand out
# - Inconsistent visual experience
# 
# After this fix:
# - ALL text gets washed-out treatment in practice mode
# - Consistent visual experience across all text types
# - Better focus on what you're currently typing
# - More immersive practice experience
