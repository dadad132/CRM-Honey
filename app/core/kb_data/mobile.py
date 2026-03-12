"""Mobile device and phone troubleshooting articles and diagnostic tree."""

ARTICLES = [
    {
        "category": "Mobile & Phone",
        "problem_title": "Email not syncing on mobile phone",
        "problem_description": "Corporate email is not syncing on the user's iPhone or Android phone. May show authentication errors or just not receive new emails.",
        "problem_keywords": "phone email, mobile email, email sync phone, ios email, android email, mobile outlook, phone not syncing",
        "solution_steps": (
            "1. For Outlook mobile app (recommended):\n"
            "   - Remove the account: Settings > tap account > Delete Account\n"
            "   - Re-add: Settings > Add Account > use company email\n"
            "   - If MFA enabled: May need to approve the MFA prompt on setup\n"
            "2. For iOS native Mail app:\n"
            "   - Settings > Mail > Accounts > find the account\n"
            "   - Delete and re-add as 'Microsoft Exchange'\n"
            "   - Server: outlook.office365.com (for M365)\n"
            "   - For on-prem Exchange: Use the OWA server address\n"
            "3. For Android native Mail/Gmail app:\n"
            "   - Settings > Accounts > Remove the account\n"
            "   - Re-add as Exchange/Office 365\n"
            "4. Check if app password is needed:\n"
            "   - Some MFA configurations require an app-specific password\n"
            "   - Generate at: mysignins.microsoft.com > Security Info\n"
            "5. Check Conditional Access policies:\n"
            "   - Organization may require approved apps only (Outlook)\n"
            "   - Check Intune device compliance\n"
            "6. Verify mailbox is active:\n"
            "   - Can user log in to Outlook on web? (outlook.office365.com)\n"
            "   - If web works, problem is phone-specific\n"
            "7. For ActiveSync issues:\n"
            "   - Check if ActiveSync is enabled for the user\n"
            "   - Exchange admin: Get-CASMailbox -Identity user | fl ActiveSync*\n"
            "8. Check date/time on phone: Must be set to automatic"
        ),
    },
    {
        "category": "Mobile & Phone",
        "problem_title": "Phone not connecting to corporate Wi-Fi",
        "problem_description": "Mobile device cannot connect to the company Wi-Fi network. May get authentication errors or the network doesn't appear.",
        "problem_keywords": "phone wifi, mobile wifi, corporate wifi, phone can't connect, wifi authentication, 802.1x phone, wifi certificate",
        "solution_steps": (
            "1. Basic checks:\n"
            "   - Toggle Wi-Fi off and on\n"
            "   - Restart the phone\n"
            "   - Forget the network and reconnect\n"
            "2. For WPA2-Enterprise (802.1X) networks:\n"
            "   - These require username/password or certificate\n"
            "   - Enter domain\\username or username@domain.com\n"
            "   - EAP method must match: PEAP, TLS, or TTLS\n"
            "   - If certificate-based: Cert must be installed on device\n"
            "3. For certificate-based Wi-Fi:\n"
            "   - Certificate may need to be deployed via MDM (Intune)\n"
            "   - Check: Settings > General > Profiles (iOS) for installed certs\n"
            "   - Android: Settings > Security > Trusted credentials\n"
            "4. If using Intune/MDM:\n"
            "   - Wi-Fi profile should auto-deploy to enrolled devices\n"
            "   - Check device enrollment status\n"
            "   - Sync the device: Settings > Accounts > Work account > Sync\n"
            "5. MAC address filtering:\n"
            "   - iOS 14+/Android 10+ use randomized MAC by default\n"
            "   - If MAC filtering is used: Disable Private Address for this network\n"
            "   - iOS: Settings > Wi-Fi > (i) next to network > Private Address > Off\n"
            "6. Guest vs Corporate network:\n"
            "   - Corporate may require enrolled/managed devices\n"
            "   - Personal devices might only work on guest network"
        ),
    },
    {
        "category": "Mobile & Phone",
        "problem_title": "MDM/Intune enrollment failing on device",
        "problem_description": "Mobile device won't enroll in Microsoft Intune or company MDM. Enrollment process fails, stalls, or shows an error.",
        "problem_keywords": "intune enrollment, mdm enroll, device enrollment, intune failed, mdm error, company portal, device management",
        "solution_steps": (
            "1. Prerequisites:\n"
            "   - User must have an Intune license assigned\n"
            "   - Check enrollment restrictions: Intune > Devices > Enrollment restrictions\n"
            "   - Device OS must meet minimum version requirements\n"
            "2. For iOS enrollment:\n"
            "   - Download Company Portal from App Store\n"
            "   - Sign in with corporate credentials\n"
            "   - Follow prompts to install management profile\n"
            "   - Go to Settings > General > Device Management > trust the profile\n"
            "   - If using Apple Business Manager: Device should auto-enroll\n"
            "3. For Android enrollment:\n"
            "   - Download Company Portal or Microsoft Intune app\n"
            "   - For Work Profile: Follow the work profile setup\n"
            "   - For Fully Managed: Factory reset first, then enroll\n"
            "   - Accept all permissions requested\n"
            "4. Common enrollment failures:\n"
            "   - Device limit reached: User has too many enrolled devices\n"
            "   - OS too old: Update the device OS\n"
            "   - Personal device blocked: Policy may only allow corporate devices\n"
            "   - Already enrolled: Unenroll first, then re-enroll\n"
            "5. Troubleshooting:\n"
            "   - Delete the Company Portal app data/cache and retry\n"
            "   - On Android: Settings > Apps > Company Portal > Clear Data\n"
            "   - Check Intune > Devices > All devices for the enrollment status\n"
            "6. After enrollment:\n"
            "   - Device must sync and become compliant\n"
            "   - May take 15-30 minutes for policies to apply\n"
            "   - Retry: Open Company Portal > Sync"
        ),
    },
    {
        "category": "Mobile & Phone",
        "problem_title": "Mobile device lost or stolen",
        "problem_description": "Employee has lost their phone or it was stolen. The device has corporate email and potentially sensitive data. Need to secure it remotely.",
        "problem_keywords": "lost phone, stolen phone, remote wipe, find my phone, lost device, stolen device, mobile wipe",
        "solution_steps": (
            "1. Immediate actions:\n"
            "   - Reset the user's password for all corporate accounts\n"
            "   - Revoke active sessions\n"
            "2. Remote wipe via Intune:\n"
            "   - Intune > Devices > find the device\n"
            "   - For company data only: 'Retire' (removes corporate data but not personal)\n"
            "   - For full wipe: 'Wipe' (factory resets the entire device)\n"
            "   - Choose Retire for BYOD, Wipe for company-owned\n"
            "3. Remote wipe via Exchange ActiveSync:\n"
            "   - Exchange admin center > Recipients > Mailbox > Mobile Devices\n"
            "   - Select the device > Wipe Device\n"
            "4. Help user find the device:\n"
            "   - iPhone: icloud.com/find (or Find My iPhone app from another device)\n"
            "   - Android: google.com/android/find (Find My Device)\n"
            "   - Both can show location, play sound, lock device\n"
            "5. Block the SIM if company-owned:\n"
            "   - Contact the mobile carrier to suspend the line\n"
            "6. Document the incident:\n"
            "   - Device serial number)\n"
            "   - What corporate data was on it\n"
            "   - Was the device encrypted?\n"
            "   - Was a PIN/biometric lock enabled?\n"
            "7. If device is found later:\n"
            "   - If wiped: Re-enroll and reconfigure\n"
            "   - If only retired: Re-enroll corporate profile"
        ),
    },
    {
        "category": "Mobile & Phone",
        "problem_title": "Teams or Zoom calls not working on mobile",
        "problem_description": "User cannot make or receive Teams/Zoom calls on their phone. Audio may not work, video is blank, or calls drop immediately.",
        "problem_keywords": "teams phone, zoom phone, mobile call, teams audio, mobile meeting, phone calls teams, video call phone",
        "solution_steps": (
            "1. Basic checks:\n"
            "   - Update the app to latest version from App Store/Play Store\n"
            "   - Check internet connection (try switching between Wi-Fi and cellular)\n"
            "   - Restart the app (force close and reopen)\n"
            "2. Permission issues:\n"
            "   - iOS: Settings > Teams/Zoom > Microphone: ON, Camera: ON\n"
            "   - Android: Settings > Apps > Teams/Zoom > Permissions > Mic + Camera\n"
            "   - Also check: Notification permissions (for incoming call alerts)\n"
            "3. No audio in calls:\n"
            "   - Check phone isn't on silent/Do Not Disturb\n"
            "   - Check Bluetooth: May be routing audio to disconnected BT device\n"
            "   - In the call: Tap speaker icon to switch audio output\n"
            "   - Try using speakerphone\n"
            "4. Calls dropping:\n"
            "   - Poor network: Move to stronger Wi-Fi or cellular signal\n"
            "   - Check battery saver: May be killing the app in background\n"
            "   - Android: Settings > Battery > Teams > Don't optimize\n"
            "   - iOS: Settings > Teams > Background App Refresh: ON\n"
            "5. Video not working:\n"
            "   - Check camera permission (see step 2)\n"
            "   - Close other apps using camera\n"
            "   - Toggle camera off and on in the call\n"
            "6. Clear app cache:\n"
            "   - Android: Settings > Apps > Teams > Storage > Clear Cache\n"
            "   - iOS: Delete and reinstall the app"
        ),
    },
    {
        "category": "Mobile & Phone",
        "problem_title": "Company app not installing or updating on phone",
        "problem_description": "Corporate app deployed through Intune or MDM won't install on the user's phone. Shows errors or stays in 'installing' state.",
        "problem_keywords": "app install, company app, intune app, mdm app, app not installing, app deploy, managed app",
        "solution_steps": (
            "1. Check app requirements:\n"
            "   - Is the device OS version compatible?\n"
            "   - Is there enough storage space?\n"
            "   - Is the device enrolled in Intune/MDM?\n"
            "2. Force sync:\n"
            "   - Open Company Portal > Menu > Sync\n"
            "   - Or: Settings > Accounts > Work account > Sync\n"
            "   - Wait 15-30 minutes for the app to push\n"
            "3. For iOS:\n"
            "   - Check that the user accepted the MDM push notification\n"
            "   - Settings > General > VPN & Device Management > Management Profile should be installed\n"
            "   - For App Store apps: User may need to accept install prompt\n"
            "   - Check Apple ID is signed in to App Store\n"
            "4. For Android:\n"
            "   - Work Profile apps install in the 'Work' tab\n"
            "   - Check Managed Google Play Store (in Work profile)\n"
            "   - Google account must be set up in Work profile\n"
            "5. Check Intune admin portal:\n"
            "   - Apps > Monitor > App install status\n"
            "   - Find the app and check per-device status\n"
            "   - Look for error codes\n"
            "6. Common fixes:\n"
            "   - Restart the device\n"
            "   - Ensure good network connection during install\n"
            "   - Remove old version first and retry\n"
            "   - Sign out and back in to Company Portal"
        ),
    },
    {
        "category": "Mobile & Phone",
        "problem_title": "Mobile hotspot not working for laptop",
        "problem_description": "User's phone hotspot won't connect to their laptop, or connects but has no internet. Common issue when office internet is down.",
        "problem_keywords": "hotspot, mobile hotspot, tethering, phone hotspot, hotspot no internet, personal hotspot, wifi hotspot",
        "solution_steps": (
            "1. Enable hotspot properly:\n"
            "   - iPhone: Settings > Personal Hotspot > Allow Others to Join\n"
            "   - Android: Settings > Network > Hotspot & Tethering > Wi-Fi Hotspot\n"
            "2. Connect from laptop:\n"
            "   - The phone's hotspot should appear as a Wi-Fi network\n"
            "   - Enter the password shown in hotspot settings\n"
            "   - Alternative: USB tethering (more reliable but needs USB cable)\n"
            "3. If connected but no internet:\n"
            "   - Check phone has cellular data enabled\n"
            "   - Check cellular signal strength\n"
            "   - Toggle airplane mode on/off on the phone\n"
            "   - On laptop: Forget the hotspot network and reconnect\n"
            "4. Carrier restrictions:\n"
            "   - Some carriers block or charge extra for hotspot\n"
            "   - Check with carrier if tethering is included in the plan\n"
            "5. Performance issues:\n"
            "   - Hotspot is limited by cellular speed\n"
            "   - Move to better signal area\n"
            "   - Reduce the number of connected devices\n"
            "   - Some carriers throttle hotspot speeds\n"
            "6. If hotspot disconnects frequently:\n"
            "   - iPhone: Keep the hotspot settings screen open (prevents sleep)\n"
            "   - Android: Settings > Hotspot > Turn off automatically when not in use: OFF\n"
            "   - Keep phone plugged in (battery saver may disable hotspot)"
        ),
    },
    {
        "category": "Mobile & Phone",
        "problem_title": "Phone calendar not syncing with Outlook",
        "problem_description": "Calendar on mobile phone doesn't match Outlook calendar. Meetings are missing or showing at wrong times on the phone.",
        "problem_keywords": "calendar sync, phone calendar, meeting not showing, mobile calendar, outlook calendar phone, calendar wrong time",
        "solution_steps": (
            "1. Check which calendar app:\n"
            "   - Use Outlook mobile for best sync with corporate calendar\n"
            "   - Native calendar apps may have sync delays\n"
            "2. In Outlook mobile:\n"
            "   - Calendar > tap the calendar icon (top) > ensure the correct calendar is checked\n"
            "   - Shared calendars may need to be added separately\n"
            "   - Pull down to refresh\n"
            "3. For native iOS Calendar:\n"
            "   - Settings > Calendar > Accounts > Exchange account\n"
            "   - Toggle Calendars OFF and back ON\n"
            "   - Check Fetch New Data: Push should be enabled for Exchange\n"
            "4. For Android native Calendar:\n"
            "   - Settings > Accounts > Exchange > Sync Calendar: ON\n"
            "   - Google Calendar app > hamburger menu > check the exchange account calendar\n"
            "5. Wrong timezone:\n"
            "   - Settings > General > Date & Time > Set Automatically: ON\n"
            "   - In Outlook: Settings > Calendar > check timezone setting\n"
            "   - Different timezones between phone and Outlook cause meeting time mismatches\n"
            "6. If specific meetings are missing:\n"
            "   - Check if they're on a shared calendar (these may not sync)\n"
            "   - Re-accept the meeting invitation\n"
            "   - Remove and re-add the email account\n"
            "7. Allow sufficient time: Calendar sync can take 15-30 minutes"
        ),
    },
    {
        "category": "Mobile & Phone",
        "problem_title": "Phone screen cracked or unresponsive",
        "problem_description": "Company phone screen is cracked, partially unresponsive, or completely dead. Need to determine repair vs replacement options.",
        "problem_keywords": "cracked screen, broken screen, phone screen, unresponsive screen, screen replacement, phone repair, broken phone",
        "solution_steps": (
            "1. Assess the damage:\n"
            "   - Is the screen cracked but still functional? (Can still use it)\n"
            "   - Is part of the touch screen unresponsive?\n"
            "   - Is the screen completely dead/black?\n"
            "2. Immediate data concerns:\n"
            "   - If screen works partially: Back up data immediately\n"
            "   - If completely dead:\n"
            "     - iPhone: Data likely backed up to iCloud (check icloud.com)\n"
            "     - Android: Check Google backup settings\n"
            "     - Corporate data: If Intune-enrolled, data is on the server\n"
            "3. Workarounds for unresponsive screen:\n"
            "   - Connect USB mouse (Android: OTG adapter)\n"
            "   - iPhone: VoiceOver + external keyboard via Bluetooth\n"
            "   - Mirror screen: ADB for Android, QuickTime for iOS (if trusted)\n"
            "4. Repair options:\n"
            "   - Check warranty: AppleCare+ or manufacturer warranty\n"
            "   - Apple: Book Genius Bar appointment or authorized repair shop\n"
            "   - Samsung: Samsung authorized repair centers\n"
            "   - Company policy: Check if IT department handles repairs or replacements\n"
            "5. If replacing the device:\n"
            "   - Wipe old device remotely (Intune or Find My Device)\n"
            "   - Set up new device with corporate enrollment\n"
            "   - Restore from backup\n"
            "6. Prevention: Recommend screen protectors and protective cases for corporate devices"
        ),
    },
    {
        "category": "Mobile & Phone",
        "problem_title": "VPN not connecting on mobile device",
        "problem_description": "Corporate VPN app on phone won't connect. User cannot access internal resources from their mobile device while remote.",
        "problem_keywords": "vpn phone, mobile vpn, vpn not connecting, phone vpn error, vpn app, mobile remote access",
        "solution_steps": (
            "1. Basic troubleshooting:\n"
            "   - Close and reopen the VPN app\n"
            "   - Check internet connection (VPN needs internet first)\n"
            "   - Try switching between Wi-Fi and cellular\n"
            "2. Check VPN app credentials:\n"
            "   - Ensure username/password are correct\n"
            "   - Password may have changed/expired\n"
            "   - MFA: Complete the authentication prompt\n"
            "3. Certificate-based VPN:\n"
            "   - Certificate may have expired\n"
            "   - Check installed certificates:\n"
            "     - iOS: Settings > General > Profiles\n"
            "     - Android: Settings > Security > User Credentials\n"
            "   - If expired: Request new cert or sync from Intune\n"
            "4. Always-On VPN issues:\n"
            "   - If deployed via Intune: Check device compliance\n"
            "   - Try manually connecting from the VPN app\n"
            "   - Remove and re-import the VPN profile\n"
            "5. Common VPN apps:\n"
            "   - Cisco AnyConnect: Check server address is correct\n"
            "   - GlobalProtect (Palo Alto): Portal address must be reachable\n"
            "   - Pulse Secure/Ivanti: Check connection URL\n"
            "6. If VPN connects but no access:\n"
            "   - Split tunnel vs full tunnel configuration\n"
            "   - DNS may not be routing correctly\n"
            "   - Try accessing resources by IP instead of name"
        ),
    },
    {
        "category": "Mobile & Phone",
        "problem_title": "Mobile device battery draining rapidly",
        "problem_description": "Company mobile device (iPhone or Android) battery depletes much faster than normal, even with minimal use. Device may get warm.",
        "problem_keywords": "battery drain, battery life, phone battery, mobile battery, fast drain, overheating, battery usage",
        "solution_steps": (
            "1. Check battery usage:\n"
            "   - iPhone: Settings > Battery > Battery Usage by App\n"
            "   - Android: Settings > Battery > Battery Usage\n"
            "   - Identify which app is consuming the most power\n"
            "2. Common culprits:\n"
            "   - Email: Frequent push notifications or sync\n"
            "   - Teams/Zoom: Background audio/video processing\n"
            "   - Location services: GPS constantly active\n"
            "   - MDM agent: Excessive check-in frequency\n"
            "3. Quick fixes:\n"
            "   - Disable background app refresh for non-essential apps\n"
            "   - Reduce screen brightness or enable auto-brightness\n"
            "   - Turn off Bluetooth/Wi-Fi when not needed\n"
            "   - Disable 'Hey Siri' / 'OK Google' always-on listening\n"
            "4. Email optimization:\n"
            "   - Change from Push to Fetch (every 15-30 minutes)\n"
            "   - Reduce number of synced email days\n"
            "   - iPhone: Settings > Mail > Accounts > Fetch New Data\n"
            "5. Software issues:\n"
            "   - Update the OS to the latest version (battery fixes)\n"
            "   - Force-close stuck apps\n"
            "   - Reset network settings if cellular radio is draining\n"
            "6. Battery health:\n"
            "   - iPhone: Settings > Battery > Battery Health > Maximum Capacity\n"
            "   - Below 80%: Battery needs replacement\n"
            "   - Android: Use AccuBattery or similar apps\n"
            "7. MDM policy check: Ensure MDM compliance checks aren't running too frequently"
        ),
    },
    {
        "category": "Mobile & Phone",
        "problem_title": "Corporate app won't install on mobile device",
        "problem_description": "A company-deployed app from the MDM (Intune, JAMF, AirWatch) won't install, shows an error, or gets stuck downloading on the user's device.",
        "problem_keywords": "app install failed, mdm app, intune app, company portal, app deployment, app stuck, managed app",
        "solution_steps": (
            "1. Check MDM enrollment:\n"
            "   - Is the device still enrolled in MDM?\n"
            "   - iPhone: Settings > General > VPN & Device Management\n"
            "   - Android: Settings > Accounts > Work profile\n"
            "2. Company Portal / Managed App:\n"
            "   - Open the Company Portal app (Intune)\n"
            "   - Or Hub app (AirWatch/Workspace ONE)\n"
            "   - Try re-downloading the app from the company catalog\n"
            "3. Common failures:\n"
            "   - Storage full: Need at least 500 MB free\n"
            "   - OS version too old: App requires newer iOS/Android\n"
            "   - App already installed outside management: Uninstall personal copy first\n"
            "4. iOS specific:\n"
            "   - Trust the MDM profile: Settings > General > Profiles > Trust\n"
            "   - If 'Untrusted Enterprise Developer': Go to Profiles to approve\n"
            "   - Check iOS version meets minimum requirement\n"
            "5. Android specific:\n"
            "   - Work profile must be active\n"
            "   - Allow installation from unknown sources (if sideloading)\n"
            "   - Clear Google Play Store cache: Settings > Apps > Play Store > Clear Cache\n"
            "6. Re-sync with MDM:\n"
            "   - Company Portal > Settings > Sync (force sync)\n"
            "   - Or: Restart the device to trigger MDM check-in\n"
            "7. Admin side: Check Intune > Apps > Monitor > App install status for specific errors"
        ),
    },
    {
        "category": "Mobile & Phone",
        "problem_title": "Mobile device not receiving push notifications",
        "problem_description": "User's company phone isn't receiving push notifications for email, Teams, or other business apps, causing missed messages and alerts.",
        "problem_keywords": "push notifications, no notifications, mobile alerts, notification missing, silent notifications, do not disturb",
        "solution_steps": (
            "1. Check notification settings:\n"
            "   - iPhone: Settings > Notifications > select app > Allow Notifications ON\n"
            "   - Android: Settings > Apps > select app > Notifications ON\n"
            "   - Ensure: Sounds, Badges, Banners/Alerts are enabled\n"
            "2. Do Not Disturb / Focus mode:\n"
            "   - iPhone: Check Focus mode (DND, Work, Sleep may silence apps)\n"
            "   - Android: Check Do Not Disturb schedule\n"
            "   - These can silently block all notifications\n"
            "3. Battery optimization:\n"
            "   - Android aggressively kills background apps to save battery\n"
            "   - Settings > Battery > Battery Optimization > select app > Don't Optimize\n"
            "   - Samsung: Settings > Battery > App power management > Never sleeping apps\n"
            "4. Email notifications:\n"
            "   - Outlook app: Settings > Mail > Notifications > configure per account\n"
            "   - Check: Is the account set to 'Focused Inbox'? Notifications may only show for Focused\n"
            "5. Teams notifications:\n"
            "   - Teams app > Settings > Notifications > all should be ON\n"
            "   - Check: Quiet hours and Quiet days settings\n"
            "   - Desktop app running? Notifications may go to desktop instead of phone\n"
            "6. Re-register push:\n"
            "   - Force-close the app and reopen it\n"
            "   - Sign out and sign back in (re-registers push token)\n"
            "   - Reinstall the app as last resort\n"
            "7. MDM: Check if MDM policy restricts notification content on lock screen"
        ),
    },
    {
        "category": "Mobile & Phone",
        "problem_title": "Mobile device touchscreen unresponsive or erratic",
        "problem_description": "The touchscreen on a company phone or tablet is not responding to touch, responding incorrectly (ghost touches), or has dead zones.",
        "problem_keywords": "touchscreen, unresponsive screen, ghost touch, screen not working, dead zone, touch issue, screen problem",
        "solution_steps": (
            "1. Basic troubleshooting:\n"
            "   - Clean the screen with a microfiber cloth\n"
            "   - Remove screen protector (may be causing issues)\n"
            "   - Remove the case (may press on screen edges)\n"
            "   - Ensure fingers are clean and dry\n"
            "2. Force restart:\n"
            "   - iPhone (Face ID): Quick press Volume Up, Volume Down, then hold Side button\n"
            "   - iPhone (Home button): Hold Home + Power\n"
            "   - Android: Hold Power + Volume Down for 10-15 seconds\n"
            "3. Software issues:\n"
            "   - An app may be causing the issue\n"
            "   - Boot into Safe Mode (Android): Power off > hold Power > tap 'Safe Mode'\n"
            "   - If touchscreen works in Safe Mode: A third-party app is the cause\n"
            "4. Ghost touches:\n"
            "   - Usually hardware (digitizer) damage\n"
            "   - Can be caused by screen damage, even without visible cracks\n"
            "   - Moisture under the screen can cause ghost touches\n"
            "5. Calibration (Android):\n"
            "   - Some Android devices have touch calibration in Settings\n"
            "   - Or try: Settings > Display > Touch sensitivity\n"
            "6. If hardware damage:\n"
            "   - Visible screen crack: Screen replacement needed\n"
            "   - No visible damage but still failing: Internal digitizer fault\n"
            "   - Check warranty status and request repair/replacement\n"
            "7. Temporary workaround: Use a Bluetooth mouse + OTG adapter for essential tasks"
        ),
    },
    {
        "category": "Mobile & Phone",
        "problem_title": "Mobile device storage full - can't update apps or OS",
        "problem_description": "User's phone shows 'Storage Almost Full' warning. Can't install updates, take photos, or download new apps due to lack of storage space.",
        "problem_keywords": "storage full, phone storage, no space, can't update, storage warning, clear storage, free space",
        "solution_steps": (
            "1. Check storage usage:\n"
            "   - iPhone: Settings > General > iPhone Storage\n"
            "   - Android: Settings > Storage\n"
            "   - Shows what's using space: Apps, Photos, Messages, System\n"
            "2. Quick wins:\n"
            "   - Clear Safari/Chrome cache and browsing data\n"
            "   - Delete downloaded files: Files app > Downloads\n"
            "   - Remove old voicemails\n"
            "   - Delete message threads with large attachments\n"
            "3. Photos and videos:\n"
            "   - Largest space consumer on most phones\n"
            "   - Enable cloud photo library (iCloud Photos, Google Photos)\n"
            "   - Set to 'Optimize iPhone Storage' (keeps thumbnails locally)\n"
            "   - Delete duplicate or unwanted photos\n"
            "4. Apps:\n"
            "   - iPhone Storage shows each app's size + documents/data\n"
            "   - Offload unused apps: Settings > App Store > Offload Unused Apps\n"
            "   - Reinstall apps to clear accumulated cache\n"
            "5. Messaging apps:\n"
            "   - WhatsApp, Teams: Media files accumulate\n"
            "   - WhatsApp: Settings > Storage > Manage Storage\n"
            "   - Delete old conversation media\n"
            "6. Company data:\n"
            "   - Offline files in OneDrive/SharePoint app\n"
            "   - Reduce offline email sync: Outlook > Settings > reduce to 1 week\n"
            "   - Clear Company Portal app cache\n"
            "7. Consider: If 16/32 GB device, request upgrade - modern apps need 64 GB minimum"
        ),
    },
    {
        "category": "Mobile & Phone",
        "problem_title": "Bluetooth pairing or connection issues with peripherals",
        "problem_description": "Company mobile device won't pair with Bluetooth headset, car audio, wireless keyboard, or other Bluetooth peripherals. Connection drops frequently.",
        "problem_keywords": "bluetooth, pairing failed, bluetooth disconnect, headset, car bluetooth, bluetooth not working, bluetooth audio",
        "solution_steps": (
            "1. Basic pairing steps:\n"
            "   - Ensure Bluetooth is ON on both devices\n"
            "   - Put the peripheral in pairing mode (usually hold power button)\n"
            "   - Phone: Settings > Bluetooth > scan for devices\n"
            "   - Stay within 1 meter during initial pairing\n"
            "2. If already paired but not connecting:\n"
            "   - 'Forget' the device: Settings > Bluetooth > info icon > Forget\n"
            "   - Reset the peripheral (check its manual for reset procedure)\n"
            "   - Re-pair from scratch\n"
            "3. Connection dropping:\n"
            "   - Interference: Wi-Fi, microwaves, USB 3.0 devices cause interference\n"
            "   - Distance: Bluetooth range is typically 10 meters (less through walls)\n"
            "   - Battery: Low battery on peripheral causes disconnects\n"
            "4. Audio issues:\n"
            "   - Audio routing: Ensure phone is set to Bluetooth audio output\n"
            "   - iPhone: Check Control Center > AirPlay icon > select Bluetooth device\n"
            "   - Phone calls vs media: Some headsets only support one profile\n"
            "5. Android-specific:\n"
            "   - Clear Bluetooth cache: Settings > Apps > Show System > Bluetooth > Clear Cache\n"
            "   - Developer Options > Bluetooth audio codec: Try changing codec\n"
            "   - Some Android phones have Bluetooth compatibility issues\n"
            "6. Multiple connections:\n"
            "   - Some peripherals only pair with one device at a time\n"
            "   - If paired with a laptop already: Disconnect from laptop first\n"
            "   - Or get a multipoint Bluetooth headset\n"
            "7. MDM restriction: Check if MDM policy restricts Bluetooth usage"
        ),
    },
    {
        "category": "Mobile & Phone",
        "problem_title": "Company email certificate or profile error on mobile",
        "problem_description": "Mobile device shows 'Cannot Verify Server Identity', 'Certificate not trusted', or email profile errors when connecting to company Exchange server.",
        "problem_keywords": "certificate error, server identity, email profile, exchange certificate, ssl error, trust certificate, ca certificate",
        "solution_steps": (
            "1. Understanding the error:\n"
            "   - 'Cannot Verify Server Identity': SSL certificate issue\n"
            "   - The phone doesn't trust the email server's certificate\n"
            "   - Common when using internal CA or self-signed certificates\n"
            "2. Internal CA certificate:\n"
            "   - If company uses internal CA: Root CA cert must be on the phone\n"
            "   - Deploy via MDM profile (Intune, JAMF, AirWatch)\n"
            "   - Or email the .cer file to the user for manual install\n"
            "3. Install CA cert on iPhone:\n"
            "   - Open the .cer file (from email or Safari download)\n"
            "   - Settings > General > Profiles > Install Profile\n"
            "   - THEN: Settings > General > About > Certificate Trust Settings > Enable Full Trust\n"
            "   - Both steps are required on iOS\n"
            "4. Install CA cert on Android:\n"
            "   - Settings > Security > Encryption & credentials > Install certificates\n"
            "   - Select the CA certificate file\n"
            "   - May require setting a screen lock PIN/passcode\n"
            "5. Certificate mismatch:\n"
            "   - The certificate name must match the server address\n"
            "   - If mail.company.com but cert says exchange.company.com: Won't work\n"
            "   - Fix: Use the correct hostname or update the certificate SAN\n"
            "6. Expired certificate:\n"
            "   - Server-side: Renew the Exchange/email server certificate\n"
            "   - After renewal: Users may need to re-accept or re-install profile\n"
            "7. MDM profile: Push the email configuration + certificates via MDM to avoid manual steps"
        ),
    },
    {
        "category": "Mobile & Phone",
        "problem_title": "Mobile device GPS or location services not working",
        "problem_description": "Company field worker's mobile device shows incorrect location, can't get GPS fix, or location-based company apps (field service, tracking) don't work.",
        "problem_keywords": "gps, location services, gps not working, wrong location, location inaccurate, field service, gps fix",
        "solution_steps": (
            "1. Check location services:\n"
            "   - iPhone: Settings > Privacy > Location Services > ON\n"
            "   - Android: Settings > Location > ON\n"
            "   - Per-app: Ensure the field service app has 'Always' or 'While Using' permission\n"
            "2. Location accuracy:\n"
            "   - iPhone: Settings > Privacy > Location Services > System Services > toggle off/on\n"
            "   - Android: Settings > Location > Improve accuracy > Wi-Fi scanning, Bluetooth scanning ON\n"
            "   - These help when GPS alone is insufficient (indoors, urban canyons)\n"
            "3. GPS signal issues:\n"
            "   - GPS needs clear sky view - won't work well indoors or in parking garages\n"
            "   - First fix after restart may take 1-5 minutes (cold start)\n"
            "   - Move outdoors with clear sky view for initial GPS lock\n"
            "4. Reset location:\n"
            "   - iPhone: Settings > General > Reset > Reset Location & Privacy\n"
            "   - Android: Clear cache for Google Maps / location services\n"
            "   - Toggle Airplane mode ON/OFF to reset radios\n"
            "5. Compass calibration:\n"
            "   - Open compass/maps app and calibrate if prompted\n"
            "   - Move phone in a figure-8 pattern\n"
            "   - Magnetic cases can interfere with compass\n"
            "6. App-specific:\n"
            "   - Check the app's location permission is set to 'Always' (not just 'While Using')\n"
            "   - Background location: iOS 13+ requires explicit 'Always Allow'\n"
            "   - Battery optimization may kill location tracking in background\n"
            "7. MDM: Ensure MDM policy allows location services and doesn't restrict GPS"
        ),
    },
    {
        "category": "Mobile & Phone",
        "problem_title": "Mobile device screen lock or passcode policy conflict",
        "problem_description": "MDM enforces a complex passcode policy but the user can't set it, or the device keeps locking too frequently, or biometrics are disabled by policy.",
        "problem_keywords": "screen lock, passcode policy, mdm passcode, device lock, biometrics disabled, pin policy, lock timeout",
        "solution_steps": (
            "1. MDM passcode requirements:\n"
            "   - Check what the MDM policy requires:\n"
            "   - Minimum length (e.g., 6+ characters)\n"
            "   - Complexity (alphanumeric, special characters)\n"
            "   - Expiration (change every X days)\n"
            "   - Lock timeout (auto-lock after X minutes)\n"
            "2. Can't set passcode:\n"
            "   - User may be using a simple 4-digit PIN when policy requires 6+\n"
            "   - Go to Settings > Face ID/Touch ID & Passcode > Change Passcode\n"
            "   - Choose 'Passcode Options' for alphanumeric or custom length\n"
            "3. Lock timeout too short:\n"
            "   - If MDM sets 1-minute timeout and user finds it disruptive:\n"
            "   - This is a security requirement - explain why it's necessary\n"
            "   - Suggest: Enable Face ID/Touch ID for faster unlock\n"
            "   - Request exception from security team if business need exists\n"
            "4. Biometrics disabled:\n"
            "   - Some MDM policies disable Face ID/Touch ID\n"
            "   - Usually a compliance requirement\n"
            "   - If not intended: Admin adjusts MDM policy to allow biometrics\n"
            "5. 'Device Not Compliant':\n"
            "   - Company Portal shows device not compliant with passcode policy\n"
            "   - Company Portal > Check Status > see what's non-compliant\n"
            "   - Set the required passcode to become compliant\n"
            "6. After policy change:\n"
            "   - Device may require immediate passcode change\n"
            "   - Force sync: Company Portal > Settings > Sync\n"
            "   - Restart device if policy isn't applying\n"
            "7. Lost passcode: If locked out, MDM admin can remotely reset passcode (iOS) or wipe device"
        ),
    },
    {
        "category": "Mobile & Phone",
        "problem_title": "Mobile device camera or microphone not working in apps",
        "problem_description": "Camera or microphone doesn't work in Teams, Zoom, or other company apps on the mobile device. Video calls show black screen or no audio from microphone.",
        "problem_keywords": "camera not working, microphone, video call, teams camera, zoom microphone, app permissions, mobile camera",
        "solution_steps": (
            "1. Check app permissions:\n"
            "   - iPhone: Settings > select app > Camera ON, Microphone ON\n"
            "   - Android: Settings > Apps > select app > Permissions > Camera, Microphone\n"
            "   - Permission must be explicitly granted\n"
            "2. Test with built-in apps:\n"
            "   - Camera app: Does the camera work outside of Teams/Zoom?\n"
            "   - Voice Memos (iOS) / Sound Recorder (Android): Does mic work?\n"
            "   - If built-in apps work: App-specific issue\n"
            "   - If built-in apps don't work: Hardware issue\n"
            "3. Teams/Zoom specific:\n"
            "   - Teams: In-call, tap the camera/mic icon to ensure it's enabled\n"
            "   - Check in-app settings: Teams > Settings > Meetings > verify audio/video settings\n"
            "   - Another call/app may be using the camera\n"
            "4. iOS specific:\n"
            "   - Screen Time restrictions may block camera\n"
            "   - Settings > Screen Time > Content & Privacy > Allowed Apps > Camera ON\n"
            "   - MDM may restrict camera (check MDM profile)\n"
            "5. Android specific:\n"
            "   - Some Android phones have a privacy toggle for camera/mic\n"
            "   - Quick settings panel: Camera access, Microphone access toggles\n"
            "   - Ensure these are not disabled\n"
            "6. Force close and restart:\n"
            "   - Force close the app completely\n"
            "   - Clear app cache (Android: Settings > Apps > app > Clear Cache)\n"
            "   - Restart the device\n"
            "7. MDM restriction: Some MDM policies disable camera entirely - check with IT admin"
        ),
    },
    {
        "category": "Mobile & Phone",
        "problem_title": "Mobile device overheating during use",
        "problem_description": "Company phone becomes excessively hot during calls, video meetings, or normal use. May display temperature warning and shut down or throttle performance.",
        "problem_keywords": "overheating, phone hot, temperature warning, thermal throttle, hot phone, shutdown heat, mobile heat",
        "solution_steps": (
            "1. Immediate response:\n"
            "   - Remove the phone case (traps heat)\n"
            "   - Move away from direct sunlight or heat sources\n"
            "   - Stop charging if currently on charger\n"
            "   - Close resource-intensive apps (video calls, navigation)\n"
            "2. Temperature warning:\n"
            "   - iPhone: Shows 'iPhone needs to cool down' and disables features\n"
            "   - Android: May show temperature warning or auto-shutdown\n"
            "   - Let the device cool naturally (don't put in freezer - causes condensation)\n"
            "3. Common causes:\n"
            "   - Extended video calls (Teams/Zoom) on cellular data\n"
            "   - GPS navigation + charging simultaneously\n"
            "   - Using phone while fast-charging\n"
            "   - Direct sunlight (dashboard, outdoor use)\n"
            "4. Background processes:\n"
            "   - A runaway app may be using excessive CPU\n"
            "   - Check battery usage for unusually high-consumption apps\n"
            "   - Force-close suspect apps\n"
            "5. Charging:\n"
            "   - Use only approved chargers (off-brand can cause heating)\n"
            "   - Fast charging generates more heat than standard charging\n"
            "   - Don't use phone heavily while charging\n"
            "6. Software:\n"
            "   - Update to latest OS (includes thermal management improvements)\n"
            "   - A recent update may have introduced a bug\n"
            "   - Check vendor forums for known thermal issues\n"
            "7. Hardware: If persistent overheating during normal use, the battery may be failing - request service"
        ),
    },
    {
        "category": "Mobile & Phone",
        "problem_title": "Work profile or personal/work separation issues",
        "problem_description": "Android work profile or iOS managed apps have issues separating personal and work data. Can't copy between profiles or apps appear in wrong profile.",
        "problem_keywords": "work profile, personal profile, byod, work separation, managed apps, android work, container, work data",
        "solution_steps": (
            "1. Understanding work profiles:\n"
            "   - Android: Work Profile creates a separate container for work apps\n"
            "   - iOS: Managed vs Unmanaged apps (MDM marks apps as managed)\n"
            "   - By design: Data cannot flow between personal and work\n"
            "2. Can't copy/paste between profiles:\n"
            "   - This is intentional (DLP policy)\n"
            "   - Work data stays in work apps; personal data stays in personal apps\n"
            "   - If needed for legitimate work: Request policy exception from IT\n"
            "3. Android Work Profile issues:\n"
            "   - Work apps have a briefcase badge icon\n"
            "   - Work profile can be toggled off: Settings > Accounts > Work Profile > toggle\n"
            "   - If work profile missing: Re-enroll in MDM\n"
            "4. App appearing in wrong profile:\n"
            "   - Some apps install in both profiles (two copies)\n"
            "   - Work contacts showing in personal dialer: This is a managed setting\n"
            "   - Admin can configure cross-profile data sharing policies\n"
            "5. iOS managed apps:\n"
            "   - Managed apps (deployed by MDM) have data restrictions\n"
            "   - 'Open In' management prevents sharing to personal apps\n"
            "   - Can't attach work files from unmanaged apps\n"
            "6. BYOD concerns:\n"
            "   - Only work profile data is managed and wipeable by company\n"
            "   - Personal data is NOT visible to or controlled by IT\n"
            "   - Reassure users: Company can only wipe work container\n"
            "7. Re-enrollment: If work profile is corrupted, remove MDM enrollment and re-enroll"
        ),
    },
    {
        "category": "Mobile & Phone",
        "problem_title": "Mobile device cellular data not working or slow",
        "problem_description": "Company phone can't connect to cellular data, shows 'No Service', or data speeds are extremely slow despite showing signal bars.",
        "problem_keywords": "no service, cellular data, mobile data, slow data, no signal, network not available, apn, carrier",
        "solution_steps": (
            "1. Basic checks:\n"
            "   - Is cellular data enabled? Settings > Cellular > Cellular Data ON\n"
            "   - Is Airplane Mode off?\n"
            "   - Is the SIM card properly inserted?\n"
            "   - Restart the device (resets cellular radio)\n"
            "2. No service:\n"
            "   - Remove and reinsert the SIM card\n"
            "   - Try the SIM in a different phone (is SIM bad or phone bad?)\n"
            "   - Contact carrier: Account may be suspended or SIM deactivated\n"
            "   - Check for carrier outage in the area\n"
            "3. APN settings:\n"
            "   - Corporate devices may need specific APN settings\n"
            "   - iPhone: Settings > Cellular > Cellular Data Network\n"
            "   - Android: Settings > Network > Mobile network > Access Point Names\n"
            "   - Get correct APN from carrier or IT department\n"
            "4. Slow data:\n"
            "   - Check signal strength: More bars = better speed\n"
            "   - Check network type: LTE/5G is fast, 3G/H+ is slow\n"
            "   - iPhone: Settings > Cellular > Cellular Data Options > Enable LTE\n"
            "   - Data throttling: Carrier may throttle after data cap\n"
            "5. Roaming:\n"
            "   - If traveling: Enable data roaming\n"
            "   - Settings > Cellular > Data Roaming ON\n"
            "   - Be aware of roaming charges\n"
            "6. Network reset:\n"
            "   - iPhone: Settings > General > Transfer or Reset > Reset Network Settings\n"
            "   - Android: Settings > System > Reset > Reset Network Settings\n"
            "   - This resets all network settings (Wi-Fi passwords lost)\n"
            "7. eSIM: If using eSIM, check it hasn't been deactivated and data plan is active"
        ),
    },
    {
        "category": "Mobile & Phone",
        "problem_title": "Mobile device compromised or jailbroken/rooted detected",
        "problem_description": "MDM has flagged a device as jailbroken (iOS) or rooted (Android). The device is non-compliant and may have restricted access to company resources.",
        "problem_keywords": "jailbroken, rooted, compromised device, mdm compliance, non-compliant, device integrity, device trust",
        "solution_steps": (
            "1. Understanding the risk:\n"
            "   - Jailbroken/rooted devices bypass OS security controls\n"
            "   - Malware can run with elevated privileges\n"
            "   - Encryption can be bypassed\n"
            "   - Company data is at risk on these devices\n"
            "2. MDM detection:\n"
            "   - MDM (Intune, JAMF, etc.) checks device integrity at each check-in\n"
            "   - Jailbreak/root detection marks device as non-compliant\n"
            "   - Conditional Access blocks non-compliant devices from company resources\n"
            "3. False positive:\n"
            "   - Some MDM detections have false positives\n"
            "   - Old OS versions may trigger false positives\n"
            "   - Developer devices may trigger detection\n"
            "   - Update OS to latest version and re-check compliance\n"
            "4. If genuinely jailbroken/rooted:\n"
            "   - The device must be restored to stock OS\n"
            "   - iPhone: Restore via iTunes/Finder (DFU mode restore)\n"
            "   - Android: Flash stock firmware\n"
            "   - Factory reset may not remove jailbreak/root\n"
            "5. BYOD policy:\n"
            "   - Company policy should prohibit jailbroken/rooted devices\n"
            "   - User may not realize a used phone was previously jailbroken\n"
            "   - Full restore resolves in most cases\n"
            "6. After restoring:\n"
            "   - Re-enroll in MDM\n"
            "   - Force compliance check: Company Portal > Check Status\n"
            "   - Wait for compliance state to update (may take 15-30 minutes)\n"
            "7. Prevention: Include device integrity Requirements in acceptable use policy"
        ),
    },
    {
        "category": "Mobile & Phone",
        "problem_title": "SharePoint or OneDrive mobile app sync issues",
        "problem_description": "SharePoint or OneDrive apps on mobile device won't sync files. Documents show as outdated, files fail to upload, or offline access doesn't work properly.",
        "problem_keywords": "sharepoint mobile, onedrive sync, file sync mobile, offline files, upload failed, onedrive error, sync error",
        "solution_steps": (
            "1. Check account:\n"
            "   - Open OneDrive app > Settings > Account\n"
            "   - Verify signed in with the correct work account\n"
            "   - If multiple accounts: Ensure work account is selected\n"
            "2. Network:\n"
            "   - Sync requires internet connection (Wi-Fi or cellular)\n"
            "   - OneDrive may be set to 'Upload only on Wi-Fi'\n"
            "   - Settings > Camera Upload > Use Mobile Network = ON if needed\n"
            "3. Storage:\n"
            "   - Device needs free space for offline files\n"
            "   - OneDrive cloud storage may be full (check quota)\n"
            "   - Admin: Check OneDrive storage allocation for the user\n"
            "4. Upload failures:\n"
            "   - File too large: OneDrive has 250 GB per file limit\n"
            "   - File name characters: No # % & { } \\ < > * ? / $ ! : @ + | = \n"
            "   - Path too long: Full path must be under 400 characters\n"
            "5. Offline access:\n"
            "   - Mark files as 'Available Offline' in the app\n"
            "   - OneDrive > File > three dots > Make Available Offline\n"
            "   - Offline files are cached and sync when reconnected\n"
            "6. Clear cache:\n"
            "   - iOS: Delete and reinstall the OneDrive app\n"
            "   - Android: Settings > Apps > OneDrive > Clear Cache\n"
            "   - Re-sign in and re-enable offline files\n"
            "7. SharePoint: For SharePoint libraries, ensure user has at least Read permission"
        ),
    },
    {
        "category": "Mobile & Phone",
        "problem_title": "Mobile device automatic OS update causing issues",
        "problem_description": "Mobile device automatically updated the OS and now apps crash, MDM enrollment broke, or device behavior changed. Need to prevent or manage updates.",
        "problem_keywords": "os update, auto update, ios update, android update, update broke, update management, defer update, mdm update",
        "solution_steps": (
            "1. Post-update issues:\n"
            "   - Apps crashing: Force close and reopen each app\n"
            "   - Update the crashing apps (may need compatibility update)\n"
            "   - Restart device after OS update completes\n"
            "2. MDM enrollment broken:\n"
            "   - Re-check enrollment: Company Portal > Check Status\n"
            "   - If enrollment certificate expired: Re-enroll the device\n"
            "   - Contact MDM admin to verify device enrollment status\n"
            "3. Prevent future auto-updates (iOS):\n"
            "   - MDM can deploy a 'Defer software updates' restriction\n"
            "   - Intune: Device Configuration > iOS > Restrictions > Delay OS updates (up to 90 days)\n"
            "   - JAMF: Configuration Profile > Restrictions > Software Update Delay\n"
            "4. Manage updates (Android):\n"
            "   - Android Enterprise: System Update policy in MDM\n"
            "   - Options: Auto, Windowed (schedule), Postpone (up to 30 days)\n"
            "   - Samsung/Knox: Additional update controls available\n"
            "5. Testing strategy:\n"
            "   - Test new OS versions on a pilot group first\n"
            "   - Verify all company apps work on the new OS\n"
            "   - Then lift the deferral for production devices\n"
            "6. Rollback:\n"
            "   - iOS: Cannot downgrade (Apple stops signing old versions)\n"
            "   - Android: Generally cannot downgrade without factory reset\n"
            "   - This is why deferral and testing are critical\n"
            "7. Communication: Notify users before major OS updates with instructions and known issues"
        ),
    },
    {
        "category": "Mobile & Phone",
        "problem_title": "Two-factor authentication app lost or device replaced",
        "problem_description": "User got a new phone or lost their device and can't access the authenticator app (Microsoft Authenticator, Google Authenticator). Locked out of accounts.",
        "problem_keywords": "authenticator app, 2fa lost, new phone, device replacement, authenticator transfer, locked out, mfa recovery",
        "solution_steps": (
            "1. Microsoft Authenticator (recommended):\n"
            "   - Has cloud backup feature\n"
            "   - iOS: Backed up to iCloud (Settings > Cloud Backup > ON)\n"
            "   - Android: Backed up to personal Microsoft account\n"
            "   - New phone: Install app > Begin recovery > sign in to restore\n"
            "2. Google Authenticator:\n"
            "   - Recent versions support Google account sync\n"
            "   - Old versions: No backup (codes only on that device)\n"
            "   - If no sync: Must use recovery codes or admin reset for each account\n"
            "3. IT admin reset:\n"
            "   - Azure AD: User needs MFA registration reset by admin\n"
            "   - Azure Portal > Users > select user > Authentication Methods > Require re-register\n"
            "   - Or issue a Temporary Access Pass for re-registration\n"
            "4. Recovery codes:\n"
            "   - Users should save recovery codes when setting up MFA\n"
            "   - If user has recovery codes: Use them for one-time access\n"
            "   - Then re-register the new device for MFA\n"
            "5. Device transfer (planned replacement):\n"
            "   - Before wiping old phone: Transfer authenticator accounts\n"
            "   - Microsoft Authenticator: Enable Cloud Backup first\n"
            "   - Google Authenticator: Use the Transfer Accounts feature\n"
            "6. Alternative MFA methods:\n"
            "   - While waiting for authenticator setup: Use SMS or phone call MFA\n"
            "   - Admin can enable alternative methods temporarily\n"
            "7. Prevention: Always register multiple MFA methods (app + phone number + security key)"
        ),
    },
    {
        "category": "Mobile & Phone",
        "problem_title": "Mobile printing from phone or tablet not working",
        "problem_description": "User needs to print from mobile device to company printer but can't find printers, print jobs fail, or output is formatted incorrectly.",
        "problem_keywords": "mobile printing, print from phone, airprint, mobile print, wireless print, company printer, print app",
        "solution_steps": (
            "1. iPhone (AirPrint):\n"
            "   - Requires AirPrint-compatible printer on the same network\n"
            "   - Open document > Share > Print > select printer\n"
            "   - If no printers shown: Phone and printer must be on same subnet/VLAN\n"
            "2. Android printing:\n"
            "   - Built-in: Settings > Connected devices > Printing\n"
            "   - Install printer manufacturer's plugin (HP Print Service, etc.)\n"
            "   - Google Cloud Print was retired - use alternatives\n"
            "3. Corporate print solutions:\n"
            "   - Many companies use print management (PaperCut, Printix, UniFlow)\n"
            "   - Install the vendor's mobile app\n"
            "   - Usually connects via email-to-print or cloud print gateway\n"
            "4. Network issues:\n"
            "   - Mobile devices on guest/Wi-Fi may not reach printer VLAN\n"
            "   - Ask IT to enable mDNS (Bonjour) across VLANs for AirPrint\n"
            "   - Or use a print server that's accessible from the mobile network\n"
            "5. Email-to-print:\n"
            "   - Some printer systems support email-to-print\n"
            "   - Send the document as attachment to a special email address\n"
            "   - The printer picks up and prints the job\n"
            "6. Formatting issues:\n"
            "   - Print as PDF first, then print the PDF\n"
            "   - Some apps don't format well for print (web pages especially)\n"
            "   - Use 'Reader View' for web pages before printing\n"
            "7. Secure print: If company uses badge-release printing, the mobile print job waits at the printer"
        ),
    },
    {
        "category": "Mobile & Phone",
        "problem_title": "Mobile device Wi-Fi keeps disconnecting or won't auto-connect",
        "problem_description": "Mobile phone or tablet repeatedly drops Wi-Fi connection, won't auto-reconnect to known networks, or shows 'authentication error' when connecting to corporate Wi-Fi.",
        "problem_keywords": "wifi disconnect, wifi auto-connect, wifi drops, authentication error, wifi forget, wifi reconnect, corporate wifi mobile",
        "solution_steps": (
            "1. Basic Wi-Fi troubleshooting:\n"
            "   - Toggle Wi-Fi off and on\n"
            "   - Forget the network and reconnect\n"
            "   - Settings > Wi-Fi > select network > Forget > reconnect with password\n"
            "2. Network settings reset:\n"
            "   - iOS: Settings > General > Transfer or Reset > Reset Network Settings\n"
            "   - Android: Settings > System > Reset > Reset Wi-Fi, mobile & Bluetooth\n"
            "   - Warning: This removes all saved Wi-Fi passwords\n"
            "3. Corporate Wi-Fi (802.1X):\n"
            "   - Ensure correct EAP type selected (PEAP, EAP-TLS)\n"
            "   - Certificate may need to be installed\n"
            "   - MDM can push Wi-Fi profiles with correct settings\n"
            "   - iOS: Install CA certificate via profile\n"
            "4. Wi-Fi optimization:\n"
            "   - Disable 'Smart network switch' or 'Wi-Fi assist'\n"
            "   - These switch to cellular when Wi-Fi is weak\n"
            "   - Android: Disable 'Switch to mobile data automatically'\n"
            "5. Router side: Check if MAC filtering is enabled, or max client limit is reached on the access point"
        ),
    },
    {
        "category": "Mobile & Phone",
        "problem_title": "Mobile device microphone or speaker not working in calls",
        "problem_description": "Phone microphone not picking up voice during calls or Teams/Zoom meetings. Speaker sound muffled or no audio output. Other party can't hear or user can't hear them.",
        "problem_keywords": "microphone not working, speaker no sound, call audio, teams audio mobile, phone mic, speaker muffled, call quality mobile",
        "solution_steps": (
            "1. Basic checks:\n"
            "   - Remove phone case (may block microphone)\n"
            "   - Clean microphone and speaker openings\n"
            "   - Check volume is up and not on mute\n"
            "   - Test with Voice Recorder app\n"
            "2. Bluetooth interference:\n"
            "   - Disable Bluetooth to rule out audio routing to BT device\n"
            "   - Check: Audio may be routing to car Bluetooth or headset\n"
            "   - In Teams/Zoom: Check audio output device selection\n"
            "3. App permissions:\n"
            "   - iOS: Settings > Privacy > Microphone > enable for app\n"
            "   - Android: Settings > Apps > [app] > Permissions > Microphone\n"
            "   - Deny and re-grant permission if issues persist\n"
            "4. Do Not Disturb:\n"
            "   - DND mode can silence call audio\n"
            "   - Check Focus modes (iOS) or DND (Android)\n"
            "   - Disable during troubleshooting\n"
            "5. Hardware test: Try speakerphone mode, try with wired headset, try recording video. If mic works in some scenarios but not others, it's a software issue"
        ),
    },
]

DIAGNOSTIC_TREE = {
    "category": "Mobile & Phone",
    "root": {
        "title": "Mobile Device Troubleshooting",
        "node_type": "question",
        "question_text": "What mobile device issue are you experiencing?",
        "children": [
            {
                "title": "Email not syncing on phone",
                "node_type": "question",
                "question_text": "Which email app are you using?",
                "children": [
                    {
                        "title": "Outlook mobile app",
                        "node_type": "solution",
                        "solution_text": "1. Remove account: Outlook > Settings > tap account > Delete\n2. Re-add account with corporate email\n3. Complete MFA prompt if required\n4. Check Conditional Access: Organization may require Outlook app specifically\n5. Verify mailbox is active: Test login at outlook.office365.com\n6. Ensure date/time is set to automatic on phone"
                    },
                    {
                        "title": "Native Mail app (iOS/Android)",
                        "node_type": "solution",
                        "solution_text": "1. Delete the email account from phone Settings\n2. Re-add as Microsoft Exchange\n3. Server: outlook.office365.com (for M365)\n4. Enter full email and password\n5. Accept certificate prompts\n6. App password may be needed if MFA blocks native apps\n7. Consider switching to Outlook mobile app for better compatibility"
                    }
                ]
            },
            {
                "title": "Phone can't connect to corporate Wi-Fi",
                "node_type": "solution",
                "solution_text": "1. Forget network and reconnect\n2. For 802.1X: Use full email as username, EAP method must match\n3. Certificate-based: Check cert is installed (Settings > Profiles/Security)\n4. Disable Private/Random MAC address for this network\n5. If MDM-managed: Sync device to get Wi-Fi profile\n6. Personal devices may be restricted to guest network only"
            },
            {
                "title": "MDM/Intune enrollment issues",
                "node_type": "solution",
                "solution_text": "1. Verify user has Intune license\n2. Check enrollment restrictions in Intune admin portal\n3. Update device OS to latest version\n4. Download Company Portal app\n5. iOS: Accept management profile in Settings > Device Management\n6. Android: Accept all permissions, set up Work Profile\n7. If already enrolled: Unenroll first, then re-enroll\n8. Clear Company Portal app data and retry"
            },
            {
                "title": "Lost or stolen device",
                "node_type": "solution",
                "solution_text": "1. Reset user's corporate password immediately\n2. Revoke active sessions\n3. Remote wipe via Intune: 'Retire' for BYOD, 'Wipe' for company-owned\n4. Or Exchange ActiveSync wipe\n5. Help locate: icloud.com/find (iPhone) or google.com/android/find (Android)\n6. Contact carrier to suspend SIM if company-owned\n7. Document: Serial number, data on device, encryption status"
            },
            {
                "title": "Calls/meetings not working on mobile",
                "node_type": "solution",
                "solution_text": "1. Update Teams/Zoom app to latest version\n2. Check permissions: Microphone and Camera must be allowed\n3. Check phone is not on Do Not Disturb mode\n4. Check Bluetooth: Audio may route to disconnected device\n5. Disable battery optimization for the app\n6. Enable Background App Refresh (iOS)\n7. Poor audio: Switch between Wi-Fi and cellular\n8. Clear app cache and restart"
            }
        ]
    }
}
