#!/bin/bash

# Change to the project directory
cd "$(dirname "$0")"

# Activate the virtual environment
source venv/bin/activate

# Print diagnostic information
echo "Python executable: $(which python)"
echo "Python version: $(python --version)"
echo "Pip version: $(pip --version)"

# Install the package in editable mode
pip install -e .

# Run the test imports script
python test_imports.py

# Run the main application
python -m video_downloader.src.main

# Deactivate the virtual environment
deactivate
