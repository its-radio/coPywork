"""
CoPywork - A typing practice tool with syntax highlighting for programmers

CoPywork is an advanced typing practice application designed specifically for
programmers. It features VSCode-style syntax highlighting, practice mode with
progressive color restoration, and comprehensive typing statistics.

Key Features:
- Edit and Practice modes
- VSCode-compatible JSON themes
- Python syntax highlighting with Pygments
- Washed-out text in practice mode that restores as you type correctly
- Real-time WPM tracking and accuracy statistics
- Support for multiple file formats (.txt, .cw, .py, .py.cw)

Example usage:
    import copywork
    copywork.main()

Or run directly:
    python -m copywork.coPywork
"""

__version__ = "2.0.0"
__author__ = "CoPywork Contributors"
__email__ = "copywork@example.com"
__license__ = "MIT"

# Import main components for easy access
try:
    from .theme_loader import ThemeLoader
    from .syntax_highlighter import SyntaxHighlighter
    __all__ = ['ThemeLoader', 'SyntaxHighlighter']
except ImportError:
    # Handle case where dependencies aren't installed
    __all__ = []

def main():
    """Entry point for the application"""
    try:
        from .coPywork import main as app_main
        app_main()
    except ImportError as e:
        print(f"Error importing CoPywork: {e}")
        print("Please ensure all dependencies are installed: pip install -r requirements.txt")
        return 1
    return 0

if __name__ == "__main__":
    main()
