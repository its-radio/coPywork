#!/usr/bin/env python3
"""
Setup script for CoPywork - Typing Practice Tool with Syntax Highlighting
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="copywork",
    version="2.0.0",
    author="CoPywork Contributors",
    description="A typing practice tool with syntax highlighting for programmers",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/copywork",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Education",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Editors",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
            "isort>=5.10.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "copywork=copywork.coPywork:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["themes/*.json", "config/*"],
    },
    keywords="typing practice programming education syntax highlighting",
    project_urls={
        "Bug Reports": "https://github.com/your-username/copywork/issues",
        "Source": "https://github.com/your-username/copywork",
        "Documentation": "https://github.com/your-username/copywork/blob/main/README.md",
    },
)
