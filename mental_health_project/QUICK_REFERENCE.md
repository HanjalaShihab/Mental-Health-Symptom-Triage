# Quick Reference Card - Google OAuth Setup

## 🎯 Commands You'll Need

### Start the Server (if not running)
```bash
cd ~/Documents/Mental\ Health\ Symptom\ Triage/mental_health_project
source venv/bin/activate
python manage.py runserver
```
Then visit: **http://localhost:8000**

### Access Django Admin
1. Visit: **http://localhost:8000/admin/**
2. Enter your superuser credentials
3. Navigate to: **Django-allauth → Social applications**

### Create Superuser (if needed)
```bash
python manage.py createsuperuser
```

### Run Migrations (already done)
```bash
python manage.py migrate
```

### Check Server Status
Look for: `Starting development server at http://127.0.0.1:8000/`

---

## 📋 Google OAuth Setup Form

**When you create OAuth in Google Cloud, fill in:**

```
Project Name: Mental Health Triage App
API: Google+ API (enable this)
Credentials Type: OAuth 2.0 Client ID
App Type: Web application
Authorized Redirect URIs:
  - http://localhost:8000/accounts/google/login/callback/

You'll get:
  Client ID: xxxxxxx.apps.googleusercontent.com
  Client Secret: xxxxxxxxxxxxxxxx
```

---

## 🔐 Django Admin Form

**Location: Admin → Django-allauth → Social applications → Add**

```
Provider: Google (dropdown)
Name: Google OAuth
Client ID: [paste from Google]
Secret key: [paste from Google]
Sites: Select your site (usually "example.com")
```

---

## 🌐 Important URLs

| Page | URL |
|------|-----|
| Home | http://localhost:8000/ |
| Login | http://localhost:8000/login/ |
| Register | http://localhost:8000/register/ |
| Profile | http://localhost:8000/profile/ |
| Admin | http://localhost:8000/admin/ |
| Assessment | http://localhost:8000/assessment/ |
| History | http://localhost:8000/history/ |
| OAuth Callback | /accounts/google/login/callback/ |

---

## ✅ Testing Checklist

- [ ] Server running at localhost:8000
- [ ] Login page loads with Google button
- [ ] Register page loads with Google button
- [ ] Google credentials added to Django admin
- [ ] Click Google button (goes to Google login)
- [ ] Sign in with Google account
- [ ] Redirected back to app
- [ ] Logged in successfully
- [ ] Can view profile
- [ ] Can create assessment
- [ ] Assessment in history
- [ ] Can log out
- [ ] Can log back in with Google

---

## 🆘 If Something Goes Wrong

| Issue | Solution |
|-------|----------|
| Buttons not showing | Clear cache (Ctrl+F5) |
| "Not configured" error | Add social app in Django admin |
| Redirect URI mismatch | Check URL matches exactly in both Google and Django |
| Login loops | Clear browser cookies |
| Database errors | Run `python manage.py migrate` |
| Import errors | Check `source venv/bin/activate` |
| 404 on callback | Verify `/accounts/google/login/callback/` in URL |

---

## 📞 Help Resources

- **Setup Help**: QUICK_START_OAUTH.md
- **Detailed Guide**: GOOGLE_OAUTH_SETUP.md
- **Technical Info**: OAUTH_IMPLEMENTATION.md
- **Status Check**: STATUS.txt
- **Full Summary**: FINAL_SUMMARY.md

---

## ⏱️ Timeline

- **Get Credentials**: 5 minutes
- **Add to Django**: 1 minute
- **Test**: 1 minute
- **Total**: ~7 minutes

---

## 🎯 Your Goal

Once you complete the 3 steps and test, your app will:
- ✅ Let users sign in with Google
- ✅ Let users sign up with Google
- ✅ Track all assessments per user
- ✅ Save assessment history
- ✅ Show user profile stats

**That's it! You're done!** 🎉

---

## 💡 Pro Tips

1. Use your personal Google account for testing
2. You can test multiple times without issues
3. Existing password login still works
4. Assessment data is safe
5. You can add more OAuth providers later (GitHub, etc.)

---

## 🔄 If You Get Stuck

1. **Read**: QUICK_START_OAUTH.md (5 min)
2. **Check**: GOOGLE_OAUTH_SETUP.md troubleshooting
3. **Verify**: All credentials are correct
4. **Test**: Try in private/incognito browser
5. **Restart**: Server (stop and restart runserver)

---

**Ready? Open QUICK_START_OAUTH.md →**
