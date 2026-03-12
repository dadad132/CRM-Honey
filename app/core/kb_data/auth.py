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
