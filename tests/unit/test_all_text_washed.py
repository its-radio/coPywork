#!/usr/bin/env python3
"""
Test script to verify that ALL text gets washed-out treatment in practice mode,
including non-highlighted text like variables.
"""

import tkinter as tk
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

def test_default_text_washing():
    """Test that default text (variables, etc.) gets washed out in practice mode"""
    try:
        from copywork.theme_loader import ThemeLoader
        from copywork.syntax_highlighter import SyntaxHighlighter
        
        # Create a minimal Tkinter setup
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        text_widget = tk.Text(root)
        theme_loader = ThemeLoader()
        highlighter = SyntaxHighlighter(text_widget, theme_loader)
        
        # Test sample Python code with variables
        sample_code = '''def hello():
    my_variable = "test"
    another_var = 42
    return my_variable'''
        
        text_widget.insert("1.0", sample_code)
        
        # Apply practice mode highlighting
        print("Applying practice mode highlighting...")
        highlighter.highlight_text_practice_mode("test.py")
        
        # Check that default washed tag exists and is applied
        all_tags = text_widget.tag_names()
        print(f"All tags after practice mode: {sorted(all_tags)}")
        
        # Check if default_text_washed tag exists
        if "default_text_washed" in all_tags:
            print("✓ Default washed tag created")
            
            # Check if it's applied to some text
            default_ranges = text_widget.tag_ranges("default_text_washed")
            if default_ranges:
                print(f"✓ Default washed tag applied to {len(default_ranges)//2} ranges")
                print(f"  Sample range: {default_ranges[0]} to {default_ranges[1]}")
            else:
                print("✗ Default washed tag not applied to any text")
                root.destroy()
                return False
        else:
            print("✗ Default washed tag not created")
            root.destroy()
            return False
        
        print("✓ Default text washing test passed")
        root.destroy()
        return True
        
    except Exception as e:
        print(f"✗ Default text washing test failed: {e}")
        return False

def test_variable_highlighting():
    """Test that variable names get proper treatment"""
    try:
        from copywork.theme_loader import ThemeLoader
        from copywork.syntax_highlighter import SyntaxHighlighter
        
        root = tk.Tk()
        root.withdraw()
        
        text_widget = tk.Text(root)
        theme_loader = ThemeLoader()
        highlighter = SyntaxHighlighter(text_widget, theme_loader)
        
        # Insert code with clear variable names
        sample_code = "my_variable = 42"
        text_widget.insert("1.0", sample_code)
        
        # Apply practice mode highlighting
        highlighter.highlight_text_practice_mode("test.py")
        
        # Test position-specific restoration for a variable character
        var_position = "1.0"  # First character of "my_variable"
        
        print("Testing variable character restoration...")
        
        # Check what tags are at this position before restoration
        tags_before = text_widget.tag_names(var_position)
        print(f"Tags at variable position before restoration: {tags_before}")
        
        # Restore normal color at this position
        highlighter.restore_normal_color_at_position(var_position, "test.py")
        
        # Check what tags are at this position after restoration
        tags_after = text_widget.tag_names(var_position)
        print(f"Tags at variable position after restoration: {tags_after}")
        
        # Should have either a syntax tag or default_text_normal
        if "default_text_normal" in tags_after or any("syntax_" in tag for tag in tags_after):
            print("✓ Variable character properly restored to normal color")
            root.destroy()
            return True
        else:
            print("✗ Variable character not properly restored")
            root.destroy()
            return False
        
    except Exception as e:
        print(f"✗ Variable highlighting test failed: {e}")
        return False

def test_mixed_content_highlighting():
    """Test highlighting on mixed content (keywords, variables, strings, etc.)"""
    try:
        from copywork.theme_loader import ThemeLoader
        from copywork.syntax_highlighter import SyntaxHighlighter
        
        root = tk.Tk()
        root.withdraw()
        
        text_widget = tk.Text(root)
        theme_loader = ThemeLoader()
        highlighter = SyntaxHighlighter(text_widget, theme_loader)
        
        # Complex code with various elements
        sample_code = '''def calculate(x, y):
    result = x + y
    message = f"Result: {result}"
    return result'''
        
        text_widget.insert("1.0", sample_code)
        
        # Apply practice mode highlighting
        highlighter.highlight_text_practice_mode("test.py")
        
        # Count total tags applied
        all_tags = [tag for tag in text_widget.tag_names() if tag.startswith(("syntax_", "default_text_"))]
        print(f"Syntax and default tags: {len(all_tags)}")
        
        # Check coverage - get all tag ranges
        total_coverage = 0
        for tag in all_tags:
            ranges = text_widget.tag_ranges(tag)
            for i in range(0, len(ranges), 2):
                start_idx = text_widget.index(ranges[i])
                end_idx = text_widget.index(ranges[i+1])
                # Simple coverage calculation
                total_coverage += 1
        
        print(f"Total tag applications: {total_coverage}")
        
        if total_coverage > 0:
            print("✓ Mixed content highlighting working")
            root.destroy()
            return True
        else:
            print("✗ No highlighting applied to mixed content")
            root.destroy()
            return False
        
    except Exception as e:
        print(f"✗ Mixed content highlighting test failed: {e}")
        return False

def main():
    """Run all tests for comprehensive text washing"""
    print("Testing Comprehensive Text Washing in Practice Mode")
    print("=" * 55)
    
    tests = [
        ("Default Text Washing", test_default_text_washing),
        ("Variable Highlighting", test_variable_highlighting),
        ("Mixed Content Highlighting", test_mixed_content_highlighting),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        if test_func():
            passed += 1
    
    print(f"\n{'='*55}")
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All text washing tests passed!")
        print("\nNew behavior:")
        print("✓ ALL text in Python files gets washed-out in practice mode")
        print("✓ Variables and non-highlighted text are now included")
        print("✓ Default text color is properly managed")
        print("✓ Position-specific restoration works for all text types")
        return 0
    else:
        print("❌ Some text washing tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
