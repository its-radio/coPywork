#!/usr/bin/env python3
"""
Demo script to show the backspace fix in practice mode

This script demonstrates that backspacing in practice mode now only affects
the specific character being deleted, not all typing progress.
"""

def fibonacci(n):
    """Generate Fibonacci sequence up to n terms"""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    sequence = [0, 1]
    for i in range(2, n):
        sequence.append(sequence[i-1] + sequence[i-2])
    
    return sequence

def main():
    """Main function to demonstrate various Python features"""
    print("=== Backspace Fix Demo ===")
    
    # Test the fibonacci function
    result = fibonacci(10)
    print(f"Fibonacci sequence: {result}")
    
    # Dictionary comprehension
    squares = {x: x**2 for x in range(1, 6)}
    print(f"Squares: {squares}")
    
    # List comprehension with condition
    evens = [x for x in range(20) if x % 2 == 0]
    print(f"Even numbers: {evens}")
    
    # String formatting
    name = "Python"
    version = 3.11
    message = f"Welcome to {name} {version}!"
    print(message)

if __name__ == "__main__":
    main()

# Instructions for testing the backspace fix:
# 
# 1. Run: python coPywork.py demo_backspace_fix.py
# 2. Press Ctrl+M to enter Practice mode
# 3. Start typing the first line: "def fibonacci(n):"
# 4. Type several characters correctly (they should turn from washed-out to normal colors)
# 5. Press backspace to delete the last character
# 6. Notice that:
#    - Only the last character returns to washed-out state
#    - All previously typed characters remain in their normal colors
#    - Your typing progress is preserved!
#
# Before the fix:
# - Backspacing would reset ALL text to washed-out state
# - All typing progress would be lost
#
# After the fix:
# - Only the specific character is affected
# - Typing progress is preserved
# - Much better user experience!
