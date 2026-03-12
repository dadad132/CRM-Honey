"""
IT Knowledge Base Seed Data
Populates the database with common IT problems, solutions, and diagnostic trees.
Runs once on startup if the tables are empty.
Covers: Windows errors, printer issues, network, email, hardware, software, authentication.
"""
from sqlmodel import select
from app.models.knowledge_base import KBDiagnosticTree, KBResolvedCase
from app.models.support_kb import SupportArticle, SupportCategory


# =====================================================
# CATEGORIES
# =====================================================
CATEGORIES = [
    {"name": "Printer", "icon": "fas fa-print", "description": "Printer issues, print spooler, drivers"},
    {"name": "Network", "icon": "fas fa-wifi", "description": "Wi-Fi, Ethernet, DNS, VPN, connectivity"},
    {"name": "Windows", "icon": "fab fa-windows", "description": "Blue screens, updates, OS errors, performance"},
    {"name": "Email", "icon": "fas fa-envelope", "description": "Outlook, email sync, account setup"},
    {"name": "Hardware", "icon": "fas fa-desktop", "description": "Monitors, keyboards, USB, audio, drives"},
    {"name": "Software", "icon": "fas fa-laptop-code", "description": "Office apps, browsers, installations"},
    {"name": "Authentication", "icon": "fas fa-key", "description": "Passwords, account lockouts, MFA"},
    {"name": "Server", "icon": "fas fa-server", "description": "File server, Active Directory, permissions"},
]


# =====================================================
# KB ARTICLES - Real IT solutions
# =====================================================
ARTICLES = [
    # ---- PRINTER ----
    {
        "category": "Printer",
        "problem_title": "Printer shows Offline status",
        "problem_description": "The printer appears as 'Offline' in Windows despite being powered on and connected. Print jobs queue up but never print.",
        "problem_keywords": "printer offline, printer not printing, printer status offline, printer greyed out",
        "solution_steps": "1. Check the physical connection (USB cable or network cable) and ensure the printer is powered on\n2. Open Settings > Devices > Printers & Scanners\n3. Click on the printer > Open print queue\n4. Click Printer menu > uncheck 'Use Printer Offline'\n5. If still offline, restart the Print Spooler service:\n   - Press Win+R, type services.msc, press Enter\n   - Find 'Print Spooler', right-click > Restart\n6. If on network, verify the printer's IP address hasn't changed:\n   - Print a network config page from the printer\n   - Update the printer port in Printer Properties > Ports\n7. Remove and re-add the printer if the above steps don't work",
    },
    {
        "category": "Printer",
        "problem_title": "Print Spooler service keeps stopping",
        "problem_description": "The Windows Print Spooler service crashes or stops automatically. Users cannot print and get error 'The print spooler service is not running'.",
        "problem_keywords": "print spooler, spooler crash, spooler stopped, cannot print, print service",
        "solution_steps": "1. Clear the print queue folder:\n   - Stop Print Spooler: Run as Admin cmd > net stop spooler\n   - Delete all files in C:\\Windows\\System32\\spool\\PRINTERS\\\n   - Start Print Spooler: net start spooler\n2. If it keeps crashing, check for corrupt drivers:\n   - Open Print Management (printmanagement.msc)\n   - Go to All Drivers, remove any suspicious third-party drivers\n3. Run SFC scan: sfc /scannow (in elevated CMD)\n4. Check Event Viewer > Windows Logs > System for spooler crash details\n5. If a specific printer driver causes crashes, reinstall that printer with a fresh driver from manufacturer website\n6. As last resort, reset Print Spooler to defaults:\n   - Delete registry key: HKLM\\SYSTEM\\CurrentControlSet\\Control\\Print\\Printers (backup first)\n   - Restart Print Spooler service",
    },
    {
        "category": "Printer",
        "problem_title": "Printer printing blank pages",
        "problem_description": "The printer feeds paper through but pages come out completely blank or with very faint text.",
        "problem_keywords": "blank pages, empty print, no text, faint print, printer blank",
        "solution_steps": "1. Check ink/toner levels - replace if low\n2. For inkjet printers:\n   - Run the printer's built-in head cleaning utility (usually in printer properties or printer's own menu)\n   - Run it 2-3 times if needed, then print a test page\n   - Check if nozzles are clogged - print nozzle check pattern\n3. For laser printers:\n   - Remove toner cartridge, gently shake side to side to redistribute toner\n   - Check if the sealing tape was removed from a new cartridge\n   - Check the drum unit for damage\n4. Verify the correct paper size and type are selected in print settings\n5. Try printing from a different application to rule out software issues\n6. Update or reinstall the printer driver from the manufacturer's website",
    },
    {
        "category": "Printer",
        "problem_title": "Cannot add network printer - Windows cannot connect",
        "problem_description": "When trying to add a shared network printer, Windows shows 'Windows cannot connect to the printer' with error 0x0000011b or similar.",
        "problem_keywords": "add printer, network printer, 0x0000011b, cannot connect printer, shared printer, printer error",
        "solution_steps": "1. For error 0x0000011b (common after Windows update):\n   - On the PRINT SERVER: Open Registry Editor\n   - Navigate to HKLM\\SYSTEM\\CurrentControlSet\\Control\\Print\n   - Create DWORD value: RpcAuthnLevelPrivacyEnabled = 0\n   - Restart Print Spooler service\n2. Alternative fix: Install the printer driver locally first, then add the network printer\n3. Verify network connectivity to the print server: ping <server-name>\n4. Ensure File and Printer Sharing is enabled on both machines:\n   - Control Panel > Network and Sharing Center > Advanced sharing settings\n5. Check that the printer is shared and permissions allow Everyone or appropriate users\n6. If using IP: Add printer by TCP/IP address instead of browsing the network\n   - Use printer's IP address (print a config page from the printer to find it)",
    },
    {
        "category": "Printer",
        "problem_title": "Paper jam error but no paper stuck",
        "problem_description": "Printer displays 'Paper Jam' error but there is no visible paper stuck inside the printer.",
        "problem_keywords": "paper jam, ghost jam, false paper jam, paper feed error",
        "solution_steps": "1. Turn off the printer and unplug it for 30 seconds\n2. Open all accessible doors and trays, look carefully for small paper scraps\n3. Check the following common jam locations:\n   - Paper input tray (remove tray completely)\n   - Under the toner/ink cartridge area\n   - Rear access panel / duplexer\n   - Output tray area and rollers\n4. Clean the paper feed rollers with a slightly damp lint-free cloth\n5. Check for worn paper feed rollers (smooth/shiny = need replacement)\n6. Make sure paper guides in the tray are snug but not too tight against the paper\n7. Try different paper - old/damp/curled paper causes false jams\n8. Plug in and turn on - if error persists, do a full power cycle (unplug for 60 seconds)\n9. Update firmware from manufacturer website",
    },
    {
        "category": "Printer",
        "problem_title": "Printer prints very slowly",
        "problem_description": "Print jobs take much longer than expected to complete. Printer pauses between pages or takes minutes to start printing.",
        "problem_keywords": "slow printing, printer slow, slow print, print speed, printing takes long",
        "solution_steps": "1. Check print quality setting - change from 'Best' or 'High Quality' to 'Normal' or 'Draft'\n2. For network printers, check network connection quality:\n   - Use Ethernet instead of Wi-Fi if possible\n   - Check for IP conflicts\n3. Clear the print spooler queue:\n   - net stop spooler\n   - Delete files in C:\\Windows\\System32\\spool\\PRINTERS\\\n   - net start spooler\n4. Update the printer driver from manufacturer's website\n5. Check if bidirectional communication is causing delays:\n   - Printer Properties > Ports > Uncheck 'Enable bidirectional support'\n6. For large documents, check if 'Print directly to printer' helps:\n   - Printer Properties > Advanced > 'Print directly to the printer'\n7. Ensure the printer firmware is up to date\n8. Check printer's memory - complex documents may exceed printer memory",
    },
    {
        "category": "Printer",
        "problem_title": "Error 0x00000709 - Cannot set default printer",
        "problem_description": "Windows shows error 0x00000709 when trying to set a default printer, or the default printer keeps changing.",
        "problem_keywords": "0x00000709, default printer, cannot set default, printer changing",
        "solution_steps": "1. Disable Windows managing default printer:\n   - Settings > Devices > Printers & Scanners\n   - Turn off 'Let Windows manage my default printer'\n2. Set default manually:\n   - Right-click the desired printer > Set as default\n3. If error persists, fix via registry:\n   - Open regedit as Administrator\n   - Go to HKCU\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Windows\n   - Change 'Device' value to your printer name (format: PrinterName,winspool,PortName)\n   - You may need to take ownership of this key first\n4. Remove all other printers temporarily, set default, then re-add them\n5. Run printer troubleshooter: Settings > Update & Security > Troubleshoot > Printer",
    },

    # ---- WINDOWS ----
    {
        "category": "Windows",
        "problem_title": "Blue Screen KERNEL_DATA_INPAGE_ERROR",
        "problem_description": "Computer crashes with blue screen showing KERNEL_DATA_INPAGE_ERROR (0x0000007A). May happen during boot or randomly during use.",
        "problem_keywords": "blue screen, BSOD, KERNEL_DATA_INPAGE_ERROR, 0x0000007A, crash, disk error",
        "solution_steps": "1. This error usually indicates a disk or RAM problem\n2. Check disk health:\n   - Open CMD as Admin: chkdsk C: /f /r\n   - Reboot to run the scan\n   - Check SMART status: wmic diskdrive get status\n3. Test RAM:\n   - Run Windows Memory Diagnostic: mdsched.exe\n   - Choose 'Restart now and check for problems'\n4. Check for driver issues:\n   - Boot into Safe Mode (hold Shift while clicking Restart)\n   - If stable in Safe Mode, a driver is likely the cause\n   - Update storage controller and disk drivers\n5. Check Event Viewer for disk errors:\n   - Look for Event ID 7, 11, or 51 under System log\n6. If disk is failing, back up data immediately and replace the drive\n7. Disable pagefile temporarily to test: System Properties > Advanced > Performance > Virtual Memory",
    },
    {
        "category": "Windows",
        "problem_title": "Blue Screen IRQL_NOT_LESS_OR_EQUAL",
        "problem_description": "Windows crashes with IRQL_NOT_LESS_OR_EQUAL blue screen error. Often happens after installing new hardware or drivers.",
        "problem_keywords": "blue screen, IRQL_NOT_LESS_OR_EQUAL, BSOD, driver crash, 0x0000000A",
        "solution_steps": "1. This is almost always a driver issue\n2. If it started after a recent change, undo that change:\n   - Boot Safe Mode (hold Shift + Restart > Troubleshoot > Startup Settings)\n   - Uninstall recently added drivers or software\n3. Update drivers (especially network, graphics, and chipset):\n   - Open Device Manager > right-click each device > Update driver\n   - Download latest drivers from manufacturer website\n4. Run Driver Verifier to find the faulting driver:\n   - CMD (Admin): verifier /standard /all\n   - Reboot - Windows will crash and identify the bad driver\n   - Disable verifier after: verifier /reset\n5. Check for Windows updates\n6. Run SFC: sfc /scannow\n7. Run DISM: DISM /Online /Cleanup-Image /RestoreHealth\n8. Test RAM with Windows Memory Diagnostic (mdsched.exe)",
    },
    {
        "category": "Windows",
        "problem_title": "Blue Screen CRITICAL_PROCESS_DIED",
        "problem_description": "Windows shows CRITICAL_PROCESS_DIED blue screen. Computer may enter a boot loop or crash repeatedly.",
        "problem_keywords": "blue screen, CRITICAL_PROCESS_DIED, boot loop, BSOD, cannot boot",
        "solution_steps": "1. Boot into Safe Mode:\n   - Power on, force power off 3 times to trigger WinRE\n   - Troubleshoot > Advanced > Startup Settings > Enable Safe Mode\n2. In Safe Mode:\n   - Uninstall recent Windows updates: Settings > Update > View update history > Uninstall\n   - Uninstall recently installed software\n   - Update all drivers\n3. Run system file repair:\n   - CMD (Admin): sfc /scannow\n   - Then: DISM /Online /Cleanup-Image /RestoreHealth\n4. Check disk: chkdsk C: /f /r\n5. Use System Restore:\n   - WinRE > Troubleshoot > Advanced > System Restore\n   - Pick a restore point before the issue started\n6. If still failing, run Startup Repair:\n   - WinRE > Troubleshoot > Advanced > Startup Repair\n7. Last resort: Reset PC keeping files:\n   - Settings > Recovery > Reset this PC > Keep my files",
    },
    {
        "category": "Windows",
        "problem_title": "Windows Update stuck or failing",
        "problem_description": "Windows Update downloads get stuck at a percentage, fail with error codes, or the update keeps retrying and failing.",
        "problem_keywords": "windows update, update stuck, update failed, update error, 0x80070002, 0x80073712, 0x800f081f",
        "solution_steps": "1. Run the Windows Update Troubleshooter:\n   - Settings > Update & Security > Troubleshoot > Windows Update\n2. Reset Windows Update components:\n   - Open CMD as Admin and run:\n   - net stop wuauserv\n   - net stop cryptSvc\n   - net stop bits\n   - net stop msiserver\n   - ren C:\\Windows\\SoftwareDistribution SoftwareDistribution.old\n   - ren C:\\Windows\\System32\\catroot2 catroot2.old\n   - net start wuauserv\n   - net start cryptSvc\n   - net start bits\n   - net start msiserver\n3. Repair system files:\n   - sfc /scannow\n   - DISM /Online /Cleanup-Image /RestoreHealth\n4. Free up disk space (at least 20GB on C: drive)\n5. Temporarily disable antivirus\n6. Download the update manually from Microsoft Update Catalog (catalog.update.microsoft.com)\n7. Check the C:\\Windows\\Logs\\CBS\\CBS.log for specific error details",
    },
    {
        "category": "Windows",
        "problem_title": "Computer running very slow",
        "problem_description": "Windows is running extremely slowly. Applications take a long time to open, high disk or CPU usage in Task Manager.",
        "problem_keywords": "slow computer, slow pc, high cpu, high disk, 100% disk, slow performance, lag",
        "solution_steps": "1. Open Task Manager (Ctrl+Shift+Esc) and check which process uses the most CPU/Disk/Memory\n2. If disk is at 100%:\n   - Disable Superfetch/SysMain: services.msc > SysMain > Disable\n   - Disable Windows Search indexer: services.msc > Windows Search > Disable\n   - Check disk health: wmic diskdrive get status\n   - Consider upgrading to SSD if using HDD\n3. Disable startup programs:\n   - Task Manager > Startup tab > Disable unnecessary programs\n4. Run disk cleanup:\n   - Type 'Disk Cleanup' > Clean up system files > Check all boxes\n5. Check for malware:\n   - Run Windows Defender full scan\n   - Download and run Malwarebytes free scan\n6. Disable visual effects:\n   - System Properties > Advanced > Performance > Adjust for best performance\n7. Check RAM usage - if consistently above 80%, consider adding more RAM\n8. Uninstall programs you don't use\n9. Run SFC: sfc /scannow\n10. Defragment HDD (not SSD): dfrgui.exe",
    },
    {
        "category": "Windows",
        "problem_title": "Start Menu not opening or not working",
        "problem_description": "Clicking the Start button does nothing. Start Menu won't open, or opens but freezes/crashes immediately.",
        "problem_keywords": "start menu, start button, start not working, taskbar, start broken",
        "solution_steps": "1. Quick fix - restart Windows Explorer:\n   - Ctrl+Shift+Esc > find Windows Explorer > right-click > Restart\n2. Re-register Start Menu apps:\n   - Open PowerShell as Admin:\n   - Get-AppXPackage -AllUsers | Foreach {Add-AppxPackage -DisableDevelopmentMode -Register \"$($_.InstallLocation)\\AppXManifest.xml\"}\n3. Run SFC and DISM:\n   - CMD (Admin): sfc /scannow\n   - DISM /Online /Cleanup-Image /RestoreHealth\n4. Create a new user profile to test:\n   - Settings > Accounts > Family & other users > Add someone\n   - If Start works on new profile, the old profile is corrupt\n5. Check and fix Windows indexing:\n   - services.msc > Windows Search > Restart\n6. Sign out and sign back in\n7. Last resort: Create new local admin account, copy data, delete old profile",
    },
    {
        "category": "Windows",
        "problem_title": "Black screen after login",
        "problem_description": "After entering password, user sees a black screen with only a cursor visible. Desktop, taskbar, and icons don't appear.",
        "problem_keywords": "black screen, no desktop, cursor only, black screen after login, no taskbar",
        "solution_steps": "1. Try Ctrl+Shift+Esc to open Task Manager\n   - If it opens: File > Run new task > explorer.exe > check 'Create this task with administrative privileges'\n2. If Task Manager doesn't open, try Ctrl+Alt+Del > Sign out, then sign back in\n3. Boot into Safe Mode:\n   - Force power off 3 times to trigger WinRE\n   - Troubleshoot > Advanced > Startup Settings > Safe Mode with Networking\n4. In Safe Mode:\n   - Uninstall graphics/display driver, reboot to let Windows install generic one\n   - Disable Fast Startup: Control Panel > Power Options > Choose what power buttons do > Change currently unavailable settings > Uncheck 'Turn on fast startup'\n5. Rename or delete: C:\\Users\\<username>\\AppData\\Local\\Packages\\Microsoft.Windows.ShellExperienceHost\n6. Run sfc /scannow in Safe Mode\n7. Try System Restore to a working point\n8. Check for recent Windows updates and uninstall the latest one",
    },
    {
        "category": "Windows",
        "problem_title": "DLL file missing or not found errors",
        "problem_description": "Application shows 'The program can't start because XXXX.dll is missing from your computer' or 'Entry point not found in DLL'.",
        "problem_keywords": "dll missing, dll not found, dll error, missing dll, vcruntime, msvcp, api-ms-win",
        "solution_steps": "1. First identify which DLL is missing and which program needs it\n2. Install/repair Microsoft Visual C++ Redistributables:\n   - Download all versions (2010, 2012, 2013, 2015-2022) from Microsoft\n   - Install both x86 and x64 versions\n   - This fixes most vcruntime140.dll, msvcp140.dll type errors\n3. For .NET DLL errors, install/repair .NET Framework:\n   - Download from Microsoft, or use: DISM /Online /Enable-Feature /FeatureName:NetFx3\n4. Run SFC to repair system DLLs: sfc /scannow\n5. Reinstall the application that's showing the error\n6. If DirectX related: Install DirectX End-User Runtime from Microsoft\n7. NEVER download DLLs from random websites - this is a major security risk\n8. Check if the application needs to be run as Administrator",
    },
    {
        "category": "Windows",
        "problem_title": "Windows activation error or not genuine",
        "problem_description": "Windows shows 'Activate Windows' watermark, or gives 'Windows is not genuine' error. Features may be limited.",
        "problem_keywords": "activate windows, not genuine, activation error, product key, license, 0xC004C003",
        "solution_steps": "1. Check current activation status:\n   - CMD: slmgr /xpr (shows license status)\n   - CMD: slmgr /dli (shows detailed license info)\n2. Open Settings > Update & Security > Activation\n3. If you have a product key: Click 'Change product key' and enter it\n4. If it was previously activated (hardware change):\n   - Settings > Activation > Troubleshoot\n   - 'I changed hardware on this device recently'\n   - Sign in with the Microsoft account linked to the license\n5. For volume license (KMS) issues:\n   - Verify KMS server is reachable: nslookup -type=srv _vlmcs._tcp\n   - Re-activate: slmgr /ato\n6. If multi-activation (MAK) key:\n   - CMD (Admin): slmgr /ipk <MAK-KEY>\n   - slmgr /ato\n7. Run: slmgr /rearm to reset the activation timer (works up to 3 times)",
    },
    {
        "category": "Windows",
        "problem_title": "File Explorer not responding or crashing",
        "problem_description": "Windows File Explorer freezes, shows 'Not Responding', or crashes when opening folders or right-clicking files.",
        "problem_keywords": "file explorer, explorer crash, explorer not responding, folder freeze, explorer.exe",
        "solution_steps": "1. Quick fix - restart Explorer:\n   - Ctrl+Shift+Esc > Windows Explorer > Restart\n2. Clear Explorer history:\n   - Open File Explorer > View > Options > Clear File Explorer history\n3. Disable Quick Access:\n   - File Explorer Options > General > Open to 'This PC' instead of Quick Access\n   - Uncheck both options under Privacy\n4. Disable Preview Pane: View > Preview Pane (toggle off)\n5. Check for corrupt shell extensions:\n   - Download ShellExView (NirSoft) to find and disable third-party extensions\n6. Run SFC: sfc /scannow\n7. Clear thumbnail cache:\n   - Disk Cleanup > check 'Thumbnails'\n   - Or CMD: del /f /s /q %LocalAppData%\\Microsoft\\Windows\\Explorer\\thumbcache_*.db\n8. Check for problematic context menu entries (right-click handlers)\n9. Update display/graphics driver",
    },

    # ---- NETWORK ----
    {
        "category": "Network",
        "problem_title": "No internet connection - connected to Wi-Fi",
        "problem_description": "Computer shows connected to Wi-Fi but 'No Internet Access'. Web pages don't load. Shows yellow triangle on network icon.",
        "problem_keywords": "no internet, wifi no internet, connected no internet, yellow triangle, no internet access",
        "solution_steps": "1. Quick fixes (try in order):\n   - Turn Wi-Fi off and on\n   - Restart the router/modem (unplug 30 seconds)\n   - Restart the computer\n2. Reset network stack:\n   - CMD (Admin):\n   - ipconfig /release\n   - ipconfig /flushdns\n   - ipconfig /renew\n   - netsh winsock reset\n   - netsh int ip reset\n   - Restart computer\n3. Try changing DNS servers:\n   - Network adapter settings > IPv4 > Use these DNS:\n   - 8.8.8.8 and 8.8.4.4 (Google) or 1.1.1.1 and 1.0.0.1 (Cloudflare)\n4. Disable and re-enable the network adapter:\n   - Device Manager > Network Adapters > right-click > Disable, then Enable\n5. Update / reinstall Wi-Fi driver\n6. Check if other devices on the same network have internet\n   - If no: Router/ISP issue\n   - If yes: This computer's network stack issue\n7. Check proxy settings: Settings > Network > Proxy > Ensure 'Automatically detect' is on and manual proxy is off",
    },
    {
        "category": "Network",
        "problem_title": "Wi-Fi keeps disconnecting randomly",
        "problem_description": "Wi-Fi connection drops frequently and reconnects. May happen every few minutes. Other devices on the same network are stable.",
        "problem_keywords": "wifi disconnect, wifi dropping, wifi unstable, wifi keeps disconnecting, intermittent wifi",
        "solution_steps": "1. Disable Wi-Fi power management:\n   - Device Manager > Network Adapters > Wi-Fi adapter > Properties\n   - Power Management tab: Uncheck 'Allow computer to turn off this device to save power'\n   - If available, Advanced tab: Set 'Power Saving Mode' to Off\n2. Forget and reconnect to the network:\n   - Settings > Network > Wi-Fi > Manage known networks\n   - Click your network > Forget\n   - Reconnect with password\n3. Update Wi-Fi driver from manufacturer website (not Windows Update)\n4. Change the Wi-Fi adapter's roaming aggressiveness:\n   - Device Manager > adapter > Advanced > Roaming Aggressiveness > set to Lowest\n5. Check for interference:\n   - Switch router to 5GHz band if available (less interference)\n   - Move closer to the router\n6. Reset network: Settings > Network > Network reset (this removes all saved networks)\n7. If on a laptop, check that airplane mode isn't toggling",
    },
    {
        "category": "Network",
        "problem_title": "DNS_PROBE_FINISHED_NXDOMAIN error",
        "problem_description": "Browser shows 'This site can't be reached - DNS_PROBE_FINISHED_NXDOMAIN' when trying to visit websites.",
        "problem_keywords": "DNS error, NXDOMAIN, dns probe, site cant be reached, dns not resolving",
        "solution_steps": "1. Flush DNS cache:\n   - CMD (Admin): ipconfig /flushdns\n2. Release and renew IP:\n   - ipconfig /release\n   - ipconfig /renew\n3. Change DNS servers:\n   - Open Network adapter settings > IPv4 Properties\n   - Set DNS to: 8.8.8.8 / 8.8.4.4 (Google) or 1.1.1.1 / 1.0.0.1 (Cloudflare)\n4. Clear browser DNS cache:\n   - Chrome: chrome://net-internals/#dns > Clear host cache\n   - Edge: edge://net-internals/#dns > Clear host cache\n5. Reset Winsock: CMD (Admin): netsh winsock reset\n6. Disable VPN or proxy if active\n7. Restart DNS Client service: services.msc > DNS Client > Restart\n8. If only specific sites: Check if the domain actually exists, or try in incognito mode\n9. Check hosts file: C:\\Windows\\System32\\drivers\\etc\\hosts - remove any suspicious entries",
    },
    {
        "category": "Network",
        "problem_title": "Cannot connect to VPN",
        "problem_description": "VPN client fails to connect, shows connection timeout or authentication error. Was working before.",
        "problem_keywords": "VPN, vpn not connecting, vpn timeout, vpn error, vpn authentication, remote access",
        "solution_steps": "1. Restart the VPN client application\n2. Check your internet connection (VPN needs working internet first)\n3. Verify VPN credentials haven't expired or password hasn't changed\n4. Restart these Windows services:\n   - IKE and AuthIP IPsec Keying Modules\n   - IPsec Policy Agent\n   - Remote Access Connection Manager\n5. If using Windows built-in VPN:\n   - Recreate the VPN connection from scratch\n   - Try different VPN protocol (IKEv2 vs L2TP vs SSTP)\n6. Check if your firewall/antivirus is blocking VPN ports:\n   - L2TP: UDP 500, 4500, 1701\n   - IKEv2: UDP 500, 4500\n   - OpenVPN: UDP 1194\n   - SSTP: TCP 443\n7. Flush DNS and reset network: ipconfig /flushdns && netsh winsock reset\n8. If behind a hotel/public Wi-Fi, the network may be blocking VPN traffic\n9. Contact IT admin to verify the VPN server is up and your account is enabled",
    },
    {
        "category": "Network",
        "problem_title": "Cannot access shared network drive or folder",
        "problem_description": "User cannot open mapped network drives. Gets 'Windows cannot access \\\\server\\share' error. May show access denied.",
        "problem_keywords": "network drive, shared folder, cannot access, network share, mapped drive, access denied, smb",
        "solution_steps": "1. Check network connectivity: ping <server-name-or-IP>\n2. Verify the share still exists: \\\\servername\\sharename in File Explorer address bar\n3. Check credentials:\n   - Open Credential Manager (Control Panel > Credential Manager)\n   - Remove old entries for the server, then try again\n4. Enable SMB on Windows:\n   - Control Panel > Programs > Turn Windows features on/off\n   - Enable 'SMB 1.0/CIFS File Sharing Support' (if the server requires SMBv1)\n   - Prefer SMB 2.0/3.0 for security\n5. Re-map the drive:\n   - CMD: net use Z: /delete (remove old mapping)\n   - CMD: net use Z: \\\\servername\\sharename /user:domain\\username /persistent:yes\n6. Check Windows services are running:\n   - TCP/IP NetBIOS Helper\n   - Server\n   - Workstation\n7. Check that Network Discovery and File Sharing are enabled:\n   - Network and Sharing Center > Advanced sharing settings\n8. If Access Denied, check share permissions AND NTFS permissions on the server",
    },
    {
        "category": "Network",
        "problem_title": "IP address conflict detected",
        "problem_description": "Windows shows 'There is an IP address conflict with another system on the network'. Network connectivity is lost or intermittent.",
        "problem_keywords": "ip conflict, ip address conflict, duplicate ip, network conflict",
        "solution_steps": "1. Release and get a new IP:\n   - CMD (Admin): ipconfig /release\n   - ipconfig /renew\n2. If using static IP, check which other device has the same address:\n   - Use: arp -a to see the MAC addresses on the network\n   - Check DHCP server leases for conflicts\n3. Switch to DHCP (automatic) IP assignment:\n   - Network adapter > IPv4 > 'Obtain an IP address automatically'\n4. Restart the router/DHCP server to clear stale leases\n5. On the DHCP server, increase the lease time or expand the IP range\n6. If you need static IP, use one outside the DHCP range\n   - Example: If DHCP range is .100-.200, use static IP in .10-.99 range\n7. Flush ARP cache: CMD (Admin): netsh interface ip delete arpcache",
    },
    {
        "category": "Network",
        "problem_title": "Slow internet speed",
        "problem_description": "Internet is working but very slow. Web pages load slowly, downloads take too long. Speed test shows much lower than expected.",
        "problem_keywords": "slow internet, slow speed, bandwidth, slow download, slow wifi, internet speed",
        "solution_steps": "1. Run a speed test: speedtest.net or fast.com\n   - Compare result to your ISP plan speed\n2. Test with Ethernet cable to rule out Wi-Fi issues\n3. Restart router and modem (unplug 30 seconds each)\n4. Check for bandwidth hogs:\n   - Task Manager > Performance > Open Resource Monitor > Network tab\n   - Check which apps are using bandwidth\n5. Change Wi-Fi channel:\n   - Login to router admin page (usually 192.168.1.1)\n   - Change Wi-Fi channel to less congested one\n   - Use 5GHz band for faster speeds (shorter range)\n6. Update network adapter driver\n7. Disable Windows Update delivery optimization:\n   - Settings > Update > Delivery Optimization > turn off\n8. Check for malware running in background\n9. If on Wi-Fi, check signal strength and move closer to router\n10. If all devices are slow, contact your ISP",
    },

    # ---- EMAIL ----
    {
        "category": "Email",
        "problem_title": "Outlook not sending or receiving emails",
        "problem_description": "Microsoft Outlook shows 'Disconnected' or 'Trying to connect'. Emails stuck in Outbox, new emails not appearing.",
        "problem_keywords": "outlook disconnected, outlook not working, email not sending, email not receiving, outlook stuck",
        "solution_steps": "1. Check if you're working offline:\n   - Send/Receive tab > check if 'Work Offline' is active (blue highlight) > click to disable\n2. Check internet connection by opening a website in browser\n3. Restart Outlook completely (check Task Manager it's fully closed)\n4. Test connection:\n   - File > Account Settings > Account Settings > Double-click account > Test Account Settings\n5. Repair the Outlook profile:\n   - File > Account Settings > Account Settings > select account > Repair\n6. Create new Outlook profile:\n   - Control Panel > Mail > Show Profiles > Add\n   - Set new profile as default\n7. For Exchange: Check server is reachable\n   - Outlook should show server name in bottom status bar\n8. For IMAP/POP: Verify incoming/outgoing server settings\n   - IMAP: 993/SSL, POP3: 995/SSL, SMTP: 587/STARTTLS or 465/SSL\n9. Clear Outlook's auto-complete cache if sending fails:\n   - File > Options > Mail > Empty Auto-Complete List\n10. Run: outlook.exe /safe to start in Safe Mode (disables add-ins)",
    },
    {
        "category": "Email",
        "problem_title": "Outlook crashes on startup",
        "problem_description": "Microsoft Outlook crashes immediately when opened, or shows 'Microsoft Outlook has stopped working' error.",
        "problem_keywords": "outlook crash, outlook won't open, outlook stopped working, outlook error, outlook startup",
        "solution_steps": "1. Start Outlook in Safe Mode:\n   - Hold Ctrl while clicking Outlook shortcut, or\n   - Run: outlook.exe /safe\n   - If it works in Safe Mode, an add-in is the cause\n2. Disable add-ins:\n   - File > Options > Add-ins > Manage: COM Add-ins > Go\n   - Uncheck all, restart Outlook, re-enable one at a time\n3. Repair Office installation:\n   - Control Panel > Programs > Microsoft Office > Change > Quick Repair\n   - If quick repair doesn't help: Online Repair\n4. Repair the Outlook data file:\n   - Close Outlook completely\n   - Run SCANPST.EXE (Inbox Repair Tool):\n     Usually in C:\\Program Files\\Microsoft Office\\root\\Office16\\\n   - Browse to your PST/OST file and repair\n5. Delete the Navigation Pane settings file:\n   - Win+R: outlook.exe /resetnavpane\n6. Create a new Outlook profile if all else fails\n7. Check Windows Event Viewer for specific crash details",
    },
    {
        "category": "Email",
        "problem_title": "Cannot set up email account in Outlook",
        "problem_description": "Adding a new email account in Outlook fails. Auto-discover doesn't work, or manual setup gives connection errors.",
        "problem_keywords": "email setup, add account, email configuration, outlook setup, autodiscover",
        "solution_steps": "1. For Microsoft 365 / Exchange Online:\n   - Outlook should auto-detect settings using email address\n   - If auto-discover fails, check DNS MX/CNAME records for the domain\n   - Try removing and re-adding the account\n2. For IMAP/POP manual setup, common settings:\n   - Gmail: imap.gmail.com:993/SSL, smtp.gmail.com:587/STARTTLS\n   - Outlook.com: outlook.office365.com:993/SSL, smtp-mail.outlook.com:587/STARTTLS\n   - Yahoo: imap.mail.yahoo.com:993/SSL, smtp.mail.yahoo.com:587/STARTTLS\n3. For Gmail/Yahoo, use App Password instead of regular password:\n   - Go to account security settings > App Passwords > Generate one for Outlook\n4. Check if Modern Authentication is enabled/required:\n   - Some servers require OAuth2 - use Outlook 2016 or newer\n5. Disable antivirus email scanning temporarily during setup\n6. Check firewall isn't blocking ports 993, 587, 443\n7. Try the Microsoft Support and Recovery Assistant (SaRA) tool",
    },
    {
        "category": "Email",
        "problem_title": "Outlook mailbox full - cannot send or receive",
        "problem_description": "Outlook shows 'Your mailbox is full' or 'Mailbox size limit reached'. Cannot send or receive new emails.",
        "problem_keywords": "mailbox full, storage limit, mailbox size, email full, cannot send, quota",
        "solution_steps": "1. Check mailbox size:\n   - File > Account Settings > Double-click account for Exchange\n   - Or: right-click root folder > Data File Properties > Folder Size\n2. Empty Deleted Items folder:\n   - Right-click Deleted Items > Empty Folder\n3. Empty Junk Email folder\n4. Remove large attachments:\n   - Sort mail by size: Add 'Size' column > sort descending\n   - Delete or archive emails with large attachments\n5. Archive old emails:\n   - File > Options > Advanced > AutoArchive Settings\n   - Or manually: File > Open & Export > Import/Export > Export to File\n6. For Exchange/365, check Recoverable Items:\n   - Folder > Recover Deleted Items From Server > Delete permanently\n7. If Exchange admin: increase the mailbox quota for the user\n8. Clean up other folders: Sent Items often accumulates large messages\n9. Use Outlook cleanup tool: Home > Clean Up > Clean Up Folder",
    },

    # ---- HARDWARE ----
    {
        "category": "Hardware",
        "problem_title": "External monitor not detected",
        "problem_description": "Second monitor connected via HDMI/DisplayPort/VGA shows no signal or is not detected by Windows. Only one screen works.",
        "problem_keywords": "second monitor, external monitor, no signal, monitor not detected, hdmi no display, dual monitor",
        "solution_steps": "1. Check the cable connection at both ends - reseat the cable\n2. Try a different cable (cables go bad)\n3. Try a different port on the computer and/or monitor\n4. Press Win+P and select 'Extend' or 'Duplicate'\n5. Force Windows to detect:\n   - Settings > Display > Detect\n   - Or right-click desktop > Display Settings > Detect\n6. Update display/graphics driver:\n   - Device Manager > Display Adapters > Update driver\n   - Download latest from NVIDIA/AMD/Intel website\n7. Check monitor's input source:\n   - Use monitor's buttons to select the correct input (HDMI 1, DP, etc.)\n8. For USB-C/Thunderbolt connections:\n   - Not all USB-C ports support video output\n   - Check if you need a USB-C with DisplayPort Alt Mode\n9. Try booting with only the external monitor connected\n10. For docking stations, update docking station firmware and drivers",
    },
    {
        "category": "Hardware",
        "problem_title": "USB device not recognized",
        "problem_description": "When plugging in a USB device, Windows shows 'USB Device Not Recognized' or the device doesn't appear at all.",
        "problem_keywords": "usb not recognized, usb not working, usb device, usb error, usb unknown device",
        "solution_steps": "1. Try a different USB port (preferably on the back of desktop, not through a hub)\n2. Try the device on a different computer to confirm it works\n3. Restart the computer with the device unplugged, then replug\n4. Uninstall the USB device in Device Manager:\n   - Device Manager > find the device with yellow ! > right-click > Uninstall\n   - Unplug device, wait 10 seconds, replug\n5. Update USB controller drivers:\n   - Device Manager > Universal Serial Bus controllers > Update all entries\n6. Disable USB Selective Suspend:\n   - Power Options > Change Plan Settings > Advanced > USB > Disable\n7. For USB drives not showing up:\n   - Check Disk Management (diskmgmt.msc) - drive may need a drive letter assigned\n8. If device works on USB 2.0 but not USB 3.0, update USB 3.0 controller driver\n9. Try in Safe Mode to rule out driver conflicts",
    },
    {
        "category": "Hardware",
        "problem_title": "No audio / sound not working",
        "problem_description": "Computer has no sound output. Speakers or headphones connected but nothing plays. Volume icon may show red X.",
        "problem_keywords": "no audio, no sound, sound not working, speakers, headphones, volume, audio driver",
        "solution_steps": "1. Check the obvious:\n   - Make sure volume is not muted (click speaker icon in taskbar)\n   - Check hardware volume controls on speakers/keyboard\n   - Ensure speakers/headphones are properly connected\n2. Set correct playback device:\n   - Right-click speaker icon > Sound settings > Output device\n   - Or right-click speaker icon > Sounds > Playback tab\n   - Make sure the correct device is set as Default\n3. Run audio troubleshooter:\n   - Right-click speaker icon > Troubleshoot sound problems\n4. Restart Windows Audio service:\n   - services.msc > Windows Audio > Restart\n   - Also restart: Windows Audio Endpoint Builder\n5. Update audio driver:\n   - Device Manager > Sound, video and game controllers > Update\n   - Download from laptop/motherboard manufacturer website (not generic Windows driver)\n6. Uninstall audio driver and restart (Windows will reinstall):\n   - Device Manager > Audio device > Uninstall > check 'Delete driver software' > Restart\n7. Check if audio works in Safe Mode\n8. For HDMI audio: Set HDMI as default in playback devices",
    },
    {
        "category": "Hardware",
        "problem_title": "Keyboard or mouse not working",
        "problem_description": "Keyboard or mouse stops responding. Keys don't register or mouse doesn't move the cursor. May work in BIOS but not in Windows.",
        "problem_keywords": "keyboard not working, mouse not working, keyboard frozen, mouse frozen, input device",
        "solution_steps": "1. For wired devices:\n   - Try a different USB port\n   - Try the device on another computer\n   - Check the cable for damage\n2. For wireless devices:\n   - Replace/charge batteries\n   - Check the wireless receiver is plugged in\n   - Re-pair the device: often a small button on bottom + receiver\n3. For Bluetooth:\n   - Turn Bluetooth off and on\n   - Remove the device and re-pair from Settings > Bluetooth\n4. Update/reinstall drivers:\n   - Device Manager > Keyboards or Mice > Uninstall device > Restart\n   - Windows will reinstall the driver\n5. Check USB power management:\n   - Device Manager > USB Root Hub(s) > Properties > Power Management\n   - Uncheck 'Allow computer to turn off this device'\n6. Boot into Safe Mode to test (rules out driver/software conflicts)\n7. For laptop keyboard:\n   - Check if keyboard locked by Fn key combination\n   - External keyboard may override built-in one\n8. If works in BIOS but not Windows, it's a driver issue - boot Safe Mode and update",
    },
    {
        "category": "Hardware",
        "problem_title": "Laptop battery draining fast",
        "problem_description": "Laptop battery runs out much faster than expected. Battery health may have degraded, or a process is using too much power.",
        "problem_keywords": "battery drain, battery life, fast drain, power consumption, laptop battery",
        "solution_steps": "1. Check battery health report:\n   - CMD (Admin): powercfg /batteryreport\n   - Open the generated report in C:\\Users\\<username>\\battery-report.html\n   - Compare 'Design Capacity' vs 'Full Charge Capacity'\n2. Check what's draining power:\n   - Task Manager > Processes > sort by Power usage\n   - Settings > System > Battery > See which apps affect battery life\n3. Reduce power consumption:\n   - Lower screen brightness\n   - Use Battery Saver mode: Settings > Battery > Turn on now\n   - Disable Bluetooth and Wi-Fi when not needed\n4. Change power plan:\n   - Control Panel > Power Options > choose 'Balanced' or 'Power saver'\n5. Disable background apps:\n   - Settings > Privacy > Background apps > turn off unnecessary ones\n6. Update BIOS and chipset drivers from manufacturer website\n7. Calibrate battery: Charge to 100%, use until shutdown, charge back to 100%\n8. If battery health is below 60%, consider replacement",
    },

    # ---- SOFTWARE ----
    {
        "category": "Software",
        "problem_title": "Microsoft Office activation or license error",
        "problem_description": "Office shows 'Product Activation Failed', 'Unlicensed Product', or 'Your license isn't genuine'. Features may be limited to read-only.",
        "problem_keywords": "office activation, office license, unlicensed product, office not genuine, office 365 license",
        "solution_steps": "1. Check Office activation status:\n   - Open any Office app > File > Account > check under Product Information\n2. Sign out and sign back in:\n   - File > Account > Sign Out > Sign back in with the licensed account\n3. For Microsoft 365:\n   - Go to account.microsoft.com/services > verify subscription is active\n   - Check you're not exceeding device install limits (5 PCs)\n4. Repair Office activation:\n   - CMD (Admin): Navigate to C:\\Program Files\\Microsoft Office\\Office16\n   - Run: cscript ospp.vbs /act\n5. Remove old licenses:\n   - CMD (Admin): cscript ospp.vbs /dstatus (view current licenses)\n   - cscript ospp.vbs /unpkey:<last 5 of key> (remove old key)\n6. Repair Office: Control Panel > Programs > Microsoft Office > Change > Online Repair\n7. Delete Office license files:\n   - Delete all files in: %LocalAppData%\\Microsoft\\Office\\Licenses\n   - Restart Office and sign in again\n8. Use the Microsoft Support and Recovery Assistant (SaRA) tool",
    },
    {
        "category": "Software",
        "problem_title": "Application won't install - permission or compatibility error",
        "problem_description": "Software installation fails with 'Access denied', 'Insufficient privileges', or 'Not compatible with this version of Windows'.",
        "problem_keywords": "install error, access denied, compatibility, won't install, installation failed, permission",
        "solution_steps": "1. Run installer as Administrator:\n   - Right-click the installer > Run as administrator\n2. For compatibility issues:\n   - Right-click installer > Properties > Compatibility tab\n   - Check 'Run in compatibility mode for' > select Windows 8 or 7\n3. Temporarily disable antivirus/Windows Defender during install\n4. Check Windows Installer service is running:\n   - services.msc > Windows Installer > start if stopped\n5. Clean up temp files:\n   - Delete contents of %TEMP% folder\n   - Run Disk Cleanup\n6. If MSI installer fails:\n   - CMD (Admin): msiexec /i \"path\\to\\installer.msi\" /l*v install.log\n   - Check install.log for specific error\n7. Check UAC settings:\n   - Control Panel > User Account Control Settings > lower temporarily\n8. Re-register Windows Installer:\n   - CMD (Admin): msiexec /unregister then msiexec /regserver\n9. Install in Clean Boot:\n   - msconfig > Services > Hide all Microsoft > Disable all > Restart",
    },
    {
        "category": "Software",
        "problem_title": "Browser running slow or crashing",
        "problem_description": "Chrome/Edge is slow, unresponsive, using too much memory, or crashing frequently.",
        "problem_keywords": "chrome slow, edge slow, browser crash, browser slow, too many tabs, browser memory",
        "solution_steps": "1. Close unnecessary tabs (each tab uses memory)\n2. Clear browsing data:\n   - Ctrl+Shift+Delete > Clear All time > Cookies, Cache, Browsing History\n3. Disable extensions:\n   - Go to extensions page > disable all, restart browser\n   - Re-enable one at a time to find the problematic one\n4. Reset browser to defaults:\n   - Chrome: Settings > Reset and clean up > Restore to defaults\n   - Edge: Settings > Reset settings\n5. Update the browser to latest version\n6. Check for malware:\n   - Chrome: Settings > Safety check\n   - Run Windows Defender or Malwarebytes scan\n7. If using many tabs, consider a tab manager extension\n8. Create a new browser profile:\n   - Click avatar icon > Add > new profile\n   - If new profile is fast, old profile is corrupt\n9. Check hardware acceleration:\n   - Settings > System > toggle 'Use hardware acceleration'\n10. Check RAM usage: if browser uses >4GB, you may need more total RAM",
    },

    # ---- AUTHENTICATION ----
    {
        "category": "Authentication",
        "problem_title": "Account locked out - too many attempts",
        "problem_description": "User cannot log in, account is locked due to too many failed password attempts. Gets 'Account locked' or 'Account disabled' message.",
        "problem_keywords": "account locked, locked out, too many attempts, account disabled, login failed",
        "solution_steps": "1. Wait for automatic unlock (most policies: 15-30 minutes)\n2. If Active Directory:\n   - Admin opens Active Directory Users and Computers\n   - Find user > Properties > Account tab > Uncheck 'Account is locked out'\n3. Identify what's causing lockouts:\n   - Check Event Viewer on DC: Security log, Event ID 4740 (lockout)\n   - Look at the 'Caller Computer Name' field to find the source\n4. Common causes of repeated lockouts:\n   - Old password saved in Windows Credential Manager > clear it\n   - Mapped drives using old credentials > disconnect and remap\n   - Mobile phone still syncing email with old password\n   - Scheduled tasks running under the user's account\n   - VPN or Wi-Fi profile with old password\n   - Service running under user's account with old password\n5. Use Microsoft Account Lockout Tools (LockoutStatus.exe) to trace lockout source\n6. On the user's PC: cmdkey /list to see saved credentials, cmdkey /delete to remove",
    },
    {
        "category": "Authentication",
        "problem_title": "Password expired - cannot change",
        "problem_description": "User's password has expired, but they get errors when trying to change it, or the change password prompt doesn't appear.",
        "problem_keywords": "password expired, change password, password error, expired password, cannot change password",
        "solution_steps": "1. On login screen, Windows should prompt to change password after pressing Ctrl+Alt+Del\n   - If prompt doesn't appear, try pressing Ctrl+Alt+Del first\n2. Change password via Ctrl+Alt+Delete > Change a password (when logged in)\n3. If Remote Desktop:\n   - RDP client may not show the change password dialog\n   - Use the web portal or VPN into the network first to change password\n4. Password requirements to check:\n   - Minimum length (usually 8-12 characters)\n   - Must include: uppercase, lowercase, number, special character\n   - Cannot reuse last X passwords\n   - Minimum password age (can't change within first day)\n5. If user cannot log in at all:\n   - Admin: Active Directory > Reset Password > check 'User must change password at next logon'\n6. For remote/VPN users:\n   - Reset password through web portal (if available)\n   - Use Remote Desktop Gateway with NLA disabled temporarily\n7. Check that the time/date on the client PC matches the domain controller",
    },
    {
        "category": "Authentication",
        "problem_title": "MFA / Two-Factor Authentication not working",
        "problem_description": "Multi-factor authentication codes are rejected, authenticator app not generating correct codes, or MFA prompt not appearing.",
        "problem_keywords": "MFA, two-factor, 2FA, authenticator, verification code, code rejected",
        "solution_steps": "1. Check time on your phone:\n   - Authenticator codes are time-based - phone time MUST be accurate\n   - Android: Settings > System > Date & Time > Use network-provided time\n   - iPhone: Settings > General > Date & Time > Set Automatically\n2. In Microsoft Authenticator app:\n   - Click the ⚙️ gear > Time correction for codes > Sync now\n3. If codes are rejected:\n   - Make sure you're entering the code for the correct account\n   - Enter the code quickly (they expire every 30 seconds)\n   - Check if there's a typo in the displayed code\n4. If MFA prompt not appearing:\n   - Check if push notifications are enabled for the authenticator app\n   - Try 'Use a different verification method' and choose SMS or code\n5. Contact IT admin to:\n   - Reset MFA for the user's account\n   - Re-enroll MFA from scratch\n   - Check if Conditional Access policies are blocking\n6. For SMS-based MFA: Verify phone number is correct in account settings\n7. If phone is lost: Admin can generate a temporary access pass or reset MFA",
    },
    {
        "category": "Authentication",
        "problem_title": "Cannot log into computer with domain credentials",
        "problem_description": "User enters correct domain credentials but gets 'The trust relationship between this workstation and the primary domain failed' or similar error.",
        "problem_keywords": "domain login, trust relationship, domain failed, cannot login, active directory login",
        "solution_steps": "1. If 'Trust relationship failed':\n   - Log in with a LOCAL administrator account\n   - PowerShell (Admin): Reset-ComputerMachinePassword -Server <DomainController> -Credential <DomainAdmin>\n   - Or: Remove from domain (use Workgroup), restart, rejoin domain, restart\n2. If computer account disabled in AD:\n   - Admin: Active Directory > find computer > Enable Account\n   - Rejoin domain if needed\n3. Check network connectivity to domain controller:\n   - Can you ping the DC? Can you resolve domain name?\n   - Check: nltest /sc_query:<domain>\n4. If VPN is needed to reach DC:\n   - You must VPN first before domain authentication will work\n   - Log in with cached credentials first (if available)\n5. Verify time is synced with domain:\n   - Kerberos allows max 5 minutes difference\n   - CMD: w32tm /resync\n6. Check DNS: Computer must use domain controller as DNS\n   - ipconfig /all > verify DNS points to DC\n7. Clear cached credentials:\n   - Delete profile under C:\\Users\\ and cached creds in Credential Manager",
    },

    # ---- SERVER ----
    {
        "category": "Server",
        "problem_title": "File server - users getting Access Denied",
        "problem_description": "Users suddenly cannot access files or folders on the file server. Getting 'Access Denied' when trying to open, edit, or create files.",
        "problem_keywords": "access denied, file server, permission denied, ntfs permissions, share permissions, cannot access files",
        "solution_steps": "1. Check both Share permissions AND NTFS permissions:\n   - Share permissions: Right-click shared folder > Properties > Sharing > Advanced > Permissions\n   - NTFS permissions: Security tab > check the user/group has appropriate access\n   - Both must allow access - the most restrictive one applies\n2. Check the user's group memberships:\n   - Active Directory > User Properties > Member Of\n   - Ensure they're in the correct security groups\n3. Check for inherited permission changes:\n   - Security tab > Advanced > check Inheritance is enabled\n   - Look for any Deny entries (Deny overrides Allow)\n4. If one user can access but another can't:\n   - Compare effective permissions:\n   - Security > Advanced > Effective Access > select both users\n5. After changing permissions, user may need to:\n   - Log off and log back on (group membership changes)\n   - Close and reopen File Explorer\n6. Check if the file is locked by another user:\n   - On server: Computer Management > Shared Folders > Open Files\n7. Run: gpupdate /force on both server and client to refresh policies",
    },
    {
        "category": "Server",
        "problem_title": "Server disk space low - running out of storage",
        "problem_description": "Server disk is critically low on space. Services may be failing, and users cannot save files. Need to free up space urgently.",
        "problem_keywords": "low disk space, disk full, server storage, run out of space, server full, low space",
        "solution_steps": "1. Identify what's using space:\n   - WinDirStat or TreeSize Free - visual disk space analyzer\n   - PowerShell: Get-ChildItem C:\\ -Recurse | Sort-Object Length -Descending | Select-Object -First 20 FullName, @{N='SizeMB';E={[math]::Round($_.Length/1MB)}}\n2. Quick wins to free space:\n   - Empty Recycle Bin\n   - Clear C:\\Windows\\Temp and C:\\Temp\n   - Server Manager > Disk Cleanup (cleanmgr.exe) including System files\n   - Clear Windows Update cache: net stop wuauserv, delete C:\\Windows\\SoftwareDistribution\\Download\\*\n3. Check for large log files:\n   - IIS logs: C:\\inetpub\\logs\\ (can grow huge)\n   - Application logs, database transaction logs\n4. Check for old backups taking space on the local disk\n5. Move page file to another drive if C: is critical:\n   - System Properties > Advanced > Performance > Virtual Memory\n6. Enable disk quotas on user shares to prevent future issues\n7. Consider adding storage or moving data to another disk\n8. Set up monitoring/alerts for disk space thresholds (e.g., alert at 85%)",
    },
    {
        "category": "Server",
        "problem_title": "Remote Desktop cannot connect to server",
        "problem_description": "Cannot connect to server via Remote Desktop. Connection times out or gives 'Remote Desktop can't find the computer' error.",
        "problem_keywords": "remote desktop, RDP, cannot connect, remote desktop error, RDP timeout, terminal server",
        "solution_steps": "1. Verify the server is online:\n   - Ping the server: ping <servername-or-IP>\n   - If no response, check if server is powered on\n2. Check if Remote Desktop is enabled on the server:\n   - System Properties > Remote tab > Allow remote connections\n   - Ensure user is in 'Remote Desktop Users' group\n3. Check firewall:\n   - Windows Firewall must allow incoming TCP port 3389\n   - Network firewall/VPN must also allow it\n4. Check RDP service is running:\n   - On server: services.msc > Remote Desktop Services > should be Running\n5. Check for max sessions:\n   - Server may have reached max allowed RDP sessions\n   - Use: mstsc /admin to connect with an admin session\n   - Or: query session /server:<servername> to see active sessions\n6. Clear RDP cache on client:\n   - Delete: %LocalAppData%\\Microsoft\\Terminal Server Client\\Cache\n7. Check if Network Level Authentication (NLA) is causing issues:\n   - Try disabling NLA on the server temporarily\n8. For 'CredSSP encryption oracle' error:\n   - Update both client and server with latest Windows updates\n   - Or temporarily: gpedit.msc > Computer Config > Admin Templates > System > Credentials Delegation > Encryption Oracle Remediation > set to Vulnerable",
    },
]


# =====================================================
# DIAGNOSTIC TREES - Step-by-step troubleshooting flows
# =====================================================
# Format: Each tree is a dict with "root" and "children" (recursive)
# node_type: "question" = has follow-up children, "option" = clickable choice, "solution" = leaf with fix

DIAGNOSTIC_TREES = [
    # ---- PRINTER DIAGNOSTIC TREE ----
    {
        "category": "Printer",
        "root": {
            "title": "Printer Troubleshooting",
            "node_type": "question",
            "question_text": "What printer issue are you experiencing?",
            "children": [
                {
                    "title": "Printer not printing at all",
                    "node_type": "question",
                    "question_text": "How is the printer connected?",
                    "children": [
                        {
                            "title": "USB Cable",
                            "node_type": "question",
                            "question_text": "What do you see in Windows printer status?",
                            "children": [
                                {
                                    "title": "Printer shows Offline",
                                    "node_type": "solution",
                                    "solution_text": "1. Unplug the USB cable from both ends, wait 10 seconds, reconnect\n2. Open Settings > Devices > Printers & Scanners\n3. Click the printer > Open print queue > Printer menu > Uncheck 'Use Printer Offline'\n4. If still offline:\n   - Open services.msc > Restart 'Print Spooler'\n   - Try a different USB port\n   - Try a different USB cable\n5. If none of the above works, uninstall the printer:\n   - Settings > Printers > Remove device\n   - Download latest driver from manufacturer website\n   - Reinstall printer"
                                },
                                {
                                    "title": "Printer shows Ready but jobs stuck in queue",
                                    "node_type": "solution",
                                    "solution_text": "1. Cancel all pending print jobs in the queue\n2. Clear the print spooler:\n   - Open CMD as Admin\n   - Run: net stop spooler\n   - Delete all files in: C:\\Windows\\System32\\spool\\PRINTERS\\\n   - Run: net start spooler\n3. Try printing a test page:\n   - Right-click printer > Printer Properties > Print Test Page\n4. If test page fails, reinstall the printer driver from manufacturer website\n5. If test page works but documents don't print, the issue is with the application"
                                },
                                {
                                    "title": "Printer not showing in Windows at all",
                                    "node_type": "solution",
                                    "solution_text": "1. Check if the printer is powered on and the USB cable is securely connected\n2. Try a different USB port (preferably directly on the PC, not through a hub)\n3. Open Device Manager > check under 'Other devices' or 'Printers' for unknown device\n4. If yellow exclamation mark, right-click > Update driver\n5. Download and install the full driver package from the printer manufacturer website\n6. If Device Manager shows nothing when you plug in, try:\n   - Different USB cable\n   - Different computer (to verify printer USB port works)\n   - Check printer for any error lights or messages on display"
                                }
                            ]
                        },
                        {
                            "title": "Wi-Fi / Wireless",
                            "node_type": "question",
                            "question_text": "Can you print the printer's network configuration page? (Usually from printer menu > Settings > Network > Print Config)",
                            "children": [
                                {
                                    "title": "Yes - I have the printer's IP address",
                                    "node_type": "solution",
                                    "solution_text": "1. Verify the printer is on the same network as your computer\n   - Compare the first 3 octets of IP (e.g., 192.168.1.x)\n2. Ping the printer: CMD > ping <printer-IP>\n3. If ping fails:\n   - Printer may have changed IP. Reconnect printer to Wi-Fi\n   - Set a static/reserved IP for the printer in your router\n4. If ping works but can't print:\n   - Remove the printer from Windows\n   - Re-add using IP: Settings > Add printer > 'The printer I want isn't listed'\n   - Select 'Add using TCP/IP' > enter the printer's IP address\n   - Install the correct driver when prompted\n5. Ensure the print spooler is running: services.msc > Print Spooler > Start"
                                },
                                {
                                    "title": "No - printer can't connect to Wi-Fi",
                                    "node_type": "solution",
                                    "solution_text": "1. Restart both the printer and your Wi-Fi router\n2. On the printer's display/control panel:\n   - Go to Network/Wi-Fi settings\n   - Run the Wireless Setup Wizard\n   - Select your Wi-Fi network and enter the password\n3. If the printer doesn't find your network:\n   - Move the printer closer to the router\n   - Check if your router is broadcasting on 2.4GHz (many printers don't support 5GHz)\n4. For WPS setup:\n   - Press WPS button on router, then start WPS on printer within 2 minutes\n5. If Wi-Fi continues to fail:\n   - Connect printer directly via USB, then use manufacturer's software to configure Wi-Fi\n   - As fallback, use USB connection permanently\n6. Consider setting a static IP once connected to prevent future disconnections"
                                }
                            ]
                        },
                        {
                            "title": "Network / Ethernet cable",
                            "node_type": "solution",
                            "solution_text": "1. Check the Ethernet cable is plugged into both the printer and the network switch/router\n2. Check for link light on the printer's Ethernet port (should be solid or blinking)\n3. Print a network config page from the printer to find its IP address\n4. Ping the printer IP from your computer\n5. If unreachable:\n   - Try a different Ethernet cable\n   - Try a different port on the switch\n   - Check if the printer has a valid IP (not 0.0.0.0 or 169.254.x.x)\n   - Configure the printer's network settings to use DHCP or set a valid static IP\n6. If reachable but not printing:\n   - Remove and re-add the printer using its TCP/IP address\n   - Restart Print Spooler service\n   - Update the printer driver from manufacturer website"
                        },
                        {
                            "title": "Shared from another PC",
                            "node_type": "solution",
                            "solution_text": "1. Verify the host PC (sharing the printer) is powered on and connected to the network\n2. On the host PC, verify printer is shared:\n   - Printer Properties > Sharing tab > 'Share this printer' should be checked\n3. Check share permissions allow your user or 'Everyone'\n4. On your PC, check network connectivity: ping the host PC name/IP\n5. If you get error 0x0000011b:\n   - On the HOST PC registry: HKLM\\SYSTEM\\CurrentControlSet\\Control\\Print\n   - Create DWORD: RpcAuthnLevelPrivacyEnabled = 0\n   - Restart Print Spooler on both PCs\n6. Try adding by IP: \\\\<host-IP>\\<shared-printer-name>\n7. If credentials requested, use: host-PC-name\\username and their password"
                        }
                    ]
                },
                {
                    "title": "Printer prints blank pages",
                    "node_type": "question",
                    "question_text": "What type of printer is it?",
                    "children": [
                        {
                            "title": "Inkjet printer",
                            "node_type": "solution",
                            "solution_text": "1. Check ink levels: Open printer software or printer's display\n2. Replace any empty cartridges\n3. Run head cleaning:\n   - From printer properties > Maintenance tab, or\n   - From printer's built-in menu > Maintenance > Head Cleaning\n   - Run 2-3 times if first attempt doesn't fix it\n4. Print a nozzle check pattern to see which colors are blocked\n5. If cartridges are new:\n   - Ensure protective tape/film was fully removed\n   - Make sure cartridges are clicked in firmly\n6. If printer sat unused for weeks, ink may have dried:\n   - Run deep cleaning cycle (uses more ink but more thorough)\n   - In extreme cases, remove cartridges and gently clean print head contacts with distilled water"
                        },
                        {
                            "title": "Laser printer",
                            "node_type": "solution",
                            "solution_text": "1. Remove the toner cartridge\n2. Gently shake it side to side 5-6 times (redistributes toner)\n3. If new toner: Make sure you removed the orange/yellow sealing tape\n4. Check the drum unit:\n   - Look for scratches, marks, or damage on the green drum\n   - Clean gently with a dry lint-free cloth only\n   - Replace drum if damaged\n5. Check if the correct paper type is selected in print settings\n6. Print a test page from the printer itself (not from Windows)\n   - If printer's own test page is blank: Hardware issue\n   - If printer's test page works but Windows prints blank: Driver issue\n7. Reinstall printer driver from manufacturer website"
                        }
                    ]
                },
                {
                    "title": "Print quality is poor",
                    "node_type": "question",
                    "question_text": "What quality issue do you see?",
                    "children": [
                        {
                            "title": "Lines, streaks, or smudges",
                            "node_type": "solution",
                            "solution_text": "1. For inkjet:\n   - Run print head alignment from printer maintenance menu\n   - Run head cleaning 2-3 times\n   - Check for damaged or leaking cartridges\n2. For laser:\n   - The drum unit may be damaged - inspect for marks\n   - The fuser may be contaminated - clean or replace\n   - Remove toner cartridge and check for spilled toner\n3. For both types:\n   - Clean the paper feed rollers with a damp lint-free cloth\n   - Use correct paper type and quality (not too thin/thick/damp)\n   - Check print quality is set to 'Normal' or 'Best', not 'Draft'\n4. Try printing a test page and a photo - compare quality"
                        },
                        {
                            "title": "Text is blurry or faded",
                            "node_type": "solution",
                            "solution_text": "1. Check ink/toner levels - replace if low\n2. Change print quality setting from 'Draft' to 'Normal' or 'Best'\n3. For laser: Shake toner cartridge to redistribute remaining toner\n4. Run alignment: Printer Maintenance > Align Print Heads\n5. Check that the paper type setting matches the actual paper\n6. Ensure you're using the correct driver (not generic/universal)\n7. Download and install the latest driver from manufacturer website\n8. Try printing from a different application to rule out software issue"
                        },
                        {
                            "title": "Colors are wrong or missing",
                            "node_type": "solution",
                            "solution_text": "1. Run a nozzle/color check from printer maintenance\n2. Check each individual ink/toner cartridge level\n3. Replace the empty or nearly-empty color cartridge\n4. Run head cleaning cycle (for inkjet)\n5. Check print settings:\n   - Make sure 'Grayscale' or 'Black & White' is not selected\n   - Ensure correct color profile is selected\n6. From printer properties > Color Management > check settings\n7. Try printing a different document with known colors to compare"
                        }
                    ]
                },
                {
                    "title": "Paper jam issues",
                    "node_type": "solution",
                    "solution_text": "1. Turn off the printer and unplug it\n2. Open all available doors, trays, and panels\n3. Carefully remove any visible paper - pull in the direction of paper path (avoid tearing)\n4. Check these common locations:\n   - Paper input tray (remove tray completely)\n   - Under the toner/ink cartridge\n   - Rear access door / duplexer unit\n   - Output tray area\n5. Look for tiny paper scraps with a flashlight\n6. Clean the pickup rollers with a slightly damp cloth\n7. Prevent future jams:\n   - Fan the paper before loading\n   - Don't overfill the tray\n   - Use the correct paper weight\n   - Adjust paper guides snugly\n   - Store paper in a dry place (damp paper jams easily)"
                }
            ]
        }
    },

    # ---- NETWORK DIAGNOSTIC TREE ----
    {
        "category": "Network",
        "root": {
            "title": "Network Troubleshooting",
            "node_type": "question",
            "question_text": "What network issue are you experiencing?",
            "children": [
                {
                    "title": "No internet access at all",
                    "node_type": "question",
                    "question_text": "Is this affecting only one computer or all devices on the network?",
                    "children": [
                        {
                            "title": "Only this one computer",
                            "node_type": "question",
                            "question_text": "How is this computer connected?",
                            "children": [
                                {
                                    "title": "Wi-Fi",
                                    "node_type": "solution",
                                    "solution_text": "1. Turn Wi-Fi off and on from taskbar\n2. Forget the network and reconnect:\n   - Settings > Network > Wi-Fi > Manage known networks\n   - Forget > Reconnect with password\n3. Reset network adapter:\n   - CMD (Admin):\n   - ipconfig /release\n   - ipconfig /flushdns\n   - ipconfig /renew\n   - netsh winsock reset\n4. Restart the computer\n5. Check if you're getting a valid IP:\n   - CMD: ipconfig\n   - If IP starts with 169.254: DHCP not working, restart router\n6. Disable and re-enable the adapter:\n   - Device Manager > Network Adapters > Wi-Fi > Disable > Enable\n7. Update Wi-Fi driver from manufacturer website\n8. Check if airplane mode is accidentally on"
                                },
                                {
                                    "title": "Ethernet cable",
                                    "node_type": "solution",
                                    "solution_text": "1. Check cable connection - unplug and reconnect at both ends\n2. Look for link light on the network port (should be lit/blinking)\n3. Try a different Ethernet cable\n4. Try a different port on the switch/router\n5. CMD (Admin):\n   - ipconfig /release\n   - ipconfig /flushdns\n   - ipconfig /renew\n   - netsh winsock reset\n6. Check adapter is enabled:\n   - Device Manager > Network Adapters\n   - Ensure Ethernet adapter isn't disabled or showing error\n7. Check IP configuration:\n   - CMD: ipconfig\n   - Compare settings to a working computer\n   - If static IP, verify it's correct and not conflicting\n8. Restart the computer\n9. Test the port by plugging a known-working device into it"
                                }
                            ]
                        },
                        {
                            "title": "All devices on the network",
                            "node_type": "solution",
                            "solution_text": "1. Restart router/modem:\n   - Unplug power from the modem AND router\n   - Wait 30 seconds\n   - Plug in modem first, wait for all lights to stabilize\n   - Then plug in router, wait for it to boot\n2. Check status lights on modem:\n   - 'Internet' or 'Online' light should be solid green\n   - If blinking or red: ISP issue\n3. Check if the ISP has an outage:\n   - Check ISP website or social media on your phone (mobile data)\n   - Call ISP support number\n4. If using a separate modem and router:\n   - Connect a computer directly to modem (bypassing router)\n   - If internet works: Router is the problem\n   - If no internet: Modem or ISP issue\n5. Factory reset the router as last resort (you'll need to reconfigure it)\n6. Check if the ISP bill is paid and account is active"
                        }
                    ]
                },
                {
                    "title": "Internet is slow",
                    "node_type": "question",
                    "question_text": "Is the slow speed on Wi-Fi, Ethernet, or both?",
                    "children": [
                        {
                            "title": "Only slow on Wi-Fi",
                            "node_type": "solution",
                            "solution_text": "1. Move closer to the Wi-Fi router for a test\n2. Check Wi-Fi signal strength (bars icon in taskbar)\n3. Switch to 5GHz band if available (faster but shorter range)\n4. Check for interference:\n   - Microwaves, Bluetooth, other routers, cordless phones\n   - Move router away from these\n5. Change Wi-Fi channel on router:\n   - Login to router admin (192.168.1.1 or similar)\n   - Change to a less congested channel (use WiFi Analyzer app to find best one)\n6. Update Wi-Fi driver\n7. Disable power saving on Wi-Fi adapter:\n   - Device Manager > Wi-Fi adapter > Power Management > uncheck power saving\n8. Check how many devices are connected to Wi-Fi (too many = slow)\n9. Consider Wi-Fi extender or mesh system for large buildings"
                        },
                        {
                            "title": "Slow on both Wi-Fi and Ethernet",
                            "node_type": "solution",
                            "solution_text": "1. Run speed test: speedtest.net\n   - Compare result to your ISP plan\n2. Restart modem and router\n3. Check for bandwidth hogs:\n   - Is someone streaming, downloading, or video conferencing?\n   - Check router admin page for connected devices and bandwidth usage\n4. Check for malware:\n   - Run full antivirus scan\n   - Check Task Manager for suspicious high network usage\n5. Enable QoS (Quality of Service) on your router:\n   - Prioritize business applications over streaming\n6. If speed test shows correct speed but browsing is slow:\n   - Change DNS to 8.8.8.8 / 1.1.1.1\n   - Clear browser cache\n7. If speed is consistently below plan, contact ISP\n   - Have speed test results ready\n   - Ask about congestion or line issues"
                        }
                    ]
                },
                {
                    "title": "Cannot connect to network share / mapped drive",
                    "node_type": "question",
                    "question_text": "What error do you see when trying to access the share?",
                    "children": [
                        {
                            "title": "Access Denied / Permission error",
                            "node_type": "solution",
                            "solution_text": "1. Check your credentials:\n   - Open Credential Manager: Control Panel > Credential Manager\n   - Under 'Windows Credentials', remove old entries for the server\n   - Try accessing the share again - enter current username/password when prompted\n2. Verify you have permission:\n   - Ask IT admin to check both Share and NTFS permissions for your user/group\n3. Log off and log back on (picks up new group memberships)\n4. If using different domain accounts:\n   - CMD: net use \\\\server\\share /user:DOMAIN\\username\n5. Check that your PC is on the domain (for domain-joined environments)"
                        },
                        {
                            "title": "Network path not found",
                            "node_type": "solution",
                            "solution_text": "1. Verify the server is online: ping <servername>\n2. Try accessing by IP instead of name: \\\\192.168.x.x\\share\n   - If IP works but name doesn't: DNS issue\n   - Flush DNS: ipconfig /flushdns\n3. Check that SMB is enabled:\n   - Control Panel > Turn Windows features on/off\n   - Enable 'SMB 1.0/CIFS File Sharing Support' if the server requires it\n4. Check network services:\n   - services.msc > ensure 'TCP/IP NetBIOS Helper' and 'Workstation' are running\n5. Check firewall:\n   - Enable File and Printer Sharing in Windows Firewall\n6. Verify you're on the correct network (not guest Wi-Fi or VPN disconnected)"
                        },
                        {
                            "title": "The specified network name is no longer available",
                            "node_type": "solution",
                            "solution_text": "1. This often means the connection to the server dropped\n2. Remove and re-map the drive:\n   - CMD: net use Z: /delete\n   - CMD: net use Z: \\\\server\\share /persistent:yes\n3. Check network cable if wired (may be loose)\n4. Check server uptime - it may have rebooted\n5. Increase timeout settings:\n   - Registry: HKLM\\SYSTEM\\CurrentControlSet\\Services\\LanmanWorkstation\\Parameters\n   - SessTimeout (DWORD) = 60\n6. Update network adapter driver\n7. Disable SMB signing temporarily to test:\n   - Group Policy: Digital signing > Disabled"
                        }
                    ]
                },
                {
                    "title": "Wi-Fi keeps disconnecting",
                    "node_type": "solution",
                    "solution_text": "1. Disable Wi-Fi power management:\n   - Device Manager > Wi-Fi adapter > Properties > Power Management\n   - Uncheck 'Allow the computer to turn off this device to save power'\n2. Set Roaming Aggressiveness to Lowest:\n   - Device Manager > Wi-Fi adapter > Advanced > Roaming Aggressiveness\n3. Forget and reconnect to the Wi-Fi network\n4. Update Wi-Fi driver from manufacturer website (not generic Windows Update driver)\n5. Check for interference and switch to 5GHz band\n6. Disable Wi-Fi Sense: Settings > Network > Wi-Fi > manage known networks\n7. If laptop: Check if closing the lid or moving triggers disconnect\n   - This is usually the power management setting from step 1\n8. Reset network stack: netsh winsock reset && netsh int ip reset\n9. Last resort: Settings > Network > Network reset"
                }
            ]
        }
    },

    # ---- EMAIL DIAGNOSTIC TREE ----
    {
        "category": "Email",
        "root": {
            "title": "Email Troubleshooting",
            "node_type": "question",
            "question_text": "What email problem are you experiencing?",
            "children": [
                {
                    "title": "Cannot send emails",
                    "node_type": "question",
                    "question_text": "What happens when you try to send?",
                    "children": [
                        {
                            "title": "Email stuck in Outbox",
                            "node_type": "solution",
                            "solution_text": "1. Check if Outlook is in Offline mode:\n   - Send/Receive tab > 'Work Offline' should NOT be highlighted\n2. Check internet connection\n3. Try to move the email from Outbox to Drafts, then resend\n4. If stuck email can't be moved:\n   - Close Outlook completely\n   - Open Outbox in Outlook Web Access and delete the stuck email\n   - Or find the email file in your OST/PST and delete\n5. Check if attachment is too large:\n   - Most email servers limit attachments to 10-25MB\n   - Use OneDrive/SharePoint to share large files instead\n6. Restart Outlook in Safe Mode: outlook.exe /safe\n7. Rebuild OST file:\n   - Account Settings > Data Files > select account > Open File Location\n   - Rename .ost file > restart Outlook (it will rebuild)"
                        },
                        {
                            "title": "Getting a bounce-back error",
                            "node_type": "solution",
                            "solution_text": "1. Read the bounce message carefully - it contains the specific error\n2. Common bounce errors:\n   - '550 Relay denied': Your server isn't authorized to send to that domain. Check SMTP settings\n   - '552 Message size exceeds': Attachment too large. Reduce size or use a file sharing link\n   - '550 User unknown': The recipient email address doesn't exist. Check for typos\n   - '421 Too many connections': Server temporarily overloaded. Wait and retry\n   - '550 SPF/DKIM failure': Email authentication issue - IT admin needs to check DNS records\n3. If bouncing to one specific address: Ask recipient to check their spam/quarantine\n4. If bouncing to all addresses: SMTP configuration issue - contact IT admin"
                        },
                        {
                            "title": "Send button does nothing / no error",
                            "node_type": "solution",
                            "solution_text": "1. Check if Outlook is connected (bottom status bar should show 'Connected')\n2. Press F9 or click Send/Receive All Folders\n3. Restart Outlook\n4. Check Send/Receive settings:\n   - Send/Receive > Send/Receive Groups > Define Groups\n   - Make sure 'Send mail items' is checked\n5. Disable Outlook add-ins:\n   - File > Options > Add-ins > Manage COM Add-ins > disable all\n   - Restart and test\n6. Repair Outlook profile:\n   - File > Account Settings > select account > Repair\n7. Try sending from Outlook Web Access to verify it's not an Outlook client issue"
                        }
                    ]
                },
                {
                    "title": "Not receiving emails",
                    "node_type": "question",
                    "question_text": "Are you not receiving from everyone, or from specific senders?",
                    "children": [
                        {
                            "title": "Not receiving from anyone",
                            "node_type": "solution",
                            "solution_text": "1. Check if Outlook is online (not in Work Offline mode)\n2. Send yourself a test email from your phone or webmail\n3. Check webmail/OWA - are emails there but not in Outlook?\n   - If yes: Outlook sync issue. Rebuild OST file or repair profile\n4. Check Focused vs Other inbox (Outlook may have sorted your mail)\n5. Check Junk/Spam folder\n6. Verify mailbox isn't full: File > Account Settings > space used\n7. Check inbox rules: Home > Rules > Manage Rules\n   - A rule might be moving or deleting incoming mail\n8. For Exchange: Check quarantine portal for held messages\n9. Ask IT admin to check mail flow (may be blocked at server/filter level)"
                        },
                        {
                            "title": "Not receiving from specific senders",
                            "node_type": "solution",
                            "solution_text": "1. Check Junk/Spam folder - the sender's messages may be filtered there\n2. Check Block list:\n   - Home > Junk > Junk Email Options > Blocked Senders\n   - Remove the sender if listed\n3. Add sender to Safe Senders list:\n   - Junk Email Options > Safe Senders > Add\n4. Check inbox rules for any that might filter this sender\n5. Ask the sender to check their sent/outbox for bounce messages\n6. Check with IT admin:\n   - The sender's domain may be blocked at the email gateway\n   - Check spam filter quarantine for held messages\n   - Verify SPF/DKIM/DMARC records for sender's domain\n7. Ask sender to email your personal email as a test (isolates corporate filter)"
                        }
                    ]
                },
                {
                    "title": "Outlook is very slow",
                    "node_type": "solution",
                    "solution_text": "1. Check mailbox size: File > Account Settings > Data Files\n   - If OST/PST is over 5GB, archive old emails\n2. Compact the data file:\n   - File > Account Settings > Data Files > Settings > Compact Now\n3. Disable add-ins:\n   - File > Options > Add-ins > Manage COM Add-ins\n   - Disable all, restart, re-enable one at a time\n4. Disable hardware acceleration:\n   - File > Options > Advanced > Display > check 'Disable hardware graphics acceleration'\n5. Reduce Outlook cache:\n   - File > Account Settings > select account > Change > Use Cached Exchange Mode\n   - Change slider to '3 months' instead of 'All'\n6. Delete old/large Suggested Contacts\n7. Run Outlook in Safe Mode to test: outlook.exe /safe\n8. Repair Office: Control Panel > Programs > Office > Change > Quick Repair\n9. Ensure Windows and Office are up to date"
                }
            ]
        }
    },

    # ---- WINDOWS DIAGNOSTIC TREE ----
    {
        "category": "Windows",
        "root": {
            "title": "Windows Troubleshooting",
            "node_type": "question",
            "question_text": "What Windows issue are you experiencing?",
            "children": [
                {
                    "title": "Blue Screen of Death (BSOD)",
                    "node_type": "question",
                    "question_text": "When does the blue screen occur?",
                    "children": [
                        {
                            "title": "During startup / boot",
                            "node_type": "solution",
                            "solution_text": "1. Force power off 3 times during boot to enter Windows Recovery Environment (WinRE)\n2. Try Startup Repair:\n   - Troubleshoot > Advanced Options > Startup Repair\n3. Boot into Safe Mode:\n   - Troubleshoot > Advanced > Startup Settings > Enable Safe Mode\n   - In Safe Mode, uninstall recently installed software/drivers\n4. Use System Restore:\n   - Troubleshoot > Advanced > System Restore\n   - Choose a restore point before the issue started\n5. Repair system files:\n   - From WinRE Command Prompt:\n   - sfc /scannow /offbootdir=C:\\ /offwindir=C:\\Windows\n   - chkdsk C: /f /r\n6. Check disk health from Command Prompt:\n   - wmic diskdrive get status\n   - If Status is not 'OK', the drive may be failing\n7. Rebuild boot records:\n   - bootrec /scanos\n   - bootrec /fixmbr\n   - bootrec /fixboot\n   - bootrec /rebuildbcd"
                        },
                        {
                            "title": "Randomly during use",
                            "node_type": "solution",
                            "solution_text": "1. Note the stop code shown on the blue screen (e.g., IRQL_NOT_LESS_OR_EQUAL)\n2. Check for driver issues:\n   - Update all drivers (especially graphics, network, chipset)\n   - Use manufacturer website, not random driver update tools\n3. Check for overheating:\n   - Clean dust from fans and vents\n   - Monitor CPU temperature (use HWiNFO64 or Core Temp)\n   - 80°C+ under load = cooling problem\n4. Test RAM:\n   - Run: mdsched.exe (Windows Memory Diagnostic)\n5. Test disk: chkdsk C: /f /r\n6. Check Event Viewer:\n   - System log > filter by Critical and Error events\n   - Look for the source of the crash\n7. Update BIOS from manufacturer website\n8. Run SFC and DISM repair:\n   - sfc /scannow\n   - DISM /Online /Cleanup-Image /RestoreHealth"
                        },
                        {
                            "title": "After a Windows Update",
                            "node_type": "solution",
                            "solution_text": "1. Boot into Safe Mode:\n   - Force power off 3x > Troubleshoot > Advanced > Startup Settings > Safe Mode\n2. Uninstall the recent update:\n   - Settings > Update & Security > View update history > Uninstall updates\n   - Or from WinRE: Advanced > Uninstall Updates\n3. If you can't uninstall:\n   - Use System Restore to a point before the update\n4. Temporarily pause updates:\n   - Settings > Windows Update > Pause updates for 7 days\n5. Report the issue to Microsoft via Feedback Hub\n6. Check if a newer update fixes the issue\n7. If driver-related BSOD after update:\n   - The update may have replaced a working driver with a broken one\n   - In Safe Mode: Device Manager > roll back the affected driver"
                        }
                    ]
                },
                {
                    "title": "Computer won't boot / start",
                    "node_type": "question",
                    "question_text": "What do you see when you press the power button?",
                    "children": [
                        {
                            "title": "Nothing happens - no lights, no sound",
                            "node_type": "solution",
                            "solution_text": "1. Check power connections:\n   - Is the power cable plugged in? Try a different outlet\n   - For laptop: Is the adapter plugged in and showing a charge light?\n   - For desktop: Is the power supply switch ON (I = ON, O = OFF)?\n2. Test the outlet with another device (e.g., phone charger)\n3. For laptop:\n   - Remove battery (if removable), hold power button 30 seconds\n   - Plug in AC adapter without battery and try to start\n   - Try a different charger if available\n4. For desktop:\n   - Check all internal power connections (if comfortable opening)\n   - Listen for any fans or clicks when pressing power\n   - Unplug all USB devices and try again\n5. If motherboard has LED indicator, check its status\n6. This is likely a hardware failure - power supply, motherboard, or battery"
                        },
                        {
                            "title": "Lights/fans come on but no display",
                            "node_type": "solution",
                            "solution_text": "1. Check monitor:\n   - Is it turned on? Check the power light\n   - Is the right input selected (HDMI, DP, etc.)?\n   - Try a different cable\n2. Listen for any beep codes (beeping patterns = diagnostic codes)\n3. Try with only one RAM stick at a time (test each slot)\n4. Reset CMOS/BIOS:\n   - Unplug PC, remove CMOS battery for 30 seconds, replace, try again\n5. Remove all USB devices, extra drives, and peripherals\n6. For laptop: Connect an external monitor to test\n   - If external works: Screen or screen cable may be broken\n7. For desktop with discrete GPU:\n   - Try connecting monitor to motherboard video port (integrated graphics)\n   - Reseat the graphics card\n8. If you hear fans spin then PC shuts off quickly: Possible CPU or RAM issue"
                        },
                        {
                            "title": "Shows error message on screen",
                            "node_type": "solution",
                            "solution_text": "1. Note the exact error message\n2. 'Operating System Not Found' / 'No Boot Device':\n   - Check boot order in BIOS (press F2/F12/DEL during startup)\n   - Ensure the hard drive is listed\n   - If not listed: Drive may be disconnected or failed\n   - Reconnect SATA/power cables to the drive\n3. 'BOOTMGR is missing':\n   - Boot from Windows USB > Repair > Command Prompt\n   - Run: bootrec /fixmbr && bootrec /fixboot && bootrec /rebuildbcd\n4. 'Your PC ran into a problem' (blue screen loop):\n   - Enter WinRE > System Restore or Startup Repair\n5. 'Preparing Automatic Repair' loop:\n   - WinRE > Command Prompt > sfc /scannow /offbootdir=C:\\ /offwindir=C:\\Windows\n6. BIOS/UEFI screen only:\n   - Check boot device priority\n   - Disable Secure Boot if needed for older OS"
                        }
                    ]
                },
                {
                    "title": "Computer is very slow",
                    "node_type": "question",
                    "question_text": "When did the slowness start?",
                    "children": [
                        {
                            "title": "Always been slow / getting gradually worse",
                            "node_type": "solution",
                            "solution_text": "1. Open Task Manager (Ctrl+Shift+Esc)\n2. If Disk is at 100%:\n   - #1 fix: Upgrade to SSD if using a spinning hard drive (HDD)\n   - Disable SysMain: services.msc > SysMain > Disabled\n   - Disable Windows Search indexer temporarily\n3. Reduce startup programs:\n   - Task Manager > Startup > disable unnecessary programs\n4. Check RAM usage:\n   - If consistently >80%, need more RAM or fewer programs running\n   - 4GB is minimum, 8GB recommended, 16GB for heavy use\n5. Clean up disk: Disk Cleanup > Clean up system files\n6. Uninstall unused programs\n7. Run malware scan (Windows Defender + Malwarebytes free)\n8. Disable visual effects:\n   - System Properties > Advanced > Performance > Adjust for best performance\n9. Check temperature: Overheating causes throttling and slowness\n10. Consider reinstalling Windows for a fresh start if the PC is very old"
                        },
                        {
                            "title": "Suddenly became slow recently",
                            "node_type": "solution",
                            "solution_text": "1. Check Task Manager for high CPU/Memory/Disk process:\n   - Is a specific program using all resources? End it or investigate\n2. Check for recently installed software or updates\n   - Uninstall anything installed around when slowness started\n3. Run malware scan immediately:\n   - Windows Defender full scan\n   - Download and run Malwarebytes free scan\n4. Check for crypto-mining malware (high CPU usage from unknown processes)\n5. Check for disk errors:\n   - CMD: chkdsk C: /f (requires reboot)\n   - Check SMART: wmic diskdrive get status\n6. Check for Windows Updates downloading in background\n7. Run sfc /scannow to repair system files\n8. Use System Restore to go back to before the slowness started\n9. Check if antivirus is running a full scan in the background"
                        }
                    ]
                }
            ]
        }
    },

    # ---- AUTHENTICATION DIAGNOSTIC TREE ----
    {
        "category": "Authentication",
        "root": {
            "title": "Login & Authentication Troubleshooting",
            "node_type": "question",
            "question_text": "What authentication issue are you having?",
            "children": [
                {
                    "title": "Account is locked out",
                    "node_type": "question",
                    "question_text": "Is this a domain (work) account or a personal Microsoft/local account?",
                    "children": [
                        {
                            "title": "Domain / Work account",
                            "node_type": "solution",
                            "solution_text": "1. Wait 15-30 minutes (most lockout policies auto-unlock)\n2. Contact IT admin to unlock immediately:\n   - Active Directory Users and Computers > Find user\n   - Properties > Account tab > Uncheck 'Account is locked out'\n3. Change password from another device:\n   - Log into webmail or company portal from your phone\n   - Change your password there\n4. Find what's causing repeated lockouts:\n   - Old password saved in Credential Manager > delete it\n   - Phone email app with old password > update it\n   - Mapped drives using old credentials > remap\n   - Scheduled tasks or services running under your account\n5. On your PC: cmdkey /list to see all saved credentials\n   - cmdkey /delete:<target> to remove old ones"
                        },
                        {
                            "title": "Personal / Microsoft account",
                            "node_type": "solution",
                            "solution_text": "1. Go to account.live.com/password/reset from another device\n2. Verify your identity using:\n   - Backup email\n   - Phone number\n   - Authenticator app\n3. If you can't verify:\n   - Use the account recovery form: account.live.com/acsr\n4. For local Windows account lockout:\n   - If you have another admin account, log in and unlock\n   - Use Repair disk: WinRE > Command Prompt:\n     net user <username> <newpassword>\n5. Enable PIN or Windows Hello as a backup sign-in method\n6. After unlocking, change your password immediately"
                        }
                    ]
                },
                {
                    "title": "Password expired or needs changing",
                    "node_type": "solution",
                    "solution_text": "1. At the Windows login screen:\n   - Press Ctrl+Alt+Del if prompted\n   - The 'Change Password' option should appear after entering old password\n2. If Remote Desktop doesn't show change dialog:\n   - Connect to VPN first, then use webmail or company portal to change\n   - Or use Remote Desktop Web Access if available\n3. Password requirements (typical domain policy):\n   - Minimum 8-12 characters\n   - At least 1 uppercase, 1 lowercase, 1 number, 1 special character\n   - Cannot reuse last 5-12 passwords\n   - Cannot contain your username\n4. After changing:\n   - Update password on your phone (email app, Wi-Fi if using enterprise Wi-Fi)\n   - Update any saved credentials in Windows Credential Manager\n   - Reconnect mapped drives with new password\n5. If you get 'password does not meet complexity requirements':\n   - Try a longer password with mixed characters\n   - Some policies require minimum age (can't change within first day)"
                },
                {
                    "title": "MFA / Two-Factor not working",
                    "node_type": "question",
                    "question_text": "What type of MFA are you using?",
                    "children": [
                        {
                            "title": "Authenticator app (Microsoft/Google)",
                            "node_type": "solution",
                            "solution_text": "1. Check your phone's time is automatic:\n   - Authenticator codes are time-based (TOTP)\n   - If your phone clock is off by even 30 seconds, codes will fail\n   - Settings > Date & Time > Set Automatically\n2. In Microsoft Authenticator: Settings > Time correction for codes > Sync now\n3. Make sure you're using the code for the correct account:\n   - You may have multiple accounts in the app\n4. Try the Refresh button in the authenticator app\n5. If push notification not arriving:\n   - Check internet connection on phone\n   - Check notification permissions for the authenticator app\n   - Force close and reopen the app\n6. If nothing works:\n   - Click 'I can't use my authenticator app' during login\n   - Use backup method (SMS, email, backup codes)\n7. Contact IT admin to reset your MFA enrollment so you can re-register"
                        },
                        {
                            "title": "SMS text message code",
                            "node_type": "solution",
                            "solution_text": "1. Check phone signal - SMS needs cellular service (Wi-Fi calling may not receive SMS codes)\n2. Wait 1-2 minutes - codes can be delayed\n3. Click 'Resend code' if available\n4. Verify the phone number on file is correct:\n   - Log into account security settings from another method\n   - Check last 4 digits of the number match your phone\n5. Check if your phone's SMS inbox is full\n6. Try calling option instead of SMS if available\n7. Some carriers block short-code SMS:\n   - Contact your carrier to unblock short codes\n8. As backup, try 'Use a different method' and select authenticator app or email\n9. Contact IT admin if no methods work - they can provide a temporary access pass"
                        }
                    ]
                },
                {
                    "title": "Cannot log into computer at all",
                    "node_type": "question",
                    "question_text": "What error message do you see?",
                    "children": [
                        {
                            "title": "Trust relationship between workstation and domain failed",
                            "node_type": "solution",
                            "solution_text": "1. Log in with a LOCAL administrator account:\n   - At login screen, type: .\\Administrator or COMPUTERNAME\\localadmin\n2. Rejoin the domain:\n   - PowerShell (Admin): Reset-ComputerMachinePassword -Server <DCname> -Credential (Get-Credential)\n   - Enter domain admin credentials when prompted\n   - Restart\n3. Alternative method:\n   - System Properties > Computer Name > Change\n   - Change to Workgroup (e.g., 'WORKGROUP') > Restart\n   - Change back to Domain > enter domain name and admin credentials > Restart\n4. Verify:\n   - After restart, log in with domain credentials\n   - Run: nltest /sc_query:<domain> - should show 'Trusted DC connection'\n5. If no local admin account:\n   - Contact IT admin to reset from the server side\n   - Or boot from Windows USB > enable hidden Administrator account"
                        },
                        {
                            "title": "The user name or password is incorrect",
                            "node_type": "solution",
                            "solution_text": "1. Check Caps Lock is off\n2. Check keyboard layout (especially if using non-English keyboard)\n3. Try typing password in Notepad first (Show Password field if available)\n4. Check if you're logging into the correct domain:\n   - Click 'Other User' and verify the domain shown\n   - Type: DOMAIN\\username to force specific domain\n5. If password was recently changed:\n   - The computer may have cached the old password\n   - Make sure you're connected to the network to authenticate against the DC\n6. Try connecting to Wi-Fi/Ethernet before logging in:\n   - Click network icon on login screen\n7. If using cached credentials (offline/no network):\n   - You must use the last password that was used on this specific computer\n8. Reset password through IT admin or self-service portal\n9. Check account isn't disabled or locked: contact IT admin"
                        }
                    ]
                }
            ]
        }
    },

    # ---- HARDWARE DIAGNOSTIC TREE ----
    {
        "category": "Hardware",
        "root": {
            "title": "Hardware Troubleshooting",
            "node_type": "question",
            "question_text": "What hardware issue are you experiencing?",
            "children": [
                {
                    "title": "Monitor / Display issues",
                    "node_type": "question",
                    "question_text": "What is the display doing?",
                    "children": [
                        {
                            "title": "No display / No signal",
                            "node_type": "solution",
                            "solution_text": "1. Check monitor is turned on (power indicator light)\n2. Check the correct input is selected (use monitor buttons to switch HDMI/DP/VGA)\n3. Reseat the display cable on both ends\n4. Try a different cable (HDMI, DisplayPort, etc.)\n5. Try a different port on the computer and/or monitor\n6. For laptops: Press Win+P and try 'Extend' or 'Duplicate' (press blindly if screen is black)\n7. Connect a different monitor to rule out monitor failure\n8. Update display/graphics driver:\n   - Boot to Safe Mode if needed\n   - Device Manager > Display Adapters > Update or Uninstall driver\n9. For docking stations: Try connecting directly (bypass dock)\n10. Check monitor with a different device to verify it works"
                        },
                        {
                            "title": "Flickering screen",
                            "node_type": "solution",
                            "solution_text": "1. Check cable connection - loose cable causes flickering\n2. Change refresh rate:\n   - Settings > Display > Advanced display settings > choose 60Hz\n3. Update graphics driver (this is the most common fix)\n4. Check if flickering happens in Task Manager:\n   - Ctrl+Shift+Esc > does Task Manager flicker too?\n   - If yes: Display driver issue\n   - If no (only apps flicker, Task Manager stable): Incompatible app\n5. Disable hardware acceleration in affected apps\n6. For laptops: Change brightness - some screens flicker at low brightness\n7. Check for electromagnetic interference (move away from other electronics)\n8. Try a different cable type (HDMI vs DisplayPort)"
                        }
                    ]
                },
                {
                    "title": "USB device not recognized",
                    "node_type": "solution",
                    "solution_text": "1. Try a different USB port (use ports directly on the PC, not a hub)\n2. Try the device on a different computer (verify device works)\n3. Restart the computer with the device unplugged\n4. Uninstall the device:\n   - Device Manager > find device (may have yellow !) > Uninstall\n   - Unplug, wait 10 seconds, replug\n5. Update USB controller drivers:\n   - Device Manager > Universal Serial Bus controllers > Update each\n6. Disable USB Selective Suspend:\n   - Power Options > Change Plan Settings > Advanced > USB > Disable\n7. For USB drives not showing:\n   - Check Disk Management (diskmgmt.msc)\n   - Drive may need a letter assigned or be formatted\n8. Reset USB ports:\n   - Device Manager > uninstall all USB Root Hubs > restart PC\n   - Windows will reinstall them"
                },
                {
                    "title": "No sound / Audio not working",
                    "node_type": "solution",
                    "solution_text": "1. Check volume isn't muted (click speaker icon in taskbar)\n2. Check hardware: speakers powered on, headphones plugged in correctly\n3. Right-click speaker icon > Sound Settings > verify correct Output device\n4. Check individual app volume:\n   - Right-click speaker > Open Volume Mixer > check app volumes\n5. Run audio troubleshooter:\n   - Right-click speaker > Troubleshoot sound problems\n6. Restart audio services:\n   - services.msc > restart Windows Audio and Windows Audio Endpoint Builder\n7. Update audio driver from laptop/motherboard manufacturer website\n8. Uninstall audio driver and restart (Windows reinstalls automatically)\n9. If HDMI audio:\n   - Right-click speaker > Sounds > Playback\n   - Set HDMI/DisplayPort as default output\n10. Check BIOS - audio may be disabled there"
                },
                {
                    "title": "Keyboard or mouse not working",
                    "node_type": "question",
                    "question_text": "Is it a wired or wireless device?",
                    "children": [
                        {
                            "title": "Wired (USB)",
                            "node_type": "solution",
                            "solution_text": "1. Try a different USB port\n2. Try on a different computer (verify device works)\n3. Check the cable for physical damage\n4. Device Manager:\n   - Look for yellow exclamation marks under Keyboards or Mice\n   - Uninstall the device > unplug > replug (reinstalls driver)\n5. Disable USB power management:\n   - Device Manager > USB Root Hub > Power Management > uncheck power saving\n6. Boot to Safe Mode to test (rules out driver conflicts)\n7. For laptop built-in keyboard:\n   - Check if Function Lock key is active\n   - Check keyboard layout isn't changed (Win+Space to switch)\n   - External keyboards override internal in some BIOS settings"
                        },
                        {
                            "title": "Wireless / Bluetooth",
                            "node_type": "solution",
                            "solution_text": "1. Replace or charge batteries\n2. Check wireless receiver is plugged in (small USB dongle)\n3. Move closer to the receiver (within 3-10 feet)\n4. Re-pair the device:\n   - Turn device off, press pairing button, plug in receiver\n   - For Bluetooth: Settings > Bluetooth > Remove device > Add again\n5. Try a different USB port for the receiver\n6. Check for interference from other wireless devices\n7. For Bluetooth:\n   - Restart Bluetooth: Settings > Bluetooth & devices > toggle off/on\n   - Update Bluetooth driver\n   - Check Bluetooth service: services.msc > Bluetooth Support Service > restart\n8. Test with a different wireless device to isolate if it's the device or the PC"
                        }
                    ]
                }
            ]
        }
    },

    # ---- SOFTWARE DIAGNOSTIC TREE ----
    {
        "category": "Software",
        "root": {
            "title": "Software Troubleshooting",
            "node_type": "question",
            "question_text": "What type of software issue?",
            "children": [
                {
                    "title": "Microsoft Office problems",
                    "node_type": "question",
                    "question_text": "Which Office issue?",
                    "children": [
                        {
                            "title": "Office won't open / crashes",
                            "node_type": "solution",
                            "solution_text": "1. Start in Safe Mode: Run the program with /safe flag\n   - Example: winword /safe (for Word)\n   - Or hold Ctrl while clicking the Office app\n2. If it works in Safe Mode, disable add-ins:\n   - File > Options > Add-ins > COM Add-ins > Disable all\n3. Repair Office:\n   - Control Panel > Programs > Microsoft Office > Change\n   - Try Quick Repair first, then Online Repair if needed\n4. Update Office: File > Account > Update Options > Update Now\n5. Clear Office cache:\n   - Delete: %LocalAppData%\\Microsoft\\Office\\16.0\\OfficeFileCache\n6. Reset Office settings:\n   - Delete: %AppData%\\Microsoft\\Office\\ (backup first)\n7. Repair user profile by creating new Windows user\n8. Reinstall Office completely as last resort"
                        },
                        {
                            "title": "Office activation / license error",
                            "node_type": "solution",
                            "solution_text": "1. File > Account > check activation status\n2. Sign out and sign back in with the licensed account\n3. For Microsoft 365:\n   - Check subscription at account.microsoft.com/services\n   - Verify device limit not exceeded (max 5 devices)\n4. Remove old licenses:\n   - CMD (Admin): cd \\Program Files\\Microsoft Office\\Office16\n   - cscript ospp.vbs /dstatus (view licenses)\n   - cscript ospp.vbs /unpkey:<last5digits> (remove old)\n   - cscript ospp.vbs /act (reactivate)\n5. Delete credential cache:\n   - Control Panel > Credential Manager > remove Office entries\n6. Delete license files: %LocalAppData%\\Microsoft\\Office\\Licenses\n7. Repair Office installation\n8. Use Microsoft Support and Recovery Assistant (SaRA)"
                        }
                    ]
                },
                {
                    "title": "Application won't install",
                    "node_type": "solution",
                    "solution_text": "1. Run installer as Administrator (right-click > Run as administrator)\n2. Check disk space (need at least 2x the installer size free)\n3. Temporarily disable antivirus\n4. Check Windows Installer service: services.msc > Windows Installer > Running\n5. For compatibility issues:\n   - Right-click installer > Properties > Compatibility\n   - Run in compatibility mode for older Windows version\n6. Clean temp files: delete contents of %TEMP%\n7. Run in Clean Boot:\n   - msconfig > Services > Hide Microsoft > Disable all > restart\n   - Try installation\n   - Re-enable services after\n8. If MSI error, re-register Windows Installer:\n   - CMD (Admin): msiexec /unregister then msiexec /regserver\n9. Download a fresh copy of the installer (may be corrupted)"
                },
                {
                    "title": "Browser issues (Chrome/Edge)",
                    "node_type": "solution",
                    "solution_text": "1. Clear browsing data: Ctrl+Shift+Delete\n   - Clear cache, cookies, browsing history\n2. Disable all extensions:\n   - chrome://extensions or edge://extensions > toggle all off\n   - Re-enable one at a time to find the problem one\n3. Reset browser:\n   - Settings > Reset settings > Restore to defaults\n4. If pages don't load:\n   - Check internet connection first\n   - Try incognito mode (Ctrl+Shift+N)\n   - Change DNS to 8.8.8.8\n5. If browser is slow:\n   - Close unnecessary tabs\n   - Check memory in Task Manager (browser process)\n   - Create new browser profile (Settings > Profiles > Add)\n6. Update to latest version\n7. If all else fails, uninstall and reinstall the browser"
                }
            ]
        }
    },
]


async def seed_knowledge_base(workspace_id: int):
    """
    Seed the knowledge base with IT troubleshooting data.
    Only runs if the KB tables are empty for this workspace.
    """
    from app.core.database import engine
    from sqlmodel.ext.asyncio.session import AsyncSession

    async with AsyncSession(engine) as db:
        # Check if already seeded
        existing = (await db.execute(
            select(SupportArticle).where(SupportArticle.workspace_id == workspace_id).limit(1)
        )).scalar_one_or_none()
        if existing:
            return  # Already has data

        existing_case = (await db.execute(
            select(KBResolvedCase).where(KBResolvedCase.workspace_id == workspace_id).limit(1)
        )).scalar_one_or_none()
        if existing_case:
            return

        print(f"[KB Seed] Seeding IT Knowledge Base for workspace {workspace_id}...")
        # 1. Create categories
        for cat_data in CATEGORIES:
            existing_cat = (await db.execute(
                select(SupportCategory).where(
                    SupportCategory.workspace_id == workspace_id,
                    SupportCategory.name == cat_data["name"]
                )
            )).scalar_one_or_none()
            if not existing_cat:
                cat = SupportCategory(
                    workspace_id=workspace_id,
                    name=cat_data["name"],
                    icon=cat_data["icon"],
                    description=cat_data["description"],
                    article_count=0,
                )
                db.add(cat)
        await db.commit()

        # 2. Create articles
        article_counts = {}
        for art_data in ARTICLES:
            article = SupportArticle(
                workspace_id=workspace_id,
                problem_title=art_data["problem_title"],
                problem_description=art_data["problem_description"],
                problem_keywords=art_data["problem_keywords"],
                category=art_data["category"],
                solution_steps=art_data["solution_steps"],
                solution_source="verified",
                is_verified=True,
                is_active=True,
            )
            db.add(article)
            article_counts[art_data["category"]] = article_counts.get(art_data["category"], 0) + 1
        await db.commit()

        # Update category article counts
        for cat_name, count in article_counts.items():
            cat = (await db.execute(
                select(SupportCategory).where(
                    SupportCategory.workspace_id == workspace_id,
                    SupportCategory.name == cat_name
                )
            )).scalar_one_or_none()
            if cat:
                cat.article_count = count
        await db.commit()

        # 3. Create diagnostic trees
        for tree_data in DIAGNOSTIC_TREES:
            await _create_tree_node(db, workspace_id, tree_data["category"], tree_data["root"], parent_id=None, sort_order=0)
        await db.commit()

        # Count totals
        total_articles = len(ARTICLES)
        total_trees = len(DIAGNOSTIC_TREES)
        print(f"[KB Seed] ✅ Seeded {total_articles} articles, {total_trees} diagnostic trees, {len(CATEGORIES)} categories")


async def _create_tree_node(db, workspace_id: int, category: str, node_data: dict, parent_id, sort_order: int):
    """Recursively create diagnostic tree nodes"""
    node = KBDiagnosticTree(
        workspace_id=workspace_id,
        parent_id=parent_id,
        title=node_data["title"],
        node_type=node_data["node_type"],
        question_text=node_data.get("question_text"),
        solution_text=node_data.get("solution_text"),
        category=category,
        sort_order=sort_order,
        is_active=True,
    )
    db.add(node)
    await db.flush()  # Get the node.id

    children = node_data.get("children", [])
    for idx, child_data in enumerate(children):
        await _create_tree_node(db, workspace_id, category, child_data, parent_id=node.id, sort_order=idx)
