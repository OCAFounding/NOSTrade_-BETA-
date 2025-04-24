# Migrating OCAPulse.io from WordPress to Google Cloud Run

This guide will walk you through the process of migrating your OCAPulse.io website from WordPress to Google Cloud Run.

## Prerequisites

- Access to your WordPress site
- Access to your domain registrar
- Google Cloud account with billing enabled
- Google Cloud SDK installed
- Docker installed

## Step 1: Export Content from WordPress

1. Log in to your WordPress admin panel
2. Go to Tools > Export
3. Select "All content" and click "Download Export File"
4. Save the XML file to your computer

## Step 2: Prepare Your New Application

1. Make sure your application is ready for deployment:
   - All dependencies are listed in requirements.txt
   - Environment variables are properly configured
   - Static files are properly organized

2. Test your application locally:
   ```
   docker-compose up
   ```

## Step 3: Deploy to Google Cloud Run

1. Run the deployment script:
   ```
   .\scripts\deploy-google-cloud.ps1
   ```

2. Follow the instructions provided by the script to:
   - Set up domain mapping in Google Cloud Console
   - Update DNS records at your domain registrar

## Step 4: Migrate Content

1. Import your WordPress content into your new application:
   - If your application has a content management system, use its import tools
   - If not, you may need to manually transfer content or use a script

2. Update internal links to point to the new URLs

## Step 5: DNS Transition

1. Before updating DNS records, ensure your new application is fully functional at the Cloud Run URL

2. Update DNS records at your domain registrar:
   - Update A record for @ to point to the IP provided by Google Cloud
   - Update CNAME record for www to point to your Cloud Run URL

3. Keep your WordPress site running until DNS propagation is complete (can take up to 48 hours)

## Step 6: Verify Migration

1. Visit https://ocapulse.io to verify your site is accessible
2. Visit https://www.ocapulse.io to verify the www subdomain works
3. Test all functionality of your new application
4. Check that all content has been properly migrated

## Step 7: Complete Migration

1. Once you've verified everything is working correctly:
   - Back up your WordPress site one final time
   - Cancel your WordPress hosting subscription
   - Update any external links pointing to your old WordPress site

## Troubleshooting

- **DNS Issues**: Use a tool like [dnschecker.org](https://dnschecker.org/) to verify DNS propagation
- **Content Migration**: If you encounter issues with content migration, consider using a specialized migration tool or service
- **Performance**: Monitor your application's performance in Google Cloud Console and adjust resources as needed

## Cost Considerations

- Google Cloud Run has a generous free tier
- You only pay for what you use beyond the free tier
- Compare costs with your previous WordPress hosting

## Additional Resources

- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)
- [WordPress to Static Site Migration](https://www.google.com/search?q=wordpress+to+static+site+migration)
- [DNS Propagation Checker](https://dnschecker.org/) 