# Deployment Checklist

## Prerequisites

1. **Azure Account Setup**
   - [ ] Azure subscription
   - [ ] Azure Web App service created
   - [ ] App Service Plan configured
   - [ ] Application Insights enabled (optional)

2. **Environment Variables**
   Create a `.env` file with the following variables:
   ```
   # API Configuration
   PORT=8000
   HOST=0.0.0.0
   
   # Database Configuration (if needed)
   DATABASE_URL=your_database_url
   
   # API Keys
   BINANCE_API_KEY=your_binance_api_key
   BINANCE_API_SECRET=your_binance_api_secret
   
   # Monitoring
   LOG_LEVEL=INFO
   MONITORING_INTERVAL=300
   
   # Compliance
   MAX_POSITION_SIZE=1000
   RISK_PER_TRADE=0.02
   MAX_DAILY_TRADES=10
   ```

3. **Azure Web App Configuration**
   Add these application settings in Azure Portal:
   - `WEBSITES_PORT`: 8000
   - `SCM_DO_BUILD_DURING_DEPLOYMENT`: true
   - `PYTHON_VERSION`: 3.9
   - All environment variables from `.env`

4. **Required Files**
   Ensure these files are present:
   - [x] `web.config`
   - [x] `.deployment`
   - [x] `startup.sh`
   - [x] `requirements.txt`
   - [x] `azure-pipelines.yml`

## Deployment Steps

1. **Local Testing**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run tests
   pytest
   
   # Test locally
   cd api
   uvicorn main:app --reload
   ```

2. **Azure Deployment**
   ```bash
   # Login to Azure
   az login
   
   # Set subscription
   az account set --subscription "your-subscription-id"
   
   # Deploy to Azure Web App
   az webapp deployment source config-zip --resource-group "your-resource-group" --name "your-app-name" --src deployment.zip
   ```

3. **Post-Deployment Verification**
   - [ ] Check application logs in Azure Portal
   - [ ] Verify API endpoints are accessible
   - [ ] Test monitoring system
   - [ ] Verify compliance checks
   - [ ] Test stress testing framework

## Troubleshooting

Common issues and solutions:

1. **Application Not Starting**
   - Check `web.config` configuration
   - Verify Python version matches Azure Web App
   - Check application logs in Azure Portal

2. **Missing Dependencies**
   - Verify `requirements.txt` is complete
   - Check if any system-level dependencies are needed
   - Consider using Azure Web App custom startup script

3. **Environment Variables**
   - Ensure all required variables are set in Azure Web App Configuration
   - Check for any missing or incorrect values
   - Verify variable names match those in the code

4. **Performance Issues**
   - Monitor application insights
   - Check resource usage
   - Optimize database queries if applicable

## Maintenance

Regular maintenance tasks:

1. **Weekly**
   - Review application logs
   - Check for dependency updates
   - Monitor system performance

2. **Monthly**
   - Update dependencies
   - Review and update API keys
   - Check compliance settings

3. **Quarterly**
   - Full system audit
   - Security review
   - Performance optimization 