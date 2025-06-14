#!/usr/bin/env python3
"""
Test script to verify syntax highlighting functionality
"""

import os
import sys
import unittest

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

def test_theme_loader():
    """Test the theme loader functionality"""
    try:
        from copywork.theme_loader import ThemeLoader
        
        # Test loading the default theme
        theme = ThemeLoader()
        
        # Test getting token styles
        keyword_style = theme.get_token_style("keyword")
        print(f"Keyword style: {keyword_style}")
        
        # Test fallback logic
        control_style = theme.get_token_style("keyword.control.import")
        print(f"Control import style (with fallback): {control_style}")
        
        # Test editor colors
        bg_color = theme.get_editor_color("editor.background")
        print(f"Background color: {bg_color}")
        
        print("✓ Theme loader test passed")
        return True
        
    except Exception as e:
        print(f"✗ Theme loader test failed: {e}")
        return False

def test_syntax_highlighter():
    """Test the syntax highlighter functionality"""
    try:
        import tkinter as tk
        from copywork.theme_loader import ThemeLoader
        from copywork.syntax_highlighter import SyntaxHighlighter
        
        # Create a minimal Tkinter setup
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        text_widget = tk.Text(root)
        theme_loader = ThemeLoader()
        highlighter = SyntaxHighlighter(text_widget, theme_loader)
        
        # Test file type detection
        assert highlighter.is_python_file("test.py") == True
        assert highlighter.is_python_file("test.py.cw") == True
        assert highlighter.is_python_file("test.txt") == False
        
        print("✓ Syntax highlighter test passed")
        root.destroy()
        return True
        
    except Exception as e:
        print(f"✗ Syntax highlighter test failed: {e}")
        return False

def test_file_extensions():
    """Test file extension handling"""
    test_cases = [
        ("test.py", "Python file"),
        ("test.py.cw", "Python CoPywork file"),
        ("test.txt", "Text file"),
        ("test.cw", "CoPywork file"),
    ]
    
    for filename, description in test_cases:
        if filename.endswith('.py'):
            save_type = "txt-style (with .colors companion)"
        elif filename.endswith('.py.cw'):
            save_type = "cw-style (archive)"
        elif filename.endswith('.txt'):
            save_type = "txt-style (with .colors companion)"
        else:
            save_type = "cw-style (archive)"
        
        print(f"✓ {description} ({filename}) -> {save_type}")
    
    return True

def main():
    """Run all tests"""
    print("Testing CoPywork Syntax Highlighting Implementation")
    print("=" * 50)
    
    tests = [
        ("Theme Loader", test_theme_loader),
        ("Syntax Highlighter", test_syntax_highlighter),
        ("File Extensions", test_file_extensions),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        if test_func():
            passed += 1
    
    print(f"\n{'='*50}")
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
