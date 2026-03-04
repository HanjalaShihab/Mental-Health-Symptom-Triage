# Vercel Deployment Guide

## Prerequisites
- Vercel account (https://vercel.com)
- GitHub repository linked to Vercel
- Google OAuth credentials

## Environment Variables

Set these in your Vercel project settings (`Settings > Environment Variables`):

```
SECRET_KEY=your-secure-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.vercel.app,yourdomains.com
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
VERCEL=1
```

### Generate a Secure Secret Key

In Python:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## Deployment Steps

### 1. Connect GitHub Repository
1. Go to https://vercel.com/new
2. Select "Import Git Repository"
3. Choose your Mental-Health-Symptom-Triage repository
4. Click "Import"

### 2. Configure Project
- **Framework Preset**: Select "Other" (Django)
- **Build Command**: Pre-filled from `vercel.json`
- **Output Directory**: `staticfiles`

### 3. Add Environment Variables
1. Click "Environment Variables"
2. Add all variables from the list above
3. Ensure they're available for all environments (Production, Preview, Development)

### 4. Deploy
Click "Deploy" to build and deploy your application

### 5. Configure Custom Domain
1. Go to `Settings > Domains`
2. Add your custom domain
3. Follow DNS setup instructions

## Post-Deployment

### Run Database Migrations
Vercel uses ephemeral storage, so SQLite data is not persistent. For production, you'll need to:

1. Use a managed PostgreSQL database (e.g., from Vercel or AWS RDS)
2. Update `DATABASE_URL` environment variable
3. Connect Vercel to your database

### Update Google OAuth Redirect URIs
1. Go to Google Cloud Console
2. Update authorized redirect URIs to include your Vercel domain:
   - `https://yourdomain.vercel.app/accounts/google/login/callback/`

### Monitor Deployments
- View logs in Vercel dashboard
- Check deployment status in `Deployments` tab
- Monitor performance metrics

## Troubleshooting

### Static Files Not Loading
- Ensure `collectstatic` runs during build
- Check `STATIC_ROOT` and `STATICFILES_DIRS` settings
- Verify CloudFlare or CDN caching isn't blocking assets

### Database Connection Issues
- Verify `DATABASE_URL` environment variable is correct
- Check database firewall allows Vercel IP ranges
- Review logs in Vercel dashboard

### Google OAuth Failures
- Verify redirect URIs in Google Cloud Console
- Check `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` are correct
- Ensure environment variables are set in Vercel

## Local Testing
To test production settings locally:

```bash
DEBUG=False python manage.py runserver
```

Ensure all environment variables are set in `.env` file.

## Rollback
If issues occur, Vercel automatically keeps previous deployments. You can:
1. Go to `Deployments` tab
2. Click on a previous deployment
3. Click "Promote to Production"

## Further Reading
- [Vercel Django Docs](https://vercel.com/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
