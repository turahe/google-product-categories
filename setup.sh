#!/bin/bash

echo "Google Product Categories Setup"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "Error: Python is not installed"
        echo "Please install Python 3.7+ from https://python.org"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "Using Python: $($PYTHON_CMD --version)"

# Install requirements
echo "Installing requirements..."
$PYTHON_CMD -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Warning: Failed to install requirements. Continuing anyway..."
fi

# Run setup
echo ""
echo "Running setup script..."
$PYTHON_CMD setup.py

if [ $? -eq 0 ]; then
    echo ""
    echo "Setup completed successfully!"
else
    echo ""
    echo "Setup failed with exit code: $?"
    exit 1
fi

echo ""
echo "Press Enter to exit"
read
