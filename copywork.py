#!/usr/bin/env python3
"""
CoPywork - Entry point script

This script provides a convenient way to run CoPywork from the project root.
It handles the import path and launches the main application.

Usage:
    python copywork.py [file_to_open]

Examples:
    python copywork.py                          # Start with empty editor
    python copywork.py examples/demo.py         # Open a Python file
    python copywork.py examples/demo.py.cw      # Open a CoPywork archive
"""

import sys
import os

# Get the real path of the script, resolving any symlinks
script_path = os.path.realpath(__file__)
script_dir = os.path.dirname(script_path)

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(script_dir, 'src'))

def main():
    """Main entry point"""
    try:
        from copywork.coPywork import main as app_main
        return app_main()
    except ImportError as e:
        print(f"Error importing CoPywork: {e}")
        print("Please ensure all dependencies are installed:")
        print("  pip install -r requirements.txt")
        print("\nOr install in development mode:")
        print("  pip install -e .")
        return 1
    except Exception as e:
        print(f"Error running CoPywork: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
