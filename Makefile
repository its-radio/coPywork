# CoPywork Development Makefile

.PHONY: help install install-dev test test-all clean format lint type-check run demo

# Default target
help:
	@echo "CoPywork Development Commands:"
	@echo ""
	@echo "Setup:"
	@echo "  install      Install production dependencies"
	@echo "  install-dev  Install development dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  test         Run basic tests"
	@echo "  test-all     Run all tests including practice mode"
	@echo ""
	@echo "Code Quality:"
	@echo "  format       Format code with black"
	@echo "  lint         Lint code with flake8"
	@echo "  type-check   Type check with mypy"
	@echo ""
	@echo "Running:"
	@echo "  run          Run CoPywork"
	@echo "  demo         Run CoPywork with demo file"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean        Clean up temporary files"

# Installation targets
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

# Testing targets
test:
	python run_tests.py

test-all:
	python run_tests.py

# Code quality targets
format:
	black src/ tests/ examples/ *.py

lint:
	flake8 src/ tests/ examples/ *.py

type-check:
	mypy src/ tests/ examples/ *.py

# Running targets
run:
	python copywork.py

demo:
	python copywork.py examples/demo_practice_mode.py

# Maintenance targets
clean:
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete

# Virtual environment setup
venv:
	python3 -m venv .venv
	@echo "Virtual environment created. Activate with:"
	@echo "source .venv/bin/activate  # Linux/macOS"
	@echo ".venv\\Scripts\\activate   # Windows"

# Complete setup from scratch
setup: venv
	@echo "Activate the virtual environment and run 'make install-dev'"

# Check if everything is working
check: test-all format lint type-check
	@echo "All checks passed!"

# Development workflow
dev: install-dev test-all
	@echo "Development environment ready!"
