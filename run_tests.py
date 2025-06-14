#!/usr/bin/env python3
"""
Test runner for CoPywork

This script runs all tests with proper import path setup.
"""

import os
import sys
import subprocess

# Add src to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

def run_test_file(test_file):
    """Run a single test file"""
    print(f"\n{'='*50}")
    print(f"Running {test_file}")
    print('='*50)
    
    try:
        # Set PYTHONPATH environment variable
        env = os.environ.copy()
        env['PYTHONPATH'] = src_path + ':' + env.get('PYTHONPATH', '')
        
        # Run the test file
        result = subprocess.run([
            sys.executable, test_file
        ], cwd=project_root, env=env, capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error running {test_file}: {e}")
        return False

def main():
    """Run all tests"""
    print("CoPywork Test Suite")
    print("=" * 50)
    
    # List of test files to run
    test_files = [
        'tests/unit/test_syntax_highlighting.py',
        'tests/unit/test_practice_mode_highlighting.py',
        'tests/unit/test_backspace_behavior.py',
        'tests/unit/test_all_text_washed.py',
        'tests/unit/test_requirements.py',
    ]
    
    passed = 0
    total = 0
    
    for test_file in test_files:
        if os.path.exists(test_file):
            total += 1
            if run_test_file(test_file):
                passed += 1
        else:
            print(f"Warning: Test file {test_file} not found")
    
    print(f"\n{'='*50}")
    print(f"Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
