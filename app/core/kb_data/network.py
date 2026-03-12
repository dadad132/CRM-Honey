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
    {
        "category": "Network",
        "problem_title": "Slow file transfer speed on local network",
        "problem_description": "Transferring files between computers on the same network is extremely slow. Getting only a fraction of the expected LAN speed.",
        "problem_keywords": "slow transfer, file copy slow, smb slow, network speed, lan speed, copy over network, nas slow",
        "solution_steps": (
            "1. Check link speed:\n"
            "   - Control Panel > Network > adapter > Status\n"
            "   - Should show 1.0 Gbps for gigabit (not 100 Mbps)\n"
            "   - If 100 Mbps: Cable is Cat5 (needs Cat5e/Cat6) or port is 100M\n"
            "2. Check for duplex mismatch:\n"
            "   - Adapter Properties > Advanced > Speed & Duplex\n"
            "   - Set to 'Auto Negotiation' or '1.0 Gbps Full Duplex'\n"
            "3. SMB tuning:\n"
            "   - Enable SMB Multichannel: Set-SmbClientConfiguration -EnableMultiChannel $true\n"
            "   - Check SMB version: Get-SmbConnection (should be 3.x)\n"
            "   - Disable SMB signing if not needed: Group Policy > Network > Microsoft Network Client\n"
            "4. Large Send Offload:\n"
            "   - Device Manager > NIC > Advanced > Large Send Offload V2 > Enabled\n"
            "   - Enable Jumbo Frames (9014) if switch supports it\n"
            "5. Disable bandwidth throttling apps:\n"
            "   - QoS policies, antivirus scanning during transfer, OneDrive sync\n"
            "6. Use Robocopy for large transfers:\n"
            "   - robocopy source dest /MT:16 /Z (multi-threaded, restartable)\n"
            "7. Check switches/cables: Faulty cable or switch port can negotiate at lower speed"
        ),
    },
    {
        "category": "Network",
        "problem_title": "Cannot access websites by name but IP works",
        "problem_description": "Websites fail to load by domain name (e.g., google.com) but work when using IP addresses directly. Internal applications may also fail.",
        "problem_keywords": "dns resolution, website by name, dns not resolving, nslookup, dns server, name resolution, domain name",
        "solution_steps": (
            "1. Confirm DNS issue:\n"
            "   - ping 8.8.8.8 (should work - proves connectivity)\n"
            "   - ping google.com (should fail - proves DNS issue)\n"
            "   - nslookup google.com (check if DNS resolves)\n"
            "2. Check DNS settings:\n"
            "   - ipconfig /all > look at DNS Servers\n"
            "   - If blank or wrong: Set manually\n"
            "   - Adapter Properties > IPv4 > DNS: 8.8.8.8 / 8.8.4.4\n"
            "3. Flush DNS cache:\n"
            "   - ipconfig /flushdns\n"
            "   - ipconfig /registerdns\n"
            "4. Check hosts file:\n"
            "   - C:\\Windows\\System32\\drivers\\etc\\hosts\n"
            "   - Verify no incorrect entries blocking sites\n"
            "   - Malware can add entries to redirect traffic\n"
            "5. Test with nslookup:\n"
            "   - nslookup google.com 8.8.8.8 (test with Google DNS directly)\n"
            "   - If this works but default DNS fails: Internal DNS server issue\n"
            "6. DNS client service:\n"
            "   - services.msc > 'DNS Client' > should be Running\n"
            "   - Restart the service\n"
            "7. Try: netsh winsock reset and restart the computer"
        ),
    },
    {
        "category": "Network",
        "problem_title": "Network adapter keeps disconnecting and reconnecting",
        "problem_description": "Ethernet or Wi-Fi adapter drops the connection and reconnects repeatedly every few minutes. May show 'Network cable unplugged' briefly.",
        "problem_keywords": "network disconnect, adapter dropping, cable unplugged, reconnecting, intermittent, connection drops, unstable",
        "solution_steps": (
            "1. Check physical connections:\n"
            "   - Reseat the Ethernet cable at both ends\n"
            "   - Try a different cable\n"
            "   - Try a different switch port\n"
            "2. Disable power management:\n"
            "   - Device Manager > Network adapter > Properties > Power Management\n"
            "   - Uncheck 'Allow the computer to turn off this device to save power'\n"
            "3. Update or rollback driver:\n"
            "   - Device Manager > Network adapter > Update Driver\n"
            "   - If issue started after update: Roll Back Driver\n"
            "   - Download the latest driver from the manufacturer\n"
            "4. Disable Energy Efficient Ethernet:\n"
            "   - Device Manager > NIC > Advanced > Energy Efficient Ethernet > Disabled\n"
            "   - Also try: Green Ethernet > Disabled\n"
            "5. For Wi-Fi:\n"
            "   - Forget the network and reconnect\n"
            "   - Change Wi-Fi band: Try 5 GHz instead of 2.4 GHz\n"
            "   - Disable 'Connect automatically' to other networks\n"
            "   - Set network as Metered to prevent Windows updates during connection\n"
            "6. Check Event Viewer:\n"
            "   - System log > filter by source 'e1express' or 'Netwtw' (NIC driver)\n"
            "   - Look for error patterns and timestamps\n"
            "7. Replace the NIC if hardware failure is suspected"
        ),
    },
    {
        "category": "Network",
        "problem_title": "VLAN or network segmentation issues",
        "problem_description": "Device cannot communicate across VLANs or subnets. Can ping devices on the same VLAN but not on different VLANs.",
        "problem_keywords": "vlan, subnet, inter-vlan, routing, network segment, can't reach, different subnet, gateway",
        "solution_steps": (
            "1. Check default gateway:\n"
            "   - ipconfig > verify the default gateway is correct for the VLAN\n"
            "   - Each VLAN/subnet needs its own gateway (usually the router/L3 switch)\n"
            "   - If gateway is wrong: Reconfigure IP or fix DHCP scope\n"
            "2. Verify routing:\n"
            "   - From the device: tracert <target IP on other VLAN>\n"
            "   - If stops at gateway: The router isn't routing between VLANs\n"
            "   - Check router/L3 switch routing configuration\n"
            "3. Check switch VLAN configuration:\n"
            "   - Verify the port is assigned to the correct VLAN\n"
            "   - Access ports vs trunk ports: Access for endpoints, trunk for switches\n"
            "   - Native VLAN mismatch can cause issues\n"
            "4. Firewall/ACL rules:\n"
            "   - Inter-VLAN communication may be blocked by ACLs on the router\n"
            "   - Check firewall rules that filter between subnets\n"
            "5. DHCP relay:\n"
            "   - If DHCP server is on a different VLAN: IP helper-address is needed\n"
            "   - Without relay: Devices in that VLAN get no IP from DHCP\n"
            "6. Test from the gateway:\n"
            "   - Can the router ping both VLANs?\n"
            "   - Check 'ip routing' is enabled on L3 switch\n"
            "7. Common issue: VLAN tagging on the PC port should be untagged (access mode)"
        ),
    },
    {
        "category": "Network",
        "problem_title": "Wi-Fi connected but very slow speed",
        "problem_description": "Connected to Wi-Fi with strong signal but internet speeds are extremely slow. Speed test shows much lower than expected.",
        "problem_keywords": "slow wifi, wifi speed, wireless slow, wifi connected slow, bad wifi, slow internet wifi, 2.4ghz",
        "solution_steps": (
            "1. Run a speed test:\n"
            "   - Compare Wi-Fi speed vs wired speed on the same network\n"
            "   - If wired is also slow: Issue is the internet connection, not Wi-Fi\n"
            "2. Check Wi-Fi band:\n"
            "   - 2.4 GHz: Slower, more interference, longer range\n"
            "   - 5 GHz: Faster, less interference, shorter range\n"
            "   - Connect to the 5 GHz network if available\n"
            "3. Channel congestion:\n"
            "   - Use a Wi-Fi analyzer app to check channel congestion\n"
            "   - Change router channel to a less congested one\n"
            "   - 2.4 GHz: Use channels 1, 6, or 11 only\n"
            "4. Check for bandwidth hogs:\n"
            "   - Task Manager > Performance > Open Resource Monitor > Network\n"
            "   - Look for apps/processes using bandwidth (updates, cloud sync)\n"
            "5. Router placement:\n"
            "   - Move closer to router or access point\n"
            "   - Check signal strength: netsh wlan show interfaces\n"
            "   - >70% signal: Good, <50%: May cause slow speeds\n"
            "6. Wireless adapter:\n"
            "   - Check adapter speed: Device Manager > Wi-Fi > Advanced > Wireless Mode\n"
            "   - Set to 802.11ac or 802.11ax if supported\n"
            "   - Update Wi-Fi adapter driver\n"
            "7. Reset the router: Sometimes a simple reboot clears congestion"
        ),
    },
    {
        "category": "Network",
        "problem_title": "802.1X authentication failure on wired network",
        "problem_description": "Computer cannot connect to the wired network due to 802.1X authentication failure. Network shows 'No internet' or 'Identifying' indefinitely.",
        "problem_keywords": "802.1x, network authentication, eap, wired auth, nac, dot1x, port based, network access, certificate",
        "solution_steps": (
            "1. Check 802.1X settings:\n"
            "   - Network adapter Properties > Authentication tab\n"
            "   - If tab is missing: Enable '802.1X Authentication' in services\n"
            "   - Wired AutoConfig service must be running\n"
            "2. Authentication method:\n"
            "   - Settings > Authentication method > typically EAP-TLS or PEAP\n"
            "   - EAP-TLS: Requires a valid client certificate\n"
            "   - PEAP: Uses username/password with server certificate\n"
            "3. Certificate issues (EAP-TLS):\n"
            "   - Open certmgr.msc > Personal > Certificates\n"
            "   - Check the machine certificate is valid and not expired\n"
            "   - Check the root CA certificate is in Trusted Root CAs\n"
            "4. Check the RADIUS server:\n"
            "   - NPS/RADIUS logs on the server side\n"
            "   - Event Viewer on the server: Network Policy and Access Services\n"
            "   - Common: Certificate mismatch, user not in correct group\n"
            "5. Switch port configuration:\n"
            "   - Verify the switch port has 802.1X configured correctly\n"
            "   - Check if the port is in 'err-disabled' state\n"
            "   - Try a different switch port\n"
            "6. Bypass for troubleshooting:\n"
            "   - Have network admin temporarily disable 802.1X on the port\n"
            "   - If connection works: Focus on certificate/credentials\n"
            "7. Re-enroll the certificate through Group Policy or SCEP"
        ),
    },
    {
        "category": "Network",
        "problem_title": "Network shares intermittently unavailable",
        "problem_description": "Mapped network drives or UNC paths work sometimes and fail other times. May show 'The network path was not found' intermittently.",
        "problem_keywords": "network share intermittent, mapped drive drops, smb timeout, network path not found, share access, unc path",
        "solution_steps": (
            "1. Check SMB connectivity:\n"
            "   - net use (list current connections)\n"
            "   - Test-NetConnection -ComputerName server -Port 445\n"
            "   - If port 445 is intermittently blocked: Firewall issue\n"
            "2. SMB keepalive:\n"
            "   - Idle SMB connections may be dropped by firewalls or servers\n"
            "   - Registry: HKLM\\SYSTEM\\CurrentControlSet\\Services\\LanmanWorkstation\\Parameters\n"
            "   - KeepConn (DWORD): Set to 600 (seconds)\n"
            "3. Reconnect mapped drives:\n"
            "   - Right-click mapped drive > Disconnect\n"
            "   - Remap with 'Reconnect at sign-in' checked\n"
            "   - Or use a logon script: net use Z: \\\\server\\share /persistent:yes\n"
            "4. DNS resolution:\n"
            "   - The server name may resolve intermittently\n"
            "   - nslookup servername > verify consistent IP\n"
            "   - Add a static entry in hosts file as workaround\n"
            "5. Check the file server:\n"
            "   - Server may be under heavy load or running out of connections\n"
            "   - Check server Event Viewer for SMB errors\n"
            "   - Get-SmbSession on the server to see active connections\n"
            "6. Disable SMB signing if not required (can improve performance):\n"
            "   - Group Policy: Microsoft Network Client > Digitally sign communications\n"
            "7. Update SMB client: Ensure latest Windows updates are applied"
        ),
    },
    {
        "category": "Network",
        "problem_title": "Captive portal not loading on public Wi-Fi",
        "problem_description": "Connected to a public Wi-Fi (hotel, airport, coffee shop) but the login/captive portal page doesn't appear and there's no internet access.",
        "problem_keywords": "captive portal, public wifi, hotel wifi, login page, wifi portal, redirect, guest wifi, no portal",
        "solution_steps": (
            "1. Trigger the portal manually:\n"
            "   - Open a browser and go to http://neverssl.com or http://captive.apple.com\n"
            "   - These HTTP (not HTTPS) sites often trigger the redirect\n"
            "   - Try: http://1.1.1.1 or http://192.168.1.1\n"
            "2. DNS may be blocking the redirect:\n"
            "   - If using custom DNS (8.8.8.8): Temporarily switch to DHCP-provided DNS\n"
            "   - Adapter Properties > IPv4 > 'Obtain DNS server address automatically'\n"
            "   - Reconnect to the network\n"
            "3. Browser issues:\n"
            "   - Try a different browser\n"
            "   - Clear browser cache and cookies\n"
            "   - Disable extensions that might block redirects\n"
            "4. VPN interference:\n"
            "   - Disconnect any VPN before connecting to captive portal\n"
            "   - VPN may prevent the redirect from working\n"
            "   - Connect to VPN after completing the portal login\n"
            "5. Flush DNS and renew IP:\n"
            "   - ipconfig /release\n"
            "   - ipconfig /flushdns\n"
            "   - ipconfig /renew\n"
            "6. Forget and reconnect:\n"
            "   - Forget the Wi-Fi network\n"
            "   - Reconnect and wait for the portal to appear\n"
            "7. Ask front desk for direct login URL if portal still won't load"
        ),
    },
    {
        "category": "Network",
        "problem_title": "IPv6 connectivity issues",
        "problem_description": "IPv6 shows 'No network access' in network adapter status. Some websites or services that prefer IPv6 are slow or fail to load.",
        "problem_keywords": "ipv6, no network access, ipv6 connectivity, dual stack, ipv6 not working, ipv6 dns, slaac",
        "solution_steps": (
            "1. Check IPv6 status:\n"
            "   - ipconfig /all > look for IPv6 Address and Default Gateway\n"
            "   - If only fe80:: (link-local): No IPv6 routing\n"
            "   - Should have a global address (2xxx:: or prefix from ISP)\n"
            "2. Test IPv6:\n"
            "   - ping ::1 (loopback - tests IPv6 stack)\n"
            "   - ping ipv6.google.com\n"
            "   - Visit https://test-ipv6.com for detailed diagnostics\n"
            "3. If ISP doesn't support IPv6:\n"
            "   - 'No network access' for IPv6 is normal if ISP is IPv4-only\n"
            "   - This doesn't affect IPv4 connectivity\n"
            "   - Can disable IPv6 on the adapter to avoid confusion\n"
            "4. If IPv6 should work but doesn't:\n"
            "   - Check router: Is IPv6 enabled? (Router admin page)\n"
            "   - Check firewall: Windows Firewall may block ICMPv6\n"
            "   - DHCPv6 or SLAAC must be working on the network\n"
            "5. Reset IPv6:\n"
            "   - netsh interface ipv6 reset\n"
            "   - Restart the computer\n"
            "6. Prefer IPv4 over IPv6 (if IPv6 causes slowness):\n"
            "   - Registry: HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip6\\Parameters\n"
            "   - DisabledComponents (DWORD): 0x20 (prefer IPv4)\n"
            "7. Don't disable IPv6 entirely unless absolutely necessary (Microsoft supported)"
        ),
    },
    {
        "category": "Network",
        "problem_title": "DNS round robin or load balancing not working as expected",
        "problem_description": "Multiple servers behind DNS round robin but traffic is not distributing evenly. Some servers get most of the traffic while others are idle.",
        "problem_keywords": "dns round robin, load balancing, dns distribution, server load, uneven traffic, dns cache, ttl",
        "solution_steps": (
            "1. Understand DNS round robin limitations:\n"
            "   - DNS round robin rotates IP addresses in DNS responses\n"
            "   - It does NOT check server health or current load\n"
            "   - Clients/resolvers may cache one IP and reuse it\n"
            "2. Check TTL:\n"
            "   - nslookup -type=A hostname (shows TTL)\n"
            "   - Lower TTL = more frequent DNS queries = better distribution\n"
            "   - Set TTL to 60-300 seconds for round robin\n"
            "3. Client-side DNS caching:\n"
            "   - Windows DNS client caches IP addresses\n"
            "   - ipconfig /flushdns on client (temporary fix)\n"
            "   - Intermediate DNS resolvers also cache\n"
            "4. Verify round robin is configured:\n"
            "   - On DNS server: Check that round robin is enabled\n"
            "   - Windows DNS: DNS Manager > Server Properties > Advanced > Enable round robin\n"
            "   - Also enable 'Enable netmask ordering'\n"
            "5. Better alternatives:\n"
            "   - Use a proper load balancer (HAProxy, F5, Azure LB)\n"
            "   - Load balancers offer health checks and session persistence\n"
            "   - Consider cloud load balancing (AWS ELB, Azure Application Gateway)\n"
            "6. Monitor server load:\n"
            "   - Check each server's active connections and response times\n"
            "   - Uneven distribution is normal with DNS round robin"
        ),
    },
    {
        "category": "Network",
        "problem_title": "Double NAT causing connectivity issues",
        "problem_description": "Two routers on the network causing double NAT. Port forwarding doesn't work, gaming/VoIP has issues, and VPN connections fail.",
        "problem_keywords": "double nat, two routers, port forwarding not working, nat issue, cgnat, modem router, bridge mode",
        "solution_steps": (
            "1. Identify double NAT:\n"
            "   - tracert 8.8.8.8 > if you see two private IPs (192.168.x.x) in the path\n"
            "   - Check router WAN IP: If it's 192.168.x.x or 10.x.x.x, you're behind another NAT\n"
            "2. Common cause:\n"
            "   - ISP modem/router combo + your own router = two NAT layers\n"
            "   - ISP using CGNAT (Carrier-Grade NAT) - 100.64.x.x range\n"
            "3. Solution 1 - Bridge mode:\n"
            "   - Set ISP modem/router to Bridge Mode or Passthrough\n"
            "   - This disables the ISP router's NAT and lets your router handle everything\n"
            "   - Access ISP router (usually 192.168.0.1 or 192.168.1.1)\n"
            "4. Solution 2 - DMZ:\n"
            "   - On the ISP router: Set your router's WAN IP as the DMZ host\n"
            "   - This forwards all traffic to your router\n"
            "5. Solution 3 - Remove one router:\n"
            "   - Use only the ISP modem/router and disable your router\n"
            "   - Or request a modem-only device from ISP\n"
            "6. For CGNAT:\n"
            "   - Contact ISP to request a public IP address\n"
            "   - Some ISPs charge extra for a static/public IP\n"
            "   - Alternative: Use a VPN service with port forwarding\n"
            "7. Port forwarding must be configured on BOTH routers in double NAT"
        ),
    },
    {
        "category": "Network",
        "problem_title": "Wake-on-LAN (WOL) not working",
        "problem_description": "Cannot wake a remote computer using Wake-on-LAN magic packets. Computer stays off or doesn't respond to WOL commands.",
        "problem_keywords": "wake on lan, wol, magic packet, remote wake, power on remote, wake up pc, wol not working",
        "solution_steps": (
            "1. Enable WOL in BIOS:\n"
            "   - Restart > BIOS/UEFI > Power Settings or Advanced\n"
            "   - Enable 'Wake on LAN' or 'Power On by PCI-E/PCI'\n"
            "   - May be called 'Wake on Magic Packet'\n"
            "2. Enable WOL in Windows:\n"
            "   - Device Manager > Network adapter > Properties\n"
            "   - Power Management tab: Check 'Allow this device to wake the computer'\n"
            "   - Also check 'Only allow a magic packet to wake the computer'\n"
            "   - Advanced tab: 'Wake on Magic Packet' > Enabled\n"
            "3. Disable Fast Startup:\n"
            "   - Fast Startup puts the PC in a hybrid shutdown state that may prevent WOL\n"
            "   - Power Options > Choose what power buttons do > Turn off fast startup\n"
            "4. Network requirements:\n"
            "   - WOL works over Ethernet only (not Wi-Fi typically)\n"
            "   - The sending device must be on the same subnet (or use directed broadcast)\n"
            "   - Note the target PC's MAC address (ipconfig /all)\n"
            "5. Send the magic packet:\n"
            "   - Use a WOL tool or PowerShell script\n"
            "   - The packet must contain the MAC address repeated\n"
            "6. Cross-subnet WOL:\n"
            "   - Configure directed broadcast on the router\n"
            "   - ip directed-broadcast on the target VLAN interface\n"
            "   - Send magic packet to the subnet broadcast address\n"
            "7. Test: Shutdown the PC (not hibernate) and send WOL from another device"
        ),
    },
    {
        "category": "Network",
        "problem_title": "ARP table issues causing communication failures",
        "problem_description": "Devices on the same network can't communicate or have intermittent connectivity due to stale or incorrect ARP cache entries.",
        "problem_keywords": "arp, arp cache, arp table, arp poisoning, ip conflict, mac address, arp -a, communication failure",
        "solution_steps": (
            "1. View ARP table:\n"
            "   - arp -a (shows IP to MAC mappings)\n"
            "   - Check if the target IP resolves to the correct MAC address\n"
            "   - If wrong MAC: ARP cache is stale or poisoned\n"
            "2. Clear ARP cache:\n"
            "   - arp -d * (clear all ARP entries, requires admin)\n"
            "   - netsh interface ip delete arpcache\n"
            "   - ARP cache refreshes automatically, but clearing forces re-resolution\n"
            "3. IP conflict detection:\n"
            "   - Two devices with the same IP will show different MACs\n"
            "   - arp -a | find 'target IP' and verify MAC consistency\n"
            "   - Use: arping or nmap to detect duplicate IPs\n"
            "4. ARP poisoning/spoofing:\n"
            "   - Malware can send fake ARP responses to redirect traffic\n"
            "   - Use Dynamic ARP Inspection (DAI) on managed switches\n"
            "   - Check for unusual ARP entries: arp -a (same MAC for multiple IPs)\n"
            "5. Static ARP entries:\n"
            "   - For critical servers: arp -s <IP> <MAC> (static entry)\n"
            "   - Prevents poisoning for that specific IP\n"
            "6. Gratuitous ARP:\n"
            "   - When IP changes or after failover, gratuitous ARP updates are needed\n"
            "   - Some devices may not send them, causing stale entries\n"
            "7. Reduce ARP timeout: netsh interface ipv4 set subinterface <idx> mtu=1500"
        ),
    },
    {
        "category": "Network",
        "problem_title": "MTU size causing packet fragmentation issues",
        "problem_description": "Certain websites or applications fail to load while others work. Caused by MTU path mismatch leading to packet fragmentation or black-holing.",
        "problem_keywords": "mtu, packet fragmentation, mtu mismatch, jumbo frame, path mtu, mtu discovery, packet size",
        "solution_steps": (
            "1. Test for MTU issues:\n"
            "   - ping target -f -l 1472 (test with 1472 byte payload + 28 byte header = 1500)\n"
            "   - If 'Packet needs to be fragmented': MTU is lower than 1500\n"
            "   - Reduce size until ping works: ping target -f -l 1400\n"
            "   - Add 28 to the working value = your MTU\n"
            "2. Common MTU sizes:\n"
            "   - Ethernet: 1500 (standard)\n"
            "   - PPPoE: 1492 (common for DSL)\n"
            "   - VPN tunnels: 1400-1460 (overhead reduces available space)\n"
            "3. Set MTU on the interface:\n"
            "   - netsh interface ipv4 set subinterface \"Ethernet\" mtu=1400 store=persistent\n"
            "   - Or in the router: Typically in WAN/Internet settings\n"
            "4. VPN MTU issues:\n"
            "   - VPN adds headers, reducing effective MTU\n"
            "   - Set MTU on VPN adapter to 1300-1400\n"
            "   - Or configure VPN server to adjust MSS clamping\n"
            "5. Path MTU Discovery (PMTUD):\n"
            "   - Windows uses PMTUD to find the optimal MTU\n"
            "   - Firewalls blocking ICMP 'Fragmentation Needed' messages break PMTUD\n"
            "   - Ensure ICMP Type 3 Code 4 is allowed through firewalls\n"
            "6. Jumbo frames:\n"
            "   - 9000 MTU for iSCSI or NAS traffic\n"
            "   - ALL devices in the path must support jumbo frames\n"
            "   - One device with 1500 MTU breaks the chain"
        ),
    },
    {
        "category": "Network",
        "problem_title": "Network printer not found after IP change",
        "problem_description": "Network printer is unreachable after the printer's IP address changed via DHCP renewal. Users get 'printer offline' errors.",
        "problem_keywords": "printer ip change, printer offline, printer ip, dhcp printer, printer not found, static ip printer",
        "solution_steps": (
            "1. Find the printer's new IP:\n"
            "   - Print a configuration page from the printer's control panel\n"
            "   - Check DHCP server leases for the printer's MAC address\n"
            "   - Scan the network: arp -a or use Advanced IP Scanner\n"
            "2. Update the printer port:\n"
            "   - Devices and Printers > right-click printer > Printer Properties\n"
            "   - Ports tab > select the port > Configure Port\n"
            "   - Update the IP address to the new one\n"
            "3. Prevent future changes - set a static IP on the printer:\n"
            "   - Access printer web interface (http://printer-ip)\n"
            "   - Network settings > IPv4 > Manual/Static\n"
            "   - Set an IP outside the DHCP range\n"
            "4. Or use DHCP reservation:\n"
            "   - On the DHCP server: Create a reservation for the printer's MAC\n"
            "   - This always assigns the same IP via DHCP\n"
            "5. Use hostname instead of IP:\n"
            "   - Create printer port using the printer's hostname\n"
            "   - Hostname doesn't change with IP, so this is more resilient\n"
            "6. For print servers:\n"
            "   - Update the printer port on the print server\n"
            "   - Clients connected via print server don't need changes\n"
            "7. Batch update: PowerShell can update printer ports across multiple PCs"
        ),
    },
    {
        "category": "Network",
        "problem_title": "Network discovery not showing other computers",
        "problem_description": "File Explorer's Network view doesn't show other computers on the network. Cannot browse to other PCs even though ping works.",
        "problem_keywords": "network discovery, computers not showing, browse network, network view, smb browse, workgroup, netbios",
        "solution_steps": (
            "1. Enable Network Discovery:\n"
            "   - Settings > Network & Internet > Advanced sharing settings\n"
            "   - Turn on 'Network discovery'\n"
            "   - Turn on 'File and printer sharing'\n"
            "   - Apply for the correct profile (Private or Domain)\n"
            "2. Check the network profile:\n"
            "   - Settings > Network > Ethernet/Wi-Fi > Properties\n"
            "   - Set to 'Private' (not Public)\n"
            "   - Public profile disables discovery by default\n"
            "3. Required services:\n"
            "   - Function Discovery Provider Host: Running\n"
            "   - Function Discovery Resource Publication: Running\n"
            "   - SSDP Discovery: Running\n"
            "   - UPnP Device Host: Running\n"
            "4. SMB 1.0 (legacy):\n"
            "   - Older devices may need SMB 1.0 for discovery\n"
            "   - Windows Features > SMB 1.0/CIFS File Sharing Support\n"
            "   - Enable 'SMB 1.0/CIFS Client' only (not server)\n"
            "   - Note: SMB 1.0 has security risks\n"
            "5. WSD (Web Services for Devices):\n"
            "   - Windows 10+ uses WSD instead of NetBIOS for discovery\n"
            "   - Ensure WSD is not blocked by firewall\n"
            "6. Direct access still works:\n"
            "   - \\\\computername or \\\\IP-address in File Explorer\n"
            "   - Discovery just affects the browsing view\n"
            "7. Workgroup: All PCs should be in the same workgroup name"
        ),
    },
    {
        "category": "Network",
        "problem_title": "SSL/TLS certificate errors in browser",
        "problem_description": "Websites show 'Your connection is not private', NET::ERR_CERT errors, or 'This site is not secure' warnings in the browser.",
        "problem_keywords": "ssl error, certificate error, not secure, tls error, err_cert, privacy error, https warning, certificate",
        "solution_steps": (
            "1. Check the date/time:\n"
            "   - Incorrect system date/time causes certificate errors\n"
            "   - Settings > Time & Language > Set time automatically\n"
            "   - Sync now with time server\n"
            "2. Specific error codes:\n"
            "   - NET::ERR_CERT_DATE_INVALID: Certificate expired or system date wrong\n"
            "   - NET::ERR_CERT_AUTHORITY_INVALID: Untrusted CA (self-signed or internal)\n"
            "   - NET::ERR_CERT_COMMON_NAME_INVALID: Domain name mismatch\n"
            "3. For internal/corporate sites:\n"
            "   - Import the company's Root CA certificate\n"
            "   - certmgr.msc > Trusted Root Certification Authorities > Import\n"
            "   - Should be deployed via Group Policy in domain environments\n"
            "4. Browser-specific:\n"
            "   - Chrome: chrome://settings > Security > Manage certificates\n"
            "   - Firefox uses its own certificate store: Options > Privacy > View Certificates\n"
            "   - Import the CA cert in Firefox separately\n"
            "5. SSL inspection / proxy:\n"
            "   - Corporate proxy may intercept HTTPS (SSL inspection)\n"
            "   - The proxy CA cert must be trusted on the client\n"
            "   - Check certificate details: Is the issuer your company or the actual site?\n"
            "6. Clear SSL state:\n"
            "   - Internet Options > Content > Clear SSL state\n"
            "   - Clear browser cache\n"
            "7. If the certificate is legitimately expired: Contact the website owner"
        ),
    },
    {
        "category": "Network",
        "problem_title": "Port forwarding not working on router",
        "problem_description": "Configured port forwarding on the router but external users cannot reach the internal service. Internal access works fine.",
        "problem_keywords": "port forwarding, port forward, nat, open port, router port, port not working, external access, port map",
        "solution_steps": (
            "1. Verify port forwarding config:\n"
            "   - Log into router > Port Forwarding section\n"
            "   - External port, Internal IP, Internal port, Protocol (TCP/UDP/Both)\n"
            "   - Internal IP must be the correct server IP\n"
            "2. Check from external:\n"
            "   - Use a port checker (canyouseeme.org) from outside your network\n"
            "   - Or ask someone external to test\n"
            "   - Testing from inside your network may not work (hairpin NAT)\n"
            "3. Common issues:\n"
            "   - Double NAT: Check for two routers (see double NAT article)\n"
            "   - ISP blocking ports: ISPs often block port 80, 443, 25\n"
            "   - CGNAT: ISP uses 100.64.x.x range, port forwarding won't work\n"
            "4. Windows Firewall:\n"
            "   - The server's Windows Firewall must allow the port\n"
            "   - Windows Firewall > Inbound Rules > New Rule > Port\n"
            "5. Service must be listening:\n"
            "   - On the server: netstat -an | find ':PORT'\n"
            "   - The service must be listening on 0.0.0.0:PORT (not 127.0.0.1)\n"
            "6. Static IP for the server:\n"
            "   - If the server IP changes, port forward breaks\n"
            "   - Set a static IP or DHCP reservation\n"
            "7. Dynamic DNS: If your public IP changes, use a DDNS service"
        ),
    },
    {
        "category": "Network",
        "problem_title": "Network printer discovery not finding printers on the network",
        "problem_description": "Network printer discovery in Windows fails to find printers. Printers aren't visible in 'Add a printer' wizard despite being on the same network and powered on.",
        "problem_keywords": "printer discovery, find printer, network printer, add printer, printer not found, printer browse, wsd, printer search",
        "solution_steps": (
            "1. Basic connectivity:\n"
            "   - Ping the printer's IP address\n"
            "   - Print a network configuration page from the printer itself\n"
            "   - Verify printer and PC are on the same subnet/VLAN\n"
            "2. Discovery protocols:\n"
            "   - WSD (Web Services for Devices): Must be enabled on printer\n"
            "   - SNMP: Enable SNMP on printer for discovery\n"
            "   - Check: 'Network discovery' is ON in Windows (Advanced sharing settings)\n"
            "3. Firewall:\n"
            "   - Windows Firewall may block printer discovery\n"
            "   - Enable: Network Discovery firewall rules\n"
            "   - Check: mDNS, SNMP (UDP 161), WSD ports are not blocked\n"
            "4. Add printer manually:\n"
            "   - Add Printer > 'The printer that I want isn't listed'\n"
            "   - Select 'Add a printer using TCP/IP address'\n"
            "   - Enter printer's IP address directly\n"
            "5. DNS entry: For reliable access, create a DNS A record for the printer (e.g., printer-floor2.company.local) rather than relying on discovery"
        ),
    },
    {
        "category": "Network",
        "problem_title": "802.1X network authentication failures",
        "problem_description": "Wired or wireless 802.1X network authentication failing. Devices can't connect to the corporate network, get placed in guest VLAN, or show certificate errors during authentication.",
        "problem_keywords": "802.1x, radius, network authentication, nac, eap, certificate auth, nps, dot1x, wired authentication",
        "solution_steps": (
            "1. Check client-side config:\n"
            "   - Network adapter properties > Authentication tab\n"
            "   - Enable IEEE 802.1X authentication\n"
            "   - Verify EAP type matches server config (PEAP, EAP-TLS)\n"
            "2. Certificate issues:\n"
            "   - EAP-TLS: Client needs valid computer/user certificate\n"
            "   - PEAP: Client needs to trust the RADIUS server's certificate\n"
            "   - Check: Certificate expiration, CA trust chain\n"
            "   - certutil -store my (list personal certificates)\n"
            "3. RADIUS/NPS server:\n"
            "   - NPS event log: Security log on RADIUS server\n"
            "   - Common: Reason Code 16 (authentication failed)\n"
            "   - Check: Network Policy conditions match the connecting client\n"
            "   - Verify: Shared secret matches between switch and NPS\n"
            "4. Switch/AP config:\n"
            "   - Verify RADIUS server IP and shared secret on switch\n"
            "   - Check: Authentication port (1812) and accounting port (1813)\n"
            "   - Guest VLAN: Ensure fallback VLAN is configured\n"
            "5. Group Policy: Deploy 802.1X settings via GPO (Computer Config > Windows Settings > Security > Wired/Wireless Network Policies)"
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
