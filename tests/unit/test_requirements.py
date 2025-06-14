#!/usr/bin/env python3
"""
Test script to verify all required dependencies are available
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

def test_core_dependencies():
    """Test that core dependencies are available"""
    print("Testing core dependencies...")
    
    try:
        import tkinter
        print("✓ tkinter available")
    except ImportError as e:
        print(f"✗ tkinter not available: {e}")
        return False
    
    try:
        import pygments
        print(f"✓ pygments available (version: {pygments.__version__})")
    except ImportError as e:
        print(f"✗ pygments not available: {e}")
        return False
    
    return True

def test_pygments_features():
    """Test specific Pygments features we use"""
    print("\nTesting Pygments features...")
    
    try:
        from pygments.lexers import PythonLexer
        from pygments.token import Token
        print("✓ Pygments lexers and tokens available")
    except ImportError as e:
        print(f"✗ Pygments features not available: {e}")
        return False
    
    # Test tokenization
    try:
        lexer = PythonLexer()
        tokens = list(lexer.get_tokens("def hello(): pass"))
        print(f"✓ Python tokenization working ({len(tokens)} tokens)")
    except Exception as e:
        print(f"✗ Python tokenization failed: {e}")
        return False
    
    return True

def test_copywork_modules():
    """Test that CoPywork modules can be imported"""
    print("\nTesting CoPywork modules...")
    
    try:
        from copywork.theme_loader import ThemeLoader
        print("✓ theme_loader module available")
    except ImportError as e:
        print(f"✗ theme_loader not available: {e}")
        return False
    
    try:
        from copywork.syntax_highlighter import SyntaxHighlighter
        print("✓ syntax_highlighter module available")
    except ImportError as e:
        print(f"✗ syntax_highlighter not available: {e}")
        return False
    
    return True

def test_theme_loading():
    """Test that theme loading works"""
    print("\nTesting theme loading...")
    
    try:
        from copywork.theme_loader import ThemeLoader
        theme = ThemeLoader()
        
        # Test basic theme functionality
        keyword_color = theme.get_foreground_color("keyword")
        print(f"✓ Theme loading working (keyword color: {keyword_color})")
        return True
    except Exception as e:
        print(f"✗ Theme loading failed: {e}")
        return False

def main():
    """Run all dependency tests"""
    print("CoPywork Dependency Test")
    print("=" * 30)
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print()
    
    tests = [
        ("Core Dependencies", test_core_dependencies),
        ("Pygments Features", test_pygments_features),
        ("CoPywork Modules", test_copywork_modules),
        ("Theme Loading", test_theme_loading),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if test_func():
            passed += 1
        print()
    
    print("=" * 30)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All dependencies are working correctly!")
        print("\nYou can now run CoPywork:")
        print("  python coPywork.py")
        print("  python coPywork.py demo_practice_mode.py")
        return 0
    else:
        print("❌ Some dependencies are missing or not working!")
        print("\nTo fix issues:")
        print("  pip install -r requirements.txt")
        print("  # On Ubuntu/Debian: sudo apt-get install python3-tk")
        print("  # On macOS: brew install python-tk")
        return 1

if __name__ == "__main__":
    sys.exit(main())
