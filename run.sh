#!/bin/bash

# Change to the project directory
cd "$(dirname "$0")"

# Print Python and pip versions
echo "Python version:"
python3 --version

echo "Pip version:"
python3 -m pip --version

# Activate the virtual environment
source venv/bin/activate

# Print Python path and installed packages
echo "Python executable:"
which python3

echo "Installed packages:"
pip list

# Run the application with verbose output
PYTHONPATH=. python3 -m src.main

# Deactivate the virtual environment
deactivate
