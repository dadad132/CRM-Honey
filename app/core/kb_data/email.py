"""Email and Outlook troubleshooting articles and diagnostic tree."""

ARTICLES = [
    {
        "category": "Email & Outlook",
        "problem_title": "Outlook stuck on Loading Profile or won't open",
        "problem_description": "Microsoft Outlook is stuck on 'Loading Profile' screen, hangs during startup, or crashes immediately when opening.",
        "problem_keywords": "outlook loading profile, outlook won't open, outlook stuck, outlook crash, outlook hangs, outlook startup",
        "solution_steps": (
            "1. Start Outlook in Safe Mode:\n"
            "   - Hold Ctrl and click the Outlook icon, or\n"
            "   - Win+R: outlook.exe /safe\n"
            "   - If it works in Safe Mode, an add-in is the problem\n"
            "2. Disable add-ins:\n"
            "   - In Safe Mode: File > Options > Add-ins > COM Add-ins > Go\n"
            "   - Uncheck all add-ins > OK > restart normally\n"
            "   - Enable add-ins one at a time to find the culprit\n"
            "3. Repair the Outlook data file (.ost or .pst):\n"
            "   - Close Outlook\n"
            "   - Find SCANPST.EXE:\n"
            "   - C:\\Program Files\\Microsoft Office\\root\\Office16\\SCANPST.EXE\n"
            "   - Or: C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\SCANPST.EXE\n"
            "   - Browse to the .ost/.pst file and click 'Start'\n"
            "4. Create a new Outlook profile:\n"
            "   - Control Panel > Mail > Show Profiles > Add\n"
            "   - Set up the email account in the new profile\n"
            "   - Set the new profile as default\n"
            "5. Delete the Navigation Pane settings file:\n"
            "   - Close Outlook > Delete: %appdata%\\Microsoft\\Outlook\\profilename.xml\n"
            "6. Repair Office installation:\n"
            "   - Settings > Apps > Microsoft Office > Modify > Online Repair"
        ),
    },
    {
        "category": "Email & Outlook",
        "problem_title": "Outlook not receiving emails",
        "problem_description": "Outlook is not receiving new emails. Send works but inbox does not update. May work in webmail (OWA) but not in the desktop client.",
        "problem_keywords": "not receiving email, no new email, inbox not updating, outlook receive, email missing, inbox empty",
        "solution_steps": (
            "1. Check webmail (OWA/Outlook.com) - if emails are there, it's a client issue\n"
            "2. Force send/receive: Press F9 or click Send/Receive All Folders\n"
            "3. Check if working offline:\n"
            "   - Look at bottom status bar for 'Working Offline'\n"
            "   - Send/Receive tab > Work Offline (toggle off)\n"
            "4. Check Focused/Other inbox:\n"
            "   - Emails may be in the 'Other' tab instead of 'Focused'\n"
            "   - View > Show Focused Inbox > toggle off\n"
            "5. Check rules:\n"
            "   - A rule may be moving/deleting incoming emails\n"
            "   - File > Manage Rules & Alerts > review all rules\n"
            "6. Check Junk/Spam folder\n"
            "7. Recreate the OST file:\n"
            "   - Close Outlook\n"
            "   - Rename: %localappdata%\\Microsoft\\Outlook\\*.ost to .ost.bak\n"
            "   - Reopen Outlook - it will recreate the OST from server\n"
            "8. Check mailbox quota:\n"
            "   - File > Account Settings > double-click account\n"
            "   - Full mailbox may stop receiving\n"
            "9. Remove and re-add the email account in Outlook"
        ),
    },
    {
        "category": "Email & Outlook",
        "problem_title": "Outlook keeps asking for password repeatedly",
        "problem_description": "Outlook constantly prompts for password. Even after entering the correct password, it asks again within minutes or after restart.",
        "problem_keywords": "outlook password, keeps asking password, password prompt, outlook login, credential prompt, authentication",
        "solution_steps": (
            "1. Clear cached credentials:\n"
            "   - Control Panel > Credential Manager > Windows Credentials\n"
            "   - Remove all entries with 'outlook', 'office', or 'microsoft' in them\n"
            "2. Check Outlook authentication:\n"
            "   - File > Account Settings > double-click account > More Settings\n"
            "   - Security tab: Check 'Logon network security' is set to 'Anonymous Authentication' or 'Negotiate'\n"
            "3. Enable Modern Authentication:\n"
            "   - Registry: HKCU\\Software\\Microsoft\\Office\\16.0\\Common\\Identity\n"
            "   - DWORD: EnableADAL = 1\n"
            "   - DWORD: Version = 1\n"
            "4. For Microsoft 365/Exchange Online:\n"
            "   - Modern Auth must be enabled on the tenant\n"
            "   - Check if MFA is enabled - may need an App Password\n"
            "5. Create a new Outlook profile:\n"
            "   - Control Panel > Mail > Show Profiles > Add\n"
            "6. Check account password hasn't expired\n"
            "7. Repair Office: Settings > Apps > Microsoft Office > Modify > Online Repair\n"
            "8. Update Office to the latest version"
        ),
    },
    {
        "category": "Email & Outlook",
        "problem_title": "Outlook search not working or returning no results",
        "problem_description": "Searching for emails in Outlook returns no results or incomplete results. Search box may not respond.",
        "problem_keywords": "outlook search, search not working, search no results, search broken, find email, outlook search index",
        "solution_steps": (
            "1. Rebuild the Outlook search index:\n"
            "   - File > Options > Search > Indexing Options\n"
            "   - Click 'Advanced' > Rebuild > OK\n"
            "   - Wait for indexing to complete (may take hours for large mailboxes)\n"
            "2. Check indexing status:\n"
            "   - In Outlook search bar, click 'Search Tools' > 'Indexing Status'\n"
            "   - Wait until it shows 0 items remaining\n"
            "3. Verify Outlook is included in search index:\n"
            "   - Indexing Options > Modify > check 'Microsoft Outlook'\n"
            "4. Repair Outlook data file:\n"
            "   - Use SCANPST.EXE on the OST/PST file\n"
            "5. Add registry fix for Windows 11 search:\n"
            "   - HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Search\n"
            "   - DWORD: PreventIndexingOutlook = 0\n"
            "6. Run sfc /scannow to repair system files\n"
            "7. If using Exchange Online, try searching in OWA to verify results\n"
            "8. Re-create Outlook profile as last resort"
        ),
    },
    {
        "category": "Email & Outlook",
        "problem_title": "Outlook calendar sync issues",
        "problem_description": "Calendar appointments not syncing between devices. Meetings showing on phone but not on desktop or vice versa. Shared calendars not updating.",
        "problem_keywords": "calendar sync, calendar not updating, meeting missing, shared calendar, calendar not syncing, outlook calendar",
        "solution_steps": (
            "1. Force sync:\n"
            "   - Send/Receive tab > Send/Receive All Folders (F9)\n"
            "2. Check which calendar you're viewing:\n"
            "   - Make sure the correct calendar is checked in the calendar pane\n"
            "   - Calendar events may be on a sub-calendar you're not viewing\n"
            "3. For shared calendars:\n"
            "   - Remove the shared calendar > re-add it\n"
            "   - Verify you have the right permissions (at least Reviewer)\n"
            "4. Check online mode vs cached mode:\n"
            "   - File > Account Settings > double-click account > More Settings > Advanced\n"
            "   - Try toggling 'Use Cached Exchange Mode'\n"
            "   - If cached, increase the 'Mail to keep offline' slider\n"
            "5. On mobile devices:\n"
            "   - Remove and re-add the account\n"
            "   - Check sync settings (should be Push or every 15 minutes)\n"
            "6. Clear the local calendar cache:\n"
            "   - Close Outlook, rename the .ost file, reopen Outlook\n"
            "7. For teams meeting issues:\n"
            "   - Ensure Teams add-in is enabled in Outlook\n"
            "   - File > Options > Add-ins > check Teams Meeting Add-in"
        ),
    },
    {
        "category": "Email & Outlook",
        "problem_title": "OST or PST file corrupted",
        "problem_description": "Outlook shows errors about the data file. Cannot open or access emails. May see 'The file is not an Outlook data file (.ost)' or similar errors.",
        "problem_keywords": "ost corrupt, pst corrupt, data file error, scanpst, ost repair, pst repair, outlook data file",
        "solution_steps": (
            "1. Repair with Inbox Repair Tool (SCANPST.EXE):\n"
            "   - Close Outlook completely\n"
            "   - Find SCANPST:\n"
            "   - Office 365/2019: C:\\Program Files\\Microsoft Office\\root\\Office16\\SCANPST.EXE\n"
            "   - Office 2016: C:\\Program Files (x86)\\Microsoft Office\\Office16\\SCANPST.EXE\n"
            "   - Browse to the data file:\n"
            "   - OST: %localappdata%\\Microsoft\\Outlook\\\n"
            "   - PST: Check File > Account Settings > Data Files for location\n"
            "   - Click 'Start' > repair > 'Repair'\n"
            "   - May need to run multiple times\n"
            "2. If OST is corrupt beyond repair:\n"
            "   - Delete the OST file (emails are still on the server)\n"
            "   - Reopen Outlook - it will recreate the OST and sync from Exchange/365\n"
            "3. If PST is corrupt beyond repair:\n"
            "   - PST files are local only - there's no server copy\n"
            "   - Try third-party PST repair tools (Stellar, Kernel PST Repair)\n"
            "   - Check for backup copies of the PST file\n"
            "4. Prevent future corruption:\n"
            "   - Don't store PST on network drives\n"
            "   - Close Outlook properly (don't force-close)\n"
            "   - Keep PST under 10GB for best reliability"
        ),
    },
    {
        "category": "Email & Outlook",
        "problem_title": "Cannot send emails - stuck in Outbox",
        "problem_description": "Emails are stuck in the Outbox and won't send. Clicking Send/Receive doesn't help. May show errors in the status bar.",
        "problem_keywords": "stuck outbox, cannot send, email stuck, send error, outbox, outlook send fail",
        "solution_steps": (
            "1. Check if working offline:\n"
            "   - Send/Receive tab > 'Work Offline' button should NOT be highlighted\n"
            "2. Check for large attachments:\n"
            "   - Most email servers reject attachments > 25-50MB\n"
            "   - Open the stuck email from Outbox, reduce/remove attachment, resend\n"
            "3. Move the stuck email:\n"
            "   - Open Outbox > click and drag the email to Drafts folder\n"
            "   - Edit and try sending again\n"
            "4. If you can't open the stuck email:\n"
            "   - Start Outlook in Safe Mode: outlook.exe /safe\n"
            "   - Delete the email from Outbox\n"
            "5. Check SMTP settings:\n"
            "   - File > Account Settings > double-click account\n"
            "   - Verify outgoing server address and port\n"
            "   - Common SMTP ports: 587 (TLS), 465 (SSL), 25 (unencrypted)\n"
            "6. For Exchange/365 accounts:\n"
            "   - Check if mailbox is over quota (can't send when full)\n"
            "   - File > Account Settings check mailbox size\n"
            "7. Recreate the Send/Receive group:\n"
            "   - Send/Receive tab > Send/Receive Groups > Define\n"
            "8. Run Outlook in Safe Mode to rule out add-in interference"
        ),
    },
    {
        "category": "Email & Outlook",
        "problem_title": "Outlook mailbox is full - over quota",
        "problem_description": "Receiving 'Your mailbox is full' or 'Your mailbox is almost full' messages. Cannot send or receive new emails.",
        "problem_keywords": "mailbox full, over quota, mailbox size, mailbox limit, storage full, outlook quota, email quota",
        "solution_steps": (
            "1. Check mailbox size:\n"
            "   - File > Info > Mailbox Settings shows size and quota\n"
            "2. Empty Deleted Items:\n"
            "   - Right-click Deleted Items > Empty Folder\n"
            "   - Also empty: Junk Email folder\n"
            "3. Empty 'Recoverable Items' (hidden deleted items):\n"
            "   - In Outlook OWA: Deleted Items > 'Recover items deleted from this folder'\n"
            "   - Select all > Purge\n"
            "4. Find large emails:\n"
            "   - Search: size:>5MB (finds emails larger than 5MB)\n"
            "   - Sort by size and delete large ones\n"
            "   - Or use: Folder Properties > Folder Size to find large folders\n"
            "5. Archive old emails:\n"
            "   - File > Info > Cleanup Tools > Archive\n"
            "   - Set an archive date (e.g., older than 1 year)\n"
            "6. For Exchange/M365: Admin can increase mailbox quota\n"
            "7. Use Online Archive if available (M365 E3/E5)\n"
            "8. Clean up old calendar events and sent items\n"
            "9. Save attachments to OneDrive/SharePoint and delete from email"
        ),
    },
    {
        "category": "Email & Outlook",
        "problem_title": "Outlook rules not working or not applying",
        "problem_description": "Email rules created in Outlook are not processing incoming emails. Rules may work in OWA but not in the desktop client or vice versa.",
        "problem_keywords": "outlook rules, rules not working, email rules, filter not working, auto move, rules broken",
        "solution_steps": (
            "1. Check rule type:\n"
            "   - Client-only rules (with specific conditions) only run when Outlook is open\n"
            "   - Server-side rules run even when Outlook is closed\n"
            "   - Rules marked '(client-only)' need desktop Outlook running\n"
            "2. Check rule order:\n"
            "   - File > Manage Rules & Alerts\n"
            "   - Rules process top-to-bottom\n"
            "   - A rule higher in the list with 'stop processing more rules' can block others\n"
            "3. Check if rules are enabled:\n"
            "   - Each rule needs a checkmark next to it\n"
            "4. Reset rules cache:\n"
            "   - Close Outlook\n"
            "   - Win+R: outlook.exe /cleanrules\n"
            "   - This DELETES all rules - recreate them after\n"
            "5. Rules may be disabled if they have errors:\n"
            "   - Re-create the rule instead of editing broken ones\n"
            "6. For Exchange/365:\n"
            "   - Mailbox rules have a size limit (256KB by default)\n"
            "   - Too many/complex rules can exceed the limit\n"
            "   - Simplify rules or increase with PowerShell\n"
            "7. Recreate rules in OWA for server-side processing"
        ),
    },
    {
        "category": "Email & Outlook",
        "problem_title": "Outlook autodiscover not working - cannot configure email",
        "problem_description": "Outlook cannot automatically configure the email account. Autodiscover fails, and manual configuration is needed. Error: 'Encrypted connection not available'.",
        "problem_keywords": "autodiscover, auto discover, configure email, email setup, outlook setup, encrypted connection",
        "solution_steps": (
            "1. Test Autodiscover:\n"
            "   - Ctrl+click Outlook tray icon > Test Email AutoConfiguration\n"
            "   - Enter email and password > Test\n"
            "   - Check which method succeeded/failed\n"
            "2. If Autodiscover fails:\n"
            "   - Check DNS records: nslookup -type=CNAME autodiscover.yourdomain.com\n"
            "   - Should point to autodiscover.outlook.com (for M365)\n"
            "   - Or check SRV record: nslookup -type=SRV _autodiscover._tcp.yourdomain.com\n"
            "3. For Exchange on-premise:\n"
            "   - Check Autodiscover virtual directory in EAC/EMS\n"
            "   - Test: https://autodiscover.yourdomain.com/autodiscover/autodiscover.xml\n"
            "   - Check SSL certificate is valid and trusted\n"
            "4. Clear Autodiscover cache:\n"
            "   - Delete: %localappdata%\\Microsoft\\Outlook\\16\\AutoD*.xml\n"
            "5. If manual configuration needed:\n"
            "   - For M365: outlook.office365.com, port 443, HTTPS\n"
            "   - For Exchange: Use your Exchange server's URL\n"
            "6. Check that required ports are open:\n"
            "   - HTTPS (443) to autodiscover endpoint\n"
            "   - Firewall/proxy may be blocking"
        ),
    },
    {
        "category": "Email & Outlook",
        "problem_title": "Email bounce back with NDR error message",
        "problem_description": "Sent emails are returned with a Non-Delivery Report (NDR/bounce). Various error codes like 550, 553, 5.7.1, 5.1.1, etc.",
        "problem_keywords": "bounce back, ndr, undeliverable, delivery failed, 550, 553, 5.7.1, 5.1.1, email rejected, email returned",
        "solution_steps": (
            "1. Common NDR codes and fixes:\n"
            "   - 5.1.1 (Bad destination mailbox): Recipient address doesn't exist - check spelling\n"
            "   - 5.2.2 (Mailbox full): Recipient's mailbox is over quota - contact them\n"
            "   - 5.4.1 (Recipient address rejected): DNS/routing issue on recipient side\n"
            "   - 5.5.0 (SMTP error): Server configuration issue\n"
            "   - 5.7.1 (Relay denied): Your server isn't allowed to send to that domain\n"
            "   - 5.7.23 (SPF failure): Your domain's SPF record is missing or wrong\n"
            "2. For 5.7.x (authentication/relay errors):\n"
            "   - Check SMTP authentication is enabled\n"
            "   - Verify your email domain's SPF, DKIM, and DMARC DNS records\n"
            "3. For 5.1.x (address errors):\n"
            "   - Double-check the recipient email address\n"
            "   - Remove the address from autocomplete: start typing, press X on the suggestion\n"
            "4. For 4.x.x (temporary failures):\n"
            "   - These are temporary - the server will retry automatically\n"
            "   - Usually resolves within hours\n"
            "5. If all emails bounce: Check your domain isn't on a blacklist\n"
            "   - Use mxtoolbox.com/blacklists.aspx to check"
        ),
    },
    {
        "category": "Email & Outlook",
        "problem_title": "Outlook high memory or CPU usage",
        "problem_description": "Outlook is using excessive memory (RAM) or CPU. System becomes slow when Outlook is running. Outlook may freeze or become unresponsive.",
        "problem_keywords": "outlook slow, outlook memory, outlook cpu, outlook freeze, outlook laggy, high memory outlook, high cpu outlook",
        "solution_steps": (
            "1. Check mailbox size:\n"
            "   - Very large mailboxes (10GB+) cause high resource use\n"
            "   - Archive old emails to reduce size\n"
            "2. Disable add-ins:\n"
            "   - File > Options > Add-ins > COM Add-ins > Go\n"
            "   - Disable all, restart, enable one at a time\n"
            "   - Common culprits: Adobe Acrobat, Skype, old CRM plugins\n"
            "3. Reduce cached mode timeline:\n"
            "   - File > Account Settings > double-click account\n"
            "   - Reduce 'Mail to keep offline' to 3 or 6 months\n"
            "4. Compact the OST file:\n"
            "   - File > Account Settings > Data Files > select file > Settings > Compact Now\n"
            "5. Disable RSS feeds:\n"
            "   - File > Options > Advanced > uncheck RSS-related options\n"
            "6. Use Hardware Graphics Acceleration:\n"
            "   - File > Options > Advanced > check 'Disable hardware graphics acceleration' (paradoxically, this helps sometimes)\n"
            "7. Repair Office: Settings > Apps > Microsoft Office > Modify > Online Repair\n"
            "8. Create a new Outlook profile to test"
        ),
    },
    {
        "category": "Email & Outlook",
        "problem_title": "Out of Office / automatic replies not working",
        "problem_description": "Configured Out of Office (automatic replies) but senders are not receiving the auto-reply. OOF may show as enabled but doesn't actually send.",
        "problem_keywords": "out of office, automatic reply, oof, auto reply, vacation message, out of office not working",
        "solution_steps": (
            "1. Verify OOF is enabled:\n"
            "   - In Outlook: File > Automatic Replies > Send automatic replies\n"
            "   - Check the date range is correct (if using scheduled dates)\n"
            "2. Check which replies are configured:\n"
            "   - 'Inside My Organization' tab: replies to internal contacts\n"
            "   - 'Outside My Organization' tab: replies to external contacts\n"
            "   - Check 'My contacts only' vs 'Anyone outside my organization'\n"
            "3. OOF rules:\n"
            "   - Auto-replies are sent once per sender (not every time)\n"
            "   - The cache resets when OOF is turned off and on again\n"
            "4. Test from a different account:\n"
            "   - Send a test email from an external account\n"
            "   - Check the sender's Junk/Spam folder for the auto-reply\n"
            "5. For Exchange/M365:\n"
            "   - Check mailbox in Exchange Admin Center\n"
            "   - PowerShell: Get-MailboxAutoReplyConfiguration -Identity user@domain.com\n"
            "6. Transport rules may block auto-replies:\n"
            "   - Check Exchange transport rules for any that affect auto-replies\n"
            "7. Enable OOF via OWA as an alternative"
        ),
    },
    {
        "category": "Email & Outlook",
        "problem_title": "Email attachments won't open or are blocked",
        "problem_description": "Cannot open attachments in Outlook. May see 'Outlook blocked access to the following potentially unsafe attachments' or attachments show as winmail.dat.",
        "problem_keywords": "attachment blocked, cannot open attachment, unsafe attachment, winmail.dat, blocked file type, outlook attachment",
        "solution_steps": (
            "1. If 'potentially unsafe attachment' blocked:\n"
            "   - Outlook blocks .exe, .bat, .js, .vbs, etc. by default\n"
            "   - Have sender re-send in a .zip file (not password protected)\n"
            "   - Or have sender upload to OneDrive/SharePoint and share a link\n"
            "2. To unblock specific file types (admin):\n"
            "   - Registry: HKCU\\Software\\Microsoft\\Office\\16.0\\Outlook\\Security\n"
            "   - Add String: Level1Remove = .exe;.bat (file types to unblock)\n"
            "   - Warning: This reduces security\n"
            "3. Attachments showing as winmail.dat:\n"
            "   - Sender is using Rich Text Format (RTF)\n"
            "   - Fix on sender side: New email > Format Text > change to HTML\n"
            "   - Or: File > Options > Mail > Compose in HTML format\n"
            "   - Recipient workaround: Use winmaildat.com to decode\n"
            "4. Cannot preview attachments:\n"
            "   - Install the application for that file type\n"
            "   - File > Options > Trust Center > Trust Center Settings > Attachment Handling\n"
            "   - Check 'Turn off Attachment Preview' is not checked\n"
            "5. For large attachments (>25MB):\n"
            "   - Use OneDrive/SharePoint integration to send links instead"
        ),
    },
    {
        "category": "Email & Outlook",
        "problem_title": "Outlook error 'Cannot start Microsoft Outlook. Cannot open the Outlook window'",
        "problem_description": "Outlook fails with 'Cannot start Microsoft Outlook. Cannot open the Outlook window. The set of folders cannot be opened.' error.",
        "problem_keywords": "cannot start outlook, cannot open outlook window, set of folders, outlook error start, 0x80040154",
        "solution_steps": (
            "1. Reset the Navigation Pane:\n"
            "   - Win+R: outlook.exe /resetnavpane\n"
            "2. Start in Safe Mode:\n"
            "   - Win+R: outlook.exe /safe\n"
            "   - If it works, disable add-ins one by one\n"
            "3. Repair the Outlook data file:\n"
            "   - Find and run SCANPST.EXE\n"
            "   - Browse to the .ost / .pst file in %localappdata%\\Microsoft\\Outlook\\\n"
            "4. Delete the Outlook profile and recreate:\n"
            "   - Control Panel > Mail > Show Profiles\n"
            "   - Remove the profile > Add new one\n"
            "5. Rename/delete the OST file:\n"
            "   - Close Outlook completely\n"
            "   - Go to %localappdata%\\Microsoft\\Outlook\\\n"
            "   - Rename .ost file to .ost.bak\n"
            "   - Reopen Outlook to recreate it\n"
            "6. Repair Office:\n"
            "   - Settings > Apps > Microsoft Office > Modify > Quick Repair first\n"
            "   - If that fails, try Online Repair\n"
            "7. Check for Compatibility Mode:\n"
            "   - Right-click Outlook shortcut > Properties > Compatibility\n"
            "   - Ensure 'Run in compatibility mode' is NOT checked"
        ),
    },
]

DIAGNOSTIC_TREE = {
    "category": "Email & Outlook",
    "root": {
        "title": "Email Troubleshooting",
        "node_type": "question",
        "question_text": "What email problem are you experiencing?",
        "children": [
            {
                "title": "Outlook won't open or crashes",
                "node_type": "question",
                "question_text": "Does Outlook open in Safe Mode? (Win+R > outlook.exe /safe)",
                "children": [
                    {
                        "title": "Yes - Safe Mode works",
                        "node_type": "solution",
                        "solution_text": "An add-in is causing the issue:\n1. In Safe Mode: File > Options > Add-ins\n2. COM Add-ins > Go > Uncheck ALL add-ins > OK\n3. Restart Outlook normally\n4. If it works, enable add-ins one at a time to find the culprit\n5. Common problem add-ins: Adobe Acrobat, old CRM plugins, browser toolbars\n6. Keep the problem add-in disabled or update it"
                    },
                    {
                        "title": "No - Safe Mode also fails",
                        "node_type": "solution",
                        "solution_text": "The Outlook profile or data file is likely corrupt:\n1. Try resetting nav pane: Win+R > outlook.exe /resetnavpane\n2. Repair the data file with SCANPST.EXE:\n   - Find it in C:\\Program Files\\Microsoft Office\\root\\Office16\\\n   - Run it on the .ost file in %localappdata%\\Microsoft\\Outlook\\\n3. If repair doesn't work, delete the .ost file (Outlook will recreate it)\n4. Create a new Outlook profile:\n   - Control Panel > Mail > Show Profiles > Add\n5. If still failing: Repair Office installation:\n   - Settings > Apps > Microsoft Office > Modify > Online Repair"
                    }
                ]
            },
            {
                "title": "Not receiving emails",
                "node_type": "question",
                "question_text": "Can you see the emails in webmail (OWA / outlook.com)?",
                "children": [
                    {
                        "title": "Yes - webmail has the emails",
                        "node_type": "solution",
                        "solution_text": "Desktop Outlook sync issue:\n1. Check if Working Offline: Send/Receive > Work Offline (toggle off)\n2. Force sync: Press F9\n3. Check Focused vs Other inbox tab\n4. Check Rules: File > Manage Rules - a rule may be moving emails\n5. Recreate OST: Close Outlook > rename .ost file > reopen\n6. Check cached mode settings: reduce to 3 months\n7. Remove and re-add the account"
                    },
                    {
                        "title": "No - webmail also missing emails",
                        "node_type": "solution",
                        "solution_text": "Server-side issue:\n1. Check Junk/Spam folder in webmail\n2. Check mailbox quota - full mailbox blocks new mail\n3. Check mail flow rules in Exchange Admin Center\n4. Check if the sender's domain is blacklisted\n5. Ask sender to check their bounce-back/NDR message\n6. Check transport rules in Exchange/M365 admin\n7. Verify MX DNS records: nslookup -type=mx yourdomain.com"
                    }
                ]
            },
            {
                "title": "Cannot send emails",
                "node_type": "solution",
                "solution_text": "1. Check if Working Offline (Send/Receive tab)\n2. Check Outbox for stuck emails\n   - Move stuck email to Drafts, edit, and resend\n3. Check attachment size (max 25-50MB typically)\n4. Check mailbox quota - full mailbox can't send\n5. Verify SMTP settings: server, port (587/465), TLS/SSL\n6. Check if your domain/IP is blacklisted\n7. For Exchange: check smtp relay settings\n8. Send test from webmail to isolate client vs server"
            },
            {
                "title": "Keeps asking for password",
                "node_type": "solution",
                "solution_text": "1. Clear cached credentials:\n   - Control Panel > Credential Manager > Windows Credentials\n   - Remove all outlook/office/microsoft entries\n2. Check if password recently changed\n3. Enable Modern Authentication:\n   - Registry: HKCU\\Software\\Microsoft\\Office\\16.0\\Common\\Identity\n   - EnableADAL = 1, Version = 1\n4. Check if MFA is enabled (may need App Password)\n5. Create a new Outlook profile\n6. Repair Office installation"
            },
            {
                "title": "Search not finding emails",
                "node_type": "solution",
                "solution_text": "1. Rebuild search index:\n   - File > Options > Search > Indexing Options > Advanced > Rebuild\n2. Wait for indexing to complete (check status in Search Tools)\n3. Verify Outlook is included in index locations\n4. Compact the OST file\n5. Try searching in OWA to compare results\n6. As last resort: create new Outlook profile"
            },
            {
                "title": "Calendar or meeting issues",
                "node_type": "solution",
                "solution_text": "1. Force sync: Press F9\n2. Check you're viewing the correct calendar\n3. For shared calendars: remove and re-add\n4. Check cached mode settings and increase sync window\n5. For Teams meetings: ensure Teams add-in is enabled\n6. On mobile: remove and re-add the account\n7. Clear local cache: rename .ost file and restart"
            }
        ]
    }
}
