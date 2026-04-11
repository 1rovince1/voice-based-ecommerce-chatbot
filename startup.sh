#!/bin/bash
# Stop execution if process_data_files.py fails
set -e

echo "Processing data files..."
python process_data_files.py

echo "Starting FastAPI backend..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload