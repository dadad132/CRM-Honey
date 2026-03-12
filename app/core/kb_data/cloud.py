"""Cloud services, Microsoft 365, and SaaS troubleshooting articles and diagnostic tree."""

ARTICLES = [
    {
        "category": "Cloud & M365",
        "problem_title": "Microsoft 365 user cannot sign in",
        "problem_description": "User cannot sign into Microsoft 365 services (Teams, Outlook, SharePoint). May get 'account locked', 'password expired', or 'access denied'.",
        "problem_keywords": "m365 login, office 365 login, microsoft 365, cannot sign in, m365 password, azure ad login, entra login",
        "solution_steps": (
            "1. Check account status in Azure AD / Entra ID:\n"
            "   - portal.azure.com > Azure Active Directory > Users > find user\n"
            "   - Check: Sign-in blocked? Account disabled?\n"
            "   - Check: Password expired?\n"
            "2. Reset password:\n"
            "   - Azure AD > Users > Reset password\n"
            "   - Or M365 Admin Center > Users > Active users > Reset password\n"
            "   - User will be prompted to change on next sign-in\n"
            "3. Check for account lockout:\n"
            "   - Azure AD > Sign-in logs > filter by user > look for errors\n"
            "   - Common: 50053 (locked), 50126 (wrong password), 50057 (disabled)\n"
            "4. MFA issues:\n"
            "   - If user lost MFA device: Admin resets MFA\n"
            "   - Azure AD > Users > user > Authentication methods > Require re-register MFA\n"
            "5. Conditional Access blocking:\n"
            "   - Check sign-in logs for CA policy failures\n"
            "   - Common: Non-compliant device, wrong location, unapproved app\n"
            "6. License issues:\n"
            "   - User must have a valid M365 license assigned\n"
            "   - M365 Admin > Users > user > Licenses\n"
            "7. If hybrid AD: Check on-prem AD account status too\n"
            "   - Sync issues may mean password doesn't match between on-prem and cloud"
        ),
    },
    {
        "category": "Cloud & M365",
        "problem_title": "SharePoint site not accessible or error",
        "problem_description": "Users cannot access a SharePoint Online site. Getting 'Access Denied', 'Sorry, this site hasn't been shared with you', or 403 error.",
        "problem_keywords": "sharepoint access, sharepoint denied, sharepoint error, sharepoint permissions, sharepoint site, sharepoint online",
        "solution_steps": (
            "1. Check permissions:\n"
            "   - SharePoint site > Settings (gear icon) > Site permissions\n"
            "   - User must be a member, visitor, or owner of the site\n"
            "   - Share the site: Settings > Site permissions > Invite people\n"
            "2. Check if site uses Microsoft 365 Group:\n"
            "   - Team sites are connected to M365 Groups\n"
            "   - Add user to the group: M365 Admin > Groups > find group > Members > Add\n"
            "3. External sharing:\n"
            "   - If user is external: Check that external sharing is enabled\n"
            "   - SharePoint Admin Center > Sites > select site > Policies > External sharing\n"
            "4. Conditional Access:\n"
            "   - If accessing from unmanaged device: Policy may block\n"
            "   - Check Azure AD sign-in logs for CA failures\n"
            "5. Check the site URL:\n"
            "   - Ensure the URL is correct (typos are common)\n"
            "   - Old site may have been renamed or deleted\n"
            "6. Check SharePoint service health:\n"
            "   - M365 Admin Center > Health > Service health > SharePoint\n"
            "   - May be an ongoing outage\n"
            "7. Browser issues:\n"
            "   - Clear browser cache and cookies\n"
            "   - Try InPrivate/Incognito mode\n"
            "   - Try a different browser"
        ),
    },
    {
        "category": "Cloud & M365",
        "problem_title": "OneDrive sync not working or stuck",
        "problem_description": "OneDrive for Business is not syncing files. Sync icon shows processing forever, files are out of date, or sync has paused.",
        "problem_keywords": "onedrive sync, onedrive stuck, onedrive not syncing, onedrive error, onedrive paused, onedrive processing",
        "solution_steps": (
            "1. Check OneDrive status:\n"
            "   - Click OneDrive icon in system tray\n"
            "   - Look for error messages or paused status\n"
            "   - If paused: Click Resume syncing\n"
            "2. Common sync issues:\n"
            "   - File name contains invalid characters (# % & : | < > \" ? *)\n"
            "   - File path too long (max 400 characters)\n"
            "   - File too large (max 250 GB)\n"
            "   - File is locked by another application\n"
            "3. Reset OneDrive:\n"
            "   - Win+R > %localappdata%\\Microsoft\\OneDrive\\onedrive.exe /reset\n"
            "   - Wait 2 minutes, then OneDrive should restart\n"
            "   - If it doesn't restart: Run OneDrive from Start menu\n"
            "4. Check storage:\n"
            "   - OneDrive storage quota (default 1 TB for Business)\n"
            "   - Check: OneDrive icon > Settings > Account > Storage used\n"
            "   - If full: Clean up or request more storage\n"
            "5. Network issues:\n"
            "   - Check internet connection\n"
            "   - OneDrive > Settings > Network > check upload/download limits aren't too low\n"
            "   - Proxy or VPN may interfere\n"
            "6. Known Folder Move issues:\n"
            "   - Desktop, Documents, Pictures redirected to OneDrive\n"
            "   - If issues: OneDrive > Settings > Backup > Manage backup\n"
            "   - May need to stop backup and re-enable\n"
            "7. Unlink and relink:\n"
            "   - OneDrive > Settings > Account > Unlink this PC\n"
            "   - Sign in again and choose which folders to sync"
        ),
    },
    {
        "category": "Cloud & M365",
        "problem_title": "Teams admin - cannot create new team or channels",
        "problem_description": "Users or admins cannot create new Microsoft Teams teams or channels. May get permission errors or the option is greyed out.",
        "problem_keywords": "teams create team, teams channel, teams admin, teams permission, create team, new channel, teams policy",
        "solution_steps": (
            "1. Check Teams policies:\n"
            "   - Teams Admin Center > Teams > Teams policies\n"
            "   - 'Create private channels' and team creation may be restricted\n"
            "2. M365 Group creation restrictions:\n"
            "   - Creating a Team creates an M365 Group\n"
            "   - Azure AD may restrict who can create groups\n"
            "   - Azure AD > Groups > General > 'Users can create groups': Check who can\n"
            "   - If restricted: Add user to the approved group creation group\n"
            "3. License requirements:\n"
            "   - User needs a Teams-included license\n"
            "   - Some licenses don't include full Teams functionality\n"
            "4. For channel creation:\n"
            "   - Team owner controls who can create channels\n"
            "   - Team > Settings > Member permissions > Allow members to create channels\n"
            "   - Private channels have separate limits (max 30 per team)\n"
            "5. Team limits:\n"
            "   - User can be member of max 1000 teams\n"
            "   - Org limit: 500,000 teams per tenant\n"
            "   - Team can have max 25,000 members\n"
            "6. For admins creating on behalf:\n"
            "   - Teams Admin Center > Teams > Manage teams > Add\n"
            "   - Or PowerShell: New-Team -DisplayName 'Team Name' -Description 'Description'"
        ),
    },
    {
        "category": "Cloud & M365",
        "problem_title": "Azure AD / Entra ID sync issues with on-premises AD",
        "problem_description": "Azure AD Connect is not syncing changes between on-premises Active Directory and Azure AD/Entra ID. Users or password changes not appearing in the cloud.",
        "problem_keywords": "azure ad connect, ad sync, entra sync, azure ad sync, password sync, hybrid identity, aad connect",
        "solution_steps": (
            "1. Check Azure AD Connect status:\n"
            "   - On the server running AAD Connect:\n"
            "   - Open Azure AD Connect Health from Start menu\n"
            "   - Or check: M365 Admin Center > Health > Directory Sync Status\n"
            "2. Check sync service:\n"
            "   - Open Synchronization Service Manager\n"
            "   - Check for failed or stopped sync cycles\n"
            "   - Look at the error column for details\n"
            "3. Force a sync:\n"
            "   - PowerShell (on AAD Connect server):\n"
            "   - Start-ADSyncSyncCycle -PolicyType Delta (sync changes)\n"
            "   - Start-ADSyncSyncCycle -PolicyType Initial (full sync - slow)\n"
            "4. Common sync errors:\n"
            "   - Invalid characters in attributes (e.g., special chars in ProxyAddresses)\n"
            "   - Duplicate attributes between users\n"
            "   - Orphaned objects in the connector space\n"
            "5. Password hash sync not working:\n"
            "   - Check AAD Connect config: Password sync should be enabled\n"
            "   - Verify the password sync agent is running\n"
            "   - User may need to change password again to trigger sync\n"
            "6. Check the Azure AD Connect server:\n"
            "   - Auto-upgrade enabled? Check for pending updates\n"
            "   - Disk space on the AAD Connect server\n"
            "   - Time sync correct?\n"
            "7. Azure AD Connect logs:\n"
            "   - Event Viewer > Application > source: ADSync\n"
            "   - Event Viewer > Application > source: Directory Synchronization"
        ),
    },
    {
        "category": "Cloud & M365",
        "problem_title": "Exchange Online mailbox migration issues",
        "problem_description": "Mailbox migration from on-premises Exchange to Exchange Online is failing, stalled, or completing with errors.",
        "problem_keywords": "mailbox migration, exchange online, migration failed, exchange migration, hybrid exchange, move mailbox, migration batch",
        "solution_steps": (
            "1. Check migration status:\n"
            "   - Exchange Admin Center > Migration > check batch status\n"
            "   - Or PowerShell: Get-MoveRequest | Get-MoveRequestStatistics\n"
            "2. Common migration failures:\n"
            "   - Large mailbox: Increase bad item limit\n"
            "     Set-MoveRequest -Identity user -BadItemLimit 100 -AcceptLargeDataLoss\n"
            "   - Corrupt items preventing migration\n"
            "   - MRS Proxy not configured on on-prem Exchange\n"
            "3. Check prerequisites:\n"
            "   - MRS Proxy enabled on on-prem: EAC > Servers > Virtual Directories > EWS > MRSProxy enabled\n"
            "   - Migration endpoint configured in EXO\n"
            "   - Hybrid Configuration Wizard completed successfully\n"
            "4. Stalled migrations:\n"
            "   - Resume: Resume-MoveRequest -Identity user\n"
            "   - If stuck past 95%: May need final switchover\n"
            "   - Complete: Complete-MoveRequest -Identity user\n"
            "5. Performance issues:\n"
            "   - Throttling by M365 (slow by design)\n"
            "   - Network bandwidth between on-prem and M365\n"
            "   - Schedule large migrations for off-hours\n"
            "6. After migration:\n"
            "   - Update Outlook profile to connect to M365\n"
            "   - Update DNS (MX, Autodiscover) if needed\n"
            "   - Test email flow and calendar functionality"
        ),
    },
    {
        "category": "Cloud & M365",
        "problem_title": "M365 service outage affecting users",
        "problem_description": "Multiple users are reporting issues with M365 services (Teams, Outlook, SharePoint). May be a Microsoft service outage.",
        "problem_keywords": "m365 outage, office 365 down, teams outage, outlook outage, sharepoint outage, service health, microsoft outage",
        "solution_steps": (
            "1. Check M365 Service Health:\n"
            "   - admin.microsoft.com > Health > Service health\n"
            "   - Shows active incidents and advisories\n"
            "   - Green = healthy, Yellow = advisory, Red = incident\n"
            "2. Check external status pages:\n"
            "   - status.office365.com\n"
            "   - downdetector.com for community reports\n"
            "   - Twitter/X: @MSABOREA_365Status\n"
            "3. If outage confirmed:\n"
            "   - Communicate to users: Acknowledge the issue\n"
            "   - Set expectations: Microsoft is working on it\n"
            "   - Provide workarounds if available (e.g., use web version)\n"
            "4. If no outage listed but users affected:\n"
            "   - Check if it's a specific region or tenant issue\n"
            "   - Check local network connectivity\n"
            "   - Clear browser cache / restart apps\n"
            "   - Try from a different network\n"
            "5. Document the impact:\n"
            "   - How many users affected?\n"
            "   - Which services are impacted?\n"
            "   - When did it start?\n"
            "6. Open a support ticket:\n"
            "   - M365 Admin Center > Support > New service request\n"
            "   - Include: Impact scope, start time, error messages\n"
            "7. After resolution: Verify with users that service is restored"
        ),
    },
    {
        "category": "Cloud & M365",
        "problem_title": "M365 license assignment and management",
        "problem_description": "User is missing features, apps not activating, or getting 'You don't have a license' errors. Need to assign or manage M365 licenses.",
        "problem_keywords": "m365 license, office license, assign license, no license, license management, license error, subscription",
        "solution_steps": (
            "1. Check current licenses:\n"
            "   - M365 Admin Center > Users > Active users > select user\n"
            "   - Licenses and apps tab: Shows assigned licenses\n"
            "2. Assign a license:\n"
            "   - Select user > Licenses and apps > check the license to assign\n"
            "   - Choose which apps to enable/disable under the license\n"
            "   - Save changes\n"
            "3. Check available licenses:\n"
            "   - M365 Admin Center > Billing > Licenses\n"
            "   - Shows total, assigned, available for each subscription\n"
            "   - If none available: Purchase more or reclaim from inactive users\n"
            "4. Group-based licensing (recommended):\n"
            "   - Azure AD > Groups > create group > Licenses\n"
            "   - Assign license to group > add users to group\n"
            "   - Automatic assignment when users join the group\n"
            "5. License conflicts:\n"
            "   - User has multiple licenses with overlapping services\n"
            "   - Azure AD > Users > user > Licenses > check for errors\n"
            "   - Remove conflicting license\n"
            "6. For Office apps not activating:\n"
            "   - Open any Office app > File > Account\n"
            "   - Sign out and sign in with licensed account\n"
            "   - May need to run: cscript ospp.vbs /dstatus (for Office status)\n"
            "7. Allow up to 24 hours for license changes to take effect in all services"
        ),
    },
    {
        "category": "Cloud & M365",
        "problem_title": "Teams guest access not working",
        "problem_description": "External guests cannot access the Teams team they were invited to. Getting access denied or invitation not received.",
        "problem_keywords": "teams guest, guest access, external user teams, teams invite, guest not working, external teams, b2b",
        "solution_steps": (
            "1. Check guest access is enabled:\n"
            "   - Teams Admin Center > Org-wide settings > Guest access > ON\n"
            "   - Azure AD > External Identities > External collaboration settings\n"
            "   - Check: Guest invite restrictions (who can invite guests)\n"
            "2. Check the invitation:\n"
            "   - Guest should receive an email invitation\n"
            "   - Check their spam/junk folder\n"
            "   - Resend: Teams > Team > Members > re-invite the guest\n"
            "3. Guest acceptance:\n"
            "   - Guest must accept the invitation\n"
            "   - They need a Microsoft account or create one with their email\n"
            "   - Work accounts: May need admin consent from their organization\n"
            "4. Conditional Access may block:\n"
            "   - CA policies may restrict guest access\n"
            "   - Check: Azure AD > Conditional Access > Policies > look for guest-related policies\n"
            "   - May need to exclude guest users or create a separate policy\n"
            "5. Specific domain blocking:\n"
            "   - Azure AD > External Identities > Collaboration restrictions\n"
            "   - Check if the guest's domain is blocked\n"
            "   - Add their domain to the allowlist\n"
            "6. Guest cannot see content:\n"
            "   - Check channel permissions: Guests may not have access to all channels\n"
            "   - Private channels: Guests must be explicitly added\n"
            "7. For SharePoint/file access: Guest may need separate SharePoint sharing invitation"
        ),
    },
    {
        "category": "Cloud & M365",
        "problem_title": "Power Automate flow failing or not triggering",
        "problem_description": "Power Automate (Flow) is not running when expected. Automated workflow fails, doesn't trigger, or completes with errors.",
        "problem_keywords": "power automate, flow failing, flow not trigger, power automate error, flow stopped, automated workflow",
        "solution_steps": (
            "1. Check flow status:\n"
            "   - flow.microsoft.com > My flows > find the flow\n"
            "   - Check: Is it turned on?\n"
            "   - Check run history for error details\n"
            "2. Common trigger issues:\n"
            "   - 'When an item is created' triggers have polling intervals (1-5 min)\n"
            "   - Connection expired: Reconnect by editing the flow\n"
            "   - Connection was the previous employee's: Update to current user\n"
            "3. Connection errors:\n"
            "   - Flow > Edit > click on failing action\n"
            "   - Check connection status (may show red exclamation)\n"
            "   - Remove and recreate the connection\n"
            "   - Ensure the connected account has permissions\n"
            "4. Exceeded limits:\n"
            "   - Free/included plans have daily run limits\n"
            "   - Check: Power Platform Admin Center > Environments > Analytics\n"
            "   - May need a Power Automate premium license\n"
            "5. Action-specific errors:\n"
            "   - Click the failed action in run history to see the error\n"
            "   - Common: Missing fields, wrong data type, API throttling\n"
            "   - Add error handling: Configure Run After settings\n"
            "6. For scheduled flows:\n"
            "   - Check timezone is correct\n"
            "   - Check recurrence settings\n"
            "   - Flow may have been turned off due to repeated failures"
        ),
    },
    {
        "category": "Cloud & M365",
        "problem_title": "Microsoft Teams meeting recording not available",
        "problem_description": "Teams meeting recordings don't appear after the meeting ends. Recording button is grayed out, or recordings are lost and can't be found by participants.",
        "problem_keywords": "teams recording, meeting recording, recording missing, recording not available, teams video, recording failed, stream",
        "solution_steps": (
            "1. Where recordings are saved:\n"
            "   - Channel meetings: SharePoint > channel folder > Recordings\n"
            "   - Non-channel meetings: OneDrive of the person who clicked Record\n"
            "   - Recordings are no longer saved to Stream (Classic)\n"
            "2. Recording not appearing:\n"
            "   - Recordings can take 10-60 minutes to process after meeting ends\n"
            "   - Check the meeting chat: Recording link appears there\n"
            "   - Check OneDrive > Recordings folder\n"
            "3. Recording button grayed out:\n"
            "   - Admin must enable recording: Teams Admin Center > Meeting Policies\n"
            "   - 'Allow cloud recording' must be ON\n"
            "   - Guest/anonymous users cannot record\n"
            "   - User must have appropriate license (E3/E5/Business)\n"
            "4. Recording expired:\n"
            "   - Teams recordings auto-expire (default: 120 days)\n"
            "   - Admin can change: Meeting Policies > Default expiration time\n"
            "   - Users get email notification before expiration\n"
            "   - Download before expiration to keep permanently\n"
            "5. Sharing recordings:\n"
            "   - Click the recording in chat > Share\n"
            "   - OneDrive sharing permissions apply\n"
            "   - By default: Only meeting participants can view\n"
            "6. Transcription:\n"
            "   - Transcription is separate from recording\n"
            "   - Enable: Meeting Policies > Allow transcription\n"
            "   - Transcript appears as .vtt file alongside the recording\n"
            "7. Storage: Recordings count against OneDrive/SharePoint storage quota"
        ),
    },
    {
        "category": "Cloud & M365",
        "problem_title": "Azure AD Conditional Access blocking legitimate users",
        "problem_description": "Users are blocked from accessing M365 or company apps due to Conditional Access policies. Error messages about compliance, location, or device requirements.",
        "problem_keywords": "conditional access, blocked access, ca policy, azure ad block, compliance block, location policy, device requirement",
        "solution_steps": (
            "1. Identify the block:\n"
            "   - User sees: 'You cannot access this right now' or 'Access has been blocked'\n"
            "   - The error usually includes a Correlation ID\n"
            "   - Azure AD > Sign-in logs > search by user > check Conditional Access tab\n"
            "2. Common block reasons:\n"
            "   - Device not compliant (not enrolled in Intune/MDM)\n"
            "   - Signing in from untrusted location (IP not in named locations)\n"
            "   - Using a non-approved browser or OS\n"
            "   - MFA requirement not satisfied\n"
            "3. Sign-in log analysis:\n"
            "   - Azure Portal > Azure AD > Sign-in logs\n"
            "   - Find the failed sign-in > Conditional Access tab\n"
            "   - Shows which policies were evaluated and which blocked access\n"
            "4. Device compliance:\n"
            "   - Intune > Devices > find the device > Compliance\n"
            "   - What compliance check is failing?\n"
            "   - Fix the compliance issue or adjust the policy\n"
            "5. Location-based:\n"
            "   - Azure AD > Named Locations > check if user's IP is listed\n"
            "   - For VPN users: Add VPN exit IP to named locations\n"
            "   - For traveling users: Consider exceptions or MFA instead of block\n"
            "6. Troubleshoot tool:\n"
            "   - Azure AD > Diagnose and solve problems > Conditional Access troubleshooter\n"
            "   - Or: 'What If' tool in Conditional Access blade\n"
            "   - Simulates sign-in to see which policies would apply\n"
            "7. Emergency: Use 'break glass' admin accounts that are excluded from CA policies"
        ),
    },
    {
        "category": "Cloud & M365",
        "problem_title": "SharePoint site permissions confusion or access denied",
        "problem_description": "Users can't access SharePoint sites, lists, or documents. Permissions seem correct but users still get 'Access Denied' or 'Request Access' screen.",
        "problem_keywords": "sharepoint permissions, access denied, site permissions, sharepoint access, sharing, permission inheritance, request access",
        "solution_steps": (
            "1. Check user's permissions:\n"
            "   - SharePoint site > Settings (gear) > Site Permissions\n"
            "   - Or: Site Settings > Site Permissions > Check Permissions\n"
            "   - Enter the user's name to see their effective permissions\n"
            "2. Permission levels:\n"
            "   - Full Control: Site owners (manage everything)\n"
            "   - Edit/Contribute: Can add/modify content\n"
            "   - Read: View only\n"
            "   - Limited Access: System level (usually automatic)\n"
            "3. Broken inheritance:\n"
            "   - Folder or document may have unique permissions\n"
            "   - Break permission inheritance means site permissions don't apply\n"
            "   - Check the specific item: Library > Item > Manage Access\n"
            "4. Sharing links:\n"
            "   - Files shared via link may not grant site access\n"
            "   - Types: Anyone, People in org, Specific people\n"
            "   - Check sharing settings: Site > Settings > Site Sharing\n"
            "5. M365 Group connected:\n"
            "   - Team sites are connected to M365 Groups\n"
            "   - Adding to the M365 Group grants site access\n"
            "   - Azure AD > Groups > add the user as a member\n"
            "6. External sharing:\n"
            "   - If sharing with external/guest users:\n"
            "   - SharePoint Admin Center > Sharing > must allow external sharing\n"
            "   - Tenant level AND site level both must allow it\n"
            "7. Access requests: Configure 'Access Request Settings' to route requests to the right person"
        ),
    },
    {
        "category": "Cloud & M365",
        "problem_title": "Microsoft 365 email delivery delays or NDR bounce",
        "problem_description": "Emails sent through Exchange Online are delayed by hours or bounced back with Non-Delivery Reports (NDR/bounce messages) to senders.",
        "problem_keywords": "email delay, ndr, bounce, non-delivery, email bounce, exchange online, mail flow, delayed email",
        "solution_steps": (
            "1. Check NDR error code:\n"
            "   - 550 5.1.1: Recipient not found (typo in address)\n"
            "   - 550 5.7.1: Relay denied or blocked by policy\n"
            "   - 550 5.4.1: Recipient address rejected\n"
            "   - 452 4.5.3: Too many recipients\n"
            "   - 550 5.7.606/501: Blocked for spam/abuse\n"
            "2. Message trace:\n"
            "   - Exchange Admin Center > Mail Flow > Message Trace\n"
            "   - Search by sender, recipient, date range\n"
            "   - Shows: Delivery status, time, reason for failure\n"
            "3. Delayed delivery:\n"
            "   - Check mailbox rules: Is 'Delay Delivery' enabled?\n"
            "   - Transport rules: Admin rules may queue messages\n"
            "   - Large attachments take longer to scan\n"
            "   - Microsoft service issues: Check admin.microsoft.com > Health\n"
            "4. Blocked for spam:\n"
            "   - Microsoft may block your domain if flagged as spam source\n"
            "   - Check: mxtoolbox.com for blacklist status\n"
            "   - Submit delisting request if on Microsoft's block list\n"
            "   - Review SPF, DKIM, DMARC records\n"
            "5. SPF/DKIM/DMARC:\n"
            "   - SPF: DNS TXT record listing authorized senders\n"
            "   - DKIM: Email signing for authenticity\n"
            "   - DMARC: Policy for handling SPF/DKIM failures\n"
            "   - All three should be configured for reliable delivery\n"
            "6. Mail flow rules:\n"
            "   - Exchange Admin > Mail Flow > Rules\n"
            "   - Check for rules that redirect, delay, or block messages\n"
            "7. Connector issues: If using hybrid, check inbound/outbound connectors are correctly configured"
        ),
    },
    {
        "category": "Cloud & M365",
        "problem_title": "OneDrive Known Folder Move (KFM) not redirecting folders",
        "problem_description": "OneDrive Known Folder Move configured via policy is not redirecting Desktop, Documents, and Pictures folders to OneDrive. Or files are stuck syncing.",
        "problem_keywords": "known folder move, kfm, onedrive redirect, desktop redirect, documents onedrive, folder redirect, kfm error",
        "solution_steps": (
            "1. KFM requirements:\n"
            "   - OneDrive sync client must be current version\n"
            "   - Windows 10/11 (not supported on macOS for KFM via GPO)\n"
            "   - User must be signed into OneDrive with work account\n"
            "2. Configure via GPO/Intune:\n"
            "   - GPO: Computer Config > Admin Templates > OneDrive\n"
            "   - 'Silently move Windows known folders to OneDrive' = Enabled\n"
            "   - Requires your Azure AD Tenant ID\n"
            "   - Intune: Device Configuration > Admin Templates > OneDrive\n"
            "3. Common errors:\n"
            "   - 'Files can't be moved': Unsupported file types (.pst, OneNote notebooks)\n"
            "   - 'Path too long': Some file paths exceed 400 character limit\n"
            "   - 'Folder not empty': Previous redirect still active\n"
            "4. Troubleshoot:\n"
            "   - Check: Are the folders already redirected by GPO folder redirection?\n"
            "   - KFM and GPO folder redirection conflict\n"
            "   - Remove GPO folder redirection first\n"
            "5. PST files:\n"
            "   - Outlook PST files in Documents block KFM\n"
            "   - Move PST files out of Documents folder first\n"
            "   - Or migrate PST to Online Archive\n"
            "6. OneNote notebooks:\n"
            "   - Local OneNote notebooks in Documents block KFM\n"
            "   - Move notebooks to OneDrive manually first\n"
            "   - Then re-run KFM\n"
            "7. Verify: OneDrive icon > Settings > Backup > check which folders are managed"
        ),
    },
    {
        "category": "Cloud & M365",
        "problem_title": "Microsoft Teams channels and tabs missing or broken",
        "problem_description": "Teams channels are not loading, tabs show errors or blank pages, or custom tabs/apps added to channels stop working for users.",
        "problem_keywords": "teams channel, teams tab, tab not loading, channel error, teams app, custom tab, channel missing",
        "solution_steps": (
            "1. Channel not loading:\n"
            "   - Clear Teams cache: Close Teams > delete %appdata%\\Microsoft\\Teams\\Cache\n"
            "   - Also clear: blob_storage, databases, GPUcache, IndexedDB, Local Storage, tmp\n"
            "   - Restart Teams\n"
            "2. Tab showing blank/error:\n"
            "   - SPO/Website tab: Check if the URL is still accessible\n"
            "   - Third-party app tab: The app service may be down\n"
            "   - Try opening the tab in browser (right-click > Open in browser)\n"
            "3. Missing channels:\n"
            "   - Channel may have been hidden: Team name > More options > Manage Team\n"
            "   - Hidden channels: Click 'hidden channels' at the bottom of channel list\n"
            "   - Channel deleted: Team owner can view and restore within 30 days\n"
            "4. Custom app/tab permissions:\n"
            "   - Teams Admin Center > Teams Apps > Permission Policies\n"
            "   - Check if the app is allowed for the user's policy\n"
            "   - Third-party apps may be blocked by admin policy\n"
            "5. SharePoint tab issues:\n"
            "   - SharePoint tabs need user to have access to the SharePoint site\n"
            "   - If access denied in the tab: Grant SharePoint permissions\n"
            "6. Teams web vs desktop:\n"
            "   - Try the web version (teams.microsoft.com) to isolate desktop client issues\n"
            "   - If works on web: Reinstall desktop client\n"
            "7. Admin: Check Teams Admin Center > Teams > Manage Teams for team/channel health"
        ),
    },
    {
        "category": "Cloud & M365",
        "problem_title": "Azure AD Connect sync errors or attribute conflicts",
        "problem_description": "Azure AD Connect shows synchronization errors. On-premises AD objects aren't appearing in Azure AD, or attribute conflicts prevent user sync.",
        "problem_keywords": "azure ad connect, sync error, directory sync, aad connect, attribute conflict, sync conflict, hybrid identity",
        "solution_steps": (
            "1. Check sync status:\n"
            "   - Synchronization Service Manager (miisclient.exe) on the AAD Connect server\n"
            "   - Check: Operations tab > latest runs > look for errors\n"
            "   - Azure Portal > Azure AD Connect > Sync Status\n"
            "2. Common sync errors:\n"
            "   - AttributeValueMustBeUnique: Duplicate attribute (e.g., proxyAddress)\n"
            "   - InvalidSoftMatch: UPN/email conflicts with cloud-only account\n"
            "   - LargeObject: Object exceeds attribute limits\n"
            "3. Duplicate attribute:\n"
            "   - Two objects have the same proxyAddress or UserPrincipalName\n"
            "   - Find duplicates: Get-ADUser -Filter {proxyAddresses -like '*duplicate@domain.com*'}\n"
            "   - Remove the duplicate on one object\n"
            "4. Force sync:\n"
            "   - PowerShell on AAD Connect server:\n"
            "   - Start-ADSyncSyncCycle -PolicyType Delta (quick sync)\n"
            "   - Start-ADSyncSyncCycle -PolicyType Initial (full sync - use sparingly)\n"
            "5. Object not syncing:\n"
            "   - Check the OU filtering: AAD Connect wizard > Customize synchronization options\n"
            "   - Is the user's OU included in sync?\n"
            "   - Check Metaverse Search in Sync Service Manager\n"
            "6. Password hash sync:\n"
            "   - If PHS not working: Restart 'Microsoft Azure AD Sync' service\n"
            "   - Enable PHS troubleshooting: Invoke-ADSyncDiagnostics\n"
            "   - Users must change password once for PHS to sync initial hash\n"
            "7. Health: Azure AD Connect Health shows sync health in Azure Portal > AAD Connect"
        ),
    },
    {
        "category": "Cloud & M365",
        "problem_title": "Microsoft 365 admin portal slow or inaccessible",
        "problem_description": "The Microsoft 365 admin center (admin.microsoft.com) is loading slowly, timing out, or showing errors when trying to manage users, licenses, or settings.",
        "problem_keywords": "admin portal, admin center, m365 admin, admin slow, portal timeout, admin inaccessible, azure portal",
        "solution_steps": (
            "1. Check service health:\n"
            "   - admin.microsoft.com/adminportal/home#/servicehealth\n"
            "   - Or: status.office365.com (public status page)\n"
            "   - Microsoft may be experiencing a portal outage\n"
            "2. Browser troubleshooting:\n"
            "   - Clear browser cache and cookies for microsoft.com\n"
            "   - Try InPrivate/Incognito window\n"
            "   - Try a different browser (Edge, Chrome, Firefox)\n"
            "   - Disable browser extensions (ad blockers may interfere)\n"
            "3. Network:\n"
            "   - Check internet connectivity and speed\n"
            "   - If behind proxy: Ensure *.microsoft.com is allowed\n"
            "   - Try from a different network (mobile hotspot) to isolate\n"
            "4. PowerShell alternative:\n"
            "   - If portal is down, use PowerShell for admin tasks\n"
            "   - Install-Module Microsoft.Graph\n"
            "   - Connect-MgGraph -Scopes 'User.ReadWrite.All'\n"
            "   - Get-MgUser, New-MgUser, etc.\n"
            "5. Specific page issues:\n"
            "   - Some admin pages are heavier than others\n"
            "   - Users page with 10,000+ users: Use search/filter instead of scrolling\n"
            "   - Use PowerShell for bulk operations\n"
            "6. Conditional Access:\n"
            "   - Your own CA policies may block or complicate admin portal access\n"
            "   - Ensure admin accounts aren't blocked by overly restrictive policies\n"
            "7. Alternative portals: Use specific admin centers directly (exchange, sharepoint, teams admin)"
        ),
    },
    {
        "category": "Cloud & M365",
        "problem_title": "Exchange Online mailbox migration stuck or failed",
        "problem_description": "Mailbox migration from on-premises Exchange to Exchange Online is stuck at a certain percentage, failed with errors, or completed with missing items.",
        "problem_keywords": "mailbox migration, exchange migration, migration batch, move request, hybrid migration, migration stuck, cutover migration",
        "solution_steps": (
            "1. Check migration status:\n"
            "   - Exchange Admin Center > Migration > Migration batches\n"
            "   - Or PowerShell: Get-MoveRequest | Get-MoveRequestStatistics\n"
            "   - Look at: PercentComplete, Status, StatusDetail\n"
            "2. Stuck migration:\n"
            "   - 'Stalled': Usually transient - will retry automatically\n"
            "   - 'Failed': Check FailureType and Message for specific error\n"
            "   - 95%: Waiting for final cutover (sync completion)\n"
            "3. Common errors:\n"
            "   - 'Large item limit exceeded': Increase -LargeItemLimit parameter\n"
            "   - 'Bad item limit exceeded': Increase -BadItemLimit parameter\n"
            "   - Corruption: Some items can't be migrated (calendar corruption)\n"
            "4. Resume failed migration:\n"
            "   - Set-MoveRequest -Identity user@domain.com -BadItemLimit 50 -LargeItemLimit 50\n"
            "   - Resume-MoveRequest -Identity user@domain.com\n"
            "   - Monitor: Get-MoveRequestStatistics -Identity user@domain.com\n"
            "5. Speed optimization:\n"
            "   - Ensure MRS Proxy is enabled on on-premises Exchange\n"
            "   - Increase concurrent move limit if available bandwidth allows\n"
            "   - Migrate in batches during off-hours\n"
            "6. Missing items:\n"
            "   - Check: Get-MoveRequestStatistics -IncludeReport\n"
            "   - Bad items are skipped and logged\n"
            "   - Export report: $stats.Report.Entries to review each item\n"
            "7. Post-migration: Update Autodiscover DNS, test mail flow, and verify client reconnection"
        ),
    },
    {
        "category": "Cloud & M365",
        "problem_title": "Microsoft Intune device enrollment failures",
        "problem_description": "Devices fail to enroll in Microsoft Intune. Users see enrollment errors in Company Portal, or enrollment completes but policies don't apply.",
        "problem_keywords": "intune enrollment, device enrollment, company portal, enrollment failed, intune error, mdm enrollment, autopilot",
        "solution_steps": (
            "1. Check enrollment restrictions:\n"
            "   - Intune > Devices > Enrollment Restrictions\n"
            "   - Device type restrictions: Is the OS/platform allowed?\n"
            "   - Device limit restrictions: Has user exceeded their device limit?\n"
            "2. Common enrollment errors:\n"
            "   - 0x801c03ed: Device already enrolled or stale object exists\n"
            "   - 80180014: Device limit reached\n"
            "   - 0x80180026: Enrollment restrictions deny this device type\n"
            "3. Prerequisites:\n"
            "   - User must have an Intune license assigned\n"
            "   - Azure AD > Users > Licenses > verify Intune license\n"
            "   - MDM authority must be set to Intune (not hybrid)\n"
            "4. Windows enrollment:\n"
            "   - Settings > Accounts > Access work or school > Connect\n"
            "   - Enter work email > follows MDM enrollment flow\n"
            "   - If already Azure AD joined: Should auto-enroll if MDM scope is set\n"
            "   - Intune > Devices > Windows > Windows Enrollment > MDM User Scope = All\n"
            "5. iOS enrollment:\n"
            "   - Install Company Portal from App Store\n"
            "   - Open > Sign in > follow enrollment prompts\n"
            "   - Install the management profile when prompted\n"
            "   - If 'Profile Failed to Install': Check Apple MDM certificate validity\n"
            "6. Android enrollment:\n"
            "   - Install Company Portal from Play Store\n"
            "   - Sign in > Set up Work Profile\n"
            "   - If fails: Ensure Android Enterprise is connected in Intune\n"
            "7. Autopilot: For new Windows devices, check Autopilot deployment profile assignment"
        ),
    },
    {
        "category": "Cloud & M365",
        "problem_title": "Power BI report not loading or showing data errors",
        "problem_description": "Power BI dashboards and reports show errors, fail to load data, display stale data, or scheduled refresh fails for shared reports.",
        "problem_keywords": "power bi, report error, data refresh, power bi failed, dashboard error, dataset refresh, power bi gateway",
        "solution_steps": (
            "1. Report not loading:\n"
            "   - Clear browser cache (Power BI Service runs in browser)\n"
            "   - Try a different browser or InPrivate mode\n"
            "   - Check Power BI service status: admin.microsoft.com > Health\n"
            "2. Data refresh failure:\n"
            "   - Power BI Service > Dataset > Settings > Scheduled Refresh\n"
            "   - Check: Refresh History for specific error messages\n"
            "   - Common: Credentials expired, data source unreachable\n"
            "3. On-premises data gateway:\n"
            "   - Required for on-premises data sources (SQL Server, file shares)\n"
            "   - Check gateway status: Power BI > Settings > Manage Gateways\n"
            "   - Gateway service must be running on the gateway server\n"
            "   - Credentials stored in gateway may need updating\n"
            "4. Credential issues:\n"
            "   - Dataset > Settings > Data source credentials > Edit Credentials\n"
            "   - Re-enter credentials if password changed\n"
            "   - Service accounts may have expired passwords\n"
            "5. Row-level security (RLS):\n"
            "   - Users see 'no data' but admin sees data: RLS not configured for user's role\n"
            "   - Check RLS roles in Power BI Desktop > Modeling > Manage Roles\n"
            "   - Assign users to roles in Power BI Service\n"
            "6. Capacity issues:\n"
            "   - Premium/Embedded capacity may be throttled\n"
            "   - Large datasets may exceed Pro license limits (1 GB)\n"
            "   - Premium: 10 GB per dataset, higher refresh frequency\n"
            "7. Publishing: If report was updated in Desktop, republish to the same workspace"
        ),
    },
    {
        "category": "Cloud & M365",
        "problem_title": "Azure Virtual Machine performance slow or unresponsive",
        "problem_description": "Azure VM is running slowly, experiencing high CPU/memory, or becoming unresponsive. Applications hosted on the VM are timing out.",
        "problem_keywords": "azure vm, virtual machine slow, azure performance, vm unresponsive, azure cpu, azure disk, vm size",
        "solution_steps": (
            "1. Check VM metrics:\n"
            "   - Azure Portal > VM > Monitoring > Metrics\n"
            "   - Key metrics: CPU %, Available Memory, Disk IOPS, Network In/Out\n"
            "   - Identify the bottleneck: CPU, memory, disk, or network\n"
            "2. CPU constrained:\n"
            "   - If CPU consistently >80%: VM size is too small\n"
            "   - Resize VM: VM > Size > select larger size\n"
            "   - This requires a VM restart\n"
            "   - Consider: B-series for bursty workloads (cheaper)\n"
            "3. Memory constrained:\n"
            "   - If available memory is low: Applications are paging to disk\n"
            "   - Resize to a memory-optimized size (E-series, M-series)\n"
            "   - Or: Identify which process is consuming memory\n"
            "4. Disk performance:\n"
            "   - Standard HDD: Very slow for production workloads\n"
            "   - Upgrade to Premium SSD or Ultra Disk\n"
            "   - Check: Disk IOPS consumed vs provisioned\n"
            "   - VM size also limits disk throughput (check VM limits)\n"
            "5. Temporary disk:\n"
            "   - Azure VMs have a temporary disk (D: on Windows)\n"
            "   - Data on temp disk is lost during maintenance\n"
            "   - Use temp disk for pagefile/swap only\n"
            "6. Boot diagnostics:\n"
            "   - If VM is unresponsive: VM > Support + troubleshooting > Boot diagnostics\n"
            "   - Shows: Screenshot of the console and serial log\n"
            "   - Can identify: Stuck at boot, BSOD, login prompt\n"
            "7. Serial console: VM > Support > Serial Console for direct console access when RDP fails"
        ),
    },
    {
        "category": "Cloud & M365",
        "problem_title": "Microsoft Teams external or guest user access issues",
        "problem_description": "External users can't join Teams, guest users can't access shared channels or files, or guest user experience is degraded with missing features.",
        "problem_keywords": "teams guest, external user, guest access, teams external, guest permissions, b2b, external collaboration",
        "solution_steps": (
            "1. Guest access settings:\n"
            "   - Teams Admin Center > Org-wide Settings > Guest Access\n"
            "   - 'Allow guest access in Teams' must be ON\n"
            "   - Configure specific guest permissions below\n"
            "2. External access vs Guest access:\n"
            "   - External access: Chat/call with users in other orgs (federation)\n"
            "   - Guest access: Added as member of a Team (sees channels, files)\n"
            "   - Both have separate settings in Teams Admin Center\n"
            "3. Azure AD guest settings:\n"
            "   - Azure Portal > Azure AD > External Identities > External collaboration settings\n"
            "   - Who can invite guests? (Admins, members, or guests themselves)\n"
            "   - Guest user access restrictions (limited or same as members)\n"
            "4. Specific domain restrictions:\n"
            "   - Teams Admin Center > External Access > blocked/allowed domains\n"
            "   - If allow list is configured: Guest's domain must be listed\n"
            "   - Azure AD > External Identities > Collaboration restrictions\n"
            "5. Guest can't access files:\n"
            "   - SharePoint sharing settings must allow external sharing\n"
            "   - SharePoint Admin > Sharing > at least 'New and existing guests'\n"
            "   - If 'Only people in your organization': Guests can't access files\n"
            "6. Guest experience:\n"
            "   - Guests don't see: Org chart, calendar scheduling, some apps\n"
            "   - Guests can: Chat, call, share files, attend meetings\n"
            "   - Guest switch tenants: User icon > Switch tenant\n"
            "7. Shared channels: For cross-org collaboration without guest accounts, use Shared Channels (preview)"
        ),
    },
    {
        "category": "Cloud & M365",
        "problem_title": "Microsoft 365 license assignment or management issues",
        "problem_description": "Users don't have the right M365 license, can't access certain services, or license assignment via group-based licensing shows errors.",
        "problem_keywords": "m365 license, license assignment, group license, license error, office license, insufficient licenses, license conflict",
        "solution_steps": (
            "1. Check user's licenses:\n"
            "   - M365 Admin Center > Users > Active Users > select user > Licenses\n"
            "   - Shows assigned licenses and enabled services\n"
            "   - Or PowerShell: Get-MgUserLicenseDetail -UserId user@domain.com\n"
            "2. Missing service:\n"
            "   - License is assigned but specific service is disabled\n"
            "   - Example: Teams is disabled within the E3 license\n"
            "   - Edit license > toggle ON the specific service\n"
            "3. Group-based licensing:\n"
            "   - Azure AD > Groups > select group > Licenses\n"
            "   - Check for 'Users with errors' count\n"
            "   - Common error: 'Not enough licenses' (pool exhausted)\n"
            "   - Common error: 'Conflicting service plans'\n"
            "4. Conflicting licenses:\n"
            "   - User has two licenses with overlapping services\n"
            "   - Example: E3 + Teams standalone = conflict\n"
            "   - Fix: Remove the redundant standalone license\n"
            "5. License count:\n"
            "   - M365 Admin Center > Billing > Licenses\n"
            "   - Shows: Available, Assigned, and total for each subscription\n"
            "   - Purchase more licenses or reclaim from inactive users\n"
            "6. Reclaim licenses:\n"
            "   - Run 'Inactive users' report in Admin Center > Reports\n"
            "   - Users not signed in for 90+ days may not need a license\n"
            "   - Remove license from inactive/departed users\n"
            "7. Automation: Use Azure AD dynamic groups to auto-assign licenses based on department/role"
        ),
    },
    {
        "category": "Cloud & M365",
        "problem_title": "Azure Multi-Factor Authentication (MFA) registration issues",
        "problem_description": "Users can't complete MFA registration, the registration prompt doesn't appear, or the registration page shows errors for new or existing users.",
        "problem_keywords": "mfa registration, azure mfa, mfa setup, authentication methods, mfa prompt, register mfa, security info",
        "solution_steps": (
            "1. MFA registration portal:\n"
            "   - Users register at: https://aka.ms/mysecurityinfo\n"
            "   - Or: They are prompted during sign-in when MFA is required\n"
            "2. Registration not prompted:\n"
            "   - Check: Is MFA actually required for this user?\n"
            "   - Per-user MFA: Azure AD > Users > Per-user MFA\n"
            "   - Conditional Access: Check if CA policy requires MFA\n"
            "   - Security Defaults: If enabled, all users must register within 14 days\n"
            "3. Registration page errors:\n"
            "   - Browser issues: Clear cache, try InPrivate/Incognito\n"
            "   - Phone number format: Use international format (+1 for US)\n"
            "   - App notification not received: Check phone internet connection\n"
            "4. Temporary Access Pass:\n"
            "   - Admin can issue a temporary pass for MFA registration\n"
            "   - Azure AD > Users > select user > Authentication Methods > Add > TAP\n"
            "   - User signs in with TAP and registers their permanent MFA method\n"
            "5. Authentication methods policy:\n"
            "   - Azure AD > Security > Authentication Methods\n"
            "   - Enable the methods you want: Authenticator, SMS, FIDO2, etc.\n"
            "   - Can target specific groups for each method\n"
            "6. Combined registration:\n"
            "   - Azure AD uses 'combined registration experience'\n"
            "   - If old registration page shows: Enable combined registration\n"
            "   - Azure AD > User Settings > Manage user feature preview settings\n"
            "7. Bulk registration: For new deployments, use 'Registration campaign' to prompt all users"
        ),
    },
    {
        "category": "Cloud & M365",
        "problem_title": "SharePoint site storage quota exceeded",
        "problem_description": "SharePoint Online site has reached its storage quota. Users can't upload files and receive 'storage limit exceeded' or 'site is out of space' errors.",
        "problem_keywords": "sharepoint storage, site quota, storage limit, sharepoint full, site storage, quota exceeded, sharepoint space",
        "solution_steps": (
            "1. Check site storage:\n"
            "   - SharePoint Admin Center > Sites > Active Sites\n"
            "   - Shows: Storage used and storage limit per site\n"
            "   - Or: Site Settings > Storage Metrics\n"
            "2. Identify large content:\n"
            "   - Site Settings > Storage Metrics\n"
            "   - Shows breakdown by library, list, recycle bin\n"
            "   - Often: Recycle bin holds significant data\n"
            "3. Empty recycle bins:\n"
            "   - Site Recycle Bin: Site Contents > Recycle Bin\n"
            "   - Second-stage recycle bin: Bottom of Recycle Bin page\n"
            "   - These count against storage quota\n"
            "4. Version history:\n"
            "   - Each file version counts toward storage\n"
            "   - Library Settings > Versioning > reduce max versions\n"
            "   - Default 500 versions per file can consume huge space\n"
            "   - Consider reducing to 50-100 versions\n"
            "5. Increase quota: SharePoint Admin Center > Sites > select site > Storage limit > increase"
        ),
    },
    {
        "category": "Cloud & M365",
        "problem_title": "Microsoft Forms or Planner access and creation issues",
        "problem_description": "Users can't create Microsoft Forms surveys or Planner boards. Forms show as read-only or Planner tab in Teams shows errors.",
        "problem_keywords": "microsoft forms, planner, forms access, planner not working, forms disabled, planner error, planner teams",
        "solution_steps": (
            "1. Forms licensing:\n"
            "   - Forms requires M365 Business/E1/E3/E5 license\n"
            "   - Check: User has an active M365 license with Forms enabled\n"
            "   - Admin Center > Users > Licenses > Microsoft Forms ON\n"
            "2. Forms disabled by admin:\n"
            "   - M365 Admin Center > Settings > Org settings > Microsoft Forms\n"
            "   - Check: 'Allow people in your org to use Forms'\n"
            "   - External sharing settings for forms\n"
            "3. Planner licensing:\n"
            "   - Planner is included in M365 Business/E1/E3/E5\n"
            "   - User must also have an Exchange Online mailbox\n"
            "   - Planner uses M365 Groups (requires group creation rights)\n"
            "4. Planner in Teams:\n"
            "   - Tasks by Planner tab: Check if Planner app is enabled\n"
            "   - Teams Admin Center > Teams Apps > Permission Policies\n"
            "   - Ensure 'Tasks by Planner and To Do' app is allowed\n"
            "5. Group creation: If users can't create Planner plans, check if M365 Group creation is restricted to specific groups"
        ),
    },
    {
        "category": "Cloud & M365",
        "problem_title": "Microsoft Defender for Office 365 quarantine and policy issues",
        "problem_description": "Legitimate emails are being quarantined by Defender for Office 365. Users can't access quarantine, or anti-phishing policies are too aggressive.",
        "problem_keywords": "quarantine, defender, safe links, safe attachments, anti-phishing, eop, email quarantine, false positive",
        "solution_steps": (
            "1. Check quarantine:\n"
            "   - Security.microsoft.com > Email & collaboration > Review > Quarantine\n"
            "   - Users can access their own quarantine at security.microsoft.com/quarantine\n"
            "   - Admin can release quarantined messages\n"
            "2. Release false positives:\n"
            "   - Select the message > Release (delivers to inbox)\n"
            "   - Report as 'not junk' to improve future detection\n"
            "   - Submit to Microsoft for analysis\n"
            "3. Anti-spam policy:\n"
            "   - Security > Policies > Anti-spam > check thresholds\n"
            "   - Bulk mail threshold: Lower = more aggressive (default 7)\n"
            "   - Allow list: Add trusted senders or domains\n"
            "4. Anti-phishing policy:\n"
            "   - Impersonation protection may block legitimate senders\n"
            "   - Add trusted senders to impersonation exceptions\n"
            "   - Mailbox intelligence can reduce false positives\n"
            "5. Safe Links/Attachments: If blocking legitimate URLs or files, add to tenant allow/block list"
        ),
    },
    {
        "category": "Cloud & M365",
        "problem_title": "Microsoft Teams phone system or calling issues",
        "problem_description": "Teams phone system calls failing, no dial tone, calls dropping, or unable to make/receive PSTN calls through Teams calling plans or Direct Routing.",
        "problem_keywords": "teams phone, teams calling, pstn, dial tone, direct routing, calling plan, teams voice, phone system",
        "solution_steps": (
            "1. Check licensing:\n"
            "   - Phone System license must be assigned\n"
            "   - Calling Plan OR Direct Routing must be configured\n"
            "   - Admin Center > Users > Licenses > Phone System\n"
            "2. Phone number assignment:\n"
            "   - Teams Admin Center > Voice > Phone Numbers\n"
            "   - Is a number assigned to the user?\n"
            "   - Emergency address must be set for E911 compliance\n"
            "3. Calling policy:\n"
            "   - Teams Admin Center > Voice > Calling Policies\n"
            "   - Check: 'Make private calls' is enabled\n"
            "   - Voicemail, call forwarding, simultaneous ring settings\n"
            "4. Direct Routing:\n"
            "   - Session Border Controller (SBC) must be online and paired\n"
            "   - Teams Admin Center > Voice > Direct Routing > check SBC status\n"
            "   - Voice routing policies must route calls through the SBC\n"
            "5. Quality: If calls drop or have poor audio, check Teams Admin Center > Analytics > Call Quality Dashboard"
        ),
    },
    {
        "category": "Cloud & M365",
        "problem_title": "Azure AD security defaults vs Conditional Access conflicts",
        "problem_description": "Organization has enabled both security defaults and Conditional Access policies causing conflicts, unexpected MFA prompts, or blocked access.",
        "problem_keywords": "security defaults, conditional access, mfa conflict, azure ad security, ca policy, baseline policy, security conflict",
        "solution_steps": (
            "1. Security Defaults vs Conditional Access:\n"
            "   - Security Defaults: Free, basic protection (MFA for all, block legacy auth)\n"
            "   - Conditional Access: Paid (Azure AD P1+), granular policies\n"
            "   - CANNOT use both simultaneously\n"
            "2. Check current state:\n"
            "   - Azure Portal > Azure AD > Properties > Manage Security Defaults\n"
            "   - If enabled: All Conditional Access policies are ignored\n"
            "   - Disable Security Defaults before creating CA policies\n"
            "3. Migration path:\n"
            "   - Create CA policies that replicate Security Defaults:\n"
            "   - Policy 1: Require MFA for all users\n"
            "   - Policy 2: Block legacy authentication\n"
            "   - Policy 3: Require MFA for admin roles\n"
            "4. then disable Security Defaults after CA policies are active\n"
            "   - Test with a pilot group first\n"
            "   - Use 'Report-only' mode to preview CA impact\n"
            "5. Break glass: Always exclude 2 emergency admin accounts from ALL Conditional Access policies"
        ),
    },
]

DIAGNOSTIC_TREE = {
    "category": "Cloud & M365",
    "root": {
        "title": "Cloud & M365 Troubleshooting",
        "node_type": "question",
        "question_text": "What cloud service issue are you experiencing?",
        "children": [
            {
                "title": "User cannot sign into M365",
                "node_type": "question",
                "question_text": "What error or behavior is the user seeing?",
                "children": [
                    {
                        "title": "Wrong password / Account locked",
                        "node_type": "solution",
                        "solution_text": "1. Reset password: M365 Admin > Users > Reset password\n2. Check Azure AD sign-in logs for error codes\n3. If hybrid: Check on-prem AD account status too\n4. Wait 15 min for lockout to clear, or unlock in AD\n5. If MFA issue: Reset MFA from Azure AD > User > Authentication methods"
                    },
                    {
                        "title": "Conditional Access / device blocking",
                        "node_type": "solution",
                        "solution_text": "1. Check Azure AD sign-in logs: Filter by user > Conditional Access tab\n2. Identify which policy is blocking\n3. Common: Non-compliant device, wrong location, unapproved app\n4. Fix: Make device compliant, or adjust CA policy\n5. Temporary: Create an exclusion for the user while troubleshooting"
                    }
                ]
            },
            {
                "title": "SharePoint access issues",
                "node_type": "solution",
                "solution_text": "1. Check site permissions: Site Settings > Site permissions\n2. Add user as member/visitor\n3. If M365 Group-linked: Add user to the M365 Group\n4. Check external sharing settings for external users\n5. Clear browser cache, try InPrivate mode\n6. Check M365 Service Health for outages"
            },
            {
                "title": "OneDrive sync problems",
                "node_type": "solution",
                "solution_text": "1. Check OneDrive icon in system tray for errors\n2. Check for invalid file names/paths (no # % & : | chars)\n3. Reset: %localappdata%\\Microsoft\\OneDrive\\onedrive.exe /reset\n4. Check storage quota\n5. Check network: Remove upload/download bandwidth limits\n6. Unlink and relink account if persistent"
            },
            {
                "title": "Azure AD Connect / sync issues",
                "node_type": "solution",
                "solution_text": "1. Check sync status: M365 Admin > Health > Directory Sync Status\n2. On AAD Connect server: Open Synchronization Service Manager\n3. Force sync: Start-ADSyncSyncCycle -PolicyType Delta\n4. Check for sync errors (duplicate attributes, invalid chars)\n5. Check AAD Connect server health (disk, time, connectivity)\n6. Check Event Viewer: ADSync and Directory Synchronization sources"
            },
            {
                "title": "M365 service outage",
                "node_type": "solution",
                "solution_text": "1. Check: admin.microsoft.com > Health > Service health\n2. Check status.office365.com and downdetector.com\n3. If confirmed: Communicate to users, provide workarounds\n4. If not listed: Check local network, clear cache, try different browser\n5. Open support ticket with impact details\n6. Verify resolution with users after outage ends"
            }
        ]
    }
}
