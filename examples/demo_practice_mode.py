#!/usr/bin/env python3
"""
Demo Python file to showcase practice mode syntax highlighting

This file demonstrates various Python syntax elements that will be
highlighted differently in edit mode vs practice mode.
"""

import os
import sys
from datetime import datetime
from typing import List, Dict, Optional

# Global constants
VERSION = "1.0.0"
DEBUG = True

class Calculator:
    """A simple calculator class to demonstrate syntax highlighting"""
    
    def __init__(self, precision: int = 2):
        self.precision = precision
        self.history: List[str] = []
    
    def add(self, a: float, b: float) -> float:
        """Add two numbers"""
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return round(result, self.precision)
    
    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers"""
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return round(result, self.precision)
    
    @property
    def last_operation(self) -> Optional[str]:
        """Get the last operation from history"""
        return self.history[-1] if self.history else None

def fibonacci(n: int) -> List[int]:
    """Generate Fibonacci sequence up to n terms"""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    sequence = [0, 1]
    for i in range(2, n):
        next_num = sequence[i-1] + sequence[i-2]
        sequence.append(next_num)
    
    return sequence

def process_data(data: Dict[str, any]) -> Dict[str, any]:
    """Process data with various operations"""
    result = {}
    
    # String operations
    if "name" in data:
        result["formatted_name"] = data["name"].upper().strip()
    
    # Number operations
    if "numbers" in data:
        numbers = data["numbers"]
        result["sum"] = sum(numbers)
        result["average"] = sum(numbers) / len(numbers) if numbers else 0
        result["max"] = max(numbers) if numbers else None
    
    # Boolean operations
    result["has_data"] = bool(data)
    result["is_valid"] = len(data) > 0 and "name" in data
    
    return result

# Main execution
if __name__ == "__main__":
    print("=== CoPywork Practice Mode Demo ===")
    
    # Create calculator instance
    calc = Calculator(precision=3)
    
    # Perform some calculations
    print(f"Addition: {calc.add(15.5, 23.7)}")
    print(f"Multiplication: {calc.multiply(4.2, 8.1)}")
    print(f"Last operation: {calc.last_operation}")
    
    # Generate Fibonacci sequence
    fib_sequence = fibonacci(10)
    print(f"Fibonacci (10 terms): {fib_sequence}")
    
    # Process sample data
    sample_data = {
        "name": "  Python Programming  ",
        "numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "active": True
    }
    
    processed = process_data(sample_data)
    print(f"Processed data: {processed}")
    
    # List comprehension example
    squares = [x**2 for x in range(1, 11) if x % 2 == 0]
    print(f"Even squares: {squares}")
    
    # Dictionary comprehension
    word_lengths = {word: len(word) for word in ["python", "syntax", "highlighting"]}
    print(f"Word lengths: {word_lengths}")
    
    # Exception handling
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        print(f"Error caught: {e}")
    finally:
        print("Demo completed successfully!")
    
    # Lambda function
    double = lambda x: x * 2
    print(f"Double of 21: {double(21)}")
    
    # F-string with expressions
    current_time = datetime.now()
    print(f"Current time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n--- Instructions ---")
    print("1. Open this file in CoPywork")
    print("2. Switch to Practice mode (Ctrl+M)")
    print("3. Notice how syntax highlighting becomes washed out")
    print("4. Start typing to see colors restore as you type correctly")
    print("5. Try typing incorrectly to see bright red highlighting")
