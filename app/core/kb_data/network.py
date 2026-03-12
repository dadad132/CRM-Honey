"""Network troubleshooting articles and diagnostic tree."""

ARTICLES = [
    {
        "category": "Network",
        "problem_title": "No internet connection - Windows says 'No Internet'",
        "problem_description": "Computer is connected to Wi-Fi or Ethernet but shows 'No Internet Access'. Browser cannot load any websites.",
        "problem_keywords": "no internet, no internet access, connected no internet, wifi no internet, ethernet no internet",
        "solution_steps": (
            "1. Quick restart:\n"
            "   - Restart your computer\n"
            "   - Restart your router/modem (unplug 30 seconds, plug back in)\n"
            "2. Run Windows Network Troubleshooter:\n"
            "   - Right-click network icon in taskbar > Troubleshoot problems\n"
            "3. Release and renew IP:\n"
            "   - CMD (Admin):\n"
            "   - ipconfig /release\n"
            "   - ipconfig /renew\n"
            "4. Flush DNS cache:\n"
            "   - ipconfig /flushdns\n"
            "5. Reset network stack:\n"
            "   - netsh winsock reset\n"
            "   - netsh int ip reset\n"
            "   - Restart computer\n"
            "6. Try a different DNS server:\n"
            "   - Network adapter settings > IPv4 > Use: 8.8.8.8 and 8.8.4.4\n"
            "7. Check if other devices have internet:\n"
            "   - If no devices have internet: ISP or router problem\n"
            "   - If only your PC: PC network settings problem\n"
            "8. Disable and re-enable the network adapter:\n"
            "   - Device Manager > Network adapters > right-click > Disable, then Enable"
        ),
    },
    {
        "category": "Network",
        "problem_title": "Wi-Fi keeps disconnecting randomly",
        "problem_description": "Wireless connection drops frequently. Wi-Fi disconnects every few minutes or hours and sometimes reconnects automatically.",
        "problem_keywords": "wifi disconnect, wireless dropping, wifi unstable, wifi keeps dropping, intermittent wifi, wireless disconnect",
        "solution_steps": (
            "1. Disable power management for Wi-Fi adapter:\n"
            "   - Device Manager > Network adapters > Wi-Fi adapter > Properties\n"
            "   - Power Management tab > Uncheck 'Allow computer to turn off this device to save power'\n"
            "2. Update Wi-Fi driver:\n"
            "   - Download latest from laptop/adapter manufacturer (NOT Windows Update)\n"
            "   - If new driver is worse, roll back: Device Manager > Driver > Roll Back\n"
            "3. Forget and reconnect to network:\n"
            "   - Settings > Network > Wi-Fi > Manage known networks\n"
            "   - Forget the network > reconnect with password\n"
            "4. Change Wi-Fi adapter settings:\n"
            "   - Device Manager > Wi-Fi adapter > Properties > Advanced tab\n"
            "   - Set 'Roaming Aggressiveness' to Lowest\n"
            "   - Set 'Wireless Mode' to match your router (802.11ac or ax)\n"
            "5. Check for interference:\n"
            "   - Move closer to router to test\n"
            "   - Other electronics, microwaves, and Bluetooth can interfere\n"
            "   - Switch router to 5GHz band if supported\n"
            "6. On the router:\n"
            "   - Change Wi-Fi channel to a less congested one\n"
            "   - Update router firmware\n"
            "   - Restart the router"
        ),
    },
    {
        "category": "Network",
        "problem_title": "DNS resolution failure - Can't resolve hostnames",
        "problem_description": "Websites show 'DNS_PROBE_FINISHED_NXDOMAIN' or 'Server DNS address could not be found'. Can ping IP addresses but not domain names.",
        "problem_keywords": "dns error, dns probe, dns not resolving, DNS_PROBE_FINISHED_NXDOMAIN, dns failure, cannot resolve",
        "solution_steps": (
            "1. Flush DNS cache:\n"
            "   - CMD (Admin): ipconfig /flushdns\n"
            "2. Test DNS resolution:\n"
            "   - CMD: nslookup google.com\n"
            "   - If it fails, DNS server is the problem\n"
            "3. Change to public DNS:\n"
            "   - Network adapter properties > IPv4 > Use the following DNS:\n"
            "   - Google: 8.8.8.8 / 8.8.4.4\n"
            "   - Cloudflare: 1.1.1.1 / 1.0.0.1\n"
            "   - Quad9: 9.9.9.9 / 149.112.112.112\n"
            "4. Reset DNS client service:\n"
            "   - CMD (Admin): net stop dnscache && net start dnscache\n"
            "5. Check hosts file for bad entries:\n"
            "   - C:\\Windows\\System32\\drivers\\etc\\hosts\n"
            "   - Remove any suspicious entries\n"
            "6. Clear browser DNS cache:\n"
            "   - Chrome: chrome://net-internals/#dns > Clear host cache\n"
            "7. If on a domain: Check that DC/DNS server is reachable\n"
            "   - nslookup google.com <your-dns-server-ip>\n"
            "8. Check if VPN or proxy is interfering with DNS"
        ),
    },
    {
        "category": "Network",
        "problem_title": "VPN connection failing or disconnecting",
        "problem_description": "Cannot connect to the company VPN, or VPN connects briefly then drops. Common errors: 809, 812, 789, 800.",
        "problem_keywords": "vpn error, vpn disconnect, vpn not connecting, vpn failed, error 809, error 789, ipsec, l2tp",
        "solution_steps": (
            "1. Common VPN error codes:\n"
            "   - Error 800: VPN server unreachable - check internet connection and server address\n"
            "   - Error 809: Firewall blocking - enable IPSec/L2TP ports (UDP 500, 4500)\n"
            "   - Error 789: L2TP issue - check pre-shared key and IPSec settings\n"
            "   - Error 812: Authentication failed - verify username and password\n"
            "2. For L2TP/IPSec behind NAT:\n"
            "   - Registry fix: HKLM\\SYSTEM\\CurrentControlSet\\Services\\PolicyAgent\n"
            "   - Add DWORD: AssumeUDPEncapsulationContextOnSendRule = 2\n"
            "   - Restart computer\n"
            "3. Restart IPSec services:\n"
            "   - services.msc > IKE and AuthIP IPsec Keying Modules > Restart\n"
            "   - IPsec Policy Agent > Restart\n"
            "4. Check firewall:\n"
            "   - Allow UDP ports 500, 4500 and Protocol 50 (ESP)\n"
            "   - Or allow the VPN application through the firewall\n"
            "5. Update network adapter and VPN client software\n"
            "6. Try different VPN protocol (IKEv2, SSTP, OpenVPN) if available\n"
            "7. Disable IPv6 on the VPN adapter\n"
            "8. Check if another VPN client is interfering"
        ),
    },
    {
        "category": "Network",
        "problem_title": "Mapped network drives not connecting on login",
        "problem_description": "Mapped network drives show red X at startup. Cannot access them until manually reconnecting. Group Policy drives not mapping.",
        "problem_keywords": "mapped drive, network drive, red X, drive not connected, map network drive, GPO drive mapping",
        "solution_steps": (
            "1. Red X but drive still works when clicked:\n"
            "   - This is a timing issue - network isn't ready before drives try to connect\n"
            "   - Enable 'Always wait for the network at computer startup and logon':\n"
            "   - gpedit.msc > Computer Config > Admin Templates > System > Logon > Enable\n"
            "2. Re-create the mapped drive:\n"
            "   - Right-click the drive > Disconnect\n"
            "   - Map it again: File Explorer > This PC > Map network drive\n"
            "   - Check 'Reconnect at sign-in'\n"
            "3. Ensure credential persistence:\n"
            "   - When mapping, check 'Connect using different credentials' if needed\n"
            "   - Save the credential in Credential Manager:\n"
            "   - Control Panel > Credential Manager > Windows Credentials > Add\n"
            "4. For domain environments:\n"
            "   - Verify the user has permission to the share\n"
            "   - Check Group Policy drive mapping: gpresult /r\n"
            "   - Force GP update: gpupdate /force\n"
            "5. Check the server/share is accessible:\n"
            "   - CMD: net view \\\\servername\n"
            "   - Test: ping servername\n"
            "6. Disable offline files if causing confusion:\n"
            "   - Control Panel > Sync Center > Manage Offline Files > Disable\n"
            "7. Use a login script instead of persistent mapping for reliability"
        ),
    },
    {
        "category": "Network",
        "problem_title": "IP address conflict detected",
        "problem_description": "Windows shows 'There is an IP address conflict with another system on the network'. Internet stops working.",
        "problem_keywords": "ip conflict, ip address conflict, duplicate ip, same ip, ip collision",
        "solution_steps": (
            "1. Release and get a new IP:\n"
            "   - CMD (Admin): ipconfig /release && ipconfig /renew\n"
            "2. If using static IP:\n"
            "   - Change to a different IP address that's not in use\n"
            "   - Or switch to DHCP: Adapter settings > IPv4 > Obtain automatically\n"
            "3. Find the conflicting device:\n"
            "   - CMD: arp -a (shows all IP/MAC on the network)\n"
            "   - From router admin page: Check DHCP leases\n"
            "   - Use Advanced IP Scanner (free tool) to find the other device\n"
            "4. On the router/DHCP server:\n"
            "   - Check for overlapping DHCP and static IP ranges\n"
            "   - Best practice: Reserve a range for static IPs (e.g., .1-.50) and DHCP above that\n"
            "   - Use DHCP reservations instead of static IPs on devices\n"
            "5. Restart DHCP server service (if your DHCP server is a Windows Server)\n"
            "6. If a device has a stale DHCP lease:\n"
            "   - On that device: ipconfig /release && ipconfig /renew"
        ),
    },
    {
        "category": "Network",
        "problem_title": "Very slow network speed / internet speed",
        "problem_description": "File transfers are very slow, websites load slowly, speed tests show much lower than expected bandwidth.",
        "problem_keywords": "slow network, slow internet, slow speed, bandwidth, slow download, slow wifi, slow transfer",
        "solution_steps": (
            "1. Run a speed test: speedtest.net or fast.com\n"
            "   - Compare with your ISP plan speed\n"
            "   - Test wired (Ethernet) vs wireless to isolate the issue\n"
            "2. If Wi-Fi is slow but Ethernet is fast:\n"
            "   - Move closer to router\n"
            "   - Switch to 5GHz band (faster but shorter range)\n"
            "   - Change Wi-Fi channel on router to less congested one\n"
            "   - Update Wi-Fi adapter driver\n"
            "   - Check for interference (microwaves, too many devices)\n"
            "3. If both wired and wireless are slow:\n"
            "   - Restart router and modem\n"
            "   - Check if many devices are using bandwidth (streaming, downloads)\n"
            "   - Contact ISP if speed is much lower than plan\n"
            "4. Check for bandwidth hogs:\n"
            "   - Task Manager > Performance > Open Resource Monitor > Network tab\n"
            "   - Check which process uses the most bandwidth\n"
            "5. Disable auto-tuning:\n"
            "   - CMD (Admin): netsh int tcp set global autotuninglevel=disabled\n"
            "   - To re-enable: netsh int tcp set global autotuninglevel=normal\n"
            "6. For slow file transfer on LAN:\n"
            "   - Check if Ethernet is linked at 100Mbps (should be 1Gbps)\n"
            "   - Replace cable with Cat5e or Cat6\n"
            "   - Check switch port speed and duplex settings"
        ),
    },
    {
        "category": "Network",
        "problem_title": "Ethernet connected but no internet",
        "problem_description": "Ethernet cable is plugged in and shows connected, but there's no internet. May show 'Unidentified Network' or 'No Internet'.",
        "problem_keywords": "ethernet no internet, wired no internet, unidentified network, ethernet not working, lan no internet",
        "solution_steps": (
            "1. Check physical connection:\n"
            "   - Ensure Ethernet cable clicks into both PC and wall/switch/router\n"
            "   - Try a different cable\n"
            "   - Check link lights on the network port (should be blinking)\n"
            "2. Check IP configuration:\n"
            "   - CMD: ipconfig\n"
            "   - If IP starts with 169.254.x.x: DHCP isn't working\n"
            "   - If no IP at all: adapter may be disabled\n"
            "3. APIPA address (169.254.x.x) fix:\n"
            "   - Restart DHCP: ipconfig /release && ipconfig /renew\n"
            "   - Check that DHCP server/router is working\n"
            "   - Try manual IP: Set a static IP in the same subnet as your router\n"
            "4. 'Unidentified Network' fix:\n"
            "   - Network and Sharing Center > Change adapter settings\n"
            "   - Right-click adapter > Disable, then Enable\n"
            "5. Reset network:\n"
            "   - CMD (Admin): netsh winsock reset\n"
            "   - netsh int ip reset\n"
            "   - Restart computer\n"
            "6. Update or reinstall Ethernet driver:\n"
            "   - Device Manager > Network adapters > Ethernet > Update/Uninstall driver\n"
            "7. Check switch/router port: Try a different port"
        ),
    },
    {
        "category": "Network",
        "problem_title": "Cannot access network shared folder",
        "problem_description": "Cannot access a shared folder on another computer. May show 'You do not have permission', 'Network path not found', or 'Access denied'.",
        "problem_keywords": "shared folder, network share, access denied share, cannot access share, smb, network path not found",
        "solution_steps": (
            "1. Test basic connectivity:\n"
            "   - Can you ping the server? CMD: ping servername\n"
            "   - Can you browse the server? CMD: net view \\\\servername\n"
            "2. 'Network path not found':\n"
            "   - Check the server name/IP is correct\n"
            "   - Try by IP: \\\\192.168.1.100\\sharename\n"
            "   - Ensure the server is on and the share exists\n"
            "   - Check firewall on the server allows File and Printer Sharing\n"
            "3. 'Access is denied':\n"
            "   - Verify you have share AND NTFS permissions\n"
            "   - Try connecting with explicit credentials: net use \\\\server\\share /user:domain\\username\n"
            "   - Clear saved credentials: Control Panel > Credential Manager > remove old entries\n"
            "4. Enable SMB on Windows 10/11:\n"
            "   - Windows Features > check 'SMB 1.0/CIFS File Sharing Support' (for old NAS/devices)\n"
            "   - Better: update the server to support SMB2/3\n"
            "5. Enable Network Discovery:\n"
            "   - Network and Sharing Center > Advanced sharing settings\n"
            "   - Turn on Network discovery and File and printer sharing\n"
            "6. Check the share permissions on the server:\n"
            "   - Right-click shared folder > Properties > Sharing > Permissions"
        ),
    },
    {
        "category": "Network",
        "problem_title": "Wi-Fi network not appearing in list",
        "problem_description": "The Wi-Fi network you want to connect to is not showing up in the list of available networks, but other devices can see it.",
        "problem_keywords": "wifi not showing, network not found, hidden network, wifi not visible, ssid not appearing, can't find wifi",
        "solution_steps": (
            "1. Check if the network is hidden (SSID broadcast disabled):\n"
            "   - Settings > Network > Wi-Fi > Manage known networks > Add a new network\n"
            "   - Enter the SSID (network name) exactly as configured on the router\n"
            "2. Check Wi-Fi adapter:\n"
            "   - Is Wi-Fi enabled? Check for a physical switch or Fn key toggle\n"
            "   - Is Airplane mode off? Settings > Network > Airplane mode\n"
            "3. Check if adapter supports the frequency:\n"
            "   - 5GHz networks won't show on adapters that only support 2.4GHz\n"
            "   - Check adapter specs in Device Manager > Network adapters > Properties\n"
            "4. Refresh the network list:\n"
            "   - Toggle Wi-Fi off and on\n"
            "   - Or right-click network icon > Disconnect, then reconnect\n"
            "5. Update Wi-Fi driver:\n"
            "   - Download latest from manufacturer website\n"
            "6. Reset Wi-Fi adapter:\n"
            "   - Device Manager > Wi-Fi adapter > Disable, wait 5 seconds, Enable\n"
            "7. Check router:\n"
            "   - Restart the router\n"
            "   - Verify the SSID is being broadcast\n"
            "   - Check if MAC filtering is enabled (blocking your device)"
        ),
    },
    {
        "category": "Network",
        "problem_title": "Proxy server errors or can't connect through proxy",
        "problem_description": "Browser shows 'Unable to connect to the proxy server' (ERR_PROXY_CONNECTION_FAILED). Unable to browse the internet.",
        "problem_keywords": "proxy error, proxy server, ERR_PROXY_CONNECTION_FAILED, proxy settings, proxy not working, proxy",
        "solution_steps": (
            "1. Check if a proxy is set and if you need one:\n"
            "   - Settings > Network > Proxy\n"
            "   - If you don't use a proxy: Turn off 'Use a proxy server'\n"
            "   - Set 'Automatically detect settings' to On\n"
            "2. Check browser-specific proxy settings:\n"
            "   - Chrome uses Windows proxy settings\n"
            "   - Firefox has its own: Options > Network Settings > No proxy\n"
            "3. If you need a proxy for your organization:\n"
            "   - Verify the proxy address and port are correct\n"
            "   - Try the proxy URL in the 'Automatic proxy setup' field instead\n"
            "4. Clear proxy settings via CMD:\n"
            "   - CMD: netsh winhttp reset proxy\n"
            "5. Check for malware:\n"
            "   - Malware often sets proxy to redirect traffic\n"
            "   - Run Windows Defender and Malwarebytes scan\n"
            "   - Check: HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings\n"
            "   - ProxyEnable should be 0 if no proxy needed\n"
            "6. Remove any suspicious browser extensions\n"
            "7. Reset Internet Explorer settings (affects Windows proxy):\n"
            "   - Internet Options > Advanced > Reset"
        ),
    },
    {
        "category": "Network",
        "problem_title": "DHCP not assigning IP addresses",
        "problem_description": "Computers on the network are not getting IP addresses from DHCP. Devices get APIPA addresses (169.254.x.x) instead.",
        "problem_keywords": "dhcp not working, no ip address, 169.254, apipa, dhcp server, dhcp scope, ip assignment",
        "solution_steps": (
            "1. Verify DHCP server is running:\n"
            "   - On Windows Server: Server Manager > DHCP > check service status\n"
            "   - On router: Access admin page and check DHCP settings\n"
            "2. Check DHCP scope:\n"
            "   - Are there available addresses? The scope may be exhausted\n"
            "   - Expand the scope or reduce lease time to free up addresses\n"
            "   - Check: DHCP console > Scope > Address Pool and Active Leases\n"
            "3. Check for rogue DHCP:\n"
            "   - Another device may be running DHCP (common: personal routers)\n"
            "   - From affected PC: ipconfig /all - check 'DHCP Server' IP\n"
            "   - It should be your official DHCP server's IP\n"
            "4. Restart DHCP service:\n"
            "   - On server: services.msc > DHCP Server > Restart\n"
            "   - On router: Reboot the router\n"
            "5. Check network connectivity between client and DHCP:\n"
            "   - DHCP uses UDP ports 67 and 68\n"
            "   - If on different subnet, need a DHCP relay agent / IP helper\n"
            "6. On client: ipconfig /release && ipconfig /renew\n"
            "7. Check Event Viewer on DHCP server for errors"
        ),
    },
    {
        "category": "Network",
        "problem_title": "Ping works but cannot browse websites",
        "problem_description": "Can ping IP addresses (e.g., 8.8.8.8) successfully but cannot open any websites in the browser. May also fail to ping domain names.",
        "problem_keywords": "ping works no browse, dns issue, ping ip works, can ping but no internet, browser not loading",
        "solution_steps": (
            "1. If you can ping IPs but not domain names: DNS problem\n"
            "   - Flush DNS: ipconfig /flushdns\n"
            "   - Test: nslookup google.com\n"
            "   - Change DNS to 8.8.8.8 or 1.1.1.1\n"
            "2. If you can ping IPs AND domain names but browser doesn't work:\n"
            "   - Check proxy settings: Settings > Network > Proxy > disable proxy\n"
            "   - Clear browser cache and cookies\n"
            "   - Try a different browser\n"
            "   - Check Windows Firewall isn't blocking the browser\n"
            "3. Reset browser:\n"
            "   - Chrome: Settings > Reset and clean up > Restore to defaults\n"
            "   - Edge: Settings > Reset settings\n"
            "4. Check date and time on PC (wrong date = SSL/TLS failures)\n"
            "5. Reset WinSock:\n"
            "   - netsh winsock reset\n"
            "   - Restart computer\n"
            "6. Check hosts file: C:\\Windows\\System32\\drivers\\etc\\hosts\n"
            "   - Look for entries blocking websites\n"
            "7. Disable browser extensions one by one to find conflicts"
        ),
    },
    {
        "category": "Network",
        "problem_title": "SMB/CIFS share access error after Windows update",
        "problem_description": "After a Windows update, cannot access network shares. Error 'You can't access this shared folder because your organization's security policies block unauthenticated guest access'.",
        "problem_keywords": "smb error, guest access blocked, shared folder update, smb1, smb2, cifs, organization security policies",
        "solution_steps": (
            "1. This is caused by Windows disabling insecure guest logons for SMB2\n"
            "2. If connecting to a NAS or older device that uses guest access:\n"
            "   - Best fix: Set up authentication on the NAS/server (add username/password)\n"
            "   - Quick fix via Group Policy: gpedit.msc\n"
            "   - Computer Config > Admin Templates > Network > Lanman Workstation\n"
            "   - 'Enable insecure guest logons' > Enabled (less secure)\n"
            "3. If the NAS/device only supports SMB1:\n"
            "   - Enable SMB1 (not recommended for security):\n"
            "   - Windows Features > SMB 1.0/CIFS File Sharing Support > check it\n"
            "   - Better: Update the NAS firmware to support SMB2/3\n"
            "4. If 'Access Denied' on a Windows share:\n"
            "   - Check both NTFS and Share permissions on the server\n"
            "   - Ensure the sharing user account exists and password hasn't expired\n"
            "5. Clear cached credentials:\n"
            "   - CMD: net use * /delete (removes all mapped drives)\n"
            "   - Credential Manager > remove old entries\n"
            "   - Reconnect with current credentials\n"
            "6. Check network profile: Set to 'Private' (not Public) for local sharing"
        ),
    },
    {
        "category": "Network",
        "problem_title": "Network printer not found or cannot print over network",
        "problem_description": "Cannot find or connect to a network printer. Printer was working before but now shows offline or inaccessible from other computers.",
        "problem_keywords": "network printer, printer not found, printer offline, shared printer, print server, printer network",
        "solution_steps": (
            "1. Verify the printer is online:\n"
            "   - Check printer display panel for IP address and status\n"
            "   - Ping the printer: CMD: ping <printer-ip>\n"
            "2. If ping fails:\n"
            "   - Check Ethernet cable or Wi-Fi connection on printer\n"
            "   - Restart the printer\n"
            "   - Print a network config page from the printer itself\n"
            "3. If ping works but can't print:\n"
            "   - Remove and re-add the printer:\n"
            "   - Settings > Printers & Scanners > Remove device > Add printer\n"
            "   - Add by IP: TCP/IP Address > enter printer IP\n"
            "4. For shared printer through another PC:\n"
            "   - Ensure the host PC is ON and the printer is shared\n"
            "   - Check: \\\\hostname\\printername or \\\\ip-address\\printername\n"
            "5. Windows Update printer fix (error 0x0000011b):\n"
            "   - On the print server/host PC, add registry key:\n"
            "   - HKLM\\SYSTEM\\CurrentControlSet\\Control\\Print\n"
            "   - DWORD: RpcAuthnLevelPrivacyEnabled = 0\n"
            "   - Restart Print Spooler\n"
            "6. Check Windows Firewall allows File and Printer Sharing\n"
            "7. Restart Print Spooler: net stop spooler && net start spooler"
        ),
    },
    {
        "category": "Network",
        "problem_title": "Traceroute shows high latency or packet loss",
        "problem_description": "Network connection has high ping/latency. Running tracert or pathping shows timeouts or high latency at certain hops.",
        "problem_keywords": "high ping, latency, traceroute, tracert, packet loss, pathping, network slow, lag",
        "solution_steps": (
            "1. Run a traceroute to identify where the problem is:\n"
            "   - CMD: tracert google.com\n"
            "   - Note which hop shows the jump in latency\n"
            "2. Run pathping for more detail:\n"
            "   - CMD: pathping google.com (takes several minutes)\n"
            "   - Shows packet loss at each hop\n"
            "3. Interpreting results:\n"
            "   - High latency at hop 1 (your router): Local network issue\n"
            "   - High latency at hop 2-3: ISP issue\n"
            "   - High latency only at final destination: Server issue\n"
            "   - Timeouts (*) at intermediate hops but destination works: Normal - some routers don't respond to ICMP\n"
            "4. For local network latency:\n"
            "   - Use wired connection instead of Wi-Fi\n"
            "   - Check for bandwidth-heavy usage on network\n"
            "   - Restart router\n"
            "5. For ISP issues:\n"
            "   - Contact ISP with traceroute results\n"
            "   - Check ISP status page for outages\n"
            "6. For gaming/real-time latency:\n"
            "   - Enable QoS on router to prioritize traffic\n"
            "   - Close background downloads/streaming\n"
            "   - Use Ethernet instead of Wi-Fi"
        ),
    },
    {
        "category": "Network",
        "problem_title": "Firewall blocking network traffic",
        "problem_description": "Applications or services can't communicate over the network due to firewall blocking. Need to identify and allow the blocked traffic.",
        "problem_keywords": "firewall blocking, port blocked, firewall rule, windows firewall, allow port, open port",
        "solution_steps": (
            "1. Test if firewall is the issue:\n"
            "   - Temporarily disable Windows Firewall (for testing only):\n"
            "   - CMD (Admin): netsh advfirewall set allprofiles state off\n"
            "   - If the app works now, it's a firewall issue\n"
            "   - Re-enable immediately: netsh advfirewall set allprofiles state on\n"
            "2. Find out what port/protocol the application uses:\n"
            "   - Check the application documentation\n"
            "   - Use Resource Monitor: Network > Listening Ports\n"
            "   - Or CMD: netstat -an | findstr LISTENING\n"
            "3. Allow an application through firewall:\n"
            "   - Firewall > Allow an app > Change settings > Allow another app > Browse\n"
            "4. Create a port rule:\n"
            "   - Firewall > Advanced settings > Inbound Rules > New Rule > Port\n"
            "   - Specify TCP or UDP and port number\n"
            "5. Check Event Viewer for blocked connections:\n"
            "   - Enable firewall logging:\n"
            "   - Advanced settings > Windows Firewall Properties > Logging\n"
            "   - Log dropped packets > Yes\n"
            "   - Check log at: C:\\Windows\\System32\\LogFiles\\Firewall\\pfirewall.log\n"
            "6. Common ports to allow:\n"
            "   - RDP: TCP 3389 | SMB: TCP 445 | HTTPS: TCP 443\n"
            "   - DNS: TCP/UDP 53 | DHCP: UDP 67-68"
        ),
    },
    {
        "category": "Network",
        "problem_title": "Computer cannot join or authenticate to domain",
        "problem_description": "Error when trying to join Active Directory domain or domain logon fails with 'trust relationship failed' or 'domain not available'.",
        "problem_keywords": "domain join, trust relationship, cannot join domain, domain login failed, active directory, domain trust",
        "solution_steps": (
            "1. 'Trust relationship between this workstation and the primary domain has failed':\n"
            "   - Fix: Log in with local admin account\n"
            "   - PowerShell (Admin): Reset-ComputerMachinePassword -Server \"DomainControllerName\" -Credential domain\\admin\n"
            "   - Or: Remove from domain (set to WORKGROUP), restart, rejoin domain\n"
            "2. 'Domain is not available' when joining:\n"
            "   - Check DNS: DNS must point to a domain controller\n"
            "   - ipconfig /all > check DNS server is the DC IP\n"
            "   - Test: nslookup domain.local (should resolve to DC)\n"
            "3. Verify network connectivity to DC:\n"
            "   - Ping the DC by name and IP\n"
            "   - Test required ports: CMD: nltest /sc_query:domain\n"
            "4. Check time sync:\n"
            "   - Computer time must be within 5 minutes of DC\n"
            "   - Set NTP to DC: w32tm /config /manualpeerlist:dc-ip /syncfromflags:manual /update\n"
            "   - Force sync: w32tm /resync\n"
            "5. Verify there are available computer objects in the OU\n"
            "6. Check the domain admin account has permissions to join computers\n"
            "7. Standard users can join up to 10 computers by default - may need increase\n"
            "8. Check that required ports are open between client and DC (TCP 88, 135, 389, 445, 636)"
        ),
    },
    {
        "category": "Network",
        "problem_title": "Wi-Fi connects but limited connectivity (no internet)",
        "problem_description": "Wi-Fi shows 'Connected, No Internet' or 'Limited' status. May show yellow triangle warning on the network icon.",
        "problem_keywords": "limited connectivity, wifi limited, no internet wifi, connected limited, yellow triangle, wifi no internet access",
        "solution_steps": (
            "1. Check if the issue is the router or just your device:\n"
            "   - Test another device on the same Wi-Fi\n"
            "   - If all devices have no internet: Router/ISP issue\n"
            "2. Forget and reconnect:\n"
            "   - Settings > Network > Wi-Fi > Manage known networks > Forget\n"
            "   - Reconnect with the password\n"
            "3. Reset TCP/IP:\n"
            "   - CMD (Admin):\n"
            "   - netsh winsock reset\n"
            "   - netsh int ip reset\n"
            "   - ipconfig /flushdns\n"
            "   - Restart computer\n"
            "4. Set Google DNS:\n"
            "   - Adapter settings > Wi-Fi > IPv4 > DNS: 8.8.8.8 / 8.8.4.4\n"
            "5. Disable IPv6:\n"
            "   - Adapter properties > uncheck IPv6\n"
            "   - Some captive portals and routers have IPv6 issues\n"
            "6. Reset network adapter:\n"
            "   - Settings > Network > Status > Network reset (last resort, removes all settings)\n"
            "7. Check router:\n"
            "   - Restart router\n"
            "   - Check DHCP pool isn't exhausted\n"
            "   - Check if MAC filtering is blocking your device"
        ),
    },
]

DIAGNOSTIC_TREE = {
    "category": "Network",
    "root": {
        "title": "Network Troubleshooting",
        "node_type": "question",
        "question_text": "What type of network problem are you experiencing?",
        "children": [
            {
                "title": "No internet connection at all",
                "node_type": "question",
                "question_text": "Are you using Wi-Fi or Ethernet (wired)?",
                "children": [
                    {
                        "title": "Wi-Fi",
                        "node_type": "question",
                        "question_text": "Is the Wi-Fi connected (shows connected but no internet)?",
                        "children": [
                            {
                                "title": "Yes - connected but no internet",
                                "node_type": "solution",
                                "solution_text": "1. Check if other devices have internet on same Wi-Fi\n   - If no devices have internet: Restart router (unplug 30 sec)\n   - If only your PC: Continue below\n2. Reset network:\n   - CMD (Admin): ipconfig /release && ipconfig /renew\n   - ipconfig /flushdns\n   - netsh winsock reset\n   - Restart computer\n3. Change DNS to 8.8.8.8 / 8.8.4.4\n4. Forget and reconnect to the Wi-Fi network\n5. Disable IPv6 on the adapter"
                            },
                            {
                                "title": "No - Wi-Fi is disconnected or network not showing",
                                "node_type": "solution",
                                "solution_text": "1. Check if Wi-Fi is turned on:\n   - Check for physical Wi-Fi switch or Fn key combination\n   - Settings > Network > Wi-Fi > toggle On\n   - Check Airplane Mode is OFF\n2. If the network doesn't appear:\n   - It may be a hidden SSID - manually add it\n   - Check if Wi-Fi adapter is enabled in Device Manager\n3. Reset Wi-Fi adapter:\n   - Device Manager > Wi-Fi adapter > Disable then Enable\n4. Update or reinstall Wi-Fi driver\n5. Restart the router to refresh the SSID broadcast"
                            }
                        ]
                    },
                    {
                        "title": "Ethernet (wired)",
                        "node_type": "solution",
                        "solution_text": "1. Check physical connection:\n   - Is the cable plugged in firmly at both ends?\n   - Are there link lights on the port?\n   - Try a different cable and port\n2. Check IP: Run 'ipconfig' in CMD\n   - 169.254.x.x = no DHCP response\n   - No IP = adapter disabled\n3. Release/renew: ipconfig /release && ipconfig /renew\n4. Reset: netsh winsock reset && netsh int ip reset && restart\n5. Reinstall Ethernet driver from Device Manager\n6. Check switch port or try a different one"
                    }
                ]
            },
            {
                "title": "Internet is slow",
                "node_type": "question",
                "question_text": "Is the slowness on all devices or just one computer?",
                "children": [
                    {
                        "title": "All devices are slow",
                        "node_type": "solution",
                        "solution_text": "1. Restart router and modem (unplug both for 30 seconds)\n2. Run a speed test on speedtest.net\n3. If speed is much lower than your plan:\n   - Contact your ISP\n   - Check for ISP outages in your area\n4. Check for bandwidth-heavy usage:\n   - Is someone streaming, downloading, or running large uploads?\n5. Check for too many connected devices\n6. Update router firmware\n7. If Wi-Fi: Change channel or switch to 5GHz\n8. Consider if your ISP plan is sufficient for your usage"
                    },
                    {
                        "title": "Only one computer is slow",
                        "node_type": "solution",
                        "solution_text": "1. Check which process uses bandwidth:\n   - Task Manager > Performance > Open Resource Monitor > Network\n2. Run malware scan (malware can use bandwidth)\n3. If on Wi-Fi: Move closer to router or connect via Ethernet\n4. Update network adapter driver\n5. Disable power management on network adapter:\n   - Device Manager > adapter > Properties > Power Management\n   - Uncheck 'Allow computer to turn off this device'\n6. Reset network stack: netsh winsock reset + restart\n7. Try disabling auto-tuning:\n   - netsh int tcp set global autotuninglevel=disabled"
                    }
                ]
            },
            {
                "title": "Can't access shared folders or printers",
                "node_type": "solution",
                "solution_text": "1. Verify the target PC/server is on and reachable:\n   - ping servername or ping IP\n2. Check if you can browse: net view \\\\servername\n3. Enable Network Discovery:\n   - Network and Sharing Center > Advanced sharing > Turn on\n4. Clear old credentials:\n   - Credential Manager > remove entries for the server\n5. Try accessing by IP: \\\\192.168.1.x\\sharename\n6. Check firewall allows File and Printer Sharing\n7. Check SMB is enabled:\n   - Windows Features > SMB 1.0/CIFS (for old devices)\n8. Verify share AND NTFS permissions on the server"
            },
            {
                "title": "VPN connection issues",
                "node_type": "solution",
                "solution_text": "1. Check internet connection first (VPN needs internet)\n2. Verify VPN server address and credentials\n3. Common error codes:\n   - 800: Server unreachable - check address\n   - 809: Firewall blocking - allow ports 500, 4500 UDP\n   - 789: L2TP key mismatch - check pre-shared key\n   - 812: Auth failed - check username/password\n4. For L2TP behind NAT:\n   - Add registry key AssumeUDPEncapsulationContextOnSendRule=2\n   - Restart computer\n5. Update VPN client software\n6. Restart IKE and IPsec services"
            },
            {
                "title": "DNS / Can't resolve domain names",
                "node_type": "solution",
                "solution_text": "1. Test: nslookup google.com\n   - If this fails: DNS problem confirmed\n2. Flush DNS: ipconfig /flushdns\n3. Change DNS server:\n   - Use Google (8.8.8.8) or Cloudflare (1.1.1.1)\n4. Reset DNS client: net stop dnscache && net start dnscache\n5. Check hosts file for bad entries:\n   - C:\\Windows\\System32\\drivers\\etc\\hosts\n6. Clear browser DNS cache\n7. For domain PCs: Verify DC is reachable and running DNS"
            }
        ]
    }
}
