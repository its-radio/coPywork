# CoPywork Installation Guide

## Quick Start

### Option 1: Using Virtual Environment (Recommended)

```bash
# Clone or navigate to the project directory
cd /path/to/copywork

# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
# On Linux/macOS:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run CoPywork
python coPywork.py
```

### Option 2: System-wide Installation

```bash
# Install dependencies system-wide
pip install pygments

# Run CoPywork
python coPywork.py
```

### Option 3: Development Setup

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python test_syntax_highlighting.py
python test_practice_mode_highlighting.py

# Run CoPywork
python coPywork.py
```

## System Requirements

### Python Version
- Python 3.8 or higher
- Tested with Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13

### Operating Systems
- Linux (Ubuntu, Debian, Fedora, etc.)
- macOS (10.14+)
- Windows (10+)

### Dependencies

#### Required
- `pygments>=2.10.0` - Syntax highlighting engine
- `tkinter` - GUI framework (usually included with Python)

#### Optional (Development)
- `pytest>=7.0.0` - Testing framework
- `black>=22.0.0` - Code formatting
- `flake8>=4.0.0` - Code linting
- `mypy>=0.950` - Type checking

## Platform-Specific Instructions

### Ubuntu/Debian
```bash
# Install tkinter if not available
sudo apt-get update
sudo apt-get install python3-tk python3-venv

# Follow standard installation
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### macOS
```bash
# Install Python with tkinter support (if using Homebrew)
brew install python-tk

# Follow standard installation
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Windows
```bash
# tkinter is usually included with Python on Windows
# Follow standard installation in Command Prompt or PowerShell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Troubleshooting

### Common Issues

#### 1. "No module named 'tkinter'"
**Solution:**
- **Ubuntu/Debian:** `sudo apt-get install python3-tk`
- **macOS:** `brew install python-tk`
- **Windows:** Reinstall Python with tkinter support

#### 2. "No module named 'pygments'"
**Solution:**
```bash
pip install pygments
```

#### 3. Virtual environment activation issues
**Solution:**
```bash
# Make sure you're in the project directory
cd /path/to/copywork

# Recreate the virtual environment
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### 4. Permission errors on Linux/macOS
**Solution:**
```bash
# Use virtual environment instead of system-wide installation
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Verification

Test your installation:
```bash
# Test basic functionality
python -c "import tkinter; import pygments; print('All dependencies available!')"

# Test CoPywork modules
python -c "from theme_loader import ThemeLoader; from syntax_highlighter import SyntaxHighlighter; print('CoPywork modules working!')"

# Run the application
python coPywork.py demo_practice_mode.py
```

## Development Environment

For contributors and developers:

```bash
# Clone the repository
git clone <repository-url>
cd copywork

# Set up development environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

# Run tests
python test_syntax_highlighting.py
python test_practice_mode_highlighting.py

# Format code
black *.py

# Lint code
flake8 *.py

# Type check
mypy *.py
```

## Docker (Optional)

For containerized deployment:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "coPywork.py"]
```

## Next Steps

After installation:
1. Read the [README.md](README.md) for basic usage
2. Check [SYNTAX_HIGHLIGHTING_README.md](SYNTAX_HIGHLIGHTING_README.md) for syntax highlighting features
3. Review [PRACTICE_MODE_FEATURES.md](PRACTICE_MODE_FEATURES.md) for practice mode details
4. Try the demo: `python coPywork.py demo_practice_mode.py`
