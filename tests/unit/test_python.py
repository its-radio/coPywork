#!/usr/bin/env python3
"""
A sample Python file to test syntax highlighting
"""

import os
import sys
from datetime import datetime

# This is a comment
def hello_world(name: str = "World") -> str:
    """
    A simple function that returns a greeting
    """
    if name:
        return f"Hello, {name}!"
    else:
        return "Hello, World!"

class Calculator:
    """A simple calculator class"""
    
    def __init__(self):
        self.result = 0
    
    def add(self, x: float, y: float) -> float:
        """Add two numbers"""
        self.result = x + y
        return self.result
    
    def multiply(self, x: float, y: float) -> float:
        """Multiply two numbers"""
        self.result = x * y
        return self.result

# Main execution
if __name__ == "__main__":
    calc = Calculator()
    print(hello_world("Python"))
    print(f"2 + 3 = {calc.add(2, 3)}")
    print(f"4 * 5 = {calc.multiply(4, 5)}")
    
    # List comprehension example
    numbers = [1, 2, 3, 4, 5]
    squares = [x**2 for x in numbers if x % 2 == 0]
    print(f"Even squares: {squares}")
