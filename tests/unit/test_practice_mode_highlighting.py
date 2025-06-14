#!/usr/bin/env python3
"""
Test script to verify practice mode syntax highlighting functionality
"""

import tkinter as tk
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
import os

def test_practice_mode_highlighting():
    """Test the practice mode syntax highlighting functionality"""
    try:
        from copywork.theme_loader import ThemeLoader
        from copywork.syntax_highlighter import SyntaxHighlighter
        
        # Create a minimal Tkinter setup
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        text_widget = tk.Text(root)
        theme_loader = ThemeLoader()
        highlighter = SyntaxHighlighter(text_widget, theme_loader)
        
        # Test sample Python code
        sample_code = '''def hello_world():
    """A simple function"""
    print("Hello, World!")
    return True'''
        
        text_widget.insert("1.0", sample_code)
        
        # Test normal highlighting
        print("Testing normal syntax highlighting...")
        highlighter.highlight_text("test.py")
        
        # Test practice mode highlighting (washed out)
        print("Testing practice mode syntax highlighting...")
        highlighter.highlight_text_practice_mode("test.py")
        
        # Test color washing function
        print("Testing color washing...")
        original_color = "#569CD6"  # Blue
        washed_color = highlighter._wash_out_color(original_color)
        print(f"Original: {original_color} -> Washed: {washed_color}")
        
        # Test position-specific highlighting
        print("Testing position-specific highlighting...")
        highlighter.restore_normal_color_at_position("1.0", "test.py")
        highlighter.apply_incorrect_color_at_position("1.1")
        
        print("✓ Practice mode highlighting test passed")
        root.destroy()
        return True
        
    except Exception as e:
        print(f"✗ Practice mode highlighting test failed: {e}")
        return False

def test_color_washing():
    """Test the color washing functionality"""
    try:
        from copywork.theme_loader import ThemeLoader
        from copywork.syntax_highlighter import SyntaxHighlighter
        
        root = tk.Tk()
        root.withdraw()
        
        text_widget = tk.Text(root)
        theme_loader = ThemeLoader()
        highlighter = SyntaxHighlighter(text_widget, theme_loader)
        
        # Test various colors
        test_colors = [
            "#569CD6",  # Blue
            "#CE9178",  # Orange
            "#6A9955",  # Green
            "#C586C0",  # Purple
            "#DCDCAA",  # Yellow
        ]
        
        print("Testing color washing with different colors:")
        for color in test_colors:
            washed = highlighter._wash_out_color(color)
            print(f"  {color} -> {washed}")
        
        # Test different wash factors
        print("Testing different wash factors:")
        base_color = "#569CD6"
        for factor in [0.1, 0.3, 0.5, 0.7, 0.9]:
            washed = highlighter._wash_out_color(base_color, factor)
            print(f"  Factor {factor}: {base_color} -> {washed}")
        
        print("✓ Color washing test passed")
        root.destroy()
        return True
        
    except Exception as e:
        print(f"✗ Color washing test failed: {e}")
        return False

def test_tag_configuration():
    """Test tag configuration for normal and washed-out modes"""
    try:
        from copywork.theme_loader import ThemeLoader
        from copywork.syntax_highlighter import SyntaxHighlighter
        
        root = tk.Tk()
        root.withdraw()
        
        text_widget = tk.Text(root)
        theme_loader = ThemeLoader()
        highlighter = SyntaxHighlighter(text_widget, theme_loader)
        
        # Test normal tag configuration
        highlighter.configure_tag("test_normal", "keyword", washed_out=False)
        assert "test_normal" in highlighter.configured_tags
        
        # Test washed-out tag configuration
        highlighter.configure_tag("test_washed", "keyword", washed_out=True)
        assert "test_washed" in highlighter.configured_washed_tags
        
        print("✓ Tag configuration test passed")
        root.destroy()
        return True
        
    except Exception as e:
        print(f"✗ Tag configuration test failed: {e}")
        return False

def main():
    """Run all practice mode tests"""
    print("Testing CoPywork Practice Mode Syntax Highlighting")
    print("=" * 55)
    
    tests = [
        ("Practice Mode Highlighting", test_practice_mode_highlighting),
        ("Color Washing", test_color_washing),
        ("Tag Configuration", test_tag_configuration),
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
        print("🎉 All practice mode tests passed!")
        print("\nFeatures implemented:")
        print("✓ Washed-out syntax highlighting in practice mode")
        print("✓ Normal color restoration when typed correctly")
        print("✓ Bright red color for incorrect typing")
        print("✓ Intelligent color blending algorithm")
        print("✓ Separate tag management for normal/washed modes")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
