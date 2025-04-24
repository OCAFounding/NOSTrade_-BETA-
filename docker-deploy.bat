@echo off
echo NOS Trade Docker Deployment
echo ================================

REM Check if Docker is installed
where docker >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: Docker is not installed.
    echo Please install Docker first: https://docs.docker.com/get-docker/
    exit /b 1
)

REM Check if Docker Compose is installed
where docker-compose >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: Docker Compose is not installed.
    echo Please install Docker Compose first: https://docs.docker.com/compose/install/
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    echo Warning: .env file not found.
    echo Creating .env file from .env.example...
    if exist .env.example (
        copy .env.example .env
        echo .env file created. Please edit it with your configuration.
    ) else (
        echo Error: .env.example file not found.
        echo Please create a .env file with your configuration.
        exit /b 1
    )
)

REM Create necessary directories
echo Creating necessary directories...
if not exist logs mkdir logs
if not exist data mkdir data

REM Build and start the containers
echo Building and starting containers...
docker-compose up -d --build

REM Check if containers are running
if %ERRORLEVEL% equ 0 (
    echo Containers started successfully!
    echo API is available at: http://localhost:8000
    echo API documentation is available at: http://localhost:8000/docs
    
    REM Show container status
    echo Container status:
    docker-compose ps
) else (
    echo Error: Failed to start containers.
    echo Check the logs with: docker-compose logs
    exit /b 1
)

echo Deployment completed!
echo To view logs, run: docker-compose logs -f
echo To stop the application, run: docker-compose down 