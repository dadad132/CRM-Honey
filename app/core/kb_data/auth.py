"""Authentication, accounts and access troubleshooting articles and diagnostic tree."""

ARTICLES = [
    {
        "category": "Account & Access",
        "problem_title": "Active Directory account locked out repeatedly",
        "problem_description": "User's AD account keeps getting locked out frequently. After unlocking, it locks again within minutes or hours.",
        "problem_keywords": "account locked, lockout, ad locked, active directory lockout, locked out, login failed, lockout policy",
        "solution_steps": (
            "1. Unlock the account immediately:\n"
            "   - AD Users and Computers > find user > Properties > Account > Unlock account\n"
            "   - Or PowerShell: Unlock-ADAccount -Identity username\n"
            "2. Find the source of the lockouts:\n"
            "   - On the PDC emulator domain controller:\n"
            "   - Event Viewer > Security log > filter Event ID 4740\n"
            "   - The 'Caller Computer Name' field shows which device is sending bad passwords\n"
            "3. Use Microsoft Account Lockout Tools:\n"
            "   - Download AccountLockout tools from Microsoft\n"
            "   - Run LockoutStatus.exe - shows lockout time and source DC\n"
            "   - Run EventCombMT.exe - searches all DCs for lockout events\n"
            "4. Common lockout sources:\n"
            "   - Mobile phone with old password for email\n"
            "   - Mapped drives with saved credentials\n"
            "   - Scheduled tasks running under the user's account\n"
            "   - Services running as the user (services.msc)\n"
            "   - Cached credentials in Credential Manager\n"
            "   - RDP sessions with old credentials\n"
            "   - Old browser sessions (Chrome autofill, etc.)\n"
            "5. On the source device:\n"
            "   - Clear Credential Manager entries\n"
            "   - Update stored passwords\n"
            "   - Check saved Wi-Fi credentials using the user account"
        ),
    },
    {
        "category": "Account & Access",
        "problem_title": "Cannot reset password or password doesn't meet requirements",
        "problem_description": "User cannot change their password. Gets 'password does not meet complexity requirements' or 'password recently used' errors.",
        "problem_keywords": "password reset, password requirements, complexity, cannot change password, password policy, password history",
        "solution_steps": (
            "1. Check password policy:\n"
            "   - CMD: net accounts (shows local policy)\n"
            "   - For domain: gpresult /r to see applied policy\n"
            "2. Default AD password complexity requires:\n"
            "   - At least 3 of: uppercase, lowercase, numbers, special characters\n"
            "   - Minimum 8 characters (varies by policy)\n"
            "   - Cannot contain the user's username or display name\n"
            "   - Cannot be any of the last X passwords (history)\n"
            "3. Common reasons password change fails:\n"
            "   - Minimum password age: Must wait X days after last change\n"
            "   - Password history: Cannot reuse recent passwords\n"
            "   - Password contains your name or username\n"
            "4. Admin reset:\n"
            "   - AD Users and Computers > user > Reset Password\n"
            "   - Check 'User must change password at next logon' if needed\n"
            "   - PowerShell: Set-ADAccountPassword -Identity user -Reset -NewPassword (ConvertTo-SecureString 'TempP@ss1' -AsPlainText -Force)\n"
            "5. If user is in a special OU with different policy:\n"
            "   - Check Fine-Grained Password Policies (PSOs)\n"
            "   - Get-ADFineGrainedPasswordPolicy -Filter *\n"
            "6. For local accounts: Use net user username newpassword from admin CMD"
        ),
    },
    {
        "category": "Account & Access",
        "problem_title": "MFA (Multi-Factor Authentication) issues",
        "problem_description": "User cannot complete MFA verification. Authenticator app not generating codes, not receiving text messages, or MFA prompt not appearing.",
        "problem_keywords": "mfa, multi-factor, authenticator, two-factor, 2fa, verification code, mfa failed, authenticator app",
        "solution_steps": (
            "1. Authenticator app not generating codes:\n"
            "   - Check phone time is correct (auto sync): Settings > Date & Time > auto\n"
            "   - Authenticator may need time sync: Open app > Settings > Time correction for codes\n"
            "   - If phone was reset/replaced: Re-register MFA (need admin help)\n"
            "2. Not receiving SMS codes:\n"
            "   - Check phone has signal and can receive texts\n"
            "   - Check the phone number on file is correct\n"
            "   - SMS may be blocked by carrier - try a different method\n"
            "3. MFA prompt not appearing:\n"
            "   - Check phone has internet connection for push notifications\n"
            "   - Open authenticator app manually and approve\n"
            "   - Try 'I can't use my Microsoft Authenticator app right now' for alternate method\n"
            "4. To reset MFA for a user (Admin):\n"
            "   - Azure AD > Users > find user > Authentication methods > Require re-register MFA\n"
            "   - Or: AzureAD > Users > user > Revoke MFA sessions\n"
            "5. Backup methods:\n"
            "   - Set up multiple MFA methods (app + phone + backup email)\n"
            "   - Save recovery codes when setting up MFA\n"
            "6. For new phone: Transfer authenticator accounts before wiping old phone\n"
            "   - Microsoft Authenticator has cloud backup feature"
        ),
    },
    {
        "category": "Account & Access",
        "problem_title": "User cannot log into domain-joined computer",
        "problem_description": "User enters correct credentials but cannot log into the domain computer. May show 'logon failure', 'trust relationship failed', or 'no logon servers available'.",
        "problem_keywords": "cannot login, domain login, logon failure, trust relationship, logon server, domain logon, login failed",
        "solution_steps": (
            "1. 'Trust relationship failed':\n"
            "   - Log in with a local admin account\n"
            "   - Remove from domain: System Properties > Change > set to WORKGROUP\n"
            "   - Restart > rejoin the domain > restart\n"
            "   - Or PowerShell (Admin): Reset-ComputerMachinePassword -Credential domain\\admin\n"
            "2. 'No logon servers available':\n"
            "   - PC can't reach the domain controller (DC)\n"
            "   - Check network cable/Wi-Fi connection\n"
            "   - Check DNS: ipconfig /all > DNS should point to DC\n"
            "   - Ping the DC: ping dc-name\n"
            "   - If VPN is required: connect to VPN before logging in, or use cached credentials\n"
            "3. 'Account has been locked out':\n"
            "   - Contact IT admin to unlock in AD\n"
            "   - Find lockout source (see Account Lockout troubleshooting)\n"
            "4. 'Password has expired':\n"
            "   - Press OK on the message > Windows will prompt for password change\n"
            "   - If not on network: Can't change - use VPN or contact IT for reset\n"
            "5. Work with cached credentials:\n"
            "   - If you've logged in before, Windows can use cached credentials\n"
            "   - This only works for the last few users who logged into that PC\n"
            "6. Check that the account isn't disabled in AD\n"
            "7. Check computer time is within 5 minutes of DC time"
        ),
    },
    {
        "category": "Account & Access",
        "problem_title": "VPN won't authenticate or certificate errors",
        "problem_description": "VPN connection fails with authentication or certificate errors. May show certificate expired, untrusted CA, or authentication method mismatch.",
        "problem_keywords": "vpn certificate, vpn auth, certificate expired, vpn authentication, ssl vpn, vpn login fail, certificate error",
        "solution_steps": (
            "1. Certificate expired:\n"
            "   - Check certificate dates: certmgr.msc > Personal > Certificates\n"
            "   - If expired: Request new certificate from your CA or IT admin\n"
            "   - For SSL VPN: Server certificate may be expired - contact VPN admin\n"
            "2. 'The certificate is not trusted':\n"
            "   - Install the root CA certificate:\n"
            "   - Get the CA cert from IT > double-click > Install > Local Machine > Trusted Root Certification Authorities\n"
            "3. Authentication method mismatch:\n"
            "   - VPN Properties > Security > check authentication method\n"
            "   - Must match what the VPN server expects (EAP, MS-CHAPv2, certificate, etc.)\n"
            "4. Credential issues:\n"
            "   - Delete saved VPN credentials: Credential Manager > remove VPN entries\n"
            "   - Re-enter username and password\n"
            "   - For domain auth: Use domain\\username or user@domain format\n"
            "5. Windows update may break VPN:\n"
            "   - Some updates change IPSEC/L2TP behavior\n"
            "   - Check for recent updates and uninstall if VPN worked before\n"
            "6. Update VPN client software to latest version\n"
            "7. Check with IT admin if your account has VPN permissions"
        ),
    },
    {
        "category": "Account & Access",
        "problem_title": "SSO (Single Sign-On) not working - keeps asking to login",
        "problem_description": "Users have to log in repeatedly to applications that should use Single Sign-On. Browser keeps redirecting to login page.",
        "problem_keywords": "sso, single sign-on, sso not working, keeps asking login, sso login, federated, saml, oidc",
        "solution_steps": (
            "1. Clear browser cookies and cache:\n"
            "   - Ctrl+Shift+Del > clear all data\n"
            "   - SSO tokens are often stored in cookies\n"
            "2. Check browser settings:\n"
            "   - Ensure third-party cookies are not blocked for the SSO domain\n"
            "   - Add the SSO IdP URL to trusted sites\n"
            "   - For NTLM/Kerberos SSO: Add the IdP to the Intranet zone\n"
            "3. Kerberos SSO issues:\n"
            "   - Check clock skew: Time must be within 5 min of DC\n"
            "   - Flush Kerberos tickets: klist purge\n"
            "   - Get new tickets: klist get krbtgt\n"
            "   - Check: klist (should show valid TGT)\n"
            "4. For Azure AD SSO:\n"
            "   - Check Seamless SSO settings in Azure AD Connect\n"
            "   - Verify the AZUREADSSOACC computer account in AD\n"
            "   - Check the Kerberos key hasn't expired (roll it every 30 days)\n"
            "5. For SAML SSO:\n"
            "   - Check SAML assertion in browser dev tools (Network tab)\n"
            "   - Verify certificate hasn't expired on IdP or SP side\n"
            "   - Check nameID format and attribute mappings\n"
            "6. Try InPrivate/Incognito browser to test without cached state\n"
            "7. Check if Conditional Access policies are blocking access"
        ),
    },
    {
        "category": "Account & Access",
        "problem_title": "Azure AD / Entra ID Conditional Access blocking user",
        "problem_description": "User cannot access cloud applications. Gets blocked by Conditional Access policy with messages like 'You can't get there from here' or 'Device compliance required'.",
        "problem_keywords": "conditional access, blocked, can't access, device compliance, entra id, azure ad, access denied cloud",
        "solution_steps": (
            "1. Identify the blocking policy:\n"
            "   - Azure Portal > Entra ID > Sign-in logs > find the user's failed attempt\n"
            "   - Check the 'Conditional Access' tab to see which policy blocked access\n"
            "2. 'Device compliance required':\n"
            "   - The device must be enrolled in Intune and compliant\n"
            "   - Check device compliance: Intune > Devices > find device > Compliance\n"
            "   - Common non-compliance: Missing updates, no encryption, no antivirus\n"
            "   - Fix the compliance issue on the device\n"
            "3. 'Require Hybrid Azure AD Join':\n"
            "   - Device must be joined to both on-prem AD and Azure AD\n"
            "   - Check status: dsregcmd /status > look for AzureAdJoined: YES\n"
            "   - If not joined: Check Azure AD Connect sync, verify device is in AD\n"
            "4. 'Require approved client app':\n"
            "   - User must use a specific app (e.g., Outlook instead of native mail)\n"
            "5. Location-based blocking:\n"
            "   - User may be outside allowed locations\n"
            "   - Use VPN to connect from a trusted location\n"
            "6. 'Require MFA':\n"
            "   - Ensure MFA is set up for the user\n"
            "7. As admin: Review and adjust CA policies if too restrictive\n"
            "   - Test with 'What If' tool in Conditional Access"
        ),
    },
    {
        "category": "Account & Access",
        "problem_title": "NTLM or Kerberos authentication failures",
        "problem_description": "Authentication fails in domain environment. Applications or services get NTLM/Kerberos errors. May see 'Access Denied' when accessing domain resources.",
        "problem_keywords": "kerberos error, ntlm failure, authentication, krb, spn, kerberos ticket, domain auth, negotiate failure",
        "solution_steps": (
            "1. Check Kerberos tickets:\n"
            "   - CMD: klist (shows current Kerberos tickets)\n"
            "   - klist purge (clear all tickets)\n"
            "   - Sign out/in to get new tickets\n"
            "2. Kerberos: Check time sync:\n"
            "   - Must be within 5 minutes of DC\n"
            "   - w32tm /query /status (check sync status)\n"
            "   - w32tm /resync (force sync)\n"
            "3. SPN (Service Principal Name) issues:\n"
            "   - Kerberos double-hop or SPN errors:\n"
            "   - setspn -L accountname (list SPNs)\n"
            "   - setspn -A HTTP/servername.domain.com account (register SPN)\n"
            "   - Check for duplicate SPNs: setspn -X (find duplicates)\n"
            "4. Falling back to NTLM:\n"
            "   - If Kerberos fails, Windows falls back to NTLM\n"
            "   - NTLM may be blocked by policy: Check group policy\n"
            "   - Event ID 4776 (NTLM auth) and 4768 (Kerberos TGT) in Security logs\n"
            "5. DNS issues prevent Kerberos:\n"
            "   - Kerberos needs forward AND reverse DNS to work\n"
            "   - nslookup servername (and reverse: nslookup IP)\n"
            "6. For service accounts:\n"
            "   - Check if password has expired\n"
            "   - Use Managed Service Accounts (gMSA) for automatic password rotation"
        ),
    },
    {
        "category": "Account & Access",
        "problem_title": "BitLocker recovery key needed or BitLocker locked out",
        "problem_description": "Computer is asking for a BitLocker recovery key at boot. Drive is encrypted and won't unlock with normal PIN/password.",
        "problem_keywords": "bitlocker recovery, recovery key, bitlocker locked, encrypted drive, bitlocker, tpm, boot",
        "solution_steps": (
            "1. Find the BitLocker recovery key:\n"
            "   - Microsoft account: https://aka.ms/myrecoverykey\n"
            "   - Azure AD/Entra ID: Sign in at myaccount.microsoft.com > Devices\n"
            "   - Active Directory: AD admin can retrieve keys from computer object\n"
            "   - USB drive: Check if key was saved to USB\n"
            "   - Printout: Check if the key was printed and stored\n"
            "2. Common triggers for recovery mode:\n"
            "   - BIOS/UEFI update\n"
            "   - Hardware changes (new RAM, motherboard repair)\n"
            "   - Boot order changes in BIOS\n"
            "   - TPM cleared or failed\n"
            "   - Secure Boot changes\n"
            "3. After entering recovery key:\n"
            "   - Suspend BitLocker before making BIOS changes:\n"
            "   - manage-bde -protectors -disable C:\n"
            "   - Make changes, then resume: manage-bde -protectors -enable C:\n"
            "4. If recovery key is lost:\n"
            "   - Check ALL possible locations (Azure AD, AD, Microsoft account, USB)\n"
            "   - If truly lost: Data is unrecoverable - reinstall Windows\n"
            "5. To prevent future issues:\n"
            "   - Back up recovery key to multiple locations\n"
            "   - Suspend BitLocker before BIOS updates\n"
            "   - Store keys in Azure AD for org-managed devices"
        ),
    },
    {
        "category": "Account & Access",
        "problem_title": "User profile corrupt or temporary profile loading",
        "problem_description": "Windows logs in with a temporary profile. User's files, desktop, and settings are missing. May show 'We can't sign into your account' notification.",
        "problem_keywords": "temporary profile, temp profile, corrupt profile, profile not loading, user profile, we can't sign in",
        "solution_steps": (
            "1. Sign out and restart the computer:\n"
            "   - Sometimes a simple restart fixes the temporary profile\n"
            "2. Fix via Registry (most common solution):\n"
            "   - Log in with a different admin account\n"
            "   - regedit > HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\ProfileList\n"
            "   - Find the SID key that matches the user (check ProfileImagePath)\n"
            "   - If there are two SID entries (one ending in .bak):\n"
            "   - Rename the one WITHOUT .bak to .old\n"
            "   - Rename the one WITH .bak to remove the .bak\n"
            "   - On the now-active key: Set 'State' DWORD to 0\n"
            "   - Delete 'RefCount' DWORD if it exists\n"
            "   - Restart\n"
            "3. If the profile is truly corrupt:\n"
            "   - Create a new user account\n"
            "   - Copy data from old profile: C:\\Users\\oldprofile to C:\\Users\\newprofile\n"
            "   - Copy: Desktop, Documents, Downloads, Pictures, Favorites, AppData\n"
            "4. Check disk space: Very low C: drive can cause profile load failures\n"
            "5. Run: sfc /scannow and DISM /Online /Cleanup-Image /RestoreHealth\n"
            "6. Check Event Viewer > Application log for User Profile Service errors"
        ),
    },
    {
        "category": "Account & Access",
        "problem_title": "Group Policy not applying or incorrect settings",
        "problem_description": "Group Policy settings are not being applied to users or computers. GPO created but changes not taking effect on target machines.",
        "problem_keywords": "group policy, gpo, policy not applying, gpupdate, gpo not working, group policy error",
        "solution_steps": (
            "1. Force Group Policy update:\n"
            "   - CMD: gpupdate /force\n"
            "   - Check result: gpresult /r (summary) or gpresult /h report.html\n"
            "2. Check GPO is linked and enabled:\n"
            "   - GPMC > find the GPO > check Linked Sites/Domains/OUs\n"
            "   - Ensure the link is enabled (not disabled or broken)\n"
            "   - Check 'Enforced' if needed to override other policies\n"
            "3. Check the computer/user is in the correct OU:\n"
            "   - GPOs apply to the OU they're linked to\n"
            "   - Move the object to the correct OU if needed\n"
            "4. Check GPO scope:\n"
            "   - Computer Configuration applies to computer objects\n"
            "   - User Configuration applies to user objects\n"
            "   - Don't confuse the two!\n"
            "5. Check security filtering:\n"
            "   - GPO > Scope > Security Filtering\n"
            "   - Must include the target users/computers/groups\n"
            "   - Also need 'Authenticated Users' with Read permission\n"
            "6. Check WMI filter:\n"
            "   - A WMI filter may be excluding the target\n"
            "   - Test: wmic path win32_operatingsystem get caption\n"
            "7. Block inheritance / Enforced:\n"
            "   - An OU may have 'Block Inheritance' set\n"
            "   - Use 'Enforced' on the GPO to override\n"
            "8. Check DC replication:\n"
            "   - repadmin /replsummary - ensure all DCs are in sync"
        ),
    },
    {
        "category": "Account & Access",
        "problem_title": "Windows Hello PIN not working or can't set up",
        "problem_description": "Windows Hello PIN doesn't work at login. 'Something went wrong' when setting up PIN. PIN option is greyed out or missing.",
        "problem_keywords": "windows hello, pin not working, pin error, hello pin, fingerprint, face recognition, something went wrong pin",
        "solution_steps": (
            "1. Reset the PIN:\n"
            "   - Settings > Accounts > Sign-in options > PIN > 'I forgot my PIN'\n"
            "   - This will sign out and allow re-setup\n"
            "2. Delete PIN data and recreate:\n"
            "   - Log in with password instead of PIN\n"
            "   - Delete: C:\\Windows\\ServiceProfiles\\LocalService\\AppData\\Local\\Microsoft\\NGC\n"
            "   - (May need to take ownership of NGC folder first)\n"
            "   - Restart > set up PIN again\n"
            "3. Check TPM:\n"
            "   - PIN requires TPM to be healthy\n"
            "   - Run: tpm.msc > check status = Ready\n"
            "   - If TPM shows error: Clear TPM in tpm.msc (this may require BitLocker suspension)\n"
            "4. For domain-joined PCs:\n"
            "   - Group Policy may restrict PIN: Computer Config > Admin Templates > Windows Hello\n"
            "   - PIN must be enabled in policy\n"
            "5. 'Something went wrong' during setup:\n"
            "   - Reset ngc folder (step 2 above)\n"
            "   - Check that the CNG Key Isolation service is running (services.msc)\n"
            "   - Run: dsregcmd /status to verify Azure AD/domain join status\n"
            "6. For fingerprint/face recognition:\n"
            "   - Update biometric driver from Device Manager > Biometric\n"
            "   - Remove and re-enroll biometric data"
        ),
    },
    {
        "category": "Account & Access",
        "problem_title": "User cannot access network shares despite correct permissions",
        "problem_description": "User has NTFS and share permissions but still gets 'Access Denied' when trying to access folders on the file server.",
        "problem_keywords": "access denied, share permissions, ntfs permissions, network share, file server, access error, folder access",
        "solution_steps": (
            "1. Check effective permissions:\n"
            "   - Right-click folder > Properties > Security > Advanced > Effective Access\n"
            "   - Enter the username and check the effective permissions\n"
            "   - Access = intersection of Share AND NTFS permissions (most restrictive wins)\n"
            "2. Share permissions vs NTFS:\n"
            "   - Share permissions (right-click > Sharing > Advanced Sharing > Permissions)\n"
            "   - NTFS permissions (right-click > Properties > Security)\n"
            "   - Both must allow the access type (Read, Write, Full Control)\n"
            "3. Group membership:\n"
            "   - AD group changes take effect after next logon\n"
            "   - User must log off and log back on to get new group token\n"
            "   - Check: whoami /groups (on the user's PC)\n"
            "4. ABE (Access-Based Enumeration):\n"
            "   - If enabled: Users can only see folders they have access to\n"
            "   - Server Manager > File Services > check ABE settings\n"
            "5. Broken inheritance:\n"
            "   - Folder Properties > Security > Advanced > check inheritance\n"
            "   - If inheritance is disabled: Permissions may be incomplete\n"
            "   - Re-enable inheritance from parent folders\n"
            "6. SID issues:\n"
            "   - Deleted and recreated accounts have different SIDs\n"
            "   - Old ACEs still reference the old SID (shows as unknown)\n"
            "   - Remove old SID entries and re-add the new account\n"
            "7. Network credentials: Windows Credential Manager may have cached wrong credentials"
        ),
    },
    {
        "category": "Account & Access",
        "problem_title": "Azure AD device registration failed or stale",
        "problem_description": "Device is not properly registered in Azure AD or shows stale registration. Conditional Access policies block access because device is unrecognized.",
        "problem_keywords": "azure ad device, device registration, conditional access, device compliance, intune enrollment, hybrid join, aad join",
        "solution_steps": (
            "1. Check device registration status:\n"
            "   - CMD: dsregcmd /status\n"
            "   - Look for: AzureAdJoined: YES/NO, DomainJoined: YES/NO\n"
            "   - WorkplaceJoined: YES/NO (personal device registered)\n"
            "2. Common issues:\n"
            "   - AzureAdJoined = NO: Device isn't registered\n"
            "   - Device certificate missing or expired\n"
            "   - Azure AD Connect sync issues (for hybrid join)\n"
            "3. Re-register the device:\n"
            "   - Settings > Accounts > Access work or school\n"
            "   - Disconnect and reconnect to your organization\n"
            "   - For Azure AD Join: May need to re-join the device\n"
            "4. For Hybrid Azure AD Join:\n"
            "   - Device must be in AD AND synced to Azure AD\n"
            "   - Check Azure AD Connect: Sync Status, error logs\n"
            "   - SCP (Service Connection Point) must be configured in AD\n"
            "   - dsregcmd /debug for detailed troubleshooting\n"
            "5. Stale device cleanup:\n"
            "   - Azure Portal > Azure AD > Devices > filter by 'stale'\n"
            "   - Delete stale device entries\n"
            "   - Re-register the device from the client\n"
            "6. Certificate issues:\n"
            "   - certmgr.msc > Personal > Certificates > look for device cert\n"
            "   - Issued by: MS-Organization-Access\n"
            "   - If expired or missing: Re-register\n"
            "7. Network: Device registration requires access to *.microsoftonline.com and device.login.microsoftonline.com"
        ),
    },
    {
        "category": "Account & Access",
        "problem_title": "RADIUS authentication failing for Wi-Fi or VPN",
        "problem_description": "Users cannot authenticate to enterprise Wi-Fi (WPA2-Enterprise) or VPN because RADIUS authentication is failing.",
        "problem_keywords": "radius, wpa2 enterprise, nps, radius reject, eap, wifi auth, 802.1x wireless, radius server",
        "solution_steps": (
            "1. Check NPS server logs:\n"
            "   - Event Viewer > Custom Views > Server Roles > Network Policy and Access Services\n"
            "   - Look for Event IDs: 6272 (accept), 6273 (reject)\n"
            "   - The reject reason code tells you exactly what failed\n"
            "2. Common reject reasons:\n"
            "   - Reason Code 16: Authentication failure (wrong password/cert)\n"
            "   - Reason Code 22: Client doesn't match any NPS policy\n"
            "   - Reason Code 48: NPS policy doesn't match connection request\n"
            "   - Reason Code 65: Incorrectly configured EAP type\n"
            "3. Certificate validation:\n"
            "   - EAP-TLS: Both client and server need valid certificates\n"
            "   - PEAP: Server needs a certificate trusted by the client\n"
            "   - Check cert expiry and trust chain on both sides\n"
            "4. NPS policy order:\n"
            "   - Policies are evaluated top-down, first match wins\n"
            "   - Ensure the correct policy matches before a deny-all policy\n"
            "   - Connection Request Policies > Network Policies\n"
            "5. RADIUS secret mismatch:\n"
            "   - The shared secret on the AP/switch must match the RADIUS client in NPS\n"
            "   - Re-enter the shared secret on both sides\n"
            "   - Case-sensitive! Check for trailing spaces\n"
            "6. Group membership:\n"
            "   - NPS policy condition may require specific AD group membership\n"
            "   - Verify the user is in the correct group\n"
            "7. Test from the client: Remove the Wi-Fi profile, reconnect, and check for certificate prompts"
        ),
    },
    {
        "category": "Account & Access",
        "problem_title": "Self-service password reset (SSPR) not working",
        "problem_description": "Users cannot use the self-service password reset feature in Azure AD / Microsoft 365. SSPR page shows errors or doesn't appear.",
        "problem_keywords": "sspr, self service, password reset, forgot password, reset password, azure ad password, microsoft 365 password",
        "solution_steps": (
            "1. Check SSPR is enabled:\n"
            "   - Azure Portal > Azure AD > Password reset\n"
            "   - 'Self service password reset enabled' = All or Selected\n"
            "   - If 'Selected': User must be in the enabled group\n"
            "2. User registration:\n"
            "   - Users must register for SSPR at aka.ms/ssprsetup\n"
            "   - Registration requires: Phone number, alternate email, or authenticator app\n"
            "   - If not registered: 'Contact your admin' error appears\n"
            "3. Authentication methods:\n"
            "   - Azure AD > Password reset > Authentication methods\n"
            "   - Set number of methods required (1 or 2)\n"
            "   - Configure available methods: Phone, Email, Security Questions, App\n"
            "4. For hybrid (on-premises AD + Azure AD):\n"
            "   - Password writeback must be enabled in Azure AD Connect\n"
            "   - Azure AD Connect > Optional features > Password writeback\n"
            "   - Without this: SSPR changes Azure AD password but not on-premises\n"
            "5. Licensing:\n"
            "   - SSPR requires Azure AD Premium P1 or P2 license\n"
            "   - Or Microsoft 365 Business Premium\n"
            "   - Check user license assignment in the admin portal\n"
            "6. Errors during reset:\n"
            "   - 'Password doesn't meet policy': On-premises password policy is too strict\n"
            "   - 'Contact your admin': User not enabled for SSPR or not registered\n"
            "7. Audit: Azure AD > Password reset > Audit logs (shows all SSPR activity)"
        ),
    },
    {
        "category": "Account & Access",
        "problem_title": "Service account password expired causing application failures",
        "problem_description": "An application stopped working because the service account's password expired. Scheduled tasks, services, and integrations fail simultaneously.",
        "problem_keywords": "service account, password expired, application failed, scheduled task, service logon, password expiry, managed account",
        "solution_steps": (
            "1. Identify the failed service account:\n"
            "   - Check Event Viewer > System for service logon failures\n"
            "   - Check Task Scheduler for failed tasks\n"
            "   - services.msc > Look for services in 'Stopped' state\n"
            "2. Reset the password:\n"
            "   - Active Directory Users and Computers > find the account\n"
            "   - Right-click > Reset Password\n"
            "   - Update the password everywhere it's used\n"
            "3. Update all places using the account:\n"
            "   - Services: services.msc > Properties > Log On tab > update password\n"
            "   - Scheduled Tasks: Task Scheduler > Properties > update credentials\n"
            "   - IIS Application Pools: IIS Manager > App Pools > Advanced > Identity\n"
            "   - SQL Server services: SQL Server Configuration Manager\n"
            "4. Prevent future expiry:\n"
            "   - AD account Properties > Account tab > 'Password never expires'\n"
            "   - Better: Use Group Managed Service Accounts (gMSA)\n"
            "   - gMSA: AD automatically manages the password\n"
            "5. Set up gMSA:\n"
            "   - PowerShell: New-ADServiceAccount -Name svc_app -DNSHostName svc.domain.com\n"
            "   - Install on target server: Install-ADServiceAccount svc_app\n"
            "   - Use 'svc_app$' as the service account\n"
            "6. Password change notification:\n"
            "   - Set up alerts for approaching password expiry\n"
            "   - PowerShell: Get-ADUser -Filter * -Properties PasswordExpires\n"
            "7. Document all service accounts and where they're used (critical!)"
        ),
    },
    {
        "category": "Account & Access",
        "problem_title": "User profile size too large causing slow logon",
        "problem_description": "User takes very long to log in because their roaming profile or redirected folders are too large. Login takes 5-15 minutes.",
        "problem_keywords": "slow logon, roaming profile, profile size, user profile, slow login, profile load, redirected folders",
        "solution_steps": (
            "1. Check profile size:\n"
            "   - C:\\Users\\username (local profile)\n"
            "   - Right-click > Properties > Size\n"
            "   - Profiles over 1 GB significantly slow logon\n"
            "2. Common profile bloaters:\n"
            "   - AppData\\Local\\Microsoft\\Outlook (large OST/PST files)\n"
            "   - Desktop folder (users storing files on Desktop)\n"
            "   - Downloads folder\n"
            "   - Browser cache (AppData\\Local\\Google\\Chrome)\n"
            "3. Folder Redirection:\n"
            "   - Redirect Desktop, Documents, etc. to a network share\n"
            "   - Group Policy > User Config > Windows Settings > Folder Redirection\n"
            "   - Files stay on the server, not in the roaming profile\n"
            "4. Exclude folders from roaming:\n"
            "   - Group Policy > User Config > Admin Templates > System > User Profiles\n"
            "   - 'Exclude directories in roaming profile'\n"
            "   - Add: AppData\\Local (should always be excluded)\n"
            "5. Profile cleanup:\n"
            "   - Remove temporary files: %temp%, AppData\\Local\\Temp\n"
            "   - Move large files off the Desktop to a network drive\n"
            "   - Configure Disk Cleanup to run on profiles\n"
            "6. Consider local profiles:\n"
            "   - If roaming isn't needed: Switch to local profiles\n"
            "   - Or use FSLogix Profile Containers (for VDI/RDS)\n"
            "7. Profile quota: Set profile quota via Group Policy to limit size"
        ),
    },
    {
        "category": "Account & Access",
        "problem_title": "OAuth / API token authentication errors",
        "problem_description": "Application integration fails with OAuth errors like 'invalid_grant', 'token expired', or 'consent required'. API access stops working.",
        "problem_keywords": "oauth, token, api auth, invalid grant, token expired, consent, bearer token, api key, refresh token",
        "solution_steps": (
            "1. Common OAuth errors:\n"
            "   - invalid_grant: Refresh token expired or revoked\n"
            "   - interaction_required: User must re-authenticate (consent changed)\n"
            "   - invalid_client: App registration issues\n"
            "   - AADSTS700003: Device code expired\n"
            "2. Refresh token expired:\n"
            "   - Azure AD refresh tokens expire after 90 days of inactivity\n"
            "   - Revoked if password changed\n"
            "   - Re-authenticate the application/user\n"
            "3. App registration check:\n"
            "   - Azure Portal > Azure AD > App registrations\n"
            "   - Verify: Client ID, redirect URI, and API permissions\n"
            "   - Check if client secret has expired (Certificates & secrets)\n"
            "4. Consent issues:\n"
            "   - Admin consent may be required for certain permissions\n"
            "   - Azure Portal > Enterprise Applications > app > Permissions > Grant admin consent\n"
            "5. Token validation:\n"
            "   - Check the token at jwt.ms (paste the token)\n"
            "   - Verify: aud (audience), iss (issuer), exp (expiry)\n"
            "   - audience must match the API you're calling\n"
            "6. Renew client secret:\n"
            "   - App registration > Certificates & secrets > New client secret\n"
            "   - Update the application configuration with the new secret\n"
            "   - Secrets expire: Set a calendar reminder before expiry\n"
            "7. Service principal: Ensure the Enterprise Application is enabled and not blocked"
        ),
    },
    {
        "category": "Account & Access",
        "problem_title": "Remote Desktop 'account is disabled' or 'not allowed'",
        "problem_description": "User gets 'Your account has been disabled' or 'The connection was denied because your user account is not authorized' when trying to RDP.",
        "problem_keywords": "rdp denied, account disabled, rdp not allowed, remote desktop access, user not authorized, rdp permission",
        "solution_steps": (
            "1. Check account status:\n"
            "   - Active Directory Users and Computers > find user > Properties > Account\n"
            "   - Ensure 'Account is disabled' is NOT checked\n"
            "   - Check: Account expiration date (Account expires field)\n"
            "2. Remote Desktop Users group:\n"
            "   - User must be in the 'Remote Desktop Users' group on the target machine\n"
            "   - Or be a local Administrator\n"
            "   - On target: Computer Management > Local Users > Groups > Remote Desktop Users\n"
            "   - Add the user or their AD group\n"
            "3. Group Policy:\n"
            "   - Computer Config > Windows Settings > Security > Local Policies > User Rights\n"
            "   - 'Allow log on through Remote Desktop Services' must include the user/group\n"
            "   - 'Deny log on through Remote Desktop Services' must NOT include the user\n"
            "4. NLA (Network Level Authentication):\n"
            "   - System Properties > Remote > 'Allow connections only from computers running RDP with NLA'\n"
            "   - If the client doesn't support NLA: Uncheck this (less secure)\n"
            "5. RD Gateway:\n"
            "   - If going through RD Gateway: User must be in the Gateway's authorization policy\n"
            "   - RAP (Resource Authorization Policy) and CAP (Connection Authorization Policy)\n"
            "6. Account lockout:\n"
            "   - The account may be locked (not disabled)\n"
            "   - AD account > 'Unlock account' checkbox\n"
            "7. MFA: If Conditional Access requires MFA for RDP, use RD Gateway with MFA support"
        ),
    },
    {
        "category": "Account & Access",
        "problem_title": "DNS-based authentication issues (SPN and delegation)",
        "problem_description": "Kerberos authentication fails with SPN errors. Double-hop authentication doesn't work. Web apps can't pass credentials to backend databases.",
        "problem_keywords": "spn, kerberos, delegation, double hop, service principal, constrained delegation, kerberos error",
        "solution_steps": (
            "1. Check SPN registration:\n"
            "   - CMD: setspn -L accountname (list SPNs for the account)\n"
            "   - Verify the correct SPN exists: HTTP/hostname, HTTP/hostname.domain.com\n"
            "   - Missing SPN: setspn -A HTTP/hostname accountname\n"
            "2. Duplicate SPN check:\n"
            "   - Duplicate SPNs cause authentication failures\n"
            "   - setspn -X (find duplicate SPNs in the domain)\n"
            "   - Remove duplicates: setspn -D SPN accountname\n"
            "3. Kerberos delegation (double-hop):\n"
            "   - Problem: User > Web Server > SQL Server (credentials don't pass through)\n"
            "   - AD: Service account > Delegation tab\n"
            "   - Option 1: 'Trust this user for delegation to any service' (unconstrained - risky)\n"
            "   - Option 2: 'Trust for delegation to specified services only' (constrained - recommended)\n"
            "4. Constrained delegation setup:\n"
            "   - On the middle-tier service account\n"
            "   - Add the SPN of the back-end service (e.g., MSSQLSvc/server:1433)\n"
            "   - Select 'Use any authentication protocol' if needed\n"
            "5. Resource-Based Constrained Delegation (RBCD):\n"
            "   - Modern approach: Configured on the back-end resource\n"
            "   - PowerShell: Set-ADComputer backend -PrincipalsAllowedToDelegateToAccount frontend$\n"
            "6. Kerberos event log:\n"
            "   - Enable Kerberos logging: HKLM\\SYSTEM\\CurrentControlSet\\Control\\Lsa\\Kerberos\\Parameters\n"
            "   - LogLevel = 1 (DWORD)\n"
            "   - Check System event log for Kerberos errors\n"
            "7. klist: Use 'klist tickets' to see current Kerberos tickets and verify TGT/TGS"
        ),
    },
    {
        "category": "Account & Access",
        "problem_title": "Shared computer logon very slow with multiple profiles",
        "problem_description": "Shared or multi-user computers have slow logons due to many user profiles cached on the machine. Disk space may also be low.",
        "problem_keywords": "shared computer, multiple profiles, slow logon, profile cleanup, disk full, user profiles, shared pc",
        "solution_steps": (
            "1. Check user profiles on disk:\n"
            "   - System Properties > Advanced > User Profiles > Settings\n"
            "   - Shows all profiles and their size\n"
            "   - Delete old profiles (select and Delete)\n"
            "2. Automatic profile cleanup:\n"
            "   - Group Policy > Computer Config > Admin Templates > System > User Profiles\n"
            "   - 'Delete user profiles older than a specified number of days on system restart'\n"
            "   - Set to 30-90 days depending on usage\n"
            "3. Disk Cleanup:\n"
            "   - cleanmgr > Clean up system files > Previous Windows installations\n"
            "   - Delete temp files, Windows Update cache\n"
            "4. Script cleanup:\n"
            "   - PowerShell: Get-CimInstance -Class Win32_UserProfile | Where {-not $_.Special -and $_.LastUseTime -lt (Get-Date).AddDays(-60)} | Remove-CimInstance\n"
            "   - Schedule as a maintenance task\n"
            "5. Mandatory profiles:\n"
            "   - For shared PCs: Use a mandatory profile\n"
            "   - All users get the same profile, changes aren't saved\n"
            "   - Create profile > rename NTUSER.DAT to NTUSER.MAN\n"
            "6. Shared PC mode (Windows 10/11):\n"
            "   - Settings > Accounts > Shared PC\n"
            "   - Or Intune: Device restrictions > Shared PC\n"
            "   - Automatically cleans up profiles\n"
            "7. FSLogix: For VDI/RDS, use FSLogix Profile Containers (profiles on network)"
        ),
    },
    {
        "category": "Account & Access",
        "problem_title": "Expired certificate blocking smart card or PIV logon",
        "problem_description": "Smart card or PIV card logon fails because the certificate on the card has expired or the issuing CA certificate is expired.",
        "problem_keywords": "smart card, piv, certificate expired, card logon, cac, smart card error, certificate logon, pki",
        "solution_steps": (
            "1. Check card certificate:\n"
            "   - Insert the smart card > open Certificate Manager or card middleware\n"
            "   - Check the certificate expiration date\n"
            "   - If expired: Certificate needs renewal\n"
            "2. Renew the certificate:\n"
            "   - Contact your PKI/security team to issue a new certificate\n"
            "   - May require physical visit to security office\n"
            "   - Some systems support online renewal via the card middleware\n"
            "3. CA certificate check:\n"
            "   - The issuing CA's certificate must be trusted on the domain controller\n"
            "   - Publish the CA cert in AD: certutil -dspublish ca-cert.cer\n"
            "   - Or: Group Policy for certificate distribution\n"
            "4. CRL/OCSP:\n"
            "   - Domain controller checks if the card cert is revoked\n"
            "   - CRL must be accessible: certutil -verify -urlfetch cert.cer\n"
            "   - If CRL endpoint is unreachable: Logon fails\n"
            "5. Domain controller certificate:\n"
            "   - DCs need a 'Domain Controller Authentication' certificate\n"
            "   - Check DC cert: certlm.msc > Personal > Certificates\n"
            "   - If expired: Re-enroll from the CA\n"
            "6. Smart card reader:\n"
            "   - Device Manager > Smart card readers > check for errors\n"
            "   - Try a different reader\n"
            "   - Update reader drivers\n"
            "7. Credential Manager: Delete any cached smart card credentials and retry"
        ),
    },
    {
        "category": "Account & Access",
        "problem_title": "Account lockout source is unknown or difficult to find",
        "problem_description": "A user's AD account keeps getting locked out but the source of the lockout is unknown. Need to identify which device or application is causing it.",
        "problem_keywords": "lockout source, account lockout, find lockout, lockout investigation, bad password, lockout tool, pdce",
        "solution_steps": (
            "1. Find the PDC Emulator:\n"
            "   - Account lockout events are forwarded to the PDC Emulator DC\n"
            "   - PowerShell: Get-ADDomain | Select PDCEmulator\n"
            "   - All investigation starts on this DC\n"
            "2. Check Security Event Log on PDCe:\n"
            "   - Event Viewer > Security > filter by Event ID 4740\n"
            "   - Shows: 'Caller Computer Name' = the source of the lockout\n"
            "   - Also check Event ID 4771 (Kerberos pre-auth failed) and 4776 (NTLM)\n"
            "3. Microsoft Account Lockout Tools:\n"
            "   - Download 'Account Lockout and Management Tools' from Microsoft\n"
            "   - LockoutStatus.exe: Shows lockout status on all DCs\n"
            "   - EventCombMT.exe: Search event logs across multiple DCs\n"
            "4. Common lockout sources:\n"
            "   - Old mapped drives with cached credentials\n"
            "   - Mobile devices with old password (ActiveSync)\n"
            "   - Scheduled tasks running as the user\n"
            "   - Saved RDP connections with old password\n"
            "   - Credential Manager entries\n"
            "5. On the source machine:\n"
            "   - Open Credential Manager > remove old entries for the user\n"
            "   - Check scheduled tasks running as the user\n"
            "   - Check services running as the user\n"
            "   - Check browser saved passwords\n"
            "6. Increase lockout threshold temporarily:\n"
            "   - While investigating, increase the threshold to avoid disruption\n"
            "   - Default Policy > Account Lockout Policy > Account lockout threshold\n"
            "7. NetLogon logging: Enable on the DC for detailed auth failure logs"
        ),
    },
    {
        "category": "Account & Access",
        "problem_title": "LDAP or LDAPS connection issues from applications",
        "problem_description": "Applications that use LDAP for authentication or directory queries fail to connect. LDAPS (secure LDAP) connections are refused.",
        "problem_keywords": "ldap, ldaps, ldap connection, directory service, active directory ldap, ldap bind, ldap ssl, port 389",
        "solution_steps": (
            "1. Test LDAP connectivity:\n"
            "   - LDAP: Port 389 (unencrypted) or Port 636 (LDAPS/SSL)\n"
            "   - Test-NetConnection -ComputerName dc.domain.com -Port 389\n"
            "   - Test-NetConnection -ComputerName dc.domain.com -Port 636\n"
            "2. LDAP bind test:\n"
            "   - ldp.exe (built into Windows RSAT)\n"
            "   - Connection > Connect > server: dc.domain.com, port: 389\n"
            "   - Connection > Bind > enter credentials\n"
            "   - For LDAPS: Check SSL box, port 636\n"
            "3. LDAPS certificate:\n"
            "   - LDAPS requires a certificate on the domain controller\n"
            "   - The DC needs a cert with the DC's FQDN in the subject\n"
            "   - certlm.msc > Personal > Certificates on the DC\n"
            "   - Issue from internal CA or install a third-party cert\n"
            "4. Certificate trust:\n"
            "   - The application/client must trust the CA that issued the DC cert\n"
            "   - Import the Root CA cert on the client machine\n"
            "   - For Linux/Java apps: Import into the Java trust store or OS CA bundle\n"
            "5. Channel binding and signing:\n"
            "   - Microsoft is enforcing LDAP signing and channel binding\n"
            "   - Applications must support signed LDAP or use LDAPS\n"
            "   - Check: Group Policy > LDAP server signing requirements\n"
            "6. Firewall:\n"
            "   - Ensure ports 389 (LDAP), 636 (LDAPS), 3268/3269 (Global Catalog) are open\n"
            "7. Application config: Verify the LDAP URL format: ldap://dc.domain.com or ldaps://dc.domain.com:636"
        ),
    },
    {
        "category": "Account & Access",
        "problem_title": "Fine-grained password policy not applying to users",
        "problem_description": "Password policy configured for a security group in AD is not being enforced. Users in the group still follow the default domain policy.",
        "problem_keywords": "password policy, fine grained, pso, password settings, adsi edit, password length, password complexity, granular",
        "solution_steps": (
            "1. Check FGPP requirements:\n"
            "   - Domain must be Windows Server 2008+ functional level\n"
            "   - FGPPs apply to: Users and Global Security Groups only\n"
            "   - Do NOT work on OUs directly (apply to groups in the OU instead)\n"
            "2. View existing FGPPs:\n"
            "   - AD Administrative Center > domain > System > Password Settings Container\n"
            "   - Or PowerShell: Get-ADFineGrainedPasswordPolicy -Filter *\n"
            "   - Check: Precedence, Applies To, and policy settings\n"
            "3. Check which PSO applies to a user:\n"
            "   - PowerShell: Get-ADUserResultantPasswordPolicy username\n"
            "   - If null: Default Domain Policy applies\n"
            "   - If a PSO name: That FGPP is in effect\n"
            "4. Common issues:\n"
            "   - PSO applied to a Distribution Group (must be Security Group)\n"
            "   - PSO applied to an OU (doesn't work - must be group or user)\n"
            "   - Precedence conflict: Lower number = higher priority\n"
            "5. Create or modify FGPP:\n"
            "   - AD Administrative Center > Password Settings Container > New\n"
            "   - Set: Minimum length, complexity, lockout threshold, etc.\n"
            "   - Set precedence (1 = highest priority)\n"
            "   - 'Directly Applies To': Add the security group\n"
            "6. Group nesting:\n"
            "   - FGPPs do NOT apply through nested groups\n"
            "   - The user must be a DIRECT member of the group\n"
            "7. After changes: User must change their password for the new policy to take full effect"
        ),
    },
    {
        "category": "Account & Access",
        "problem_title": "Cross-domain or cross-forest authentication failures",
        "problem_description": "Users from a trusted domain or forest cannot authenticate to resources. Trust relationship errors or access denied to cross-domain resources.",
        "problem_keywords": "trust, cross domain, cross forest, trust relationship, forest trust, domain trust, external trust, selective auth",
        "solution_steps": (
            "1. Verify trust status:\n"
            "   - Active Directory Domains and Trusts > right-click domain > Properties > Trusts\n"
            "   - Select the trust > Validate\n"
            "   - Or PowerShell: Get-ADTrust -Filter *\n"
            "2. Test trust:\n"
            "   - nltest /sc_verify:trustedDomain (from a DC)\n"
            "   - netdom verify /domain:trustedDomain\n"
            "   - Should show 'The command completed successfully'\n"
            "3. Common trust issues:\n"
            "   - DNS resolution between domains must work both ways\n"
            "   - Conditional forwarders must be configured\n"
            "   - Firewall between domains must allow AD ports (88, 389, 445, 135, etc.)\n"
            "4. Trust password reset:\n"
            "   - netdom trust localDomain /domain:remoteDomain /resetOnTrustedSide /passwordT:*\n"
            "   - Then: netdom trust localDomain /domain:remoteDomain /resetOnTrustingSide /passwordT:*\n"
            "5. Selective authentication:\n"
            "   - If the trust uses Selective Authentication\n"
            "   - Users must be explicitly granted 'Allowed to Authenticate' permission\n"
            "   - On the target server's AD computer object > Security > Add 'Allowed to Authenticate'\n"
            "6. SID filtering:\n"
            "   - External trusts enable SID filtering by default\n"
            "   - Can block access if SID history is used\n"
            "   - netdom trust /enableSIDHistory:yes (if needed)\n"
            "7. Name suffix routing: For forest trusts, ensure the UPN suffixes are routed properly"
        ),
    },
    {
        "category": "Account & Access",
        "problem_title": "Azure AD application registration and consent issues",
        "problem_description": "Third-party or custom applications can't get Azure AD tokens. Admin consent required errors appear or application permissions aren't working.",
        "problem_keywords": "app registration, azure ad app, admin consent, api permission, oauth, app consent, enterprise app",
        "solution_steps": (
            "1. Check the error message:\n"
            "   - 'AADSTS65001: Admin consent required': App needs admin approval\n"
            "   - 'AADSTS700016: Application not found': Wrong App ID or tenant\n"
            "   - Azure AD > Enterprise Applications > find the app\n"
            "2. Admin consent:\n"
            "   - Azure Portal > Azure AD > Enterprise Applications > select app\n"
            "   - Permissions tab > Grant admin consent\n"
            "   - Or: Global admin visits the consent URL\n"
            "3. App registration review:\n"
            "   - Azure AD > App Registrations > check redirect URIs\n"
            "   - Verify API permissions are correct\n"
            "   - Check client secret/certificate hasn't expired\n"
            "4. User consent settings:\n"
            "   - Azure AD > Enterprise Applications > Consent and Permissions\n"
            "   - 'Allow user consent for apps': Controls if users can approve apps themselves\n"
            "   - Restrict to admin-approved apps for security\n"
            "5. Token issues: Check that the required scopes are granted and not just requested"
        ),
    },
    {
        "category": "Account & Access",
        "problem_title": "Self-service group management and access review failures",
        "problem_description": "Users can't request group membership, group owners don't receive approval requests, or Azure AD access reviews are not completing.",
        "problem_keywords": "group management, access review, group membership, group approval, self-service group, azure ad group, entitlement",
        "solution_steps": (
            "1. Self-service group settings:\n"
            "   - Azure AD > Groups > General > Self-service group management\n"
            "   - 'Owners can manage group membership requests': Must be Yes\n"
            "   - 'Restrict user ability to access groups': check settings\n"
            "2. Group approval workflow:\n"
            "   - Group must have an owner to approve requests\n"
            "   - Azure AD > Groups > select group > Owners\n"
            "   - Add at least two owners for redundancy\n"
            "3. Access reviews:\n"
            "   - Azure AD > Identity Governance > Access Reviews\n"
            "   - Check: Is the review started? Are reviewers assigned?\n"
            "   - Reviewers get email notification (check spam)\n"
            "4. Review not completing:\n"
            "   - Check: Review end date hasn't passed\n"
            "   - If reviewers don't respond: Configure auto-apply of recommendations\n"
            "   - Settings > Auto apply results to resource\n"
            "5. Entitlement management: Use Access Packages for structured resource request workflows"
        ),
    },
    {
        "category": "Account & Access",
        "problem_title": "Cached credentials causing login to wrong account",
        "problem_description": "Windows Credential Manager has stored old or incorrect credentials. User keeps authenticating with the wrong account to network resources or web services.",
        "problem_keywords": "cached credentials, credential manager, saved password, wrong credentials, stored password, windows credentials",
        "solution_steps": (
            "1. Open Credential Manager:\n"
            "   - Control Panel > Credential Manager\n"
            "   - Or: Start > search 'Credential Manager'\n"
            "   - Shows: Web Credentials and Windows Credentials\n"
            "2. Windows Credentials:\n"
            "   - Look for entries pointing to the problematic server/service\n"
            "   - Click the entry > Remove\n"
            "   - Common entries: network shares, RDP connections, Exchange\n"
            "3. Web Credentials:\n"
            "   - Stored by browsers and apps\n"
            "   - Look for the service URL and remove old entries\n"
            "4. Command line:\n"
            "   - cmdkey /list (shows all stored credentials)\n"
            "   - cmdkey /delete:targetname (remove specific credential)\n"
            "   - Useful for scripting credential cleanup\n"
            "5. After clearing: Access the resource again and enter the correct credentials when prompted"
        ),
    },
    {
        "category": "Account & Access",
        "problem_title": "Windows Hello for Business provisioning failures",
        "problem_description": "Windows Hello for Business PIN or biometric setup fails during provisioning. Users get errors during OOBE or when trying to set up Hello in Settings.",
        "problem_keywords": "windows hello, hello for business, pin provisioning, biometric, hello error, hello setup, hello enrollment",
        "solution_steps": (
            "1. Check requirements:\n"
            "   - Azure AD joined or Hybrid Azure AD joined device\n"
            "   - User must have MFA registered\n"
            "   - TPM 2.0 chip (recommended)\n"
            "   - Windows 10/11 Pro or Enterprise\n"
            "2. Common errors:\n"
            "   - 'Something went wrong' during PIN setup: MFA not completed\n"
            "   - 'An error happened during PIN setup': TPM issue or network\n"
            "   - Run: dsregcmd /status to check device registration state\n"
            "3. TPM issues:\n"
            "   - Device Manager > Security Devices > check TPM\n"
            "   - tpm.msc to view TPM status\n"
            "   - Clear TPM in BIOS as last resort (will reset Hello)\n"
            "4. Policy:\n"
            "   - Intune: Device Configuration > Windows Hello for Business\n"
            "   - GPO: Computer Config > Admin Templates > Windows Hello for Business\n"
            "   - Check for conflicting policies\n"
            "5. Re-provision: Delete existing Hello container and re-provision from Settings > Accounts > Sign-in options"
        ),
    },
    {
        "category": "Account & Access",
        "problem_title": "Group Policy Preferences drive mapping not applying",
        "problem_description": "Network drive mappings configured via Group Policy Preferences don't appear for users. Drive letters are missing or map to the wrong location.",
        "problem_keywords": "drive mapping, gpp, group policy preferences, mapped drive, network drive, drive letter, map drive gpo",
        "solution_steps": (
            "1. Check GPP configuration:\n"
            "   - GPMC > GPO > User Config > Preferences > Windows Settings > Drive Maps\n"
            "   - Verify: Drive letter, UNC path, reconnect setting, label\n"
            "   - Action: 'Replace' is recommended (deletes and recreates)\n"
            "2. Item-level targeting:\n"
            "   - GPP supports targeting by security group, OU, IP range, etc.\n"
            "   - Check: Common tab > Item-level targeting\n"
            "   - Is the user in the targeted group?\n"
            "3. Credential issue:\n"
            "   - If UNC path requires different credentials (cross-domain):\n"
            "   - GPP drive maps run as the user, can't specify different creds\n"
            "   - Solution: Use netuse or cmdkey for cross-domain shares\n"
            "4. gpresult check:\n"
            "   - gpresult /r (shows applied GPOs including Preferences)\n"
            "   - gpresult /h report.html for detailed HTML report\n"
            "   - Look for drive map entries in the Preferences section\n"
            "5. Server availability: Verify the file server and share path are accessible from the user's workstation"
        ),
    },
]

DIAGNOSTIC_TREE = {
    "category": "Account & Access",
    "root": {
        "title": "Account & Access Troubleshooting",
        "node_type": "question",
        "question_text": "What account or access issue are you experiencing?",
        "children": [
            {
                "title": "Account is locked out",
                "node_type": "solution",
                "solution_text": "1. Unlock in AD: Find user > Properties > Account > Unlock\n2. Find lockout source:\n   - On PDC: Security log > Event ID 4740\n   - Shows 'Caller Computer Name' = the source\n3. Common sources:\n   - Mobile phone with old email password\n   - Mapped drives with saved credentials\n   - Running services/tasks with the account\n   - Old RDP sessions\n4. On source device: Clear Credential Manager\n5. Update password everywhere it's stored"
            },
            {
                "title": "Cannot log in to computer",
                "node_type": "question",
                "question_text": "What error message do you see?",
                "children": [
                    {
                        "title": "Trust relationship failed",
                        "node_type": "solution",
                        "solution_text": "1. Log in with local admin account (.\\administrator)\n2. Rejoin domain:\n   - Remove from domain (set to WORKGROUP) > restart\n   - Join domain again > restart\n3. Or use PowerShell (quicker):\n   - Reset-ComputerMachinePassword -Credential domain\\admin\n4. Check that DNS points to domain controller"
                    },
                    {
                        "title": "No logon servers available",
                        "node_type": "solution",
                        "solution_text": "1. Computer can't reach the domain controller\n2. Check network: Is cable plugged in? Is Wi-Fi connected?\n3. Check DNS: ipconfig /all - DNS should be the DC's IP\n4. Ping the DC by hostname and IP\n5. If working remotely: Connect VPN before login\n6. Can still log in with cached credentials if you've logged in before"
                    },
                    {
                        "title": "Other login error",
                        "node_type": "solution",
                        "solution_text": "1. Password expired: Change at the prompt or contact IT for reset\n2. Account disabled: IT admin must re-enable in AD\n3. Account not found: Check for typos in username\n4. Wrong password: Try Caps Lock off, correct keyboard layout\n5. Log in with local admin account to troubleshoot\n6. Check computer time is synced with DC (within 5 minutes)"
                    }
                ]
            },
            {
                "title": "MFA / Two-Factor issues",
                "node_type": "solution",
                "solution_text": "1. Authenticator not working: Check phone time is correct (auto-sync)\n2. Not receiving SMS: Check signal and phone number on file\n3. For Microsoft Authenticator: Re-register MFA (admin required)\n4. Admin reset: Azure AD > Users > Authentication methods > Re-register\n5. Set up backup MFA methods: app + phone + backup email\n6. Transfer authenticator to new phone BEFORE wiping old phone"
            },
            {
                "title": "BitLocker asking for recovery key",
                "node_type": "solution",
                "solution_text": "Find your recovery key:\n1. Microsoft account: https://aka.ms/myrecoverykey\n2. Azure AD: myaccount.microsoft.com > Devices\n3. IT admin: Can retrieve from AD or Intune\n4. USB drive or printout from initial setup\n\nPrevention:\n- Suspend BitLocker before BIOS changes\n- manage-bde -protectors -disable C:\n- Make changes, then re-enable"
            },
            {
                "title": "Temporary profile loading",
                "node_type": "solution",
                "solution_text": "1. Restart computer (may fix it)\n2. Fix via Registry:\n   - Log in as different admin user\n   - HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\ProfileList\n   - Find user's SID (check ProfileImagePath)\n   - If two entries (one with .bak): rename to swap them\n   - Set State=0, delete RefCount\n   - Restart\n3. If profile is truly corrupt:\n   - Create new user account\n   - Copy data from C:\\Users\\old to C:\\Users\\new"
            },
            {
                "title": "Group Policy not applying",
                "node_type": "solution",
                "solution_text": "1. Force update: gpupdate /force\n2. Check results: gpresult /h report.html > open in browser\n3. Verify GPO is linked and enabled in GPMC\n4. Check user/computer is in the correct OU\n5. Check Security Filtering includes the target\n6. Check for Block Inheritance on the OU\n7. Verify DC replication: repadmin /replsummary\n8. Computer Config = applies to computer objects\n   User Config = applies to user objects"
            }
        ]
    }
}
