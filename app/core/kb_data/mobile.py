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
