#!/bin/bash

# Exit on error
set -e

echo "Starting deployment process..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please update .env with your configuration values"
    exit 1
fi

# Build and start containers
echo "Building and starting containers..."
docker-compose up -d --build

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 10

# Run tests
echo "Running tests..."
docker-compose exec api pytest

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "Tests passed successfully"
else
    echo "Tests failed. Stopping deployment..."
    docker-compose down
    exit 1
fi

echo "Deployment completed successfully!"
echo "API is available at http://localhost:8000"
echo "API documentation is available at http://localhost:8000/docs" 