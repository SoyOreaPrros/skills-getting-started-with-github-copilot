#!/bin/bash
# Test runner script for the Mergington High School API

echo "Running FastAPI tests with pytest..."
echo "======================================="

# Run tests with coverage
python -m pytest tests/ --cov=src --cov-report=term-missing --cov-report=html -v

echo ""
echo "Test run complete!"
echo "HTML coverage report generated in htmlcov/ directory"