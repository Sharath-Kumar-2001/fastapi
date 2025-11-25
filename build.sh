#!/bin/bash
set -e  # Exit on first error

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Installing frontend dependencies..."
cd frontend-router-concept
npm install

echo "Building frontend..."
npm run build

echo "Running database migrations..."
cd ..
alembic upgrade head

echo "Build completed successfully!"