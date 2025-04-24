# PowerShell script for deploying OCAPulse.io to Google Cloud Run

# Configuration
$PROJECT_ID = Read-Host "Enter your Google Cloud Project ID"
$REGION = "us-central1"
$SERVICE_NAME = "ocapulse-api"
$DOMAIN = "ocapulse.io"

# Function to check if a command exists
function Test-CommandExists {
    param ($command)
    $oldPreference = $ErrorActionPreference
    $ErrorActionPreference = 'stop'
    try {
        if (Get-Command $command) { return $true }
    } catch {
        return $false
    } finally {
        $ErrorActionPreference = $oldPreference
    }
}

# Check prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Cyan

if (-not (Test-CommandExists "gcloud")) {
    Write-Host "Error: Google Cloud SDK (gcloud) is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install it from: https://cloud.google.com/sdk/docs/install" -ForegroundColor Yellow
    exit 1
}

if (-not (Test-CommandExists "docker")) {
    Write-Host "Error: Docker is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install it from: https://docs.docker.com/get-docker/" -ForegroundColor Yellow
    exit 1
}

# Step 1: Set up Google Cloud Project
Write-Host "Setting up Google Cloud project..." -ForegroundColor Cyan
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Step 2: Build and push Docker image
Write-Host "Building and pushing Docker image..." -ForegroundColor Cyan
docker build -t gcr.io/$PROJECT_ID/$SERVICE_NAME .
gcloud auth configure-docker
docker push gcr.io/$PROJECT_ID/$SERVICE_NAME

# Step 3: Deploy to Cloud Run
Write-Host "Deploying to Cloud Run..." -ForegroundColor Cyan
gcloud run deploy $SERVICE_NAME `
    --image gcr.io/$PROJECT_ID/$SERVICE_NAME `
    --platform managed `
    --region $REGION `
    --allow-unauthenticated

# Get the deployed URL
$DEPLOYED_URL = (gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format="value(status.url)")

Write-Host "Deployment completed!" -ForegroundColor Green
Write-Host "Your service is deployed at: $DEPLOYED_URL" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Go to the Cloud Run page in Google Cloud Console" -ForegroundColor Yellow
Write-Host "2. Select your service ($SERVICE_NAME)" -ForegroundColor Yellow
Write-Host "3. Go to the 'Domain mappings' tab" -ForegroundColor Yellow
Write-Host "4. Click 'Add mapping'" -ForegroundColor Yellow
Write-Host "5. Enter your domain ($DOMAIN) and follow the instructions" -ForegroundColor Yellow
Write-Host ""
Write-Host "After domain mapping is set up, update your DNS records at your domain registrar:" -ForegroundColor Yellow
Write-Host "- Update A record for @ to point to the IP provided by Google Cloud" -ForegroundColor Yellow
Write-Host "- Update CNAME record for www to point to $DEPLOYED_URL" -ForegroundColor Yellow 