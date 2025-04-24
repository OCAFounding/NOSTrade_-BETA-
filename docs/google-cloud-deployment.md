# Deploying OCAPulse.io to Google Cloud Run

This guide will walk you through the process of deploying your OCAPulse.io application to Google Cloud Run and configuring your domain to point to it.

## Prerequisites

- Google Cloud account with billing enabled
- Google Cloud SDK installed
- Docker installed
- Domain (OCAPulse.io) registered and managed by a domain registrar

## Step 1: Set Up Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Cloud Run API:
   ```
   gcloud services enable run.googleapis.com
   ```
4. Enable the Container Registry API:
   ```
   gcloud services enable containerregistry.googleapis.com
   ```

## Step 2: Build and Push Docker Image

1. Navigate to your project directory:
   ```
   cd /path/to/ocapulse.io
   ```

2. Build the Docker image:
   ```
   docker build -t gcr.io/YOUR_PROJECT_ID/ocapulse-api .
   ```

3. Configure Docker to authenticate with Google Cloud:
   ```
   gcloud auth configure-docker
   ```

4. Push the image to Google Container Registry:
   ```
   docker push gcr.io/YOUR_PROJECT_ID/ocapulse-api
   ```

## Step 3: Deploy to Cloud Run

1. Deploy the container to Cloud Run:
   ```
   gcloud run deploy ocapulse-api \
     --image gcr.io/YOUR_PROJECT_ID/ocapulse-api \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

2. Note the URL provided after deployment (e.g., `https://ocapulse-api-xxxxx-uc.a.run.app`)

## Step 4: Configure Domain for Cloud Run

1. Go to the [Cloud Run page](https://console.cloud.google.com/run) in the Google Cloud Console
2. Select your service (ocapulse-api)
3. Go to the "Domain mappings" tab
4. Click "Add mapping"
5. Enter your domain (ocapulse.io) and click "Continue"
6. Follow the instructions to verify domain ownership and configure DNS

## Step 5: Update DNS Records

You'll need to update your DNS records at your domain registrar. The exact steps depend on your registrar, but generally:

1. Log in to your domain registrar's control panel
2. Find the DNS management section
3. Update the A record for the root domain (@):
   - Type: A
   - Name: @ (or leave blank)
   - Value: The IP address provided by Google Cloud
   - TTL: 3600 (or default)

4. Update the CNAME record for www:
   - Type: CNAME
   - Name: www
   - Value: The Cloud Run URL (e.g., `ocapulse-api-xxxxx-uc.a.run.app`)
   - TTL: 3600 (or default)

5. Remove or update any WordPress-specific records

## Step 6: Verify Domain Setup

1. Wait for DNS propagation (can take up to 48 hours, but usually much faster)
2. Visit https://ocapulse.io to verify your site is accessible
3. Visit https://www.ocapulse.io to verify the www subdomain works

## Step 7: Set Up Continuous Deployment (Optional)

1. Create a Cloud Build trigger:
   ```
   gcloud builds triggers create github \
     --repo-name=YOUR_GITHUB_REPO \
     --branch-pattern=main \
     --build-config=cloudbuild.yaml
   ```

2. Create a `cloudbuild.yaml` file in your repository:
   ```yaml
   steps:
   - name: 'gcr.io/cloud-builders/docker'
     args: ['build', '-t', 'gcr.io/$PROJECT_ID/ocapulse-api', '.']
   - name: 'gcr.io/cloud-builders/docker'
     args: ['push', 'gcr.io/$PROJECT_ID/ocapulse-api']
   - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
     entrypoint: gcloud
     args:
     - 'run'
     - 'deploy'
     - 'ocapulse-api'
     - '--image'
     - 'gcr.io/$PROJECT_ID/ocapulse-api'
     - '--region'
     - 'us-central1'
     - '--platform'
     - 'managed'
     - '--allow-unauthenticated'
   images:
   - 'gcr.io/$PROJECT_ID/ocapulse-api'
   ```

## Troubleshooting

- **DNS Propagation**: DNS changes can take time to propagate. Use a tool like [dnschecker.org](https://dnschecker.org/) to verify your DNS records.
- **SSL Certificate**: Google Cloud automatically provisions SSL certificates for your domain.
- **Domain Verification**: If you have trouble verifying domain ownership, make sure you have access to the domain's DNS settings.
- **Container Issues**: If your container fails to start, check the logs in the Google Cloud Console.

## Cost Considerations

Google Cloud Run has a generous free tier:
- 2 million requests per month
- 360,000 GB-seconds of compute time
- 180,000 vCPU-seconds of compute time

Beyond the free tier, you only pay for what you use.

## Additional Resources

- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud Run Pricing](https://cloud.google.com/run/pricing)
- [Domain Mapping for Cloud Run](https://cloud.google.com/run/docs/mapping-custom-domains) 