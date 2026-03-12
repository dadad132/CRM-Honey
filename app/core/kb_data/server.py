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
    {
        "category": "Server",
        "problem_title": "Windows Server running out of C: drive space",
        "problem_description": "Server's system drive (C:) is critically low on free space. Server performance degrading and some services may stop.",
        "problem_keywords": "disk space, c drive full, server disk, low disk, winsxs, disk cleanup, server space",
        "solution_steps": (
            "1. Quick space analysis:\n"
            "   - WinDirStat or TreeSize (free tools) to find large files/folders\n"
            "   - PowerShell: Get-ChildItem C:\\ -Recurse | Sort-Object Length -Descending | Select-Object -First 20 FullName, @{Name='SizeMB';Expression={[math]::Round($_.Length/1MB,2)}}\n"
            "2. Windows Update cleanup:\n"
            "   - Dism /Online /Cleanup-Image /StartComponentCleanup /ResetBase\n"
            "   - This cleans the WinSxS folder (can recover several GB)\n"
            "   - Disk Cleanup (cleanmgr /sageset:1) > Windows Update Cleanup\n"
            "3. Clear temp files:\n"
            "   - C:\\Windows\\Temp > delete old files\n"
            "   - C:\\Windows\\SoftwareDistribution\\Download > stop Windows Update service, delete, restart\n"
            "4. IIS logs:\n"
            "   - C:\\inetpub\\logs\\LogFiles > can grow to many GB\n"
            "   - Archive old logs, set up log rotation\n"
            "   - IIS Manager > Logging > set log file rollover\n"
            "5. Event logs:\n"
            "   - %SystemRoot%\\System32\\winevt\\Logs\n"
            "   - Set maximum log sizes (Event Viewer > Properties)\n"
            "   - Archive and clear old logs\n"
            "6. SQL/database:\n"
            "   - Move database files to a data drive (not C:)\n"
            "   - Shrink transaction logs if not needed\n"
            "7. Prevention: Always put data, logs, and databases on separate drives from the OS"
        ),
    },
    {
        "category": "Server",
        "problem_title": "DHCP scope exhausted or no available IP addresses",
        "problem_description": "DHCP server has run out of available IP addresses. New devices cannot get an IP and show 169.254.x.x (APIPA) addresses.",
        "problem_keywords": "dhcp exhausted, no ip available, dhcp scope, ip address pool, dhcp full, apipa, 169.254, dhcp lease",
        "solution_steps": (
            "1. Check scope utilization:\n"
            "   - DHCP MMC > Scope > Address Pool vs Active Leases\n"
            "   - PowerShell: Get-DhcpServerv4ScopeStatistics\n"
            "   - Shows: PercentageInUse, Free addresses\n"
            "2. Clean up stale leases:\n"
            "   - Many leases may be from devices no longer on the network\n"
            "   - Delete inactive leases manually\n"
            "   - Or reduce lease duration: 8 hours for Wi-Fi, 1-4 days for wired\n"
            "3. Reduce lease time:\n"
            "   - Scope Properties > Lease time\n"
            "   - Shorter lease = faster IP reclamation\n"
            "   - Don't set too short (5 min) or DHCP server gets hammered\n"
            "4. Expand the scope:\n"
            "   - Add more addresses to the scope range\n"
            "   - Or add a second scope (superscope)\n"
            "   - Ensure no IP conflicts with existing static addresses\n"
            "5. Add reservations wisely:\n"
            "   - Servers, printers with reservations still consume pool addresses\n"
            "   - Consider static IPs for servers (outside DHCP range)\n"
            "6. Use exclusion ranges:\n"
            "   - Exclude ranges for static devices to prevent conflicts\n"
            "   - Scope > Address Pool > Exclusion Range\n"
            "7. Failover: Set up DHCP failover with a second server for redundancy"
        ),
    },
    {
        "category": "Server",
        "problem_title": "Active Directory time synchronization out of sync",
        "problem_description": "Domain controllers or domain computers have time drift. Kerberos authentication fails because of time differences greater than 5 minutes.",
        "problem_keywords": "time sync, ntp, w32time, time drift, kerberos time, clock skew, domain time, pdc emulator",
        "solution_steps": (
            "1. Kerberos time tolerance:\n"
            "   - Default: 5 minutes maximum clock skew\n"
            "   - If time differs by more: Authentication fails\n"
            "   - 'The clock skew between the two computers is too great'\n"
            "2. Time hierarchy in AD:\n"
            "   - PDC Emulator > syncs to external NTP source\n"
            "   - Other DCs > sync from PDC Emulator\n"
            "   - Domain members > sync from any DC\n"
            "3. Configure PDC Emulator:\n"
            "   - On the PDCe DC (admin CMD):\n"
            "   - w32tm /config /manualpeerlist:\"time.nist.gov,0x1\" /syncfromflags:manual /reliable:YES /update\n"
            "   - net stop w32time; net start w32time\n"
            "   - w32tm /resync\n"
            "4. Check time source:\n"
            "   - w32tm /query /source (shows configured time source)\n"
            "   - w32tm /query /status (shows synchronization details)\n"
            "   - On PDCe: Should show external NTP server\n"
            "   - On other DCs: Should show the PDCe\n"
            "5. Fix client time:\n"
            "   - w32tm /resync /force (force time sync)\n"
            "   - If domain member: net time /set (use domain time)\n"
            "6. Virtual DCs:\n"
            "   - Disable time sync from hypervisor (VMware Tools, Hyper-V IC)\n"
            "   - VM time sync can conflict with AD time hierarchy\n"
            "7. Monitor: Set up alerts for time drift > 2 minutes"
        ),
    },
    {
        "category": "Server",
        "problem_title": "Windows Server backup failing or incomplete",
        "problem_description": "Windows Server Backup shows failures, partial completions, or doesn't run on schedule. Backup destination may be full or unreachable.",
        "problem_keywords": "server backup, wbadmin, backup failed, backup schedule, vss error, backup destination, windows backup",
        "solution_steps": (
            "1. Check backup status:\n"
            "   - wbadmin get status (shows current backup job)\n"
            "   - wbadmin get versions (shows completed backups)\n"
            "   - Event Viewer > Application > source 'Backup'\n"
            "2. Common failures:\n"
            "   - VSS errors: Volume Shadow Copy service issues\n"
            "   - Destination full: Not enough space on backup drive\n"
            "   - Network target unreachable: UNC path issues\n"
            "3. VSS troubleshooting:\n"
            "   - vssadmin list writers (check for failed writers)\n"
            "   - If a writer shows 'Failed': Restart that service\n"
            "   - Common: SQL Writer, Exchange Writer, Hyper-V Writer\n"
            "   - vssadmin list providers (check for third-party VSS providers)\n"
            "4. Disk space:\n"
            "   - Backup destination needs 1.5-2x the data size\n"
            "   - Clean up old backups: wbadmin delete backup -version:identifier\n"
            "   - Use a larger backup target\n"
            "5. Schedule issues:\n"
            "   - wbadmin enable backup (set up scheduled backup)\n"
            "   - Task Scheduler > Microsoft > Windows > Backup\n"
            "   - Check the task is enabled and scheduled correctly\n"
            "6. Network backup destination:\n"
            "   - UNC path must be accessible by the SYSTEM account\n"
            "   - Credentials may need to be stored\n"
            "7. Test restore: Regularly test restoring from backup to verify data integrity"
        ),
    },
    {
        "category": "Server",
        "problem_title": "Group Policy not applying to computers or users",
        "problem_description": "New or modified Group Policy settings are not being enforced on target computers or users. gpresult shows the GPO is not applied.",
        "problem_keywords": "gpo not applying, group policy, gpresult, gpo link, gpo filter, security filter, wmi filter, gpo debug",
        "solution_steps": (
            "1. Check GPO application:\n"
            "   - On the target: gpresult /r (summary of applied GPOs)\n"
            "   - gpresult /h report.html (detailed HTML report)\n"
            "   - Look for the GPO in 'Applied GPOs' or 'Denied GPOs'\n"
            "2. Force GPO update:\n"
            "   - gpupdate /force (forces immediate Group Policy refresh)\n"
            "   - Some settings require logoff/restart\n"
            "   - Computer Configuration: Requires restart\n"
            "   - User Configuration: Requires logoff/logon\n"
            "3. Check GPO linking:\n"
            "   - Group Policy Management Console > GPO > Scope tab\n"
            "   - Is the GPO linked to the correct OU?\n"
            "   - Is the link enabled? (not disabled)\n"
            "4. Security filtering:\n"
            "   - Scope tab > Security Filtering section\n"
            "   - Default: 'Authenticated Users' (applies to all)\n"
            "   - If filtered: The target computer/user must be in the filtered group\n"
            "   - ALSO: 'Domain Computers' must have Read permission on the GPO (Delegation tab)\n"
            "5. WMI filter:\n"
            "   - Check if a WMI filter is attached to the GPO\n"
            "   - The filter may exclude the target device\n"
            "   - Test: gwmi -query \"WMI filter query\" on target\n"
            "6. Conflicting GPOs:\n"
            "   - Higher priority GPOs may override settings\n"
            "   - Check: Precedence order in gpresult\n"
            "   - Block/Enforce inheritance can affect application\n"
            "7. Replication: Ensure AD replication is healthy (repadmin /replsummary)"
        ),
    },
    {
        "category": "Server",
        "problem_title": "Remote management tools (RSAT) not working",
        "problem_description": "Remote Server Administration Tools (RSAT) can't connect to servers. MMC snap-ins show 'RPC server is unavailable' or access denied.",
        "problem_keywords": "rsat, remote management, mmc, rpc unavailable, remote admin, server manager, remote mmc, rpc error",
        "solution_steps": (
            "1. Check RPC connectivity:\n"
            "   - Test-NetConnection -ComputerName server -Port 135 (RPC endpoint mapper)\n"
            "   - If blocked: Firewall issue between client and server\n"
            "   - RPC uses port 135 + dynamic high ports (49152-65535)\n"
            "2. Firewall rules on the server:\n"
            "   - Enable: 'Remote Service Management' rule group\n"
            "   - Enable: 'Windows Management Instrumentation (WMI)' rules\n"
            "   - Enable: 'Remote Event Log Management' rules\n"
            "   - netsh advfirewall firewall set rule group=\"Remote Service Management\" new enable=Yes\n"
            "3. Windows Remote Management (WinRM):\n"
            "   - On the server: winrm quickconfig (sets up WinRM)\n"
            "   - Check: winrm enumerate winrm/config/listener\n"
            "   - Should show HTTP listener on port 5985\n"
            "4. Install RSAT on Windows 10/11:\n"
            "   - Settings > Apps > Optional Features > Add a feature\n"
            "   - Search 'RSAT' and install needed tools\n"
            "   - Or PowerShell: Get-WindowsCapability -Online | Where Name -like 'RSAT*'\n"
            "5. Access denied:\n"
            "   - The user must be in the 'Administrators' group on the target server\n"
            "   - Or have specific delegated permissions\n"
            "   - UAC remote restrictions may block admin access\n"
            "6. DNS/name resolution:\n"
            "   - Can you ping the server by name?\n"
            "   - Try using the IP address instead of hostname\n"
            "7. Server Manager: If Server Manager can't manage remote servers, try adding them manually"
        ),
    },
    {
        "category": "Server",
        "problem_title": "SQL Server performance degradation",
        "problem_description": "SQL Server queries are running slowly. Applications that use the database are experiencing timeouts and poor response times.",
        "problem_keywords": "sql server slow, query slow, sql performance, database slow, sql timeout, sql tuning, query plan",
        "solution_steps": (
            "1. Check server resources:\n"
            "   - Task Manager or Resource Monitor on the SQL server\n"
            "   - CPU, Memory, Disk I/O - which is the bottleneck?\n"
            "   - SQL Server Management Studio > Activity Monitor\n"
            "2. Memory configuration:\n"
            "   - SQL Server by default uses as much RAM as available\n"
            "   - Set max server memory: Leave 4 GB for OS + other services\n"
            "   - SSMS > Server Properties > Memory > Maximum server memory\n"
            "3. Disk I/O:\n"
            "   - Slow disks are the most common SQL bottleneck\n"
            "   - Move database files to SSD/fast storage\n"
            "   - Separate data (.mdf) and log (.ldf) files onto different drives\n"
            "   - TempDB should be on the fastest drive\n"
            "4. Index maintenance:\n"
            "   - Fragmented indexes slow down queries\n"
            "   - ALTER INDEX ALL ON tablename REBUILD\n"
            "   - Set up a weekly index maintenance plan\n"
            "   - Update statistics: UPDATE STATISTICS tablename\n"
            "5. Identify slow queries:\n"
            "   - Activity Monitor > Recent Expensive Queries\n"
            "   - Or: sys.dm_exec_query_stats DMV\n"
            "   - Check execution plans for table scans (should be index seeks)\n"
            "6. TempDB contention:\n"
            "   - Create multiple TempDB data files (1 per CPU core, up to 8)\n"
            "   - All same size, same growth settings\n"
            "7. SQL Server Agent: Set up maintenance plans for backups, index rebuild, statistics update"
        ),
    },
    {
        "category": "Server",
        "problem_title": "Hyper-V virtual machine won't start or hangs",
        "problem_description": "A VM in Hyper-V fails to start with errors, gets stuck in 'Starting' state, or hangs at boot. Other VMs on the same host may be fine.",
        "problem_keywords": "hyper-v, vm won't start, virtual machine, vm stuck, vm hang, hypervisor, vm error, starting state",
        "solution_steps": (
            "1. Check VM state:\n"
            "   - Hyper-V Manager > check the VM's State column\n"
            "   - If 'Starting' for too long: The VM is stuck\n"
            "   - Right-click > Turn Off (last resort, may lose data)\n"
            "2. Check event logs:\n"
            "   - Event Viewer > Applications and Services > Microsoft > Windows > Hyper-V-Worker\n"
            "   - Also check: Hyper-V-VMMS events\n"
            "   - Common errors: VHD access, memory allocation, permissions\n"
            "3. Storage issues:\n"
            "   - The VHD/VHDX file must be accessible\n"
            "   - Check: Disk space on the host\n"
            "   - If on a SAN/NAS: Check connectivity and permissions\n"
            "   - VM Settings > Hard Drive > verify path exists\n"
            "4. Memory:\n"
            "   - Host may not have enough free RAM for the VM\n"
            "   - Check: Hyper-V Manager shows Memory Demand vs Assigned\n"
            "   - Reduce VM startup RAM or enable Dynamic Memory\n"
            "5. Checkpoint/snapshot:\n"
            "   - Corrupted checkpoints can prevent VM start\n"
            "   - Delete all checkpoints (merges back to base VHD)\n"
            "   - Wait for merge to complete\n"
            "6. Saved state:\n"
            "   - If VM is in 'Saved' state and won't resume: Delete saved state\n"
            "   - Right-click > Delete Saved State (VM will cold boot)\n"
            "7. VM configuration:\n"
            "   - Export the VM, delete it, and re-import\n"
            "   - This recreates the VM registration"
        ),
    },
    {
        "category": "Server",
        "problem_title": "File server performance poor with many concurrent users",
        "problem_description": "File server becomes very slow when many users access it simultaneously. File operations take long, and users experience timeouts.",
        "problem_keywords": "file server slow, smb performance, concurrent users, file share slow, server bottleneck, many users",
        "solution_steps": (
            "1. Identify the bottleneck:\n"
            "   - Task Manager > Performance on the file server\n"
            "   - Common bottlenecks in order: Disk I/O > Network > CPU > RAM\n"
            "   - Resource Monitor > Disk tab: Check disk queue length\n"
            "2. Disk performance:\n"
            "   - Average disk queue length > 2: Disk is the bottleneck\n"
            "   - Upgrade to SSD or faster RAID array\n"
            "   - Enable write caching (if UPS protects against power loss)\n"
            "3. SMB configuration:\n"
            "   - Ensure SMB 3.x is in use: Get-SmbConnection\n"
            "   - Enable SMB Multichannel: multiple NICs for parallel I/O\n"
            "   - Consider SMB Direct (RDMA) for high-performance workloads\n"
            "4. Network bandwidth:\n"
            "   - 1 Gbps may not be enough for many concurrent users\n"
            "   - Upgrade to 10 GbE or NIC teaming\n"
            "   - Check for network saturation in Task Manager > Network\n"
            "5. Antivirus exclusions:\n"
            "   - Real-time scanning on the file server kills performance\n"
            "   - Exclude the shared data folders from real-time scan\n"
            "   - Schedule full scans during off-hours\n"
            "6. Deduplication:\n"
            "   - Enable Data Deduplication on volumes with duplicate files\n"
            "   - Server Manager > Volumes > Configure Data Deduplication\n"
            "7. DFS Namespace: Distribute file shares across multiple servers for load balancing"
        ),
    },
    {
        "category": "Server",
        "problem_title": "Windows Server Update Services (WSUS) synchronization failures",
        "problem_description": "WSUS server fails to sync with Microsoft Update. Clients report no available updates, or WSUS database errors appear.",
        "problem_keywords": "wsus, wsus sync, windows update server, wsus error, update server, wsus database, wsus console",
        "solution_steps": (
            "1. Check sync status:\n"
            "   - WSUS Console > Synchronizations > check last sync result\n"
            "   - If failed: Note the error code\n"
            "   - Common: HTTP errors (proxy/firewall) or database errors\n"
            "2. Network/proxy:\n"
            "   - WSUS needs to reach windowsupdate.microsoft.com and download.microsoft.com\n"
            "   - Configure proxy in WSUS > Options > Update Source > Proxy Server\n"
            "   - Ensure firewall allows HTTPS outbound from WSUS server\n"
            "3. WSUS database maintenance:\n"
            "   - WID (Windows Internal Database) needs periodic maintenance\n"
            "   - Run the WSUS Server Cleanup Wizard:\n"
            "   - WSUS Console > Options > Server Cleanup Wizard\n"
            "   - Select all cleanup options\n"
            "4. Reindex the database:\n"
            "   - Download and run the WSUS maintenance SQL script from Microsoft\n"
            "   - For WID: sqlcmd -S \\\\.\\pipe\\Microsoft##WID\\tsql\\query -i wsus_reindex.sql\n"
            "5. Reset WSUS:\n"
            "   - wsusutil reset (resyncs metadata)\n"
            "   - Delete and recreate the content folder if corrupted\n"
            "6. Client not reporting:\n"
            "   - On client: wuauclt /detectnow /reportnow\n"
            "   - Or PowerShell: (New-Object -ComObject Microsoft.Update.AutoUpdate).DetectNow()\n"
            "   - Check Group Policy: Computer Config > Windows Update settings\n"
            "7. WSUS pool: In IIS, ensure WsusPool application pool is running and has enough memory"
        ),
    },
    {
        "category": "Server",
        "problem_title": "Terminal Server / RDS session limit or licensing issues",
        "problem_description": "Users cannot connect to Remote Desktop Services server. Error about license server, session limit, or 'too many connections'.",
        "problem_keywords": "rds license, terminal server, remote desktop services, session limit, rd license, cal, connection limit, grace period",
        "solution_steps": (
            "1. Check current sessions:\n"
            "   - Server Manager > Remote Desktop Services > Collections\n"
            "   - Or: query session (from CMD on the RDS server)\n"
            "   - Shows all active and disconnected sessions\n"
            "2. Session limits:\n"
            "   - By default: 2 admin RDP sessions (without RDS role)\n"
            "   - With RDS role: Limited by CALs\n"
            "   - Check disconnected sessions: Users may not be logging off properly\n"
            "   - Force logoff idle sessions: Group Policy > RDS > Session Time Limits\n"
            "3. RD Licensing:\n"
            "   - RD Licensing Manager (licmgr.exe) > check license status\n"
            "   - Verify: License server is activated, CALs are installed\n"
            "   - Per User vs Per Device CALs\n"
            "4. Grace period:\n"
            "   - RDS has a 120-day grace period for licensing\n"
            "   - After expiry: Only admin connections allowed\n"
            "   - Install proper CALs before grace period expires\n"
            "5. License server configuration:\n"
            "   - Server Manager > RDS > Overview > RD Licensing\n"
            "   - Ensure the license server is specified on the Session Host\n"
            "   - Group Policy: Computer Config > Admin Templates > RDS > RD Session Host > Licensing\n"
            "6. Clean up disconnected sessions:\n"
            "   - logoff <session_id> (force logoff a specific session)\n"
            "   - Set idle/disconnect timeouts in Group Policy\n"
            "7. Scaling: Consider RD Connection Broker for load balancing across multiple hosts"
        ),
    },
    {
        "category": "Server",
        "problem_title": "DNS zone transfer or secondary DNS failure",
        "problem_description": "Secondary DNS server is not receiving zone transfers from the primary. DNS records are stale or missing on the secondary server.",
        "problem_keywords": "zone transfer, secondary dns, dns replication, axfr, dns zone, primary dns, dns transfer, notify",
        "solution_steps": (
            "1. Check zone transfer status:\n"
            "   - DNS Manager on secondary > right-click zone > Properties > check SOA serial\n"
            "   - Compare serial number with primary - should match\n"
            "   - If secondary is lower: Transfer is failing\n"
            "2. Allow zone transfers on primary:\n"
            "   - DNS Manager on primary > zone Properties > Zone Transfers tab\n"
            "   - 'Allow zone transfers' must be enabled\n"
            "   - Recommended: 'Only to servers listed on the Name Servers tab'\n"
            "   - Or: 'Only to the following servers' (specify secondary IP)\n"
            "3. Firewall:\n"
            "   - Zone transfers use TCP port 53\n"
            "   - Regular DNS queries use UDP port 53\n"
            "   - Ensure TCP 53 is open between primary and secondary\n"
            "4. Test zone transfer:\n"
            "   - nslookup > server secondary_dns_ip > ls -d domain.com\n"
            "   - If fails: Check firewall and transfer settings\n"
            "5. Notify:\n"
            "   - Primary should notify secondary when changes occur\n"
            "   - Zone Properties > Zone Transfers > Notify\n"
            "   - Add the secondary server's IP\n"
            "6. Manual transfer:\n"
            "   - On secondary: Right-click zone > Transfer from Master\n"
            "   - Or: dnscmd secondary /zonerefresh domain.com\n"
            "7. AD-integrated zones: If both are DCs, use AD-integrated zones instead of zone transfers"
        ),
    },
    {
        "category": "Server",
        "problem_title": "Cluster failover or high availability issues",
        "problem_description": "Windows Server Failover Cluster node goes down and services don't fail over properly. Or unnecessary failovers occur frequently.",
        "problem_keywords": "failover cluster, cluster, high availability, cluster failover, cluster node, quorum, cluster error, wsfc",
        "solution_steps": (
            "1. Check cluster status:\n"
            "   - Failover Cluster Manager > check node status and events\n"
            "   - PowerShell: Get-ClusterNode (shows all nodes and state)\n"
            "   - Get-ClusterResource (shows resource status)\n"
            "2. Cluster validation:\n"
            "   - Run: Test-Cluster -Node node1,node2\n"
            "   - Reviews: Network, storage, system configuration\n"
            "   - Fix any warnings or errors before production\n"
            "3. Heartbeat/network:\n"
            "   - Cluster uses heartbeat to detect node failure\n"
            "   - Network issues can cause false failovers\n"
            "   - Ensure dedicated heartbeat network between nodes\n"
            "   - Check for network timeouts or packet loss\n"
            "4. Quorum:\n"
            "   - Quorum determines which nodes can run resources\n"
            "   - 2-node cluster: Must have a witness (disk or file share)\n"
            "   - Cloud witness (Azure) works well for 2-node clusters\n"
            "   - Get-ClusterQuorum (check current quorum configuration)\n"
            "5. Frequent failovers:\n"
            "   - Check resource failure policies: Failover Cluster Manager > resource Properties\n"
            "   - Increase fail-back delay to prevent 'ping-pong' between nodes\n"
            "   - Check cluster event log for the trigger\n"
            "6. Storage:\n"
            "   - Shared storage must be accessible from all nodes simultaneously\n"
            "   - Cluster Shared Volumes (CSV) or iSCSI/FC SAN\n"
            "7. Cluster log: Get-ClusterLog -TimeSpan 60 (last 60 minutes of cluster events)"
        ),
    },
    {
        "category": "Server",
        "problem_title": "IIS website returns 500 Internal Server Error",
        "problem_description": "Website hosted on IIS shows '500 Internal Server Error'. The page worked before but now shows a generic error with no details.",
        "problem_keywords": "iis 500, internal server error, iis error, web server error, asp.net error, iis application, iis crash",
        "solution_steps": (
            "1. Enable detailed errors:\n"
            "   - IIS Manager > select site > Error Pages > Edit Feature Settings\n"
            "   - Set to 'Detailed errors'\n"
            "   - Or add to web.config: <customErrors mode=\"Off\"/> (ASP.NET)\n"
            "   - ONLY for debugging - disable in production\n"
            "2. Check Event Viewer:\n"
            "   - Application log > filter by source 'ASP.NET' or 'IIS'\n"
            "   - Windows Logs > Application > look for Error entries\n"
            "3. IIS log files:\n"
            "   - C:\\inetpub\\logs\\LogFiles\\W3SVC1\\\n"
            "   - Check the latest log file for the 500 error entry\n"
            "   - Sub-status code: 500.19 (config error), 500.21 (handler), etc.\n"
            "4. Common 500 sub-codes:\n"
            "   - 500.0: Unhandled exception in application code\n"
            "   - 500.19: Configuration error (malformed web.config)\n"
            "   - 500.21: Handler not configured\n"
            "   - 500.24: Running managed code in Classic mode\n"
            "5. Application Pool:\n"
            "   - IIS Manager > Application Pools > check if the pool has stopped\n"
            "   - If stopped: Start it and check Event Viewer for the crash reason\n"
            "   - Common: Incorrect identity, missing .NET framework\n"
            "6. Permissions:\n"
            "   - App pool identity needs Read access to the site folder\n"
            "   - IIS_IUSRS group or the specific app pool identity\n"
            "7. Failed Request Tracing: Enable for detailed request-level debugging"
        ),
    },
    {
        "category": "Server",
        "problem_title": "Active Directory replication latency or conflicts",
        "problem_description": "Changes made on one domain controller take too long to appear on others. Or conflicting changes create CNF (conflict) objects in AD.",
        "problem_keywords": "ad replication, replication latency, replication conflict, cnf object, replication delay, repadmin, ad sync",
        "solution_steps": (
            "1. Check replication status:\n"
            "   - repadmin /replsummary (overview of all DC replication)\n"
            "   - repadmin /showrepl (detailed replication status for each DC)\n"
            "   - Look for failures: >0 in the 'fails' column\n"
            "2. Force replication:\n"
            "   - repadmin /syncall /Aed (sync all DCs, all partitions)\n"
            "   - Or: AD Sites and Services > right-click connection > Replicate Now\n"
            "3. Replication latency:\n"
            "   - Same site: Replication within 15 seconds (notification-based)\n"
            "   - Inter-site: Based on schedule (default: 180 minutes)\n"
            "   - Reduce: AD Sites and Services > Site Links > Properties > Change schedule\n"
            "4. CNF (Conflict) objects:\n"
            "   - Created when same object modified on two DCs before replication\n"
            "   - Search AD: \\0ACNF: in the name\n"
            "   - Review both objects, keep the correct one, delete the CNF copy\n"
            "5. Lingering objects:\n"
            "   - Objects that were deleted on one DC but still exist on another\n"
            "   - repadmin /removelingeringobjects (clean up)\n"
            "   - Enable strict replication consistency\n"
            "6. Site topology:\n"
            "   - Verify AD Sites and Services has correct site/subnet assignments\n"
            "   - All DCs should be in the correct site\n"
            "   - Site links should connect all sites\n"
            "7. Troubleshoot: dcdiag /test:replications (comprehensive replication health check)"
        ),
    },
    {
        "category": "Server",
        "problem_title": "PowerShell remoting or WinRM connection failures",
        "problem_description": "Cannot use Enter-PSSession, Invoke-Command, or other PowerShell remoting commands to manage remote servers. WinRM errors appear.",
        "problem_keywords": "powershell remoting, winrm, enter-pssession, invoke-command, ps remoting, remote powershell, winrm error",
        "solution_steps": (
            "1. Enable PS Remoting on target:\n"
            "   - PowerShell (Admin): Enable-PSRemoting -Force\n"
            "   - This starts WinRM service and configures firewall rules\n"
            "   - Sets up HTTP listener on port 5985\n"
            "2. Test connectivity:\n"
            "   - Test-WSMan -ComputerName servername\n"
            "   - If fails: WinRM not enabled or network/firewall issue\n"
            "   - Test-NetConnection -ComputerName servername -Port 5985\n"
            "3. Common errors:\n"
            "   - 'WinRM cannot process the request': WinRM not configured\n"
            "   - 'Access is denied': Need admin rights on the target\n"
            "   - 'Not in TrustedHosts': Workgroup computers need TrustedHosts\n"
            "4. TrustedHosts (for workgroup/non-domain):\n"
            "   - Set-Item WSMan:\\localhost\\Client\\TrustedHosts -Value 'servername'\n"
            "   - Or: -Value '*' (all - less secure)\n"
            "   - Required when not in the same domain\n"
            "5. Firewall rules:\n"
            "   - Port 5985 (HTTP) or 5986 (HTTPS) must be open\n"
            "   - netsh advfirewall firewall set rule name=\"Windows Remote Management (HTTP-In)\" new enable=Yes\n"
            "6. HTTPS (recommended for cross-domain):\n"
            "   - Configure HTTPS listener with a certificate\n"
            "   - winrm quickconfig -transport:https\n"
            "   - Connect: Enter-PSSession -ComputerName server -UseSSL\n"
            "7. CredSSP: For double-hop scenarios, enable CredSSP delegation (use with caution)"
        ),
    },
    {
        "category": "Server",
        "problem_title": "Windows Server time synchronization failures",
        "problem_description": "Server time is drifting or incorrect. NTP synchronization failing, causing Kerberos authentication failures, log timestamp mismatches, or certificate validation errors.",
        "problem_keywords": "ntp, time sync, time drift, w32time, kerberos time, clock skew, time source, pdc emulator",
        "solution_steps": (
            "1. Check current time config:\n"
            "   - w32tm /query /status\n"
            "   - w32tm /query /source\n"
            "   - Shows: Current source, last sync, stratum\n"
            "2. AD time hierarchy:\n"
            "   - PDC Emulator: Should sync to external NTP source\n"
            "   - All DCs: Sync to PDC Emulator\n"
            "   - Domain members: Sync to any DC\n"
            "3. Configure PDC Emulator:\n"
            "   - w32tm /config /manualpeerlist:\"time.windows.com\" /syncfromflags:MANUAL /reliable:YES /update\n"
            "   - net stop w32time && net start w32time\n"
            "   - w32tm /resync /force\n"
            "4. Kerberos max tolerance:\n"
            "   - Default: 5-minute maximum clock skew\n"
            "   - Exceeding this breaks Kerberos authentication\n"
            "   - Fix time sync before adjusting policy\n"
            "5. Hyper-V guests: Disable VMICTimeSync integration service if guest is a DC (DC gets time from AD hierarchy, not host)"
        ),
    },
    {
        "category": "Server",
        "problem_title": "Windows Server certificate services and PKI issues",
        "problem_description": "Certificate Authority (CA) not issuing certificates, certificate enrollment failures, expired CA certificate, or certificate template not available for enrollment.",
        "problem_keywords": "certificate authority, pki, ca certificate, enrollment, certificate template, adcs, certificate expired, auto enrollment",
        "solution_steps": (
            "1. Check CA service:\n"
            "   - Server Manager > Tools > Certification Authority\n"
            "   - CA status should show green checkmark\n"
            "   - If stopped: Right-click CA > Start\n"
            "2. CA certificate validity:\n"
            "   - CA Properties > General > View Certificate\n"
            "   - If CA cert is expired, no new certs can be issued\n"
            "   - Renew CA cert: Right-click CA > All Tasks > Renew CA Certificate\n"
            "3. Certificate template issues:\n"
            "   - Template must be published: CA > Certificate Templates > right-click > New > Template to Issue\n"
            "   - Template permissions: User/computer needs Enroll permission\n"
            "   - certtmpl.msc to manage templates\n"
            "4. Auto-enrollment:\n"
            "   - GPO: Computer/User Config > Policies > Windows Settings > Security > Public Key Policies\n"
            "   - Certificate Services Client - Auto-Enrollment: Enabled\n"
            "   - gpupdate /force on client\n"
            "5. CRL/OCSP: If revocation check failures, verify CRL Distribution Points are accessible (certutil -verify -urlfetch cert.cer)"
        ),
    },
    {
        "category": "Server",
        "problem_title": "DHCP server scope exhaustion or lease issues",
        "problem_description": "DHCP server running out of IP addresses in scope. Clients getting APIPA addresses (169.254.x.x), duplicate IP conflicts, or DHCP failover not working.",
        "problem_keywords": "dhcp, scope exhaustion, ip address, dhcp lease, apipa, dhcp failover, ip conflict, dhcp scope",
        "solution_steps": (
            "1. Check scope utilization:\n"
            "   - DHCP console > Scope > Address Pool\n"
            "   - Scope Statistics: Shows % in use\n"
            "   - If >85% used, take action\n"
            "2. Clean up leases:\n"
            "   - Address Leases: Review active leases\n"
            "   - Delete stale reservations for decommissioned devices\n"
            "   - Reduce lease duration: 8 hours for Wi-Fi, 1-3 days for wired\n"
            "3. Expand scope:\n"
            "   - Scope Properties > change end IP to extend range\n"
            "   - Ensure no conflicts with other scopes or static IPs\n"
            "   - Add exclusion ranges for static devices\n"
            "4. DHCP failover:\n"
            "   - Server Manager > DHCP > scope > right-click > Configure Failover\n"
            "   - Hot Standby: Primary serves all, secondary is backup\n"
            "   - Load Balance: Both servers serve (50/50 default)\n"
            "5. APIPA troubleshooting: If clients get 169.254.x.x, check DHCP server is running, network path to DHCP, and DHCP relay agent config on routers"
        ),
    },
    {
        "category": "Server",
        "problem_title": "Group Policy processing errors or slow application",
        "problem_description": "Group Policy not applying to computers or users, GPO taking too long to process, or specific policy settings not taking effect despite being configured.",
        "problem_keywords": "group policy, gpo, gpupdate, gpo not applying, policy processing, gpo slow, rsop, gpresult",
        "solution_steps": (
            "1. Diagnose GPO application:\n"
            "   - gpresult /r (summary of applied GPOs)\n"
            "   - gpresult /h report.html (detailed HTML report)\n"
            "   - Check: Denied GPOs and reason for denial\n"
            "2. Common reasons GPO doesn't apply:\n"
            "   - Security filtering: GPO doesn't apply to user/computer\n"
            "   - WMI filter: Condition not met on target computer\n"
            "   - Link disabled: GPO linked but link is disabled\n"
            "   - Block inheritance: OU has inheritance blocked\n"
            "   - Enforced: Higher-level enforced GPO overriding\n"
            "3. Force refresh:\n"
            "   - gpupdate /force (immediate refresh)\n"
            "   - Some settings require logoff/reboot: gpupdate /force /logoff\n"
            "   - Remote: Invoke-GPUpdate -Computer PC01 -Force\n"
            "4. Slow GP processing:\n"
            "   - Reduce number of GPOs (consolidate where possible)\n"
            "   - Disable unused sections (Computer/User) on each GPO\n"
            "   - Check network bandwidth to DC (GP downloads from SYSVOL)\n"
            "5. SYSVOL replication: Verify SYSVOL is replicating between DCs (dcdiag /test:sysvolcheck), inconsistent SYSVOL causes inconsistent GPO"
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
