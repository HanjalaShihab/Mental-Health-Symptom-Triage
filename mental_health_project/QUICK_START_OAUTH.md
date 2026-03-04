# Quick Start: Google OAuth Setup

## TL;DR - Get Started in 5 Minutes

### Step 1: Get Google Credentials (2 minutes)
1. Go to https://console.cloud.google.com
2. Create a new project → Enable Google+ API
3. Create OAuth 2.0 credentials (Web application type)
4. Add redirect URI: `http://localhost:8000/accounts/google/login/callback/`
5. Copy your Client ID and Client Secret

### Step 2: Configure Django (1 minute)
1. Open http://localhost:8000/admin/
2. Login with your admin account
3. Go to Django-allauth → Social applications → Add
4. Fill in:
   - Provider: **Google**
   - Name: **Google OAuth**
   - Client ID: [paste from Step 1]
   - Secret key: [paste from Step 1]
   - Sites: (select the listed site)
5. Click Save

### Step 3: Test It (2 minutes)
1. Go to http://localhost:8000/login/
2. Click the red "Continue with Google" button
3. Complete Google login
4. You're now logged in!

## Current Status

✅ **Server is running**: http://localhost:8000
✅ **Google buttons visible**: On login & register pages  
✅ **Database ready**: All allauth tables created
⏳ **Waiting for**: Google OAuth credentials (from your Google account)

## Files to Read

- **GOOGLE_OAUTH_SETUP.md** - Detailed step-by-step guide
- **OAUTH_IMPLEMENTATION.md** - Technical implementation details

## Troubleshooting

**Buttons not showing?**
- Clear browser cache and refresh (Ctrl+F5)

**Getting "Social application not configured"?**
- Make sure you saved the social app in Django admin

**Redirect URI mismatch?**
- Check exact URL matches in both Google Console AND Django admin
- For localhost, use `http://` not `https://`

## All Features Working

✅ Traditional login/register (username/password)
✅ Google OAuth buttons on login page
✅ Google OAuth buttons on register page
✅ Assessment tracking
✅ Profile management
✅ Assessment history
✅ Automatic profile creation
✅ Session management
✅ CSRF protection

## Need Help?

1. Read **GOOGLE_OAUTH_SETUP.md** for detailed instructions
2. Check Google Cloud Console for any errors
3. Ensure Client ID/Secret are correct in Django admin
4. Clear browser cache and try again

---

**Once you add credentials from Google, your app is fully functional!** 🚀
