# iOS PWA Installation Guide

## How to Install CEM as an App on iOS

Your CEM system is now ready to be installed as a Progressive Web App (PWA) on iOS devices! This works just like a native app without needing the App Store.

### For iOS (iPhone/iPad):

1. **Open Safari** (must use Safari, not Chrome or other browsers on iOS)
   - Go to your CEM URL (e.g., `https://your-domain.com` or your server IP)

2. **Tap the Share button** (square with arrow pointing up)
   - Located at the bottom of Safari on iPhone
   - Located at the top on iPad

3. **Scroll down and tap "Add to Home Screen"**
   - You'll see the CEM icon and name
   - You can customize the name if you want

4. **Tap "Add"** in the top right corner

5. **Done!** The CEM app icon will appear on your home screen

### Features when installed:

✅ **Runs like a native app** - Full screen without Safari bars
✅ **Works offline** - Access cached pages without internet
✅ **Fast loading** - Instant startup from home screen
✅ **Push notifications** - Receive updates (if enabled)
✅ **Native feel** - Smooth animations and gestures
✅ **Secure** - Must use HTTPS for security

### For Android:

1. **Open Chrome** (or any modern browser)
2. **Visit your CEM URL**
3. **Tap the banner** that says "Add CEM to Home Screen"
   - OR tap the menu (⋮) → "Install app" or "Add to Home Screen"
4. **Tap "Install"**

### Requirements:

- **HTTPS** - Your site must be served over HTTPS (not HTTP)
  - This is required for service workers and PWAs
  - Use Let's Encrypt for free SSL certificates

- **Modern Browser**
  - Safari 11.3+ on iOS
  - Chrome 70+ on Android
  - Any modern browser on desktop

### Sharing with Friends:

Simply share your CEM URL with them and have them follow the steps above!

**For iOS users:** Send them this direct link to save:
```
https://your-domain.com/web/dashboard
```

**Important:** They'll need to:
1. Create an account (or you create it for them)
2. Follow the installation steps above
3. Login once, then they'll stay logged in

### Troubleshooting:

**"Add to Home Screen" not showing?**
- Make sure you're using HTTPS (not HTTP)
- Clear Safari cache and try again
- Make sure you're on Safari (iOS requires Safari for PWA)

**App not loading offline?**
- First visit needs internet to cache pages
- Visit main pages while online to cache them

**Icon not showing correctly?**
- Clear home screen icon and re-add
- Make sure all icon files are accessible

### Testing Before Deployment:

If you're running locally:
1. You can test on localhost (http://localhost:8000)
2. Or use ngrok/localtunnel to get HTTPS for testing
3. For production, always use proper HTTPS

---

## Current Setup Status:

✅ PWA Manifest configured (`/static/manifest.json`)
✅ Service Worker ready (`/static/sw.js`)
✅ iOS meta tags added
✅ Install prompt button (for Android/Chrome)
✅ App icons (all sizes)
✅ Offline support

## Next Steps:

1. **Deploy with HTTPS** (required for iOS PWA)
2. **Test installation** on your iOS device
3. **Share URL** with friends
4. **Monitor usage** in browser DevTools

Enjoy your native-like app experience! 🎉
