# CoPywork Project Structure

This document describes the organization of the CoPywork project.

## Directory Structure

```
copywork/
├── src/copywork/              # Main source code
│   ├── __init__.py           # Package initialization
│   ├── coPywork.py           # Main application
│   ├── syntax_highlighter.py # Syntax highlighting engine
│   └── theme_loader.py       # VSCode theme parser
├── tests/                    # Test suite
│   ├── __init__.py          # Test package init
│   ├── unit/                # Unit tests
│   │   ├── __init__.py
│   │   ├── test_syntax_highlighting.py
│   │   ├── test_practice_mode_highlighting.py
│   │   ├── test_backspace_behavior.py
│   │   ├── test_all_text_washed.py
│   │   └── test_requirements.py
│   ├── integration/         # Integration tests
│   └── data/               # Test data files
│       ├── *.txt           # Sample text files
│       ├── *.cw            # Sample CoPywork files
│       └── *.json          # Test configuration files
├── examples/               # Example files and demos
│   ├── demo_practice_mode.py
│   ├── demo_backspace_fix.py
│   └── demo_variable_highlighting.py
├── docs/                   # Documentation
│   ├── INSTALL.md          # Installation guide
│   ├── SYNTAX_HIGHLIGHTING_README.md
│   ├── PRACTICE_MODE_FEATURES.md
│   └── PROJECT_STRUCTURE.md # This file
├── themes/                 # VSCode-style themes
│   └── my_theme.json       # Default theme
├── config/                 # Configuration files
├── copywork.py            # Main entry point script
├── run_tests.py           # Test runner
├── requirements.txt       # Production dependencies
├── requirements-dev.txt   # Development dependencies
├── setup.py              # Package setup
├── Makefile              # Development automation
└── README.md             # Main project documentation
```

## Core Components

### Source Code (`src/copywork/`)

- **`__init__.py`**: Package initialization and main entry point
- **`coPywork.py`**: Main application with GUI and core functionality
- **`syntax_highlighter.py`**: Pygments-based syntax highlighting engine
- **`theme_loader.py`**: VSCode JSON theme parser and manager

### Tests (`tests/`)

- **`unit/`**: Unit tests for individual components
- **`integration/`**: Integration tests for component interactions
- **`data/`**: Test data files and fixtures

### Examples (`examples/`)

- **`demo_practice_mode.py`**: Comprehensive practice mode demonstration
- **`demo_backspace_fix.py`**: Backspace behavior demonstration
- **`demo_variable_highlighting.py`**: Variable highlighting demonstration

### Documentation (`docs/`)

- **`INSTALL.md`**: Comprehensive installation guide
- **`SYNTAX_HIGHLIGHTING_README.md`**: Syntax highlighting features
- **`PRACTICE_MODE_FEATURES.md`**: Practice mode documentation
- **`PROJECT_STRUCTURE.md`**: This file

## Entry Points

### Development
```bash
# Direct script execution
python copywork.py [file]

# Package module execution
python -m copywork [file]

# Test runner
python run_tests.py

# Makefile targets
make run
make demo
make test
```

### Production
```bash
# After pip install
copywork [file]

# Or package execution
python -m copywork [file]
```

## Import Structure

The project uses relative imports within the package:

```python
# In src/copywork/coPywork.py
from .theme_loader import ThemeLoader
from .syntax_highlighter import SyntaxHighlighter

# In tests
import sys
sys.path.insert(0, 'src')
from copywork.theme_loader import ThemeLoader
```

## Development Workflow

1. **Setup**: `make venv && source .venv/bin/activate && make install-dev`
2. **Development**: Edit files in `src/copywork/`
3. **Testing**: `make test` or `python run_tests.py`
4. **Code Quality**: `make format lint type-check`
5. **Demo**: `make demo`

## File Types and Extensions

- **`.py`**: Python source files
- **`.cw`**: CoPywork archive files (ZIP format)
- **`.py.cw`**: Python CoPywork archive files
- **`.txt`**: Plain text files
- **`.json`**: VSCode theme files and configuration
- **`.md`**: Markdown documentation

## Configuration

- **`themes/`**: VSCode-style JSON theme files
- **`config/`**: Application configuration (future use)
- **`requirements*.txt`**: Python dependencies
- **`setup.py`**: Package configuration
- **`Makefile`**: Development automation

## Testing Strategy

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **Manual Testing**: Use demo files for manual verification
- **Automated Testing**: Run via `make test` or CI/CD

## Packaging

The project follows Python packaging best practices:

- Source code in `src/` directory
- Package structure with `__init__.py` files
- Entry points defined in `setup.py`
- Dependencies managed via `requirements.txt`
- Development dependencies in `requirements-dev.txt`

## Future Enhancements

Potential structural improvements:

- **`copywork/ui/`**: Separate UI components
- **`copywork/core/`**: Core business logic
- **`copywork/themes/`**: Theme management
- **`copywork/config/`**: Configuration management
- **`tests/e2e/`**: End-to-end tests
- **`docs/api/`**: API documentation
