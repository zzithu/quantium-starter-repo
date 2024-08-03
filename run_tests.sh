#!/bin/bash

# Run ./dashvisualizer.py
./dashvisualizer.py
if [ $? -ne 0 ]; then
    echo "Error running ./dashvisualizer.py"
    exit $?
fi

# Run pytest
python -m pytest
pytest_code=$?

# Check if tests passed and exit with the appropriate code
if [ $pytest_code -eq 0 ]; then
    echo "Tests passed successfully."
else
    echo "Tests failed with exit code: $pytest_code"
fi

exit $pytest_code
