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
    {
        "category": "Email & Outlook",
        "problem_title": "Outlook keeps asking for credentials after password change",
        "problem_description": "After changing domain or Microsoft 365 password, Outlook repeatedly asks for the old password, and entering the new one doesn't work.",
        "problem_keywords": "password change, credentials, credential manager, outlook password, login loop, reauthenticate",
        "solution_steps": (
            "1. Clear stored credentials:\n"
            "   - Control Panel > Credential Manager > Windows Credentials\n"
            "   - Remove all entries related to 'MicrosoftOffice', 'outlook', or 'Microsoft365'\n"
            "   - Also check 'Generic Credentials' section\n"
            "2. Close and reopen Outlook:\n"
            "   - After clearing credentials, fully close Outlook\n"
            "   - Check Task Manager to ensure OUTLOOK.EXE is not running\n"
            "   - Reopen Outlook - it should prompt for the new password\n"
            "3. Check Outlook profile:\n"
            "   - Control Panel > Mail > Show Profiles\n"
            "   - Select the profile > Properties > Email Accounts\n"
            "   - Verify the account settings are correct\n"
            "4. Modern Authentication:\n"
            "   - Ensure Modern Authentication is enabled (replaces basic auth)\n"
            "   - Registry: HKCU\\SOFTWARE\\Microsoft\\Office\\16.0\\Common\\Identity\n"
            "   - EnableADAL = 1, Version = 1\n"
            "5. Sign out of Office:\n"
            "   - Any Office app > File > Account > Sign Out\n"
            "   - Sign back in with the new password\n"
            "6. Remove cached tokens:\n"
            "   - Delete: %localappdata%\\Microsoft\\TokenBroker\\Cache\n"
            "   - Delete: %localappdata%\\Microsoft\\IdentityCache\n"
            "7. If domain-joined: Lock/unlock or sign out/sign in to update domain credentials"
        ),
    },
    {
        "category": "Email & Outlook",
        "problem_title": "Outlook calendar meeting invitations not being received",
        "problem_description": "Meeting invitations sent to users are not appearing in their inbox or calendar. Organizers see no response from the invitee.",
        "problem_keywords": "meeting invite, calendar invite, meeting not received, invitation missing, rsvp, calendar meeting, organizer",
        "solution_steps": (
            "1. Check Deleted Items and Junk:\n"
            "   - Meeting invites may be caught by spam filters\n"
            "   - Check Junk Email folder\n"
            "   - Check Deleted Items (some rules may auto-delete)\n"
            "2. Outlook rule check:\n"
            "   - File > Rules & Alerts > check all rules\n"
            "   - A rule may be moving or deleting calendar invites\n"
            "   - Look for rules that apply to 'sent to distribution list' or 'from specific sender'\n"
            "3. Auto-processing settings:\n"
            "   - File > Options > Calendar > Auto Accept/Decline\n"
            "   - If auto-decline is enabled for recurring meetings, disable it\n"
            "   - Delegates may be processing invites on behalf of the user\n"
            "4. Delegate settings:\n"
            "   - File > Account Settings > Delegate Access\n"
            "   - If a delegate has 'Send meeting requests to delegates only'\n"
            "   - Change to 'Both delegate and me'\n"
            "5. Exchange transport rules:\n"
            "   - An Exchange admin transport rule may be blocking invites\n"
            "   - Check Exchange Admin Center > Mail Flow > Rules\n"
            "6. Mailbox size:\n"
            "   - If mailbox is full, new items (including invites) can't be delivered\n"
            "   - Check mailbox size: File > Info > Mailbox Settings\n"
            "7. Resend the invitation: Ask the organizer to cancel and resend"
        ),
    },
    {
        "category": "Email & Outlook",
        "problem_title": "Outlook email signatures not displaying correctly",
        "problem_description": "Email signatures show broken images, wrong formatting, or don't appear at all. Signature looks different to recipients than in compose window.",
        "problem_keywords": "signature, email signature, signature broken, signature image, html signature, signature not showing",
        "solution_steps": (
            "1. Check signature settings:\n"
            "   - File > Options > Mail > Signatures\n"
            "   - Verify the correct signature is assigned for New Messages and Replies\n"
            "   - Check the signature preview - does it look correct?\n"
            "2. Message format:\n"
            "   - HTML format preserves formatting and images\n"
            "   - Plain Text strips all formatting\n"
            "   - File > Options > Mail > Compose messages in: HTML\n"
            "   - Check: Replying to plain text emails may strip signature formatting\n"
            "3. Broken images in signature:\n"
            "   - Images should be hosted online, not embedded from local paths\n"
            "   - Replace file:///C:/path with https://hosted/image.png\n"
            "   - Upload images to a web server or SharePoint\n"
            "   - Reduce image size (max 100-200 KB)\n"
            "4. Signature files:\n"
            "   - Located in: %appdata%\\Microsoft\\Signatures\\\n"
            "   - .htm (HTML), .rtf (Rich Text), .txt (Plain Text)\n"
            "   - Edit the .htm file directly if needed\n"
            "5. Signature not appearing on replies:\n"
            "   - Signatures must be set for both 'New messages' and 'Replies/forwards'\n"
            "   - Check both dropdowns in Signature settings\n"
            "6. Corporate signatures:\n"
            "   - If using Exchange transport rules for signatures, Outlook signature may conflict\n"
            "   - Check with IT if server-side signatures are enforced\n"
            "7. Reset signature: Delete files in the Signatures folder and recreate"
        ),
    },
    {
        "category": "Email & Outlook",
        "problem_title": "Outlook add-ins causing crashes or slowness",
        "problem_description": "Outlook runs slowly, freezes, or crashes due to problematic add-ins. Performance degrades over time as add-ins accumulate.",
        "problem_keywords": "outlook slow, add-in, addin, outlook freeze, com add-in, disabled add-in, outlook crash plugin",
        "solution_steps": (
            "1. Check for disabled add-ins:\n"
            "   - File > Options > Add-ins\n"
            "   - Look at 'Disabled Application Add-ins' at the bottom\n"
            "   - Outlook auto-disables add-ins that cause slow startup\n"
            "2. Start in Safe Mode:\n"
            "   - Hold Ctrl while clicking Outlook icon (confirm Safe Mode)\n"
            "   - Or: outlook.exe /safe\n"
            "   - If Outlook works in Safe Mode: Add-in issue confirmed\n"
            "3. Disable all add-ins:\n"
            "   - File > Options > Add-ins > Manage: COM Add-ins > Go\n"
            "   - Uncheck all add-ins > OK\n"
            "   - Restart Outlook and test\n"
            "4. Re-enable one at a time:\n"
            "   - Enable one add-in, restart Outlook, test\n"
            "   - Repeat until the problematic add-in is found\n"
            "   - Common culprits: older CRM plugins, fax add-ins, PDF printers\n"
            "5. Check startup time:\n"
            "   - File > Options > Add-ins\n"
            "   - Each add-in shows its load time\n"
            "   - Anything over 1000ms significantly affects startup\n"
            "6. Update or remove the add-in:\n"
            "   - Check for an updated version from the vendor\n"
            "   - If no longer needed: Uninstall completely from Control Panel\n"
            "7. Outlook performance: Also check file size (PST/OST > 10GB can be slow)"
        ),
    },
    {
        "category": "Email & Outlook",
        "problem_title": "Email stuck in Drafts folder and won't send",
        "problem_description": "Emails get saved to Drafts instead of being sent. Clicking Send appears to work but the email moves to Drafts, not Sent Items.",
        "problem_keywords": "email stuck drafts, won't send, draft folder, email not sending, send fails, saved to drafts",
        "solution_steps": (
            "1. Check Send/Receive:\n"
            "   - Click Send/Receive > Send All\n"
            "   - Check Send/Receive tab > Send/Receive Groups > Define\n"
            "   - Ensure 'Send mail items' is checked\n"
            "2. Work Offline mode:\n"
            "   - Send/Receive tab > check if 'Work Offline' is highlighted\n"
            "   - If enabled: Click to disable (return to online mode)\n"
            "   - Status bar should show 'Connected' not 'Working Offline'\n"
            "3. Check the outgoing server:\n"
            "   - File > Account Settings > Account > Change Account\n"
            "   - Outgoing server settings and authentication\n"
            "   - For Microsoft 365: smtp.office365.com, Port 587, STARTTLS\n"
            "4. Large attachment:\n"
            "   - Emails with large attachments may fail silently\n"
            "   - Check attachment size (Exchange default limit: 25 MB)\n"
            "   - Reduce attachment size or use OneDrive/SharePoint link\n"
            "5. Corrupted email:\n"
            "   - Open the draft > Select All > Copy\n"
            "   - Create a new email > Paste\n"
            "   - Delete the original draft and send the new one\n"
            "6. Outlook profile issue:\n"
            "   - Create a new Outlook profile and test sending\n"
            "   - Control Panel > Mail > Show Profiles > Add\n"
            "7. Check Outbox: If emails are in Outbox (not Drafts), different issue - check connectivity"
        ),
    },
    {
        "category": "Email & Outlook",
        "problem_title": "Shared mailbox not showing in Outlook",
        "problem_description": "A shared mailbox that was granted in Office 365 or Exchange doesn't appear in Outlook. User has permissions but can't see the mailbox.",
        "problem_keywords": "shared mailbox, shared email, mailbox not showing, permissions, exchange mailbox, office 365 shared",
        "solution_steps": (
            "1. Auto-mapping (Exchange/M365):\n"
            "   - Shared mailboxes with Full Access should auto-map in Outlook\n"
            "   - Takes 15-60 minutes after permission is granted\n"
            "   - Restart Outlook after waiting\n"
            "2. Manually add the shared mailbox:\n"
            "   - File > Account Settings > Account Settings\n"
            "   - Select the account > Change > More Settings > Advanced\n"
            "   - Add > enter the shared mailbox name/email\n"
            "   - OK > Next > Finish and restart Outlook\n"
            "3. In Outlook on the web:\n"
            "   - Right-click folder list > 'Add shared folder'\n"
            "   - Enter the shared mailbox email address\n"
            "4. Check permissions:\n"
            "   - Admin must grant 'Full Access' permission in Exchange Admin Center\n"
            "   - PowerShell: Get-MailboxPermission shared@domain.com\n"
            "   - Add: Add-MailboxPermission -Identity shared@domain.com -User user@domain.com -AccessRights FullAccess\n"
            "5. If auto-mapping was disabled:\n"
            "   - Remove-MailboxPermission and re-add with -AutoMapping $true\n"
            "   - Or add manually as in step 2\n"
            "6. Cached mode:\n"
            "   - If shared mailbox is large, may take time to download in Cached Mode\n"
            "   - File > Account Settings > Change > Cached Exchange Mode > Download shared folders\n"
            "7. License: Shared mailboxes in M365 don't need a license unless over 50 GB"
        ),
    },
    {
        "category": "Email & Outlook",
        "problem_title": "Outlook calendar time zones showing wrong times",
        "problem_description": "Calendar events display at wrong times. Meeting times appear different than what the organizer sent. Time zone confusion.",
        "problem_keywords": "time zone, calendar wrong time, meeting time, time offset, utc, timezone, outlook time",
        "solution_steps": (
            "1. Check Outlook time zone:\n"
            "   - File > Options > Calendar > Time zones\n"
            "   - Verify the correct time zone is selected\n"
            "   - Should match your actual location\n"
            "2. Check Windows time zone:\n"
            "   - Settings > Time & Language > Date & Time\n"
            "   - Verify time zone matches Outlook's setting\n"
            "   - Enable 'Set time zone automatically' if traveling\n"
            "3. Multiple time zones:\n"
            "   - Outlook can show up to 3 time zones on the calendar\n"
            "   - File > Options > Calendar > Time zones > Show a second/third time zone\n"
            "   - Useful for teams across time zones\n"
            "4. Meeting organizer's time zone:\n"
            "   - If the organizer is in a different time zone, Outlook converts\n"
            "   - Open the meeting > check the recurrence > time zone listed\n"
            "   - If wrong: Ask organizer to update with correct time zone\n"
            "5. Recurring meetings:\n"
            "   - Recurring meetings set in one time zone may show wrong after DST changes\n"
            "   - Delete the series and recreate with the correct time zone\n"
            "6. Daylight Saving Time:\n"
            "   - Ensure Windows updates are current (DST rules may change)\n"
            "   - Old Outlook versions may have wrong DST data\n"
            "   - Microsoft releases timezone update tools for Exchange\n"
            "7. iCalendar imports: .ics files may have time zone issues - verify VTIMEZONE in the file"
        ),
    },
    {
        "category": "Email & Outlook",
        "problem_title": "Outlook formatting lost when replying or forwarding",
        "problem_description": "Email formatting (fonts, colors, tables) gets stripped or changed when replying to or forwarding messages. HTML formatting converts to plain text.",
        "problem_keywords": "formatting lost, reply format, forward format, plain text, html email, font change, outlook format",
        "solution_steps": (
            "1. Check message format:\n"
            "   - When composing: Format Text tab > check HTML/Plain Text/Rich Text\n"
            "   - Should be HTML for most emails\n"
            "   - If Plain Text: Change to HTML\n"
            "2. Default format setting:\n"
            "   - File > Options > Mail > Compose messages in this format: HTML\n"
            "   - Also check: 'Use stationery to change default fonts and styles'\n"
            "3. Reply format:\n"
            "   - File > Options > Mail > Replies and forwards\n"
            "   - 'When replying to a message' > check format\n"
            "   - If 'Reply using the format of the original message': Will match sender's format\n"
            "4. Read as Plain Text:\n"
            "   - File > Options > Trust Center > Trust Center Settings > Email Security\n"
            "   - Uncheck 'Read all standard mail in plain text'\n"
            "   - This forces all emails to plain text on receipt\n"
            "5. Exchange transport rules:\n"
            "   - Admin transport rules may convert HTML to plain text\n"
            "   - Check Exchange Admin Center > Mail Flow > Rules\n"
            "6. Digital signatures:\n"
            "   - S/MIME signed emails may display differently\n"
            "   - Some email clients strip formatting from signed messages\n"
            "7. Recipient's email client: Some clients don't support HTML fully"
        ),
    },
    {
        "category": "Email & Outlook",
        "problem_title": "Outlook AutoComplete or address suggestions not working",
        "problem_description": "Outlook doesn't suggest email addresses when typing in the To field. Previously used contacts don't appear in autocomplete list.",
        "problem_keywords": "autocomplete, auto complete, address suggestion, contact suggest, outlook to field, address cache, nk2",
        "solution_steps": (
            "1. Check AutoComplete setting:\n"
            "   - File > Options > Mail\n"
            "   - Ensure 'Use Auto-Complete List to suggest names' is checked\n"
            "2. AutoComplete cache:\n"
            "   - Outlook stores suggestions in: %localappdata%\\Microsoft\\Outlook\\RoamCache\n"
            "   - Stream_Autocomplete_*.dat file contains the cache\n"
            "   - If corrupted: Delete the .dat files and let Outlook rebuild\n"
            "3. Clear and rebuild:\n"
            "   - File > Options > Mail > 'Empty Auto-Complete List' button\n"
            "   - This clears all suggestions - will rebuild as you send emails\n"
            "4. Outlook profile:\n"
            "   - AutoComplete is tied to the Outlook profile\n"
            "   - New profile = fresh AutoComplete cache\n"
            "   - Moving to new PC: Copy the RoamCache folder\n"
            "5. Exchange/M365:\n"
            "   - Some AutoComplete data syncs with Exchange\n"
            "   - Toggle Cached Mode off and on to refresh\n"
            "   - File > Account Settings > Change > Cached Exchange Mode\n"
            "6. GAL (Global Address List):\n"
            "   - Suggestions also come from the corporate address book\n"
            "   - If GAL not loading: Ctrl+Shift+B to open Address Book\n"
            "   - Check the correct address list is selected\n"
            "7. Search issues: Also check Outlook search indexing if contacts aren't found"
        ),
    },
    {
        "category": "Email & Outlook",
        "problem_title": "Emails delayed or arriving late",
        "problem_description": "Emails take minutes or hours to arrive instead of being delivered immediately. Both internal and external emails are delayed.",
        "problem_keywords": "email delay, late delivery, slow email, email queue, delayed delivery, mail flow, email slow",
        "solution_steps": (
            "1. Check if it's all emails or specific:\n"
            "   - Internal to internal: Exchange server issue\n"
            "   - Internal to external: Outbound mail flow\n"
            "   - External to internal: Inbound mail flow or spam filtering\n"
            "2. Outlook Send/Receive frequency:\n"
            "   - Send/Receive tab > Send/Receive Groups > Define\n"
            "   - Schedule: Every 5 minutes (or less)\n"
            "   - Manual: Click Send/Receive All Folders\n"
            "3. Cached Mode sync:\n"
            "   - In Cached Mode, press F9 to force sync\n"
            "   - Check status bar: should show 'All folders are up to date'\n"
            "   - If stuck: Try disabling and re-enabling Cached Mode\n"
            "4. Exchange queue:\n"
            "   - Admin: Exchange Management Shell > Get-Queue\n"
            "   - Check for queued messages and retry reasons\n"
            "   - Exchange Admin Center > Mail Flow > Message Trace\n"
            "5. Spam/security filtering:\n"
            "   - Third-party spam filters (Barracuda, Mimecast, etc.) can delay emails\n"
            "   - Check the spam filter dashboard for greylisting or delays\n"
            "   - Microsoft 365: Message Trace in Exchange Admin Center\n"
            "6. MX record issues:\n"
            "   - nslookup -type=mx domain.com (check MX records)\n"
            "   - If MX points to wrong server: Update DNS\n"
            "7. Deferred delivery: Check if 'Do not deliver before' is set on the message"
        ),
    },
    {
        "category": "Email & Outlook",
        "problem_title": "Outlook contact photos not displaying",
        "problem_description": "Contact photos are missing in Outlook emails and contact cards. Photos uploaded in Microsoft 365 or Active Directory don't appear.",
        "problem_keywords": "contact photo, profile picture, outlook photo, avatar, contact image, people photo, user photo",
        "solution_steps": (
            "1. Check the photo source:\n"
            "   - Microsoft 365: Photo is in Azure AD / Microsoft 365 profile\n"
            "   - On-premises: Photo is in Active Directory (thumbnailPhoto attribute)\n"
            "   - The photo must be uploaded to the correct source\n"
            "2. Update photo in M365:\n"
            "   - User: Go to outlook.office.com > click profile > Change photo\n"
            "   - Admin: Microsoft 365 Admin Center > Users > Edit user photo\n"
            "   - PowerShell: Set-UserPhoto -Identity user@domain.com -PictureData ([System.IO.File]::ReadAllBytes('photo.jpg'))\n"
            "3. Sync delay:\n"
            "   - Photo changes can take 24-48 hours to sync across all services\n"
            "   - Restart Outlook and clear the Outlook cache to speed up\n"
            "4. Cached Mode:\n"
            "   - Photos may not display in Cached Mode offline\n"
            "   - File > Account Settings > Change > 'Download Shared Folders'\n"
            "5. Photo size:\n"
            "   - Maximum recommended: 648x648 pixels\n"
            "   - File size: Under 100 KB for AD, up to 4 MB for M365\n"
            "   - Must be JPEG format\n"
            "6. Outlook People pane:\n"
            "   - View > People Pane > Normal\n"
            "   - If disabled: Photos won't show in reading pane\n"
            "7. For external contacts: Photos display only if the sender's organization publishes them"
        ),
    },
    {
        "category": "Email & Outlook",
        "problem_title": "Cannot open hyperlinks from Outlook emails",
        "problem_description": "Clicking links in Outlook emails gives an error 'Your organization's policies are preventing us from completing this action' or links don't open at all.",
        "problem_keywords": "hyperlink, outlook link, can't open link, organization policy, link error, default browser, url blocked",
        "solution_steps": (
            "1. Set default browser:\n"
            "   - Settings > Apps > Default Apps > Web browser\n"
            "   - Select a browser (Chrome, Edge, Firefox)\n"
            "   - If no default is set, Outlook can't open links\n"
            "2. Registry fix:\n"
            "   - HKCU\\SOFTWARE\\Classes\\.html > Default = htmlfile\n"
            "   - HKCU\\SOFTWARE\\Classes\\htmlfile\\shell\\open\\command > Default = \"browser_path\" \"%1\"\n"
            "3. Internet Explorer cleanup:\n"
            "   - Even if not used, IE settings affect Outlook link handling\n"
            "   - Internet Options > Programs > Reset Web Settings\n"
            "   - Internet Options > Advanced > Reset\n"
            "4. Group Policy restriction:\n"
            "   - IT may have blocked URL access from Outlook\n"
            "   - Check: User Config > Admin Templates > Microsoft Outlook > Security\n"
            "   - 'Block hyperlinks' or Safe Links policies\n"
            "5. Safe Links (Microsoft 365):\n"
            "   - ATP Safe Links rewrites URLs for scanning\n"
            "   - If misconfigured, links may be blocked\n"
            "   - Check with admin: Exchange Online Protection > Safe Links policies\n"
            "6. Repair Office:\n"
            "   - Settings > Apps > Microsoft Office > Modify > Online Repair\n"
            "   - This fixes broken file associations\n"
            "7. Workaround: Copy the link (right-click > Copy Hyperlink) and paste in browser"
        ),
    },
    {
        "category": "Email & Outlook",
        "problem_title": "Outlook email recall not working",
        "problem_description": "Attempted to recall a sent email but the recall failed. Recipients still see the original message.",
        "problem_keywords": "recall email, recall message, retract email, undo send, recall failed, message recall",
        "solution_steps": (
            "1. Recall limitations:\n"
            "   - Only works with Exchange/M365 (not POP/IMAP)\n"
            "   - Both sender and recipient must be on the same Exchange organization\n"
            "   - Does NOT work for external recipients\n"
            "2. How to recall:\n"
            "   - Sent Items > open the message > Message tab > Actions > Recall This Message\n"
            "   - Choose: Delete unread copies or Replace with new message\n"
            "3. Why recall fails:\n"
            "   - Recipient already read the message\n"
            "   - Recipient uses a non-Exchange email client (OWA may work differently)\n"
            "   - Message was moved from Inbox by a rule\n"
            "   - Cached Mode: Recall depends on server processing\n"
            "4. Recall on mobile:\n"
            "   - Cannot initiate a recall from Outlook mobile\n"
            "   - Must use Outlook desktop to recall\n"
            "5. Better alternative - Delay delivery:\n"
            "   - File > Options > Mail > Send/Receive\n"
            "   - Or create a rule: Apply rule > defer delivery by X minutes\n"
            "   - Gives a window to cancel before the email actually sends\n"
            "6. Microsoft 365 Undo Send:\n"
            "   - Outlook on the web has an 'Undo Send' button (brief 10-second window)\n"
            "   - Settings > Mail > Compose and reply > Undo send\n"
            "7. Always double-check recipients and content before sending important emails"
        ),
    },
    {
        "category": "Email & Outlook",
        "problem_title": "PST file too large or needs to be split",
        "problem_description": "Outlook PST file has grown very large causing slow performance, risk of corruption, or exceeding size limits.",
        "problem_keywords": "pst large, pst size, split pst, pst corrupt, archive pst, pst limit, data file size",
        "solution_steps": (
            "1. Check PST size:\n"
            "   - File > Account Settings > Data Files\n"
            "   - Note the file path and size\n"
            "   - Outlook 2010+: Maximum 50 GB for PST/OST\n"
            "   - Performance degrades noticeably above 10 GB\n"
            "2. Archive old emails:\n"
            "   - File > Info > Cleanup Tools > Archive\n"
            "   - Select folders and date (e.g., older than 1 year)\n"
            "   - Creates a separate archive.pst file\n"
            "3. Auto-Archive settings:\n"
            "   - File > Options > Advanced > AutoArchive Settings\n"
            "   - Run AutoArchive every X days\n"
            "   - Move old items to archive file\n"
            "4. Compact the PST:\n"
            "   - After deleting/archiving, PST doesn't shrink automatically\n"
            "   - File > Account Settings > Data Files > select PST > Settings > Compact Now\n"
            "   - This reclaims space from deleted items\n"
            "5. Empty Deleted Items:\n"
            "   - Permanently delete items in Deleted Items and Junk folders\n"
            "   - Then compact the PST (step 4)\n"
            "6. Split manually:\n"
            "   - Create a new PST: Home > New Items > More Items > Outlook Data File\n"
            "   - Drag/move folders from old PST to new PST\n"
            "   - Organize by year or category\n"
            "7. Repair corrupted PST: scanpst.exe (Inbox Repair Tool) in Office install directory"
        ),
    },
    {
        "category": "Email & Outlook",
        "problem_title": "Email bouncing with 550 5.7.1 relay denied error",
        "problem_description": "Emails to certain recipients bounce back with '550 5.7.1 Unable to relay' or 'Relay access denied' error.",
        "problem_keywords": "relay denied, 550 error, unable to relay, relay access, smtp relay, bounced email, 5.7.1",
        "solution_steps": (
            "1. Understanding the error:\n"
            "   - 'Relay denied' means the SMTP server refuses to forward the email\n"
            "   - The server only accepts mail for domains it's configured to handle\n"
            "2. Check recipient address:\n"
            "   - Verify the email address is correct (no typos)\n"
            "   - Check for extra spaces or hidden characters\n"
            "3. SMTP authentication:\n"
            "   - Ensure Outlook is configured to authenticate with the mail server\n"
            "   - File > Account Settings > Change > More Settings > Outgoing Server\n"
            "   - Check 'My outgoing server requires authentication'\n"
            "4. For on-premises Exchange:\n"
            "   - Exchange receive connectors may need 'Relay' permission\n"
            "   - Check: Exchange Management Console > Server Configuration > Hub Transport\n"
            "   - Receive Connector > Properties > Permission Groups\n"
            "5. For applications/devices sending email:\n"
            "   - Printers, scanners, LOB apps need SMTP relay configured\n"
            "   - Option 1: SMTP client submission (requires authentication)\n"
            "   - Option 2: Direct send to Exchange/M365 (MX record)\n"
            "   - Option 3: Configure an SMTP relay connector\n"
            "6. M365 SMTP relay:\n"
            "   - Configure a connector in Exchange Online for the sending IP\n"
            "   - Or use SMTP AUTH with smtp.office365.com:587\n"
            "7. SPF record: Ensure sending IP is in the SPF record for the domain"
        ),
    },
    {
        "category": "Email & Outlook",
        "problem_title": "Outlook notification sounds or pop-ups not working",
        "problem_description": "Outlook doesn't show desktop alerts or play notification sounds when new emails arrive. Notifications stopped after an update.",
        "problem_keywords": "notification, outlook alert, desktop alert, new mail sound, outlook notification, popup alert, notification sound",
        "solution_steps": (
            "1. Check Outlook notification settings:\n"
            "   - File > Options > Mail > Message arrival section\n"
            "   - Enable: 'Display a Desktop Alert'\n"
            "   - Enable: 'Play a sound'\n"
            "   - Enable: 'Show an envelope icon in the taskbar'\n"
            "2. Windows notification settings:\n"
            "   - Settings > System > Notifications\n"
            "   - Scroll down to 'Outlook' > ensure notifications are On\n"
            "   - Enable: Show notification banners, Play a sound\n"
            "3. Focus Assist (Do Not Disturb):\n"
            "   - Settings > System > Focus Assist\n"
            "   - If enabled: Set to Off or add Outlook to priority list\n"
            "   - Check automatic rules (during certain hours, presenting, etc.)\n"
            "4. Inbox rules:\n"
            "   - Rules that move emails to subfolders may bypass Inbox notifications\n"
            "   - Notifications typically only fire for Inbox delivery\n"
            "   - File > Rules & Alerts > check if rules move emails silently\n"
            "5. Sound settings:\n"
            "   - Control Panel > Sound > Sounds tab\n"
            "   - Scroll to 'Microsoft Outlook' > 'New Mail Notification'\n"
            "   - Ensure a sound is assigned and 'Play Windows Startup sound' is not interfering\n"
            "6. Multiple accounts:\n"
            "   - Notifications may only work for the default account\n"
            "   - Check per-account notification settings\n"
            "7. Restart Outlook and check for Office updates"
        ),
    },
    {
        "category": "Email & Outlook",
        "problem_title": "Cannot delete or move emails in Outlook",
        "problem_description": "Outlook gives errors when trying to delete or move emails. Messages return to their original folder after being moved.",
        "problem_keywords": "can't delete email, move error, message not deleted, outlook error, mailbox errors, move fails",
        "solution_steps": (
            "1. Clean Deleted Items:\n"
            "   - If Deleted Items is full or corrupted, deletes may fail\n"
            "   - Right-click Deleted Items > Empty Folder\n"
            "   - Also: Recover Deleted Items if available\n"
            "2. Mailbox quota:\n"
            "   - If mailbox is over quota, operations are restricted\n"
            "   - File > Info > Mailbox Settings shows size/quota\n"
            "   - Delete large emails or empty trash to free space\n"
            "3. Cached Mode sync issue:\n"
            "   - Changes made offline may conflict with server\n"
            "   - Switch to Online Mode temporarily:\n"
            "   - File > Account Settings > Change > uncheck Cached Exchange Mode\n"
            "   - Try deleting/moving, then re-enable Cached Mode\n"
            "4. Repair data file:\n"
            "   - Close Outlook\n"
            "   - For PST: Run scanpst.exe and repair\n"
            "   - For OST: Rename to .ost.bak, reopen Outlook to recreate\n"
            "5. Permissions:\n"
            "   - For shared mailboxes: You may not have delete permission\n"
            "   - Full Access is needed for delete operations\n"
            "   - Check with admin\n"
            "6. Folder properties:\n"
            "   - Right-click the folder > Properties > check for read-only\n"
            "   - Repair folder: Right-click > Properties > Clear Offline Items\n"
            "7. Last resort: Create new OST file by resetting Outlook profile"
        ),
    },
    {
        "category": "Email & Outlook",
        "problem_title": "Phishing or spoofed emails getting through to inbox",
        "problem_description": "Users receiving phishing emails that appear to come from internal addresses or known contacts. Spam filters not catching spoofed messages.",
        "problem_keywords": "phishing, spoofed email, spam, fake email, impersonation, phishing email, spoof protection",
        "solution_steps": (
            "1. Check email headers:\n"
            "   - Open the suspicious email > File > Properties > Internet Headers\n"
            "   - Check 'From' vs 'Return-Path' and 'Received' headers\n"
            "   - Spoofed emails often have mismatched sender domains\n"
            "2. Report the phishing:\n"
            "   - Home > Junk > Report as Phishing (Outlook)\n"
            "   - Or forward to the IT security team\n"
            "   - Microsoft: Report via Report Message add-in\n"
            "3. Verify SPF, DKIM, DMARC:\n"
            "   - Check the message headers for authentication results\n"
            "   - spf=pass/fail, dkim=pass/fail, dmarc=pass/fail\n"
            "   - If these fail: The domain's email authentication is misconfigured\n"
            "4. Admin: Configure email authentication:\n"
            "   - SPF: DNS TXT record specifying allowed sending servers\n"
            "   - DKIM: Cryptographic signing of outbound emails\n"
            "   - DMARC: Policy for handling SPF/DKIM failures (quarantine/reject)\n"
            "5. Anti-phishing policies (M365):\n"
            "   - Security Center > Threat Policies > Anti-phishing\n"
            "   - Enable impersonation protection for key users/domains\n"
            "   - Enable mailbox intelligence\n"
            "6. User training:\n"
            "   - Hover over links before clicking (check actual URL)\n"
            "   - Don't enter credentials on unexpected login pages\n"
            "   - Verify unusual requests through a separate channel\n"
            "7. External email tag: Configure Exchange to tag external emails with [EXTERNAL]"
        ),
    },
    {
        "category": "Email & Outlook",
        "problem_title": "Outlook delegates and shared mailbox permission issues",
        "problem_description": "Outlook delegate access not working correctly. Delegates can't see calendar, send on behalf permissions not functioning, or shared mailbox shows permission errors.",
        "problem_keywords": "delegate, send on behalf, shared mailbox permission, calendar delegate, outlook delegate, mailbox access, full access, send as",
        "solution_steps": (
            "1. Types of mailbox permissions:\n"
            "   - Full Access: Can open and read all mail\n"
            "   - Send As: Sends appearing as the mailbox (From: field)\n"
            "   - Send on Behalf: Sends showing 'on behalf of'\n"
            "   - Delegate: Calendar/inbox access with send on behalf\n"
            "2. Grant permissions (Exchange Admin):\n"
            "   - EAC > Recipients > Mailboxes > Mailbox delegation\n"
            "   - PowerShell: Add-MailboxPermission -Identity shared@co.com -User user@co.com -AccessRights FullAccess\n"
            "   - Add-RecipientPermission -Identity shared@co.com -Trustee user@co.com -AccessRights SendAs\n"
            "3. Outlook delegate setup:\n"
            "   - File > Account Settings > Delegate Access\n"
            "   - Add delegate, set permissions per folder\n"
            "   - 'Delegate receives copies of meeting requests'\n"
            "4. Auto-mapping:\n"
            "   - Full Access: Mailbox auto-appears in Outlook (auto-mapping)\n"
            "   - To disable: Remove and re-add with -AutoMapping $false\n"
            "   - Manual add: File > Account Settings > Account Settings > Change > More Settings > Advanced > Add mailbox\n"
            "5. Propagation: Permission changes can take up to 60 minutes in Exchange Online. Run Outlook in Online mode during testing"
        ),
    },
    {
        "category": "Email & Outlook",
        "problem_title": "Email attachment size limits and large file sending",
        "problem_description": "Emails with attachments being rejected due to size limits. Users can't send or receive large files via email, getting 'attachment size exceeds the allowable limit' or NDR errors.",
        "problem_keywords": "attachment size, email size limit, large attachment, file too large, attachment limit, email size, send large file, attachment rejected",
        "solution_steps": (
            "1. Default size limits:\n"
            "   - Exchange Online: 25MB per message (including encoding overhead)\n"
            "   - Exchange on-premises: Default 10MB, configurable\n"
            "   - Actual file: ~33% larger after Base64 encoding\n"
            "   - So 25MB limit = roughly 18-19MB file attachment\n"
            "2. Check current limits:\n"
            "   - Exchange Online: Get-Mailbox user@co.com | Select MaxSendSize, MaxReceiveSize\n"
            "   - Transport rule limits: Get-TransportRule | Select MaxMessageSize\n"
            "   - Connector limits may also restrict size\n"
            "3. Increase limits (on-premises):\n"
            "   - Mailbox: Set-Mailbox -MaxSendSize 50MB -MaxReceiveSize 50MB\n"
            "   - Connector: Set-SendConnector / Set-ReceiveConnector\n"
            "   - Global: Set-TransportConfig -MaxSendSize 50MB\n"
            "4. Alternative for large files:\n"
            "   - OneDrive/SharePoint: Share link instead of attachment\n"
            "   - Outlook: 'Attach > Browse web locations' uses OneDrive\n"
            "   - This also avoids mailbox bloat\n"
            "5. Recipient limits: Even if you increase your send limit, the recipient's server may reject large messages (Gmail: 25MB, many corporate: 10-15MB)"
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
