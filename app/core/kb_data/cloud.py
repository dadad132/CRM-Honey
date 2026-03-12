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
