# Google OAuth Setup Guide

This guide will help you set up Google OAuth authentication for the Mental Health Symptom Triage application.

## Overview

The application has been configured with django-allauth to support Google OAuth alongside traditional username/password authentication. Users can now sign in with their Google account by clicking the "Continue with Google" or "Sign up with Google" button on the login/register pages.

## Prerequisites

- Django development server running
- Access to [Google Cloud Console](https://console.cloud.google.com)
- A Google account

## Step 1: Create a Google OAuth Application

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select an existing one
3. Search for "Google+ API" and enable it
4. Go to **Credentials** in the left sidebar
5. Click **Create Credentials** and select **OAuth 2.0 Client IDs**
6. If prompted, configure the OAuth consent screen first:
   - Select **External** as the User Type
   - Fill in the required fields (App name, User support email, etc.)
   - Add scopes: `email` and `profile`
   - Add test users (your Google account email)
7. After consent screen is configured, create **OAuth 2.0 Client ID**:
   - Select **Web application** as the Application type
   - Add authorized redirect URIs:
     - `http://localhost:8000/accounts/google/login/callback/`
     - `http://localhost:8000/accounts/google/accounts/login/callback/`
     - `http://127.0.0.1:8000/accounts/google/login/callback/`
   - (For production, use your actual domain: `https://yourdomain.com/accounts/google/login/callback/`)

## Step 2: Get Your Credentials

After creating the OAuth 2.0 Client ID, you'll see:
- **Client ID** (looks like: `xxxxx.apps.googleusercontent.com`)
- **Client Secret** (a long alphanumeric string)

Keep these safe! You'll use them in the next step.

## Step 3: Add Credentials to Django Admin

The easiest way to configure Google OAuth is through the Django admin panel:

1. Start the Django development server if not already running:
   ```bash
   python manage.py runserver
   ```

2. Navigate to `http://localhost:8000/admin/`

3. Log in with your superuser account

4. Go to **Django-allauth > Social applications**

5. Click **Add Social Application** and fill in:
   - **Provider**: Google
   - **Name**: Google OAuth
   - **Client id**: (Paste your Google Client ID)
   - **Secret key**: (Paste your Google Client Secret)
   - **Sites**: Select the site listed (usually "example.com")

6. Click **Save**

## Step 4: Test Google OAuth

1. Go to `http://localhost:8000/login/` or `http://localhost:8000/register/`
2. You should see a red "Continue with Google" / "Sign up with Google" button
3. Click the button to test the OAuth flow
4. You'll be redirected to Google's login/consent screen
5. After authentication, you'll be automatically:
   - Created as a new user (if first time)
   - Logged in to the application
   - Redirected to the home page

## Alternative: Configuration via settings.py

Instead of using Django admin, you can also configure credentials directly in `settings.py`:

Edit `mental_health_project/settings.py` and update the `SOCIALACCOUNT_PROVIDERS` section:

```python
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'APP': {
            'client_id': 'YOUR_GOOGLE_CLIENT_ID_HERE',
            'secret': 'YOUR_GOOGLE_CLIENT_SECRET_HERE',
            'key': ''
        }
    }
}
```

## Features

- **Seamless Registration**: New users can sign up with a single click using their Google account
- **Quick Login**: Existing users can log in instantly without managing another password
- **Email Auto-fill**: User email is automatically retrieved from Google account
- **Assessment Tracking**: Google OAuth users can track their assessment history just like traditional users
- **Profile Management**: All OAuth users get an automatically created profile for tracking last assessment date

## Troubleshooting

### "Invalid client ID" or "Redirect URI mismatch"
- Verify the Client ID and Secret are correct in Django admin
- Check that the redirect URI in Google Console exactly matches the one configured
- For development, ensure you're using `http://localhost:8000`, not `http://127.0.0.1:8000` (or vice versa)

### Button not appearing
- Clear browser cache and hard refresh
- Make sure django-allauth is in INSTALLED_APPS (check settings.py)
- Verify the template has `{% load socialaccount %}` at the top

### "Social application not configured"
- Ensure you've added the social application in Django admin
- Verify the site is correctly associated with the social app

### Can't log out
- Clear browser cookies
- Try private/incognito mode for fresh session

## Production Deployment

When deploying to production:

1. Update Google OAuth credentials with your production domain
2. Add your production URLs to Google Console:
   - `https://yourdomain.com/accounts/google/login/callback/`
3. Create a superuser on production server:
   ```bash
   python manage.py createsuperuser
   ```
4. Add the social application via `/admin/` on your production site
5. Update `ALLOWED_HOSTS` in settings.py with your production domain
6. Set `DEBUG = False` in settings.py
7. Configure CSRF and CORS settings appropriately

## Security Notes

- Never commit Client ID and Secret to version control if hardcoding in settings.py
- Use environment variables for credentials in production:
  ```python
  GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
  GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
  ```
- Regularly rotate credentials
- Use HTTPS in production (not HTTP)
- Review and limit the scopes your application requests

## Support

For more information about django-allauth, visit:
- [django-allauth Documentation](https://django-allauth.readthedocs.io/)
- [Google OAuth Documentation](https://developers.google.com/identity/protocols/oauth2)
