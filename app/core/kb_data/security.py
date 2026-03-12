"""Security, malware, and incident response articles and diagnostic tree."""

ARTICLES = [
    {
        "category": "Security",
        "problem_title": "Computer infected with malware or virus",
        "problem_description": "Computer is showing signs of malware infection: popups, slow performance, unknown programs, browser redirects, or antivirus alerts.",
        "problem_keywords": "malware, virus, infected, popup, adware, trojan, worm, malware removal, antivirus",
        "solution_steps": (
            "1. Disconnect from network immediately:\n"
            "   - Unplug Ethernet or disable Wi-Fi to prevent spread\n"
            "   - Do NOT turn off the computer yet\n"
            "2. Boot into Safe Mode with Networking:\n"
            "   - Settings > Update & Security > Recovery > Restart Now\n"
            "   - Troubleshoot > Startup Settings > Restart > F5\n"
            "3. Run full antivirus scan:\n"
            "   - Windows Defender offline scan: Settings > Virus & threat protection > Scan options > Microsoft Defender Offline scan\n"
            "   - Download Malwarebytes (from known good PC): Run full scan\n"
            "   - Download AdwCleaner for adware\n"
            "4. Remove found threats:\n"
            "   - Quarantine/remove all detected items\n"
            "   - Reboot and scan again to verify clean\n"
            "5. Check for persistence mechanisms:\n"
            "   - msconfig > Startup: Disable unknown entries\n"
            "   - Task Scheduler: Remove suspicious scheduled tasks\n"
            "   - Check browser extensions: Remove unknown ones\n"
            "6. Check for unauthorized accounts:\n"
            "   - lusrmgr.msc > Users: Look for unknown accounts\n"
            "   - net user: List all local accounts\n"
            "7. Change all passwords from a clean device\n"
            "8. Update all software and OS patches\n"
            "9. Document the infection for the security team\n"
            "10. If malware persists: Consider reimaging the machine"
        ),
    },
    {
        "category": "Security",
        "problem_title": "Ransomware attack detected",
        "problem_description": "Files are encrypted, renamed with strange extensions, or a ransom note appears demanding payment. Critical data is inaccessible.",
        "problem_keywords": "ransomware, encrypted files, ransom note, files locked, decrypt, ransomware attack, crypto locker",
        "solution_steps": (
            "1. IMMEDIATELY disconnect the affected machine:\n"
            "   - Pull network cable AND disable Wi-Fi\n"
            "   - Do NOT restart the machine\n"
            "   - Do NOT pay the ransom\n"
            "2. Contain the spread:\n"
            "   - Identify all machines connected to same network\n"
            "   - Check file servers for encrypted files\n"
            "   - Consider isolating the network segment\n"
            "3. Identify the ransomware:\n"
            "   - Take photo of the ransom note\n"
            "   - Note the file extension (.locked, .encrypted, etc.)\n"
            "   - Check https://www.nomoreransom.org/ for free decryptors\n"
            "   - Upload sample to ID Ransomware\n"
            "4. Preserve evidence:\n"
            "   - Take screenshots of everything\n"
            "   - Save the ransom note file\n"
            "   - Document timeline of events\n"
            "5. Report the incident:\n"
            "   - Notify management and security team\n"
            "   - Contact cyber insurance provider\n"
            "   - Report to law enforcement (FBI IC3 or local equivalent)\n"
            "6. Recovery:\n"
            "   - Restore from clean backups (verify backups are not encrypted too)\n"
            "   - Reimage affected machines\n"
            "   - Change ALL passwords across the organization\n"
            "7. Post-incident:\n"
            "   - Determine entry point (phishing email, RDP exposure, etc.)\n"
            "   - Patch vulnerabilities\n"
            "   - Implement better backup strategy (3-2-1 rule)"
        ),
    },
    {
        "category": "Security",
        "problem_title": "Phishing email reported by user",
        "problem_description": "User received a suspicious email and may have clicked a link or opened an attachment. Need to assess and respond.",
        "problem_keywords": "phishing, suspicious email, phishing link, clicked phishing, fake email, scam email, email security",
        "solution_steps": (
            "1. If user clicked a link or opened attachment:\n"
            "   - Disconnect from network immediately\n"
            "   - Run full antivirus scan\n"
            "   - Change user's password from a different device\n"
            "   - Check for unauthorized email forwarding rules\n"
            "   - Check for MFA changes or new MFA devices registered\n"
            "2. If user only reported it (didn't click):\n"
            "   - Thank the user for reporting\n"
            "   - Collect the email (forward as attachment, not inline)\n"
            "3. Analyze the phishing email:\n"
            "   - Check sender address (not just display name)\n"
            "   - Hover over links to check actual URL\n"
            "   - Check for urgency tactics or unusual requests\n"
            "   - Look at email headers for origin\n"
            "4. Block the threat:\n"
            "   - Block the sender domain in email filter\n"
            "   - Block the phishing URL at the firewall/web filter\n"
            "   - Search mail logs: Did anyone else receive this email?\n"
            "   - Delete copies from all mailboxes\n"
            "5. If credentials were entered on phishing site:\n"
            "   - Reset password immediately\n"
            "   - Revoke all active sessions (Azure AD / M365)\n"
            "   - Check for unauthorized access in audit logs\n"
            "   - Enable MFA if not already enabled\n"
            "6. Send awareness alert to all staff about this phishing attempt"
        ),
    },
    {
        "category": "Security",
        "problem_title": "Antivirus disabled or not updating",
        "problem_description": "Windows Defender or third-party antivirus is disabled, won't turn on, or hasn't updated definitions in weeks.",
        "problem_keywords": "antivirus disabled, defender off, antivirus not updating, virus protection off, security center, definitions outdated",
        "solution_steps": (
            "1. Check Windows Security Center:\n"
            "   - Settings > Update & Security > Windows Security\n"
            "   - Check Virus & threat protection status\n"
            "2. If Defender won't enable:\n"
            "   - Check for conflicting third-party AV (only one AV should be active)\n"
            "   - Uninstall old AV completely: Use vendor's removal tool\n"
            "   - Check Tamper Protection: Settings > Windows Security > Virus & threat protection > Manage settings\n"
            "3. Re-enable via Group Policy:\n"
            "   - gpedit.msc > Computer Config > Admin Templates > Windows Components > Microsoft Defender Antivirus\n"
            "   - 'Turn off Microsoft Defender Antivirus' should be Not Configured or Disabled\n"
            "4. Re-enable via Registry:\n"
            "   - HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\n"
            "   - Delete 'DisableAntiSpyware' key if it exists\n"
            "5. Fix definition updates:\n"
            "   - Manual update: Windows Security > Virus & threat protection > Check for updates\n"
            "   - Or command line: MpCmdRun -SignatureUpdate\n"
            "6. Check Windows Update service:\n"
            "   - Defender updates come through Windows Update\n"
            "   - services.msc > Windows Update > should be Running\n"
            "7. If nothing works:\n"
            "   - sfc /scannow\n"
            "   - DISM /Online /Cleanup-Image /RestoreHealth\n"
            "   - Reset Windows Security: Get-AppxPackage Microsoft.SecHealthUI -AllUsers | Reset-AppxPackage"
        ),
    },
    {
        "category": "Security",
        "problem_title": "Suspicious account activity or unauthorized access",
        "problem_description": "Signs of unauthorized access: login from unknown location, account sending emails user didn't write, or unknown activity in audit logs.",
        "problem_keywords": "unauthorized access, account hacked, suspicious login, account compromised, security breach, login unknown location",
        "solution_steps": (
            "1. Immediate containment:\n"
            "   - Reset the user's password immediately\n"
            "   - Revoke all active sessions:\n"
            "     - Azure AD: Revoke Sessions in user properties\n"
            "     - On-prem: Reset password, which invalidates Kerberos tickets\n"
            "   - Disable the account if actively being abused\n"
            "2. Check for persistence:\n"
            "   - Check email forwarding rules (often set by attackers)\n"
            "     - Outlook > Rules > check for unknown forward rules\n"
            "     - Exchange admin: Get-InboxRule -Mailbox user@domain.com\n"
            "   - Check for registered MFA devices: Remove any unknown\n"
            "   - Check OAuth app consent: Remove unknown apps\n"
            "3. Review audit logs:\n"
            "   - M365: Security & Compliance > Audit Log Search\n"
            "   - Azure AD: Sign-in logs > filter by user\n"
            "   - On-prem: Event Viewer > Security log > Event ID 4624 (logons)\n"
            "4. Determine scope:\n"
            "   - What data did the attacker access?\n"
            "   - Were emails sent from the account?\n"
            "   - Were files accessed or downloaded?\n"
            "5. Re-enable with security:\n"
            "   - Set a strong new password\n"
            "   - Enable/reset MFA\n"
            "   - Monitor the account for 30 days\n"
            "6. Report: Document everything for compliance and legal"
        ),
    },
    {
        "category": "Security",
        "problem_title": "USB device policy enforcement",
        "problem_description": "Need to restrict USB storage devices to prevent data theft, or users are complaining USB drives are being blocked by policy.",
        "problem_keywords": "usb blocked, usb policy, usb restriction, removable storage, usb security, device control, usb disabled",
        "solution_steps": (
            "1. To BLOCK USB storage via Group Policy:\n"
            "   - Computer Config > Admin Templates > System > Removable Storage Access\n"
            "   - Enable: 'Removable Disks: Deny read access'\n"
            "   - Enable: 'Removable Disks: Deny write access'\n"
            "   - This blocks USB flash drives but allows keyboards/mice\n"
            "2. To allow specific USB devices only:\n"
            "   - Computer Config > Admin Templates > System > Device Installation > Device Installation Restrictions\n"
            "   - 'Prevent installation of devices not described by other policy settings'\n"
            "   - Add allowed device IDs to the allow list\n"
            "3. If USB is blocked and user needs an exception:\n"
            "   - Create a separate GPO for exceptions\n"
            "   - Add the user's computer to a security group\n"
            "   - Link the exception GPO only to that group\n"
            "   - Document the exception with approval\n"
            "4. Using Microsoft Endpoint Manager/Intune:\n"
            "   - Endpoint security > Device control\n"
            "   - Create a removable storage policy\n"
            "   - Assign to device or user groups\n"
            "5. For temporary access:\n"
            "   - Can also use local policy: gpedit.msc\n"
            "   - Or registry: HKLM\\SYSTEM\\CurrentControlSet\\Services\\USBSTOR\\Start\n"
            "   - Value 3 = enabled, Value 4 = disabled\n"
            "6. Always log USB usage attempts for security auditing"
        ),
    },
    {
        "category": "Security",
        "problem_title": "BitLocker recovery key needed",
        "problem_description": "Computer is asking for BitLocker recovery key at boot. User locked out of their encrypted drive.",
        "problem_keywords": "bitlocker recovery, recovery key, bitlocker locked, encryption key, bitlocker boot, drive encrypted, bitlocker",
        "solution_steps": (
            "1. Find the BitLocker recovery key:\n"
            "   a. Azure AD / Entra ID:\n"
            "      - portal.azure.com > Devices > find device > BitLocker keys\n"
            "   b. Active Directory:\n"
            "      - AD Users and Computers > find computer > Properties > BitLocker Recovery tab\n"
            "      - Or search by Key ID: Get-ADObject -Filter {objectclass -eq 'msFVE-RecoveryInformation'}\n"
            "   c. Microsoft Account:\n"
            "      - https://account.microsoft.com/devices/recoverykey\n"
            "   d. USB drive: If user saved the key to USB during setup\n"
            "   e. Printed copy: Business may have printed copies filed\n"
            "2. Enter the 48-digit recovery key on the BitLocker screen\n"
            "3. Common triggers for BitLocker recovery:\n"
            "   - BIOS/UEFI update\n"
            "   - TPM firmware update\n"
            "   - Hardware change (motherboard, SSD move)\n"
            "   - Secure Boot changes\n"
            "   - Boot order changes\n"
            "4. After recovery:\n"
            "   - Suspend BitLocker before any future BIOS/hardware changes:\n"
            "     manage-bde -protectors -disable C:\n"
            "   - Then re-enable after changes: manage-bde -protectors -enable C:\n"
            "5. If no recovery key is found:\n"
            "   - Data on the drive is unrecoverable without the key\n"
            "   - May need to reformat and reinstall Windows\n"
            "6. Prevention: Ensure BitLocker recovery keys are backed up to AD/Azure AD"
        ),
    },
    {
        "category": "Security",
        "problem_title": "Firewall blocking legitimate application traffic",
        "problem_description": "Windows Firewall or network firewall is blocking an application that needs to communicate. Application errors out on network operations.",
        "problem_keywords": "firewall blocking, firewall rule, application blocked, port blocked, windows firewall, firewall exception",
        "solution_steps": (
            "1. Identify what's being blocked:\n"
            "   - Check the application error for port/address info\n"
            "   - Windows Firewall log: C:\\Windows\\System32\\LogFiles\\Firewall\\pfirewall.log\n"
            "   - Enable logging: wf.msc > Properties > Public/Private Profile > Logging > Log Dropped Packets: Yes\n"
            "2. Create Windows Firewall exception:\n"
            "   - wf.msc > Inbound Rules > New Rule\n"
            "   - Program: Browse to the .exe file\n"
            "   - Or Port: Specify TCP/UDP and port number\n"
            "   - Action: Allow the connection\n"
            "   - Profile: Domain, Private, Public (as needed)\n"
            "3. PowerShell to create rule:\n"
            "   - New-NetFirewallRule -DisplayName 'MyApp' -Direction Inbound -Program 'C:\\path\\app.exe' -Action Allow\n"
            "   - Or: New-NetFirewallRule -DisplayName 'MyApp' -Direction Inbound -Protocol TCP -LocalPort 8080 -Action Allow\n"
            "4. For network firewall (not Windows):\n"
            "   - Contact network admin with:\n"
            "   - Source IP, Destination IP, Port, Protocol\n"
            "   - Request a firewall rule change\n"
            "5. Temporarily test by disabling firewall:\n"
            "   - Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False\n"
            "   - If app works: Firewall was the issue, create specific rule\n"
            "   - Re-enable: Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True\n"
            "6. Never leave the firewall disabled as a permanent solution"
        ),
    },
    {
        "category": "Security",
        "problem_title": "Data Loss Prevention (DLP) blocking file transfer",
        "problem_description": "User cannot send an email attachment, upload a file, or copy data because DLP policy is blocking the action.",
        "problem_keywords": "dlp blocked, data loss prevention, cannot send attachment, dlp policy, file blocked, sensitive data blocked",
        "solution_steps": (
            "1. Understand the DLP alert:\n"
            "   - What policy was triggered? (check the notification message)\n"
            "   - What sensitive data was detected? (credit card, SSN, etc.)\n"
            "   - DLP is working as intended: It detected sensitive content\n"
            "2. If the transfer is legitimate:\n"
            "   - Check if the user can override the policy\n"
            "   - Some policies allow override with justification\n"
            "   - User enters business reason and proceeds\n"
            "3. If override is not available:\n"
            "   - Remove the sensitive data from the file\n"
            "   - Redact sensitive information before sending\n"
            "   - Use an approved secure method for transferring sensitive data\n"
            "4. For false positives:\n"
            "   - Report to the security/compliance team\n"
            "   - Provide the file and explain why it's not actually sensitive\n"
            "   - They may adjust the DLP rules\n"
            "5. For IT admins - adjusting DLP:\n"
            "   - M365 Compliance Center > Data Loss Prevention > Policies\n"
            "   - Create exception rules for specific users/groups if needed\n"
            "   - Use 'Test' mode first when making DLP changes\n"
            "6. Education: Remind users about acceptable data handling practices"
        ),
    },
    {
        "category": "Security",
        "problem_title": "Endpoint not compliant with security policy",
        "problem_description": "Device showing as non-compliant in Intune/Endpoint Manager. User's access to resources is being blocked by Conditional Access.",
        "problem_keywords": "non-compliant, device compliance, intune, endpoint manager, conditional access, device not compliant, compliance policy",
        "solution_steps": (
            "1. Check compliance status:\n"
            "   - On the device: Settings > Accounts > Access work or school > Info\n"
            "   - Shows compliance status and what's failing\n"
            "2. Common compliance failures:\n"
            "   - OS not up to date: Run Windows Update\n"
            "   - No antivirus: Enable Windows Defender\n"
            "   - No encryption: Enable BitLocker\n"
            "   - Password policy: Change password to meet complexity requirements\n"
            "   - Firewall disabled: Enable Windows Firewall\n"
            "   - Jailbroken/rooted device (mobile)\n"
            "3. Fix and re-sync:\n"
            "   - Address the compliance issue\n"
            "   - Settings > Accounts > Access work or school > Info > Sync\n"
            "   - Or restart the device (triggers check-in)\n"
            "   - Compliance can take 15-60 minutes to update\n"
            "4. If the device won't become compliant:\n"
            "   - Check Intune admin portal: Devices > find device > compliance\n"
            "   - Look at the detailed compliance report\n"
            "   - May need to re-enroll the device\n"
            "5. Temporary workaround:\n"
            "   - Access resources via web browser (may bypass some CA policies)\n"
            "   - Request a temporary compliance exception from IT security\n"
            "6. For new devices: Ensure Autopilot/enrollment is complete before checking compliance"
        ),
    },
    {
        "category": "Security",
        "problem_title": "Suspicious browser extensions or toolbar installed",
        "problem_description": "User has unknown browser extensions, toolbars, or their homepage/search engine has been changed without their knowledge.",
        "problem_keywords": "browser extension, toolbar, homepage changed, search engine changed, browser hijack, unwanted extension, browser malware",
        "solution_steps": (
            "1. Remove suspicious extensions:\n"
            "   - Chrome: chrome://extensions > Remove unknown ones\n"
            "   - Edge: edge://extensions > Remove unknown ones\n"
            "   - Firefox: about:addons > Extensions > Remove\n"
            "2. Reset browser settings:\n"
            "   - Chrome: Settings > Reset settings > Restore settings to defaults\n"
            "   - Edge: Settings > Reset settings > Restore settings to defaults\n"
            "   - Firefox: Help > Troubleshooting Info > Refresh Firefox\n"
            "3. Check for installed programs:\n"
            "   - Control Panel > Programs and Features\n"
            "   - Sort by date: Look for recently installed unknown programs\n"
            "   - Uninstall suspicious entries\n"
            "4. Run malware scan:\n"
            "   - AdwCleaner (specifically for adware/browser hijackers)\n"
            "   - Malwarebytes full scan\n"
            "5. Check Group Policy for managed extensions:\n"
            "   - chrome://policy (in Chrome)\n"
            "   - edge://policy (in Edge)\n"
            "   - If 'Managed by organization' shows: extensions may be deployed by GPO\n"
            "6. Prevent future issues:\n"
            "   - Deploy extension allowlist via Group Policy\n"
            "   - Block unapproved extensions\n"
            "   - Chrome: ExtensionInstallBlocklist / ExtensionInstallAllowlist policies\n"
            "7. Educate user about not installing unknown extensions"
        ),
    },
    {
        "category": "Security",
        "problem_title": "Email account sending spam without user knowledge",
        "problem_description": "User's email account is sending spam or phishing emails to contacts. Recipients report getting suspicious emails from the user.",
        "problem_keywords": "sending spam, email hacked, account sending spam, phishing from account, email compromised, spam sent",
        "solution_steps": (
            "1. Immediate response:\n"
            "   - Reset the user's password immediately\n"
            "   - Enable MFA if not already configured\n"
            "   - Revoke all active sessions (Azure AD or Exchange)\n"
            "2. Check for mail rules:\n"
            "   - Attackers often create forwarding rules\n"
            "   - Outlook > Rules > check for unknown rules\n"
            "   - Exchange PowerShell: Get-InboxRule -Mailbox user@domain.com | fl Name,Description,ForwardTo,RedirectTo,DeleteMessage\n"
            "   - Remove any suspicious rules\n"
            "3. Check for connected apps:\n"
            "   - Azure AD > Users > user > App registrations\n"
            "   - Revoke consent for unknown apps\n"
            "4. Check delegated permissions:\n"
            "   - Someone may have delegate access and be sending from the account\n"
            "   - Get-MailboxPermission -Identity user@domain.com\n"
            "   - Remove unauthorized permissions\n"
            "5. Review sign-in logs:\n"
            "   - Azure AD > Sign-in logs > filter by user\n"
            "   - Look for logins from unusual locations\n"
            "   - Check for suspicious IP addresses\n"
            "6. Notify recipients:\n"
            "   - Send a legitimate email warning contacts about the spam\n"
            "   - Advise not to click any links from the previous spam\n"
            "7. Check if user's email domain is now on a blocklist:\n"
            "   - Use MXToolbox Blocklist Check\n"
            "   - Request removal from any lists"
        ),
    },
    {
        "category": "Security",
        "problem_title": "User credentials found in data breach notification",
        "problem_description": "A password breach monitoring service (HaveIBeenPwned / dark web monitoring) has flagged user credentials as compromised. Need to respond and remediate.",
        "problem_keywords": "breached credentials, compromised password, data breach, haveibeenpwned, leaked password, dark web, credential stuffing",
        "solution_steps": (
            "1. Immediate response:\n"
            "   - Force password reset for the affected account immediately\n"
            "   - Disable the account temporarily if suspicious activity seen\n"
            "   - Check Azure AD / M365: Sign-in logs for unusual locations or devices\n"
            "2. Determine scope:\n"
            "   - Was the breach from a corporate or personal service?\n"
            "   - If personal: User may have reused their work password elsewhere\n"
            "   - Check: https://haveibeenpwned.com for specific breach details\n"
            "3. Review account activity:\n"
            "   - Audit mailbox rules: Look for forwarding rules (attacker persistence)\n"
            "   - Check for new OAuth app consents\n"
            "   - Review recently accessed files and shared documents\n"
            "4. Enforce MFA:\n"
            "   - If not already enabled: Enable MFA immediately\n"
            "   - Revoke all active sessions: Revoke-AzureADUserAllRefreshToken\n"
            "5. Password hygiene education:\n"
            "   - Inform user about password reuse risks\n"
            "   - Recommend a password manager for unique passwords\n"
            "   - Consider implementing Azure AD Password Protection (banned password list)\n"
            "6. Organizational sweep:\n"
            "   - Check if other users share the same breached password\n"
            "   - Azure AD > Authentication methods > Password Protection\n"
            "7. Monitor: Set up alerts for impossible travel sign-ins or bulk file downloads"
        ),
    },
    {
        "category": "Security",
        "problem_title": "SSL/TLS certificate expired or misconfigured on internal service",
        "problem_description": "Internal web services, email servers, or APIs show certificate warnings. Browsers display 'Your connection is not private' for internal sites.",
        "problem_keywords": "ssl certificate, tls expired, certificate error, https warning, internal ca, certificate renewal, pki",
        "solution_steps": (
            "1. Identify the certificate issue:\n"
            "   - Browser: Click the padlock icon > View Certificate\n"
            "   - Check: Expiration date, issuer, subject/SAN names\n"
            "   - PowerShell: Test-NetConnection servername -Port 443; then\n"
            "   - [System.Net.ServicePointManager]::ServerCertificateValidationCallback to inspect\n"
            "2. Expired certificate:\n"
            "   - Renew through your CA (internal PKI or public CA)\n"
            "   - If internal CA (AD CS): certsrv web enrollment or MMC > Certificates\n"
            "   - Export new cert as .pfx with private key\n"
            "3. Install new certificate:\n"
            "   - IIS: Server Certificates > Import > bind to site (Bindings > HTTPS)\n"
            "   - Exchange: Enable-ExchangeCertificate\n"
            "   - Other services: Follow vendor documentation\n"
            "4. SAN / CN mismatch:\n"
            "   - Certificate Subject Alternative Names must match the URL used\n"
            "   - If accessing by IP: SAN must include the IP\n"
            "   - Request a new cert with correct SANs if mismatched\n"
            "5. Internal CA trust:\n"
            "   - If using internal CA: Root CA cert must be in Trusted Root store on all clients\n"
            "   - Deploy via GPO: Computer Config > Windows Settings > Security > Public Key Policies\n"
            "6. Certificate chain:\n"
            "   - Ensure intermediate CA certificates are also installed\n"
            "   - Missing intermediates cause 'unable to verify' errors\n"
            "7. Monitoring: Set up certificate expiry monitoring (60, 30, 7 day alerts)"
        ),
    },
    {
        "category": "Security",
        "problem_title": "Endpoint Detection and Response (EDR) agent alert triage",
        "problem_description": "EDR solution (CrowdStrike, SentinelOne, Defender for Endpoint) has flagged suspicious behavior on a workstation. Alert needs investigation.",
        "problem_keywords": "edr alert, crowdstrike, sentinelone, defender atp, endpoint detection, suspicious activity, threat alert, edr triage",
        "solution_steps": (
            "1. Review the alert:\n"
            "   - EDR console: Check alert severity (Critical/High/Medium/Low)\n"
            "   - What process triggered the alert? What was it doing?\n"
            "   - Is it a known false positive or a legitimate threat?\n"
            "2. Alert types:\n"
            "   - Malware detection: Known malicious file found\n"
            "   - Behavioral: Suspicious process behavior (e.g., PowerShell encoded command)\n"
            "   - Lateral movement: Unusual remote connections\n"
            "   - Persistence: Registry/startup modification\n"
            "3. Investigate the device:\n"
            "   - Check: Who is logged in? When did the activity occur?\n"
            "   - Review the process tree: Parent process > child processes\n"
            "   - Was this user-initiated or automated?\n"
            "4. Containment (if confirmed threat):\n"
            "   - Most EDRs can isolate the device from the network\n"
            "   - CrowdStrike: 'Contain Host'\n"
            "   - SentinelOne: 'Disconnect from Network'\n"
            "   - Device can still communicate with EDR console\n"
            "5. Remediation:\n"
            "   - Quarantine the malicious file\n"
            "   - Kill the malicious process\n"
            "   - Reset user credentials if account may be compromised\n"
            "6. False positives:\n"
            "   - If legitimate software triggered the alert:\n"
            "   - Create an exclusion for the file hash or path (not broad exclusions)\n"
            "   - Document the exclusion and reason\n"
            "7. Post-incident: Update detection rules and share IOCs with the team"
        ),
    },
    {
        "category": "Security",
        "problem_title": "Privilege escalation or unauthorized admin access detected",
        "problem_description": "An account that shouldn't have admin rights was found in a privileged group, or suspicious elevation of privileges was detected in logs.",
        "problem_keywords": "privilege escalation, unauthorized admin, admin access, domain admins, elevated privileges, lateral movement, admin group",
        "solution_steps": (
            "1. Audit privileged groups:\n"
            "   - Get-ADGroupMember 'Domain Admins' | Select Name,SamAccountName\n"
            "   - Also check: Enterprise Admins, Schema Admins, local Administrators\n"
            "   - Compare current membership against approved list\n"
            "2. If unauthorized member found:\n"
            "   - Remove the account from the privileged group immediately\n"
            "   - Reset the account's password\n"
            "   - Disable the account pending investigation\n"
            "3. Review how it happened:\n"
            "   - Event ID 4728/4732 (member added to security group)\n"
            "   - Who added the account? When?\n"
            "   - Was the adding account also compromised?\n"
            "4. Check for persistence:\n"
            "   - Attackers may add backdoor accounts or modify existing ones\n"
            "   - Check service accounts and rarely-used admin accounts\n"
            "   - Review scheduled tasks running as SYSTEM or admin\n"
            "5. Implement Least Privilege:\n"
            "   - Separate admin accounts from daily-use accounts\n"
            "   - Admin accounts should NOT have email or internet access\n"
            "   - Use Privileged Access Workstations (PAWs)\n"
            "6. Privileged Access Management:\n"
            "   - Implement Just-In-Time (JIT) admin access\n"
            "   - Azure AD PIM (Privileged Identity Management)\n"
            "   - Time-limited admin group membership\n"
            "7. Monitor: Enable alerts for any changes to privileged AD groups"
        ),
    },
    {
        "category": "Security",
        "problem_title": "Network intrusion detection system (IDS/IPS) alert",
        "problem_description": "Network IDS/IPS (Snort, Suricata, Palo Alto, FortiGate) has detected suspicious network traffic or blocked a connection matching known attack signatures.",
        "problem_keywords": "ids alert, ips alert, intrusion detection, network attack, signature match, firewall alert, snort, suricata",
        "solution_steps": (
            "1. Review the alert:\n"
            "   - Source IP and destination IP/port\n"
            "   - Signature/rule that triggered the alert\n"
            "   - Is the source internal (compromised host) or external (attacker)?\n"
            "2. Determine if true positive:\n"
            "   - Google the signature ID for details\n"
            "   - Does the traffic make sense for the source device?\n"
            "   - Is it a known false positive (common with certain applications)?\n"
            "3. If external attack:\n"
            "   - Verify firewall is blocking the traffic (IPS mode)\n"
            "   - Check if any internal device responded to the attack\n"
            "   - Block the source IP if persistent (geo-blocking if from unusual country)\n"
            "4. If internal source:\n"
            "   - The internal device may be compromised\n"
            "   - Investigate the device immediately\n"
            "   - Check for malware, unauthorized software, or compromised credentials\n"
            "5. Common alert types:\n"
            "   - Port scan: Reconnaissance activity\n"
            "   - Exploit attempt: Targeting a vulnerability (e.g., EternalBlue)\n"
            "   - C2 communication: Device calling back to command-and-control server\n"
            "   - Data exfiltration: Unusual outbound data transfer\n"
            "6. Tune rules:\n"
            "   - Suppress false positives with source/dest IP exceptions\n"
            "   - Don't disable rules broadly - create targeted exceptions\n"
            "7. Threat intelligence: Feed the IOCs (IPs, domains) into your blocklist"
        ),
    },
    {
        "category": "Security",
        "problem_title": "Vulnerability scan results show critical findings",
        "problem_description": "A vulnerability scanner (Nessus, Qualys, Rapid7) has identified critical or high-severity vulnerabilities on servers or workstations that need remediation.",
        "problem_keywords": "vulnerability scan, nessus, qualys, cve, critical vulnerability, patch management, security scan, remediation",
        "solution_steps": (
            "1. Prioritize findings:\n"
            "   - Critical/High with known exploits: Fix immediately\n"
            "   - CVSS score 9.0+: Top priority\n"
            "   - Check: Is there a known exploit in the wild?\n"
            "   - CISA KEV (Known Exploited Vulnerabilities) catalog\n"
            "2. Common critical findings:\n"
            "   - Missing OS patches: Windows Update / WSUS\n"
            "   - Outdated software: Java, Adobe, browsers\n"
            "   - Unsupported OS: Windows 7, Server 2012 (no patches available)\n"
            "   - Default credentials: Printers, switches, appliances\n"
            "3. Remediation plan:\n"
            "   - Test patches in a non-production environment first\n"
            "   - Schedule maintenance window for production servers\n"
            "   - Patch workstations via WSUS/SCCM/Intune\n"
            "4. Compensating controls:\n"
            "   - If immediate patching isn't possible:\n"
            "   - Network segmentation (isolate vulnerable systems)\n"
            "   - Disable the vulnerable service if not needed\n"
            "   - Apply firewall rules to limit exposure\n"
            "5. Verify remediation:\n"
            "   - Re-scan after patching to confirm fixes\n"
            "   - Don't just trust that the patch was installed\n"
            "6. False positives:\n"
            "   - Some findings may be incorrect (version detection errors)\n"
            "   - Document confirmed false positives as exceptions\n"
            "   - Require manager approval for risk acceptance\n"
            "7. Ongoing: Schedule weekly/monthly vulnerability scans and track remediation metrics"
        ),
    },
    {
        "category": "Security",
        "problem_title": "Shadow IT - unauthorized cloud services discovered",
        "problem_description": "Users are using unauthorized cloud services (personal Dropbox, Google Drive, unapproved SaaS apps) to store or share company data.",
        "problem_keywords": "shadow it, unauthorized cloud, unapproved apps, cloud access, data leakage, saas discovery, unsanctioned apps",
        "solution_steps": (
            "1. Discovery:\n"
            "   - Review firewall/proxy logs for cloud service domains\n"
            "   - Microsoft Defender for Cloud Apps (Cloud App Security)\n"
            "   - Can identify 16,000+ cloud apps and assess risk\n"
            "2. Assess the risk:\n"
            "   - What data is being stored in the unauthorized service?\n"
            "   - Is it personal data, financial data, or intellectual property?\n"
            "   - Does the service comply with company security standards?\n"
            "3. Understand WHY users use it:\n"
            "   - Often: Company tools are too slow or difficult\n"
            "   - Users need an easy way to share large files\n"
            "   - Find out what they need and provide approved alternatives\n"
            "4. Block unauthorized services:\n"
            "   - Web proxy/firewall: Block specific domains\n"
            "   - Conditional Access (Azure AD): Block unapproved apps\n"
            "   - DLP policies: Prevent upload of sensitive data\n"
            "5. Provide approved alternatives:\n"
            "   - File sharing: OneDrive/SharePoint (if M365)\n"
            "   - Communication: Teams instead of personal Slack/WhatsApp\n"
            "   - Make the approved tools easy to use\n"
            "6. Policy:\n"
            "   - Create/update Acceptable Use Policy\n"
            "   - Communicate to all users what services are approved\n"
            "   - Include in security awareness training\n"
            "7. Monitor: Set up continuous monitoring and alerts for new cloud app usage"
        ),
    },
    {
        "category": "Security",
        "problem_title": "Multi-factor authentication (MFA) bypass or failure",
        "problem_description": "Users can't complete MFA prompts, MFA is being bypassed, or a security incident suggests MFA was circumvented through token theft or SIM swap.",
        "problem_keywords": "mfa bypass, two factor, 2fa failure, authentication app, mfa not working, token theft, sim swap, mfa fatigue",
        "solution_steps": (
            "1. MFA not working for user:\n"
            "   - Check: Is the Authenticator app time synced? (Phone clock must be correct)\n"
            "   - SMS codes not arriving: Check phone number is correct in portal\n"
            "   - Authenticator app lost: Admin can reset MFA registration\n"
            "2. Re-register MFA:\n"
            "   - Azure AD: Users > Select user > Authentication methods > Require re-register\n"
            "   - Or: Reset via the MFA portal\n"
            "   - Provide temporary access pass for re-registration\n"
            "3. MFA fatigue attack:\n"
            "   - Attacker sends repeated MFA push notifications\n"
            "   - User may approve one to stop the notifications\n"
            "   - Mitigation: Enable number matching (user must type a number shown on screen)\n"
            "   - Azure AD: Authentication Methods > Microsoft Authenticator > Number matching\n"
            "4. Token theft:\n"
            "   - Adversary-in-the-Middle (AiTM) phishing can steal session tokens\n"
            "   - Token bypasses MFA (already authenticated)\n"
            "   - Mitigation: Conditional Access > Token protection, Require compliant device\n"
            "5. SIM swap:\n"
            "   - Attacker ports victim's phone number to their SIM\n"
            "   - Intercepts SMS MFA codes\n"
            "   - Mitigation: Use Authenticator app or FIDO2 keys instead of SMS\n"
            "6. Legacy protocols:\n"
            "   - IMAP, POP3, SMTP don't support MFA\n"
            "   - Block legacy authentication: Conditional Access > Block legacy auth\n"
            "7. Backup: Always register multiple MFA methods (app + phone + backup codes)"
        ),
    },
    {
        "category": "Security",
        "problem_title": "Insider threat - suspicious user behavior detected",
        "problem_description": "Monitoring tools flagged a user for unusual data access patterns, bulk file downloads, or accessing sensitive data outside their normal role.",
        "problem_keywords": "insider threat, data theft, suspicious user, bulk download, unusual access, employee termination, data exfiltration",
        "solution_steps": (
            "1. Assess the alert:\n"
            "   - What triggered the alert? (Volume, timing, type of data)\n"
            "   - Is the user's role consistent with this access?\n"
            "   - Is the user on a watch list (resignation, PIP, termination)?\n"
            "2. Gather evidence (carefully):\n"
            "   - Audit logs: File access, email forwarding rules, SharePoint downloads\n"
            "   - Sign-in logs: Unusual hours, locations, devices\n"
            "   - DLP alerts: Sensitive data being copied/shared\n"
            "   - Coordinate with HR and Legal before deep investigation\n"
            "3. Preserve evidence:\n"
            "   - Do NOT alert the user or confront them directly\n"
            "   - Export and preserve relevant logs\n"
            "   - Consider forensic disk image if needed\n"
            "   - Maintain chain of custody\n"
            "4. Access review:\n"
            "   - Does the user have more access than needed for their role?\n"
            "   - Silently reduce permissions if approved by HR/Legal\n"
            "   - Monitor any new access patterns\n"
            "5. Employee termination scenario:\n"
            "   - Pre-termination: Increase monitoring on the account\n"
            "   - Day of termination: Disable account simultaneously with HR notification\n"
            "   - Revoke all active sessions and app consents\n"
            "   - Mail forwarding, delegate access removed\n"
            "6. DLP enforcement:\n"
            "   - Block USB storage on the device\n"
            "   - Block personal cloud storage uploads\n"
            "   - Restrict printing of sensitive documents\n"
            "7. Prevention: Regular access reviews and least-privilege principles"
        ),
    },
    {
        "category": "Security",
        "problem_title": "Rogue wireless access point detected on network",
        "problem_description": "Network security scan or wireless survey has detected an unauthorized WiFi access point plugged into the corporate network, creating a security hole.",
        "problem_keywords": "rogue ap, rogue access point, unauthorized wifi, wireless security, evil twin, network scan, wireless ids",
        "solution_steps": (
            "1. Detection methods:\n"
            "   - Wireless IDS (Cisco CleanAir, Aruba RFProtect)\n"
            "   - Network scan: Devices with multiple network interfaces\n"
            "   - nmap scan of network for devices with HTTP management ports\n"
            "2. Locate the rogue AP:\n"
            "   - MAC address: Find on switch port (show mac address-table)\n"
            "   - Wireless survey tool: Walk the area to find signal source\n"
            "   - Check switch port for unknown device\n"
            "3. Assess the risk:\n"
            "   - Is the AP open (no password)? Extremely high risk\n"
            "   - Is it someone's personal hotspot? Moderate risk\n"
            "   - Is it a deliberate attack (evil twin)? Critical\n"
            "4. Immediate action:\n"
            "   - Disable the switch port the rogue AP is connected to\n"
            "   - Physically locate and remove the device\n"
            "   - Document the incident\n"
            "5. Prevent future rogue APs:\n"
            "   - 802.1X port authentication: Only authorized devices connect\n"
            "   - DHCP snooping and Dynamic ARP Inspection\n"
            "   - MAC address filtering on switch ports (limited effectiveness)\n"
            "6. Policy:\n"
            "   - Clear policy: No personal network equipment on corporate network\n"
            "   - Communicate consequences to employees\n"
            "7. Ongoing: Regular wireless security surveys (quarterly recommended)"
        ),
    },
    {
        "category": "Security",
        "problem_title": "Password spraying or brute force attack on user accounts",
        "problem_description": "Security logs show many failed login attempts across multiple accounts, suggesting a password spraying or brute force attack against the organization.",
        "problem_keywords": "password spray, brute force, failed login, account lockout, login attack, credential attack, authentication attack",
        "solution_steps": (
            "1. Identify the attack:\n"
            "   - Password spraying: Few attempts per account, many accounts targeted\n"
            "   - Brute force: Many attempts on a single account\n"
            "   - Check: Event ID 4625 (failed logon) on DCs\n"
            "   - Azure AD: Sign-in logs > Failure reason > 'Invalid password'\n"
            "2. Determine source:\n"
            "   - External (from internet): Azure AD / ADFS login pages\n"
            "   - Internal: Compromised device or insider\n"
            "   - Check the source IP addresses in the logs\n"
            "3. Immediate response:\n"
            "   - Block the source IP(s) at the firewall/proxy\n"
            "   - If any accounts successfully compromised: Reset password + revoke sessions\n"
            "   - Enable account lockout policy if not set (e.g., 5 failures in 30 minutes)\n"
            "4. Azure AD protection:\n"
            "   - Enable Azure AD Smart Lockout (automatically blocks suspicious attempts)\n"
            "   - Conditional Access: Block legacy authentication\n"
            "   - Conditional Access: Block sign-ins from suspicious locations\n"
            "5. On-premises AD:\n"
            "   - Implement account lockout policy: 5 attempts, 30 minute lockout\n"
            "   - Enable auditing: Event ID 4625, 4740 (account locked out)\n"
            "   - Consider adding ADFS Extranet Lockout\n"
            "6. Affected accounts:\n"
            "   - Identify which accounts were targeted\n"
            "   - Check if any have weak passwords that may have succeeded\n"
            "   - Force password reset for targeted accounts\n"
            "7. Long-term: Require MFA for all accounts, implement banned password list"
        ),
    },
    {
        "category": "Security",
        "problem_title": "File integrity monitoring (FIM) alert on critical system files",
        "problem_description": "File integrity monitoring has detected unexpected changes to critical system files, configuration files, or executable binaries on a server.",
        "problem_keywords": "file integrity, fim alert, file change, unauthorized modification, system file changed, file monitoring, tripwire",
        "solution_steps": (
            "1. Review the alert:\n"
            "   - Which file was modified? (Path, name, type)\n"
            "   - When was it modified? (Timestamp)\n"
            "   - Was it a scheduled change (maintenance window)?\n"
            "2. Determine legitimacy:\n"
            "   - Expected changes: Windows Updates, approved software installs\n"
            "   - Correlate with change management records\n"
            "   - Was there a recent patch Tuesday or scheduled maintenance?\n"
            "3. If unexpected:\n"
            "   - Who made the change? Check audit logs (Event ID 4663 - file access)\n"
            "   - Compare the modified file with a known-good copy\n"
            "   - Check the file hash against known malware databases (VirusTotal)\n"
            "4. Critical files to monitor:\n"
            "   - OS: C:\\Windows\\System32\\*.exe, *.dll\n"
            "   - Configuration: web.config, application configs\n"
            "   - Registry: HKLM\\System\\CurrentControlSet\\Services\n"
            "   - Startup: Startup folders, Run keys\n"
            "5. Investigate the system:\n"
            "   - Run a full antivirus/EDR scan\n"
            "   - Check for rootkits (GMER, aswMBR)\n"
            "   - Review running processes and network connections\n"
            "6. Remediation:\n"
            "   - Restore the original file from a known-good backup\n"
            "   - sfc /scannow (repair system files from Windows image)\n"
            "   - If compromised: Consider rebuilding the system\n"
            "7. Baseline: After clean state, update FIM baseline so future changes are detected"
        ),
    },
    {
        "category": "Security",
        "problem_title": "SIEM correlation rule triggered for potential incident",
        "problem_description": "The SIEM (Splunk, Sentinel, QRadar) has generated a correlated alert from multiple log sources indicating a possible security incident.",
        "problem_keywords": "siem alert, splunk, sentinel, qradar, correlation rule, security incident, log analysis, security event",
        "solution_steps": (
            "1. Review the correlation:\n"
            "   - What log sources triggered the rule? (Firewall, AD, endpoint, etc.)\n"
            "   - What events were correlated? (Timeline of events)\n"
            "   - What is the rule designed to detect?\n"
            "2. Common correlation rules:\n"
            "   - Brute force → successful login → data access (compromised account)\n"
            "   - Malware alert + outbound C2 traffic (active infection)\n"
            "   - New admin account + lateral movement (privilege escalation)\n"
            "   - Impossible travel (login from two distant locations)\n"
            "3. Investigate:\n"
            "   - Pivot on the user account: What else did they do?\n"
            "   - Pivot on the source IP: What other systems were accessed?\n"
            "   - Pivot on the device: What other alerts exist?\n"
            "4. Severity assessment:\n"
            "   - Is sensitive data at risk? (PII, financial, IP)\n"
            "   - Is the attack ongoing or historical?\n"
            "   - How many systems/users are affected?\n"
            "5. Response:\n"
            "   - Follow incident response playbook for the alert type\n"
            "   - Contain: Isolate affected devices/accounts\n"
            "   - Eradicate: Remove the threat\n"
            "   - Recover: Restore systems and verify integrity\n"
            "6. False positive handling:\n"
            "   - If confirmed false positive: Tune the rule to reduce noise\n"
            "   - Document the false positive pattern\n"
            "7. Post-incident: Update runbooks, improve detection rules, lessons learned"
        ),
    },
    {
        "category": "Security",
        "problem_title": "Web application firewall (WAF) blocking legitimate requests",
        "problem_description": "A web application firewall is blocking legitimate user requests, causing application errors or access denials for valid users.",
        "problem_keywords": "waf, web application firewall, blocked request, false positive, waf rule, application firewall, waf bypass",
        "solution_steps": (
            "1. Identify the blocked request:\n"
            "   - WAF logs: Check which rule triggered the block\n"
            "   - HTTP status code: Usually 403 Forbidden or custom block page\n"
            "   - Note the URL, method, and request body\n"
            "2. Common false positives:\n"
            "   - SQL injection rules triggered by legitimate queries\n"
            "   - XSS rules triggered by HTML in form fields\n"
            "   - File upload rules blocking legitimate attachments\n"
            "   - Rate limiting blocking high-traffic legitimate users\n"
            "3. Analyze the rule:\n"
            "   - What specific pattern triggered the WAF?\n"
            "   - Is the rule using OWASP Core Rule Set (CRS)? Which version?\n"
            "   - Can the request be modified to avoid triggering the rule?\n"
            "4. Create an exception:\n"
            "   - Whitelist the specific URL + parameter combination\n"
            "   - Don't disable the entire rule - create a targeted exception\n"
            "   - Example: Allow HTML in a specific form field on a specific page\n"
            "5. Testing:\n"
            "   - Switch WAF to detection mode (log only) temporarily\n"
            "   - Test the application thoroughly\n"
            "   - Switch back to prevention mode after tuning\n"
            "6. Best practices:\n"
            "   - Start in detection mode when deploying new WAF rules\n"
            "   - Review blocked requests daily during initial deployment\n"
            "   - Document all exceptions with business justification\n"
            "7. Update: Keep WAF rules updated (OWASP CRS updates quarterly)"
        ),
    },
    {
        "category": "Security",
        "problem_title": "DNS tunneling or DNS-based attack detected",
        "problem_description": "Security monitoring has detected unusually long DNS queries, high query volume from a single host, or DNS queries to suspicious domains, suggesting DNS tunneling.",
        "problem_keywords": "dns tunneling, dns attack, dns exfiltration, suspicious dns, dns abuse, dns malware, iodine, dns2tcp",
        "solution_steps": (
            "1. Identify signs of DNS tunneling:\n"
            "   - Unusually long subdomain names (>30 characters)\n"
            "   - High volume of DNS TXT record queries from one device\n"
            "   - DNS queries to newly registered or suspicious domains\n"
            "   - Base64-encoded or gibberish looking subdomains\n"
            "2. Investigation:\n"
            "   - DNS logs: Which device is making the queries?\n"
            "   - What domain are they querying? (The tunnel endpoint)\n"
            "   - Frequency: Hundreds/thousands of queries to same domain\n"
            "3. Common DNS tunneling tools:\n"
            "   - iodine, dns2tcp, DNSCat2\n"
            "   - Malware may use DNS for C2 communication or data exfiltration\n"
            "   - CobaltStrike and other RATs can use DNS beacons\n"
            "4. Block the threat:\n"
            "   - Block the suspicious domain at the DNS resolver\n"
            "   - Investigate the source device for malware\n"
            "   - If a legitimate device: Run full forensic investigation\n"
            "5. DNS monitoring:\n"
            "   - Enable DNS query logging on your DNS servers\n"
            "   - Feed DNS logs into your SIEM\n"
            "   - Use DNS threat intelligence feeds\n"
            "6. Prevention:\n"
            "   - Use DNS filtering services (Cisco Umbrella, Zscaler, Pi-hole)\n"
            "   - Block external DNS (only allow internal resolvers)\n"
            "   - Restrict DNS over HTTPS (DoH) on corporate devices\n"
            "7. Detection rules: Alert on DNS query length > 50 chars, TXT queries > 100/min"
        ),
    },
    {
        "category": "Security",
        "problem_title": "Data Loss Prevention (DLP) policy creating user friction",
        "problem_description": "DLP policies are blocking legitimate business activities. Users report inability to send emails with attachments or share files that are needed for their work.",
        "problem_keywords": "dlp policy, data loss prevention, dlp block, sensitive data, dlp exception, dlp rule, dlp false positive",
        "solution_steps": (
            "1. Understand the block:\n"
            "   - What was the user trying to do? (Email, file share, upload)\n"
            "   - What DLP rule triggered? (Check DLP alert in admin console)\n"
            "   - What sensitive data was detected? (Credit cards, SSN, custom pattern)\n"
            "2. Verify the detection:\n"
            "   - Was sensitive data actually present? (True vs false positive)\n"
            "   - Sometimes regex patterns match non-sensitive data\n"
            "   - Example: Part numbers that look like credit card numbers\n"
            "3. If false positive:\n"
            "   - Refine the DLP rule's detection pattern\n"
            "   - Add exceptions for specific senders, recipients, or domains\n"
            "   - Allowlist specific attachments or file types\n"
            "4. If true positive but legitimate:\n"
            "   - Some users legitimately need to share sensitive data\n"
            "   - Create an exception group with appropriate users\n"
            "   - Change policy from Block to 'Warn and allow override with justification'\n"
            "5. Policy tuning:\n"
            "   - Run DLP in test/audit mode first before blocking\n"
            "   - Review DLP reports weekly to identify false positives\n"
            "   - Gradually move from Notify to Warn to Block\n"
            "6. User education:\n"
            "   - Teach users what data triggers DLP\n"
            "   - Show them approved methods for sharing sensitive data\n"
            "   - Encrypted email, secure file sharing portals\n"
            "7. Documentation: Maintain a DLP exception register with business justification"
        ),
    },
    {
        "category": "Security",
        "problem_title": "Security audit finding: weak encryption or deprecated protocols",
        "problem_description": "Security audit or compliance scan has identified the use of weak encryption (SSL 3.0, TLS 1.0/1.1, RC4, DES, 3DES) or deprecated protocols on servers.",
        "problem_keywords": "weak encryption, tls 1.0, ssl 3.0, deprecated protocol, rc4, des, 3des, cipher suite, security audit",
        "solution_steps": (
            "1. Identify affected services:\n"
            "   - Which servers/services use the weak protocol?\n"
            "   - IIS, Exchange, RDP, SQL Server, LDAP, etc.\n"
            "   - Scan: Use IIS Crypto tool or ssllabs.com (for public-facing)\n"
            "2. Disable TLS 1.0 and 1.1:\n"
            "   - Group Policy: Computer Config > Admin Templates > Network > SSL Configuration\n"
            "   - Or: Registry (HKLM\\SYSTEM\\CurrentControlSet\\Control\\SecurityProviders\\SCHANNEL)\n"
            "   - IIS Crypto tool (Nartac Software) makes this easy\n"
            "3. Before disabling:\n"
            "   - Test: What clients/applications use TLS 1.0/1.1?\n"
            "   - Old printers, scanners, and IoT devices may not support TLS 1.2\n"
            "   - Java 7 and older only support TLS 1.0 by default\n"
            "   - Plan for client upgrades before server changes\n"
            "4. Disable weak ciphers:\n"
            "   - Remove: RC4, DES, 3DES, NULL ciphers\n"
            "   - Prefer: AES-256-GCM, AES-128-GCM, CHACHA20-POLY1305\n"
            "   - Use IIS Crypto 'Best Practices' template\n"
            "5. RDP considerations:\n"
            "   - RDP uses its own security layer\n"
            "   - Enable NLA (Network Level Authentication)\n"
            "   - Set: 'Require use of specific security layer' to SSL\n"
            "   - Minimum encryption level: High\n"
            "6. SQL Server:\n"
            "   - SQL Server Configuration Manager > Protocols > Force Encryption\n"
            "   - Assign a proper TLS certificate\n"
            "7. Verification: Re-scan after changes to confirm weak protocols are disabled"
        ),
    },
    {
        "category": "Security",
        "problem_title": "USB storage device policy enforcement issues",
        "problem_description": "USB storage devices need to be blocked company-wide, but some devices still work or authorized USB devices are being blocked by the policy.",
        "problem_keywords": "usb block, usb policy, removable storage, device control, usb whitelist, usb restriction, group policy usb",
        "solution_steps": (
            "1. Group Policy method:\n"
            "   - Computer Config > Admin Templates > System > Removable Storage Access\n"
            "   - Set: 'All Removable Storage classes: Deny all access' = Enabled\n"
            "   - Or selectively disable Read/Write for specific device types\n"
            "2. Device Installation Restriction:\n"
            "   - Computer Config > Admin Templates > System > Device Installation > Restrictions\n"
            "   - 'Prevent installation of removable devices' = Enabled\n"
            "   - Allow specific devices by Hardware ID or Device Instance ID\n"
            "3. Find device Hardware ID:\n"
            "   - Device Manager > Properties > Details > Hardware IDs\n"
            "   - Format: USB\\VID_xxxx&PID_xxxx\n"
            "   - VID = Vendor ID, PID = Product ID\n"
            "4. Whitelist approved devices:\n"
            "   - 'Allow installation of devices that match device IDs'\n"
            "   - Add the Hardware IDs of approved USB devices\n"
            "   - Process: Also enable 'Apply layered order of evaluation'\n"
            "5. Endpoint protection method:\n"
            "   - Defender for Endpoint: Device Control policies\n"
            "   - CrowdStrike: USB Device Control\n"
            "   - More granular than GPO: Can allow Read-Only, block Write\n"
            "6. Exceptions:\n"
            "   - USB keyboards, mice should not be blocked (HID class)\n"
            "   - Target only 'USB Mass Storage' class\n"
            "   - Class GUID for USB storage: {36FC9E60-C465-11CF-8056-444553540000}\n"
            "7. Audit first: Set policy to 'audit mode' to identify who uses USB before blocking"
        ),
    },
    {
        "category": "Security",
        "problem_title": "Security incident response - containment and recovery",
        "problem_description": "A confirmed security incident (malware outbreak, data breach, compromised server) requires coordinated incident response to contain and remediate.",
        "problem_keywords": "incident response, security incident, containment, recovery, malware outbreak, data breach, ir plan, forensics",
        "solution_steps": (
            "1. Preparation (before incidents):\n"
            "   - Incident response plan documented and tested\n"
            "   - IR team contacts list (IT, management, legal, PR)\n"
            "   - Forensic tools ready (disk imagers, evidence bags, USB drives)\n"
            "2. Identification:\n"
            "   - Confirm the incident is real (not a false positive)\n"
            "   - Determine scope: How many systems/users affected?\n"
            "   - What type of incident? (Malware, breach, ransomware, insider)\n"
            "   - Document everything with timestamps\n"
            "3. Containment (short-term):\n"
            "   - Isolate affected systems (network disconnect, not power off)\n"
            "   - Disable compromised accounts\n"
            "   - Block C2 domains/IPs at firewall\n"
            "   - Preserve evidence: Don't reimage yet\n"
            "4. Containment (long-term):\n"
            "   - Patch the exploited vulnerability\n"
            "   - Reset all potentially compromised credentials\n"
            "   - Apply additional monitoring on affected segments\n"
            "5. Eradication:\n"
            "   - Remove malware/attacker access from all systems\n"
            "   - Clean or reimage affected machines\n"
            "   - Verify clean state with scans\n"
            "6. Recovery:\n"
            "   - Restore systems from known-good backups\n"
            "   - Monitor closely for re-infection\n"
            "   - Gradually restore services (most critical first)\n"
            "7. Post-incident: Lessons learned meeting within 1 week, update IR plan and defenses"
        ),
    },
    {
        "category": "Security",
        "problem_title": "Suspicious outbound network traffic or data exfiltration attempts",
        "problem_description": "Firewall or security tools detecting unusual outbound traffic patterns, connections to known malicious IPs, or potential data exfiltration via DNS, HTTP, or encrypted channels.",
        "problem_keywords": "outbound traffic, data exfiltration, suspicious traffic, c2, command and control, beaconing, malicious ip, network anomaly",
        "solution_steps": (
            "1. Identify the source:\n"
            "   - Firewall logs: Source IP, destination IP, port, protocol\n"
            "   - netstat -b (shows process using connection)\n"
            "   - Resource Monitor > Network tab for real-time connections\n"
            "   - Identify process and user account making connections\n"
            "2. Analyze the traffic:\n"
            "   - Check destination IP reputation: VirusTotal, AbuseIPDB\n"
            "   - Beaconing: Regular intervals suggest C2 communication\n"
            "   - Large upload volumes may indicate data exfiltration\n"
            "   - DNS query analysis for DNS tunneling attempts\n"
            "3. Containment:\n"
            "   - Block destination IP/domain at firewall\n"
            "   - Isolate affected host from network (don't power off)\n"
            "   - Disable network adapter if urgent\n"
            "   - Preserve evidence: memory dump, disk image\n"
            "4. Investigation:\n"
            "   - Check for malware: Full AV/EDR scan\n"
            "   - Review installed programs and scheduled tasks\n"
            "   - Check autoruns: Autoruns.exe from Sysinternals\n"
            "   - Review user account activity in AD\n"
            "5. Remediation: If malware confirmed, follow incident response plan. Reimage if necessary. Update firewall rules to block C2 infrastructure. Submit IOCs to threat intelligence team"
        ),
    },
]

DIAGNOSTIC_TREE = {
    "category": "Security",
    "root": {
        "title": "Security Issue Troubleshooting",
        "node_type": "question",
        "question_text": "What type of security issue are you dealing with?",
        "children": [
            {
                "title": "Malware or virus infection",
                "node_type": "question",
                "question_text": "What type of malware issue?",
                "children": [
                    {
                        "title": "Active infection / ransomware",
                        "node_type": "solution",
                        "solution_text": "1. DISCONNECT FROM NETWORK immediately\n2. Do NOT restart the machine\n3. Document: Take photos of any ransom notes or symptoms\n4. Boot to Safe Mode with Networking\n5. Run Defender Offline Scan + Malwarebytes\n6. For ransomware: Check nomoreransom.org for free decryptors\n7. Report to security team and management\n8. Restore from clean backups if needed\n9. Change ALL passwords from a clean device"
                    },
                    {
                        "title": "Antivirus not working",
                        "node_type": "solution",
                        "solution_text": "1. Check for conflicting AV software - only one should be active\n2. Uninstall old AV using vendor removal tool\n3. Check Group Policy: gpedit.msc > Defender settings\n4. Check registry: Remove DisableAntiSpyware key\n5. Manual update: MpCmdRun -SignatureUpdate\n6. Repair: sfc /scannow then DISM /Online /Cleanup-Image /RestoreHealth\n7. Reset Windows Security: Get-AppxPackage Microsoft.SecHealthUI -AllUsers | Reset-AppxPackage"
                    }
                ]
            },
            {
                "title": "Phishing or suspicious email",
                "node_type": "question",
                "question_text": "Did the user click a link or open an attachment?",
                "children": [
                    {
                        "title": "Yes - clicked link or opened attachment",
                        "node_type": "solution",
                        "solution_text": "1. Disconnect from network\n2. Run full antivirus scan\n3. Reset user password from a DIFFERENT device\n4. Check for email forwarding rules added by attacker\n5. Check for new MFA devices registered\n6. Revoke all active sessions\n7. Monitor account for 30 days\n8. Block the phishing URL at firewall/web filter\n9. Search if others received the same email"
                    },
                    {
                        "title": "No - just reported it",
                        "node_type": "solution",
                        "solution_text": "1. Thank the user for reporting\n2. Collect the email as an attachment (not inline forward)\n3. Analyze: Check sender address, hover over links\n4. Block sender domain in email filter\n5. Block phishing URL at web filter\n6. Check mail logs: Did anyone else receive this?\n7. Delete copies from all mailboxes\n8. Send awareness alert to staff"
                    }
                ]
            },
            {
                "title": "Account compromised / unauthorized access",
                "node_type": "solution",
                "solution_text": "1. Reset password immediately\n2. Revoke all active sessions\n3. Check for email forwarding rules (attackers add these)\n4. Check for unknown MFA devices - remove them\n5. Check OAuth app consent - revoke unknown apps\n6. Review audit logs for what was accessed\n7. Enable/reset MFA\n8. Monitor account for 30 days\n9. Document for compliance reporting"
            },
            {
                "title": "BitLocker recovery needed",
                "node_type": "solution",
                "solution_text": "1. Find recovery key:\n   - Azure AD: portal.azure.com > Devices > BitLocker keys\n   - AD: Computer properties > BitLocker Recovery tab\n   - Microsoft account: account.microsoft.com/devices/recoverykey\n   - USB backup or printed copy\n2. Enter 48-digit recovery key\n3. Common triggers: BIOS update, TPM change, hardware change\n4. After recovery: Suspend BitLocker before future BIOS/hardware changes\n5. Ensure keys are backed up to AD/Azure AD going forward"
            },
            {
                "title": "Firewall blocking an application",
                "node_type": "solution",
                "solution_text": "1. Check firewall log: C:\\Windows\\System32\\LogFiles\\Firewall\\pfirewall.log\n2. Create exception: wf.msc > Inbound Rules > New Rule\n3. Choose Program (browse to .exe) or Port (specify TCP/UDP + port)\n4. PowerShell: New-NetFirewallRule -DisplayName 'Name' -Direction Inbound -Program 'path' -Action Allow\n5. For network firewall: Provide source IP, dest IP, port, protocol to network admin\n6. Never leave firewall fully disabled as a fix"
            }
        ]
    }
}
