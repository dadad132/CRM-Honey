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
