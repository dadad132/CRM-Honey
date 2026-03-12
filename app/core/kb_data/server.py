"""Server and infrastructure troubleshooting articles and diagnostic tree."""

ARTICLES = [
    {
        "category": "Server",
        "problem_title": "File server share inaccessible or slow",
        "problem_description": "Users cannot access file shares on the server, or file access is extremely slow. May show 'Access Denied' or 'Path not found'.",
        "problem_keywords": "file server, share slow, file share, access denied share, server share, smb slow, file server slow",
        "solution_steps": (
            "1. Check server is running:\n"
            "   - Ping the server by name and IP\n"
            "   - Check server console or remote desktop for errors\n"
            "2. Check the share still exists:\n"
            "   - On server: net share (lists all shares)\n"
            "   - From client: net view \\\\servername\n"
            "3. Check permissions:\n"
            "   - Both SHARE and NTFS permissions must allow access\n"
            "   - Share: right-click folder > Properties > Sharing > Advanced > Permissions\n"
            "   - NTFS: Security tab > check user or group has access\n"
            "   - Effective access is the most restrictive of the two\n"
            "4. Check disk space on server:\n"
            "   - Full disks cause errors and extreme slowness\n"
            "   - Clean up or add storage\n"
            "5. For slow file access:\n"
            "   - Check server CPU/RAM usage (Task Manager or Performance Monitor)\n"
            "   - Check for antivirus scanning files in real-time\n"
            "   - Add AV exclusion for file share folders\n"
            "   - Check network link speed between server and switch (should be 1Gbps+)\n"
            "6. Check Server service is running:\n"
            "   - services.msc > Server > should be Running\n"
            "   - Restart if stopped: net stop server && net start server\n"
            "7. Check for SMB version issues: SMB1 is slow, upgrade clients/server to SMB3\n"
            "8. If many users affected: Check for broken DFS links or replication issues"
        ),
    },
    {
        "category": "Server",
        "problem_title": "Active Directory replication failing",
        "problem_description": "Domain controllers are not replicating. Users see different results depending on which DC they authenticate to. Replication errors in Event Viewer.",
        "problem_keywords": "ad replication, domain controller, dc replication, replication error, repadmin, active directory sync",
        "solution_steps": (
            "1. Check replication status:\n"
            "   - repadmin /replsummary (overview of all DCs)\n"
            "   - repadmin /showrepl (detailed replication status for this DC)\n"
            "   - repadmin /queue (pending replication requests)\n"
            "2. Force replication:\n"
            "   - repadmin /syncall /AdeP (sync all DCs, all partitions)\n"
            "   - Or in AD Sites and Services: right-click connection > Replicate Now\n"
            "3. Check DNS:\n"
            "   - DCs must be able to resolve each other by name\n"
            "   - nslookup dc1.domain.com from DC2 and vice versa\n"
            "   - All DCs should be DNS servers or point to ones that are\n"
            "4. Check network connectivity between DCs:\n"
            "   - Required ports: TCP/UDP 53 (DNS), TCP 135, 389, 636, 3268, 445, 88\n"
            "   - Firewall may be blocking between sites\n"
            "5. Check time sync:\n"
            "   - PDC emulator syncs to external NTP\n"
            "   - All other DCs sync to PDC emulator\n"
            "   - w32tm /query /status on each DC\n"
            "6. Check Event Viewer:\n"
            "   - Directory Service log for replication errors\n"
            "   - DNS Server log for DNS issues\n"
            "7. Run dcdiag /v for comprehensive DC health check\n"
            "8. Check AD Sites and Services: Ensure site links and costs are correct"
        ),
    },
    {
        "category": "Server",
        "problem_title": "RDP access to server not working",
        "problem_description": "Cannot Remote Desktop (RDP) into the server. Connection times out, gets refused, or shows authentication errors.",
        "problem_keywords": "rdp server, remote desktop server, rdp refused, rdp timeout, rdp connection failed, rdp error",
        "solution_steps": (
            "1. Verify RDP is enabled on server:\n"
            "   - Server Manager > Local Server > Remote Desktop > Enabled\n"
            "   - Or: System Properties > Remote > Allow remote connections\n"
            "2. Check network connectivity:\n"
            "   - Can you ping the server?\n"
            "   - Test port 3389: Test-NetConnection servername -Port 3389\n"
            "3. Check Windows Firewall:\n"
            "   - Ensure 'Remote Desktop' is allowed in firewall\n"
            "   - Check for all profiles (Domain, Private, Public)\n"
            "4. Check user permissions:\n"
            "   - User must be in 'Remote Desktop Users' group on the server\n"
            "   - Or be a local Administrator\n"
            "5. Check maximum connections:\n"
            "   - Server may have hit the 2-connection limit (unlicensed RDS)\n"
            "   - Use: mstsc /admin to connect to admin session\n"
            "   - Log off disconnected sessions to free slots\n"
            "6. NLA (Network Level Authentication) errors:\n"
            "   - Client may not support NLA required by server\n"
            "   - CredSSP errors: Apply security updates on both sides\n"
            "7. If server just has RDS (Remote Desktop Services) issues:\n"
            "   - Restart Remote Desktop Services: net stop TermService && net start TermService\n"
            "8. Check if RDP port has been changed from default 3389:\n"
            "   - Registry: HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server\\WinStations\\RDP-Tcp\\PortNumber"
        ),
    },
    {
        "category": "Server",
        "problem_title": "Server disk space running critically low",
        "problem_description": "Server's disk is nearly full. Services may be failing, databases not responding, or VMs not starting due to insufficient space.",
        "problem_keywords": "server disk full, disk space server, server storage, full disk, c drive server, server cleanup",
        "solution_steps": (
            "1. Identify what's using space:\n"
            "   - Use TreeSize Free or WinDirStat to visualize disk usage\n"
            "   - Or PowerShell: Get-ChildItem C:\\ -Recurse | Sort-Object Length -Descending | Select-Object -First 20 FullName, @{N='SizeMB';E={$_.Length/1MB}}\n"
            "2. Common space hogs on servers:\n"
            "   - Windows Update cache: C:\\Windows\\SoftwareDistribution\n"
            "   - IIS logs: C:\\inetpub\\logs (can grow very fast)\n"
            "   - Windows Temp: C:\\Windows\\Temp\n"
            "   - CBS logs: C:\\Windows\\Logs\\CBS\n"
            "   - WSUS content: WsusContent folder\n"
            "   - Old backups locally stored\n"
            "3. Safe cleanup:\n"
            "   - Disk Cleanup (run as admin for system files)\n"
            "   - DISM /Online /Cleanup-Image /StartComponentCleanup\n"
            "   - Clean Windows Update: net stop wuauserv > delete SoftwareDistribution > net start wuauserv\n"
            "4. Manage logs:\n"
            "   - Set IIS log rotation and max size\n"
            "   - Archive and compress old logs\n"
            "   - Configure Event Viewer max log sizes\n"
            "5. Move data to another volume if possible\n"
            "6. Extend the partition if unallocated space exists\n"
            "7. Set up disk space monitoring/alerting to catch this earlier\n"
            "8. For VMs: Extend virtual disk through hypervisor, then extend in Disk Management"
        ),
    },
    {
        "category": "Server",
        "problem_title": "DNS server not resolving names correctly",
        "problem_description": "Internal DNS server is not resolving hostnames. Clients get wrong IPs or failures. May affect domain operations if DCs run DNS.",
        "problem_keywords": "dns server, dns resolution, dns not resolving, dns wrong, dns server error, internal dns, dns records",
        "solution_steps": (
            "1. Check DNS service is running:\n"
            "   - On DNS server: services.msc > DNS Server > Running\n"
            "   - Restart if needed: net stop dns && net start dns\n"
            "2. Test resolution from server:\n"
            "   - nslookup hostname localhost (queries the local DNS)\n"
            "   - Should return the correct IP\n"
            "3. Check for stale records:\n"
            "   - DNS Manager > forward lookup zone > look for wrong IP entries\n"
            "   - Enable scavenging: DNS Manager > server > right-click > Set Aging/Scavenging\n"
            "   - Manual cleanup: Delete incorrect records\n"
            "4. Check forwarders (for external resolution):\n"
            "   - DNS Manager > server > Properties > Forwarders\n"
            "   - Forwarders should point to ISP or public DNS (8.8.8.8, 1.1.1.1)\n"
            "   - Test: nslookup google.com <your-dns-server-ip>\n"
            "5. For AD-integrated DNS:\n"
            "   - Check zone is AD-integrated (DNS Manager > zone > Properties > Type)\n"
            "   - Ensure replication between DCs: repadmin /replsummary\n"
            "6. Check for DNS delegation issues:\n"
            "   - dcdiag /test:dns /v\n"
            "7. Client-side:\n"
            "   - ipconfig /flushdns on affected clients\n"
            "   - Check client DNS settings point to the correct server\n"
            "8. Conditional forwarders: Check if any are misconfigured"
        ),
    },
    {
        "category": "Server",
        "problem_title": "DHCP server scope exhausted or not assigning IPs",
        "problem_description": "DHCP server has run out of available IP addresses. New devices can't get IPs. Scope shows as nearly full.",
        "problem_keywords": "dhcp exhausted, dhcp full, no ip addresses, dhcp scope, dhcp server, ip pool, dhcp lease",
        "solution_steps": (
            "1. Check DHCP scope status:\n"
            "   - DHCP console > Scope > right-click > Display Statistics\n"
            "   - Shows: Total, In Use, Available\n"
            "2. Clean up stale leases:\n"
            "   - Check Address Leases > look for leases from old/removed devices\n"
            "   - Delete leases that no longer need IPs\n"
            "3. Reduce lease duration:\n"
            "   - Scope properties > Lease Duration\n"
            "   - For wired offices: 8 hours is usually fine\n"
            "   - For Wi-Fi: 2-4 hours to free addresses faster\n"
            "   - For guest networks: 1-2 hours\n"
            "4. Expand the scope:\n"
            "   - Add more IPs to the range (e.g., change .100-.200 to .100-.250)\n"
            "   - Ensure the new range doesn't conflict with static IPs or other scopes\n"
            "5. Create a new scope on a different subnet:\n"
            "   - Implement VLAN segmentation for better IP management\n"
            "6. Use DHCP reservations instead of static IPs:\n"
            "   - Servers, printers should have reservations (not static)\n"
            "   - This way they're tracked by DHCP\n"
            "7. Check for rogue DHCP:\n"
            "   - Another device giving out IPs wastes addresses\n"
            "   - Use DHCP server authorization in AD\n"
            "8. Monitor DHCP: Set up alerting at 80% utilization"
        ),
    },
    {
        "category": "Server",
        "problem_title": "Group Policy not applying to clients",
        "problem_description": "Group Policy Objects created on Domain Controller are not being applied to client computers or users. Changes not taking effect.",
        "problem_keywords": "gpo not applying, group policy, gpo client, policy not working, gpresult, gpupdate, gpo trouble",
        "solution_steps": (
            "1. On affected client:\n"
            "   - gpupdate /force\n"
            "   - gpresult /h result.html (generates report)\n"
            "   - Open result.html to see applied and denied GPOs\n"
            "2. Check the 'denied' section in gpresult:\n"
            "   - Denied: Security Filtering - user/computer not in the GPO scope\n"
            "   - Denied: WMI Filter - WMI condition not met\n"
            "   - Not Applied: GPO disabled or not linked to this OU\n"
            "3. Common mistakes:\n"
            "   - Computer policy linked to OU containing users (or vice versa)\n"
            "   - Computer/user not in the OU where GPO is linked\n"
            "   - Security filtering too restrictive\n"
            "   - Missing 'Read' permission for Authenticated Users\n"
            "4. Check GPO replication:\n"
            "   - SYSVOL replication must work for GPOs to apply\n"
            "   - net share (on DC) should show SYSVOL and NETLOGON\n"
            "   - dcdiag /test:sysvolcheck\n"
            "5. Restart Group Policy client:\n"
            "   - services.msc > Group Policy Client > Restart\n"
            "6. Reset local Group Policy (last resort):\n"
            "   - Delete: C:\\Windows\\System32\\GroupPolicy and GroupPolicyUsers\n"
            "   - gpupdate /force\n"
            "7. Check for loopback processing:\n"
            "   - Computer Config > Admin Templates > System > Group Policy\n"
            "   - 'Configure user Group Policy loopback processing mode'"
        ),
    },
    {
        "category": "Server",
        "problem_title": "Windows Server backup failing",
        "problem_description": "Windows Server Backup jobs are failing. Backup doesn't start, fails during execution, or completes with errors.",
        "problem_keywords": "server backup, backup failing, wbadmin, windows backup, backup error, vss error, shadow copy",
        "solution_steps": (
            "1. Check backup logs:\n"
            "   - Event Viewer > Applications and Services Logs > Microsoft > Windows > Backup\n"
            "   - Note the error message and event ID\n"
            "2. Common backup errors:\n"
            "   - VSS errors: Volume Shadow Copy Service failed\n"
            "   - Restart VSS: net stop vss && net start vss\n"
            "   - Check VSS writers: vssadmin list writers (look for failed state)\n"
            "   - If a writer failed: restart the associated service\n"
            "3. Disk space issues:\n"
            "   - Backup target needs sufficient free space\n"
            "   - Source volumes need temporary space for shadow copies\n"
            "4. Check backup destination:\n"
            "   - Is the backup drive connected and healthy?\n"
            "   - Is the network share accessible?\n"
            "   - Check permissions on the backup destination\n"
            "5. Retry the backup:\n"
            "   - wbadmin start backup -allcritical -backuptarget:E: -quiet\n"
            "6. For VHD-based backups:\n"
            "   - Check if the VHD is not mounted or locked\n"
            "   - Delete old VHD backups if no longer needed\n"
            "7. Reset VSS writers:\n"
            "   - Restart affected services (SQL, Exchange, etc.)\n"
            "   - Check: vssadmin list shadows (existing shadow copies)\n"
            "8. Consider using a dedicated backup solution (Veeam, Acronis) for production"
        ),
    },
    {
        "category": "Server",
        "problem_title": "IIS website not loading or showing errors",
        "problem_description": "Website hosted on IIS is not loading. Shows 500, 403, or 404 errors. Website may have stopped or the Application Pool is not running.",
        "problem_keywords": "iis error, website down, 500 error, 403 forbidden, iis not working, application pool, web server",
        "solution_steps": (
            "1. Check IIS Manager:\n"
            "   - Is the website running? Sites > your site > check status\n"
            "   - Is the Application Pool running? Application Pools > check status\n"
            "   - Start them if stopped\n"
            "2. Error 500 (Internal Server Error):\n"
            "   - Check Windows Event Viewer > Application log for details\n"
            "   - Enable detailed errors: web.config > system.web > customErrors mode='Off'\n"
            "   - Check IIS logs: C:\\inetpub\\logs\\LogFiles\\\n"
            "   - Common cause: missing .NET version, bad web.config, permission errors\n"
            "3. Error 403 (Forbidden):\n"
            "   - Check NTFS permissions on the website folder\n"
            "   - IIS_IUSRS needs Read permission\n"
            "   - App pool identity needs access\n"
            "   - Check if Directory Browsing is needed\n"
            "4. Error 404 (Not Found):\n"
            "   - Check the file exists at the path IIS is looking\n"
            "   - Check Default Document settings\n"
            "   - Check URL rewrite rules\n"
            "5. Application Pool keeps stopping:\n"
            "   - Check Event Viewer for crash details\n"
            "   - Set App Pool > Advanced > Rapid-Fail Protection > disable temporarily\n"
            "   - Check .NET version matches the application\n"
            "6. Binding issues:\n"
            "   - Check site bindings (hostname, port, IP) are correct\n"
            "   - No two sites can share the same binding"
        ),
    },
    {
        "category": "Server",
        "problem_title": "Hyper-V VM not starting or crashing",
        "problem_description": "Virtual machine won't start in Hyper-V, or starts and crashes. May show errors about virtual switch, memory, or disk issues.",
        "problem_keywords": "hyper-v, vm not starting, virtual machine, vm crash, hyper-v error, vm won't start, hypervisor",
        "solution_steps": (
            "1. Check VM status in Hyper-V Manager:\n"
            "   - Is the VM in a 'Saved' or 'Paused' state? Try resuming or deleting saved state\n"
            "   - Right-click > Delete Saved State, then Start\n"
            "2. Check resources:\n"
            "   - Memory: Does the host have enough free RAM for this VM?\n"
            "   - Disk: Is there enough space for the VHD/VHDX?\n"
            "   - CPU: Check host CPU usage\n"
            "3. Virtual switch issues:\n"
            "   - If the VM's virtual switch was deleted or renamed:\n"
            "   - VM Settings > Network Adapter > change to an existing virtual switch\n"
            "4. VHD/VHDX file issues:\n"
            "   - Check the VHD file exists at the path listed in VM settings\n"
            "   - Check the VHD is not mounted elsewhere\n"
            "   - Check disk isn't full on the VHD host volume\n"
            "5. Permission issues:\n"
            "   - Hyper-V virtual machines need access to VHD paths\n"
            "   - Check NTFS permissions on VHD directory\n"
            "6. Check Event Viewer > Hyper-V logs for specific errors\n"
            "7. If VM crashes on start:\n"
            "   - Check if Secure Boot is enabled but OS doesn't support it\n"
            "   - VM Settings > Security > adjust Secure Boot\n"
            "8. For checkpointing issues:\n"
            "   - Delete old checkpoints: right-click checkpoint > Delete\n"
            "   - Merge may take time before VM can start"
        ),
    },
    {
        "category": "Server",
        "problem_title": "Print server not deploying printers or queue errors",
        "problem_description": "Print server printers are not being deployed to clients via GPO. Print jobs are stuck in the queue. Print Spooler crashing.",
        "problem_keywords": "print server, print queue, print spooler, printer gpo, printer deploy, print job stuck, print server error",
        "solution_steps": (
            "1. Check Print Spooler on server:\n"
            "   - services.msc > Print Spooler > should be Running\n"
            "   - If stopped: Start it\n"
            "   - If it won't start or crashes: See step 5\n"
            "2. Clear stuck print jobs:\n"
            "   - net stop spooler\n"
            "   - Delete: C:\\Windows\\System32\\spool\\PRINTERS\\*\n"
            "   - net start spooler\n"
            "3. GPO printer deployment:\n"
            "   - Check GPO is linked to correct OU\n"
            "   - Computer Config > Policies > Windows Settings > Deployed Printers\n"
            "   - Or User Config > Preferences > Control Panel Settings > Printers\n"
            "   - On client: gpresult /h report.html to verify GPO applied\n"
            "4. Driver issues:\n"
            "   - Print server must have the correct driver for the OS version\n"
            "   - Add x86 AND x64 drivers on the print server\n"
            "   - For Windows 11 clients: May need V4 printer drivers\n"
            "5. Print Spooler keeps crashing:\n"
            "   - Usually a bad driver: Remove recently added printers/drivers\n"
            "   - Boot to Safe Mode, clean PRINTERS folder\n"
            "   - Use Print Management console to remove problem drivers\n"
            "6. Point and Print restrictions:\n"
            "   - Group Policy may block installing print drivers from server\n"
            "   - Computer Config > Admin Templates > Printers > Point and Print Restrictions\n"
            "   - May need to add the print server to the trusted list"
        ),
    },
    {
        "category": "Server",
        "problem_title": "Certificate expired causing service failures",
        "problem_description": "SSL/TLS certificate has expired on the server causing website errors, email failures, or LDAPS authentication issues.",
        "problem_keywords": "certificate expired, ssl expired, tls error, certificate renewal, ssl certificate, https error, cert expired",
        "solution_steps": (
            "1. Identify the expired certificate:\n"
            "   - certlm.msc (Local Machine certificates)\n"
            "   - Check Personal > Certificates for expired certs\n"
            "   - For IIS: IIS Manager > Server Certificates\n"
            "2. For IIS/web certificates:\n"
            "   - Get a new certificate (renew with same CA or get new one)\n"
            "   - Import the new cert: IIS > Server Certificates > Import\n"
            "   - Update the site binding: Sites > your site > Bindings > edit HTTPS > select new cert\n"
            "3. For internal CA certificates:\n"
            "   - Request new cert from your Enterprise CA:\n"
            "   - certlm.msc > Personal > All Tasks > Request New Certificate\n"
            "   - Follow the enrollment wizard\n"
            "4. For LDAPS (domain controller):\n"
            "   - DC needs a valid certificate for LDAPS (port 636)\n"
            "   - Check: certlm.msc on DC > Personal > Certificates\n"
            "   - The cert subject should match the DC hostname\n"
            "5. For Exchange:\n"
            "   - EAC > Servers > Certificates > renew or replace\n"
            "   - Assign new cert to services (SMTP, IMAP, IIS)\n"
            "6. After replacing certificate:\n"
            "   - Restart the affected service (IIS, Exchange, etc.)\n"
            "   - Test from client: open https://servername in browser\n"
            "7. Set up certificate expiry monitoring to prevent this in the future\n"
            "8. Consider using Let's Encrypt for automatic renewal (public-facing sites)"
        ),
    },
]

DIAGNOSTIC_TREE = {
    "category": "Server",
    "root": {
        "title": "Server Troubleshooting",
        "node_type": "question",
        "question_text": "What server issue are you experiencing?",
        "children": [
            {
                "title": "File server / share access issues",
                "node_type": "solution",
                "solution_text": "1. Check server is reachable: ping servername\n2. Check shares exist: net share (on server) or net view \\\\servername\n3. Verify NTFS AND Share permissions\n4. Check disk space on server\n5. Restart Server service: net stop server && net start server\n6. Check for SMB version issues\n7. Check Event Viewer for errors\n8. For slow access: check AV exclusions and network link speed"
            },
            {
                "title": "Active Directory / Domain Controller issues",
                "node_type": "question",
                "question_text": "What AD issue are you seeing?",
                "children": [
                    {
                        "title": "Replication not working",
                        "node_type": "solution",
                        "solution_text": "1. Check status: repadmin /replsummary\n2. Force sync: repadmin /syncall /AdeP\n3. Check DNS: DCs must resolve each other\n4. Check time sync: w32tm /query /status\n5. Check ports between DCs (53, 88, 135, 389, 445, 636, 3268)\n6. Run: dcdiag /v for full health check\n7. Check AD Sites and Services for site link configuration"
                    },
                    {
                        "title": "GPO not applying to clients",
                        "node_type": "solution",
                        "solution_text": "1. On client: gpupdate /force then gpresult /h report.html\n2. Check GPO is linked to correct OU\n3. Verify computer/user IS in that OU\n4. Check Security Filtering includes target\n5. Ensure Authenticated Users has Read permission\n6. Check SYSVOL replication: dcdiag /test:sysvolcheck\n7. Restart Group Policy Client service on client"
                    }
                ]
            },
            {
                "title": "RDP / Remote access to server",
                "node_type": "solution",
                "solution_text": "1. Verify RDP is enabled on server\n2. Test port 3389: Test-NetConnection server -Port 3389\n3. Check firewall allows Remote Desktop\n4. Check user is in Remote Desktop Users group\n5. Check max connections (2 by default without RDS)\n6. Use mstsc /admin for admin session\n7. Restart TermService if needed\n8. Check for NLA/CredSSP errors"
            },
            {
                "title": "Server disk space low",
                "node_type": "solution",
                "solution_text": "1. Use TreeSize Free to visualize usage\n2. Common space hogs:\n   - Windows Update: C:\\Windows\\SoftwareDistribution\n   - IIS logs: C:\\inetpub\\logs\n   - Windows Temp: C:\\Windows\\Temp\n   - CBS logs: C:\\Windows\\Logs\\CBS\n3. Run Disk Cleanup as admin\n4. DISM /Online /Cleanup-Image /StartComponentCleanup\n5. Archive and compress old logs\n6. Extend partition if unallocated space exists"
            },
            {
                "title": "DNS server issues",
                "node_type": "solution",
                "solution_text": "1. Check DNS service is running\n2. Test: nslookup hostname localhost\n3. Check for stale DNS records - enable scavenging\n4. Verify forwarders for external resolution\n5. For AD DNS: Check replication between DCs\n6. Run: dcdiag /test:dns /v\n7. On clients: ipconfig /flushdns\n8. Check conditional forwarders"
            },
            {
                "title": "Backup failures",
                "node_type": "solution",
                "solution_text": "1. Check Event Viewer > Backup for error details\n2. VSS errors: Restart VSS service\n3. Check VSS writers: vssadmin list writers\n4. Verify backup destination is accessible and has space\n5. Restart the service whose VSS writer failed\n6. Check source has temp space for shadow copies\n7. Delete old shadow copies: vssadmin delete shadows\n8. Run backup manually to test: wbadmin start backup"
            }
        ]
    }
}
