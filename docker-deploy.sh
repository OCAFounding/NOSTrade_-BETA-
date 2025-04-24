#!/bin/bash

# Docker deployment script for NOS Trade

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}NOS Trade Docker Deployment${NC}"
echo "================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed.${NC}"
    echo "Please install Docker first: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Error: Docker Compose is not installed.${NC}"
    echo "Please install Docker Compose first: https://docs.docker.com/compose/install/"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}Warning: .env file not found.${NC}"
    echo "Creating .env file from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo -e "${GREEN}.env file created. Please edit it with your configuration.${NC}"
    else
        echo -e "${RED}Error: .env.example file not found.${NC}"
        echo "Please create a .env file with your configuration."
        exit 1
    fi
fi

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p logs data

# Build and start the containers
echo -e "${YELLOW}Building and starting containers...${NC}"
docker-compose up -d --build

# Check if containers are running
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Containers started successfully!${NC}"
    echo "API is available at: http://localhost:8000"
    echo "API documentation is available at: http://localhost:8000/docs"
    
    # Show container status
    echo -e "${YELLOW}Container status:${NC}"
    docker-compose ps
else
    echo -e "${RED}Error: Failed to start containers.${NC}"
    echo "Check the logs with: docker-compose logs"
    exit 1
fi

echo -e "${GREEN}Deployment completed!${NC}"
echo "To view logs, run: docker-compose logs -f"
echo "To stop the application, run: docker-compose down" 