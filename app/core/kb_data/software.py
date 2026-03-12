"""Software and application troubleshooting articles and diagnostic tree."""

ARTICLES = [
    {
        "category": "Software",
        "problem_title": "Microsoft Office won't activate or shows 'Unlicensed Product'",
        "problem_description": "Microsoft Office applications show 'Unlicensed Product' or 'Product Activation Required' banner. Features may be limited.",
        "problem_keywords": "office activation, unlicensed product, office license, product key, office activate, microsoft 365 activate",
        "solution_steps": (
            "1. Check your subscription:\n"
            "   - Open any Office app > File > Account\n"
            "   - Check if it shows a valid subscription or license\n"
            "2. Sign in with the correct Microsoft account:\n"
            "   - File > Account > Sign in with the account that has the license\n"
            "   - For M365: use your work/school account\n"
            "3. Reset Office licensing:\n"
            "   - Close all Office apps\n"
            "   - CMD (Admin):\n"
            "   - cscript \"C:\\Program Files\\Microsoft Office\\Office16\\OSPP.VBS\" /dstatus\n"
            "   - For M365: Sign out, delete credentials, sign back in\n"
            "4. Clear cached credentials:\n"
            "   - Control Panel > Credential Manager > remove all office/microsoft entries\n"
            "5. Repair Office:\n"
            "   - Settings > Apps > Microsoft Office > Modify > Quick Repair\n"
            "6. For volume license (KMS/MAK):\n"
            "   - Verify KMS server: nslookup -type=srv _vlmcs._tcp.domain\n"
            "   - Force activation: cscript OSPP.VBS /act\n"
            "7. Uninstall and reinstall Office from office.com\n"
            "8. Use the Microsoft Support and Recovery Assistant (SaRA) tool"
        ),
    },
    {
        "category": "Software",
        "problem_title": "Microsoft Teams not loading or showing blank screen",
        "problem_description": "Microsoft Teams shows a blank white/black screen, gets stuck loading, or crashes on startup. May work in browser but not desktop app.",
        "problem_keywords": "teams not loading, teams blank, teams crash, teams white screen, teams stuck, microsoft teams error",
        "solution_steps": (
            "1. Clear Teams cache:\n"
            "   - Close Teams completely (right-click tray icon > Quit)\n"
            "   - Delete contents of: %appdata%\\Microsoft\\Teams\n"
            "   - Specifically delete: Cache, blob_storage, databases, GPUcache, IndexedDB, Local Storage, tmp\n"
            "   - Restart Teams\n"
            "2. For New Teams (Teams 2.0):\n"
            "   - Delete: %localappdata%\\Packages\\MSTeams_8wekyb3d8bbwe\\LocalCache\n"
            "3. Check for updates:\n"
            "   - Teams > three dots (...) > Check for updates\n"
            "4. Disable GPU acceleration:\n"
            "   - Settings > General > Disable GPU hardware acceleration > restart Teams\n"
            "5. Clear credentials:\n"
            "   - Control Panel > Credential Manager > remove Teams entries\n"
            "   - Sign out and sign back in\n"
            "6. Reinstall Teams:\n"
            "   - Uninstall from Settings > Apps\n"
            "   - Delete remaining data: %appdata%\\Microsoft\\Teams\n"
            "   - Download fresh from teams.microsoft.com\n"
            "7. Check if Teams works in browser (teams.microsoft.com)\n"
            "8. Check date/time is correct (wrong date causes auth issues)"
        ),
    },
    {
        "category": "Software",
        "problem_title": "Application installer fails or won't install",
        "problem_description": "Software installation fails with errors. Installer may freeze, show error codes, or say another installation is in progress.",
        "problem_keywords": "install fail, installer error, won't install, installation failed, msi error, setup failed, another installation",
        "solution_steps": (
            "1. 'Another installation is in progress':\n"
            "   - Wait for it to finish, or:\n"
            "   - Restart the Windows Installer: services.msc > Windows Installer > Restart\n"
            "   - Or CMD (Admin): msiexec /unregister && msiexec /regserver\n"
            "2. Run installer as Administrator:\n"
            "   - Right-click installer > Run as administrator\n"
            "3. Check disk space: Need sufficient free space on C:\n"
            "4. For MSI errors:\n"
            "   - Enable MSI logging: msiexec /i installer.msi /l*v install.log\n"
            "   - Check the log for the specific error\n"
            "5. Disable antivirus temporarily:\n"
            "   - Some antivirus blocks legitimate installers\n"
            "6. Install in Clean Boot:\n"
            "   - msconfig > Services > Hide all Microsoft services > Disable all\n"
            "   - Startup tab > Open Task Manager > disable all startup items\n"
            "   - Restart and try installing\n"
            "   - Re-enable services after install\n"
            "7. Check for .NET Framework requirement:\n"
            "   - Many apps need specific .NET versions\n"
            "   - Install from Microsoft or: DISM /Online /Enable-Feature /FeatureName:NetFx3\n"
            "8. Check the publisher's system requirements match your OS version"
        ),
    },
    {
        "category": "Software",
        "problem_title": "Browser running slow or freezing",
        "problem_description": "Chrome, Edge, or Firefox is very slow, freezes, or uses excessive memory/CPU. Web pages take a long time to load.",
        "problem_keywords": "browser slow, chrome slow, edge slow, firefox slow, browser freeze, browser memory, browser cpu",
        "solution_steps": (
            "1. Close unnecessary tabs:\n"
            "   - Each tab uses RAM - 20+ tabs can use several GB\n"
            "   - Use browser's task manager: Shift+Esc (Chrome/Edge)\n"
            "2. Disable/remove extensions:\n"
            "   - Extensions are the #1 cause of browser slowness\n"
            "   - Chrome: chrome://extensions > disable all, test, enable one at a time\n"
            "   - Edge: edge://extensions\n"
            "   - Firefox: about:addons\n"
            "3. Clear browsing data:\n"
            "   - Ctrl+Shift+Del > clear cache, cookies, browsing history\n"
            "   - Select 'All time' for the time range\n"
            "4. Disable hardware acceleration:\n"
            "   - Chrome: Settings > System > Use hardware acceleration > Off\n"
            "   - This helps with rendering issues and some GPU-related slowness\n"
            "5. Update the browser to latest version\n"
            "6. Reset browser to defaults:\n"
            "   - Chrome: Settings > Reset and clean up > Restore defaults\n"
            "   - Edge: Settings > Reset settings\n"
            "7. Check for malware: Run Malwarebytes and Windows Defender scan\n"
            "   - Adware/browser hijackers cause significant slowdown\n"
            "8. Try a different browser to compare performance"
        ),
    },
    {
        "category": "Software",
        "problem_title": "Adobe Acrobat/Reader PDF errors or crashes",
        "problem_description": "Adobe Acrobat or Reader crashes when opening PDFs, shows errors, or won't open certain PDF files.",
        "problem_keywords": "adobe crash, pdf error, acrobat crash, reader crash, pdf won't open, adobe reader, acrobat error",
        "solution_steps": (
            "1. Update Adobe to latest version:\n"
            "   - Help > Check for Updates\n"
            "2. Repair the installation:\n"
            "   - Help > Repair Installation\n"
            "3. Disable Protected Mode:\n"
            "   - Edit > Preferences > Security (Enhanced)\n"
            "   - Uncheck 'Enable Protected Mode at startup'\n"
            "   - Restart Adobe\n"
            "4. Clear cache:\n"
            "   - Delete contents of: %appdata%\\Adobe\\Acrobat\\DC\n"
            "   - Backup preferences first if needed\n"
            "5. If specific PDF won't open:\n"
            "   - Try opening the PDF in Chrome or Edge browser\n"
            "   - The PDF file may be corrupt - ask sender for a new copy\n"
            "   - Try 'Save As' from browser to a new file\n"
            "6. For printing issues from Adobe:\n"
            "   - Print as Image: File > Print > Advanced > Print As Image\n"
            "7. Reinstall Adobe:\n"
            "   - Uninstall completely using Adobe Cleaner Tool\n"
            "   - Download fresh installer from Adobe website\n"
            "8. If acrobat won't open at all: Close all instances in Task Manager first"
        ),
    },
    {
        "category": "Software",
        "problem_title": "Java application errors or Java not working",
        "problem_description": "Java-based applications don't run. Browser shows 'Java not installed' or Java applications throw exceptions. Multiple Java versions causing conflicts.",
        "problem_keywords": "java error, java not working, java install, jre, jdk, java exception, java version, java update",
        "solution_steps": (
            "1. Check if Java is installed:\n"
            "   - CMD: java -version\n"
            "   - If not found: Download from java.com or adoptium.net\n"
            "2. Check which Java version is needed:\n"
            "   - Some apps need specific versions (Java 8, 11, 17, 21)\n"
            "   - Check the application's requirements\n"
            "3. Multiple Java versions conflict:\n"
            "   - Control Panel > Programs > check for multiple Java installations\n"
            "   - Uninstall older versions if not needed\n"
            "   - Or set JAVA_HOME environment variable to the correct one\n"
            "4. Java environment variables:\n"
            "   - System Properties > Environment Variables\n"
            "   - JAVA_HOME = path to JDK/JRE (e.g., C:\\Program Files\\Java\\jdk-17)\n"
            "   - PATH should include %JAVA_HOME%\\bin\n"
            "5. If Java app throws errors:\n"
            "   - Check the Java console output for specific error messages\n"
            "   - Try: java -jar application.jar from CMD to see errors\n"
            "6. Clear Java cache:\n"
            "   - Control Panel > Java > General > Temporary Internet Files > Delete Files\n"
            "7. Update Java to latest version of the required branch\n"
            "8. For 32-bit Java apps on 64-bit Windows: Install 32-bit Java (x86)"
        ),
    },
    {
        "category": "Software",
        "problem_title": "Application compatibility issue - won't run on Windows 10/11",
        "problem_description": "Older application won't run on Windows 10 or 11. May crash, show errors, or display incorrectly.",
        "problem_keywords": "compatibility, won't run, old program, compatibility mode, legacy app, program not compatible, windows 11",
        "solution_steps": (
            "1. Run Compatibility Troubleshooter:\n"
            "   - Right-click the program > Properties > Compatibility > Run compatibility troubleshooter\n"
            "2. Set Compatibility Mode manually:\n"
            "   - Right-click > Properties > Compatibility\n"
            "   - Check 'Run in compatibility mode for:' > select older Windows\n"
            "   - Try Windows 7, 8, or the version the app was designed for\n"
            "3. Run as Administrator:\n"
            "   - Check 'Run this program as an administrator'\n"
            "   - Many older apps need admin rights\n"
            "4. DPI scaling fix:\n"
            "   - Compatibility > Change high DPI settings\n"
            "   - Check 'Override high DPI scaling' > Application\n"
            "5. Color depth and resolution:\n"
            "   - Compatibility tab > check 'Reduced color mode' > 16-bit\n"
            "   - Check 'Run in 640x480 screen resolution' if UI is broken\n"
            "6. If it still won't run:\n"
            "   - Check if vendor has an updated version\n"
            "   - Try installing in a Virtual Machine with the required OS\n"
            "   - Windows Sandbox or Hyper-V for testing\n"
            "7. For 16-bit applications: They don't run on 64-bit Windows at all\n"
            "   - Need a 32-bit Windows VM"
        ),
    },
    {
        "category": "Software",
        "problem_title": "QuickBooks errors or won't open",
        "problem_description": "QuickBooks Desktop crashes, gives errors (H202, 3371, 6000), or won't open the company file.",
        "problem_keywords": "quickbooks error, quickbooks crash, qb error, quickbooks won't open, 3371, H202, 6000, company file",
        "solution_steps": (
            "1. Error 3371: License data problem\n"
            "   - Rename: C:\\ProgramData\\Intuit\\Entitlement Client\\v8\\EntitlementDataStore.ecml\n"
            "   - Rename to: EntitlementDataStore.ecml.old\n"
            "   - Reopen QuickBooks and re-enter license info\n"
            "2. Error H202, H505 (multi-user mode):\n"
            "   - Check QuickBooks Database Server Manager is running on the host\n"
            "   - Verify the company file folder is shared with correct permissions\n"
            "   - Firewall: Allow QBDBMgrN.exe and QBW32.exe\n"
            "   - Run QuickBooks File Doctor (download from Intuit)\n"
            "3. Error 6000 series (company file issues):\n"
            "   - Copy the company file (.qbw) to the desktop and try opening from there\n"
            "   - If it works: the original location has a permissions or path issue\n"
            "   - Run QuickBooks File Doctor\n"
            "4. QuickBooks won't open:\n"
            "   - Hold Ctrl while opening QuickBooks to suppress the company file\n"
            "   - Run Quick Fix from QuickBooks Tool Hub\n"
            "5. Repair QuickBooks:\n"
            "   - Download QuickBooks Tool Hub from Intuit\n"
            "   - Run: Quick Fix My Program\n"
            "   - Then: QuickBooks Program Diagnostic Tool\n"
            "6. Company file on network: Never open over Wi-Fi, use Ethernet\n"
            "7. Keep QuickBooks updated to latest release"
        ),
    },
    {
        "category": "Software",
        "problem_title": "Zoom audio/video not working in meetings",
        "problem_description": "Zoom meeting has no audio, no video, or other participants can't hear/see you. Camera or microphone not detected.",
        "problem_keywords": "zoom audio, zoom video, zoom microphone, zoom camera, zoom no sound, zoom meeting, zoom not working",
        "solution_steps": (
            "1. Test audio/video before meeting:\n"
            "   - Zoom > Settings > Audio > Test Speaker & Microphone\n"
            "   - Settings > Video > check if camera shows your feed\n"
            "2. Select correct devices in Zoom:\n"
            "   - In meeting: Click ^ next to Mute > select your microphone\n"
            "   - Click ^ next to camera > select your camera\n"
            "3. Check Windows permissions:\n"
            "   - Settings > Privacy > Microphone > allow Zoom\n"
            "   - Settings > Privacy > Camera > allow Zoom\n"
            "4. Close other apps using camera/mic:\n"
            "   - Teams, Skype, OBS, etc. may block the device\n"
            "5. If others can't hear you:\n"
            "   - Check you're not muted (bottom-left in Zoom)\n"
            "   - Check microphone volume: Settings > Sound > Input volume\n"
            "   - Check audio isn't routed to wrong device (headset vs laptop mic)\n"
            "6. Update Zoom to latest version\n"
            "7. Reinstall Zoom audio driver:\n"
            "   - Zoom will reinstall its virtual audio device on next update\n"
            "8. Update system audio and camera drivers"
        ),
    },
    {
        "category": "Software",
        "problem_title": "Application crashes with 'APPCRASH' or 'stopped working'",
        "problem_description": "Application shows 'has stopped working' dialog or APPCRASH error with exception code like 0xc0000005 or 0xc000007b.",
        "problem_keywords": "app crash, stopped working, appcrash, 0xc0000005, 0xc000007b, application error, crash",
        "solution_steps": (
            "1. Error 0xc0000005 (Access Violation):\n"
            "   - Run as Administrator\n"
            "   - Disable DEP (Data Execution Prevention) for the app:\n"
            "   - System Properties > Advanced > Performance > DEP > Add the program\n"
            "   - Run SFC: sfc /scannow\n"
            "2. Error 0xc000007b (Bad Image):\n"
            "   - This is a 32/64-bit mismatch or missing runtime\n"
            "   - Install all Visual C++ Redistributables (x86 AND x64)\n"
            "   - Install DirectX End-User Runtime\n"
            "   - Install .NET Framework (required version)\n"
            "   - Try running the 32-bit version of the app if available\n"
            "3. General crash troubleshooting:\n"
            "   - Update the application to latest version\n"
            "   - Check Event Viewer > Application log for detailed crash info\n"
            "   - Run in Compatibility Mode (right-click > Properties > Compatibility)\n"
            "4. Clear application data/cache:\n"
            "   - Check %appdata% and %localappdata% for the app's folder\n"
            "   - Rename/delete the app's settings folder (back up first)\n"
            "5. Reinstall the application:\n"
            "   - Fully uninstall including user data\n"
            "   - Restart computer\n"
            "   - Fresh install from latest installer\n"
            "6. Check Windows and driver updates"
        ),
    },
    {
        "category": "Software",
        "problem_title": "Microsoft Office documents slow to open or save",
        "problem_description": "Word, Excel, or PowerPoint takes a very long time to open or save files. May freeze during save or show 'Not Responding'.",
        "problem_keywords": "office slow, word slow, excel slow, document slow, save slow, office freeze, excel freeze",
        "solution_steps": (
            "1. Disable add-ins:\n"
            "   - File > Options > Add-ins > COM Add-ins > Go\n"
            "   - Uncheck all > OK > restart the app\n"
            "   - Common culprits: Grammarly, antivirus, PDF converters\n"
            "2. Check file location:\n"
            "   - Files on network drives or cloud-synced folders may be slow\n"
            "   - Try copying file to local C: drive and opening from there\n"
            "3. For Excel specifically:\n"
            "   - Large files with many formulas: set Calculation to Manual\n"
            "   - Formulas > Calculation Options > Manual\n"
            "   - Check for circular references: Formulas > Error Checking\n"
            "4. Disable Protected View (if safe/internal files):\n"
            "   - File > Options > Trust Center > Trust Center Settings\n"
            "   - Protected View > uncheck all three options\n"
            "5. Repair Office:\n"
            "   - Settings > Apps > Microsoft Office > Modify > Quick Repair\n"
            "6. Clear Office cache:\n"
            "   - Delete: %localappdata%\\Microsoft\\Office\\16.0\\OfficeFileCache\n"
            "7. Check antivirus:\n"
            "   - Exclude Office file types from real-time scanning\n"
            "   - Or add the file location to AV exclusions\n"
            "8. Disable AutoSave/AutoRecover if saving too frequently"
        ),
    },
    {
        "category": "Software",
        "problem_title": "Remote Desktop (RDP) connection issues",
        "problem_description": "Cannot connect to remote computer via Remote Desktop. Shows 'Remote Desktop can't connect to the remote computer' or black screen after connecting.",
        "problem_keywords": "remote desktop, rdp, rdp error, rdp connection, remote connect, rdp black screen, mstsc",
        "solution_steps": (
            "1. Verify Remote Desktop is enabled on the target:\n"
            "   - Target PC: Settings > System > Remote Desktop > Enable\n"
            "   - Or: System Properties > Remote > Allow remote connections\n"
            "2. Check networking:\n"
            "   - Can you ping the target computer? ping hostname\n"
            "   - RDP uses TCP port 3389 by default\n"
            "   - Check firewall allows RDP: Windows Firewall > Allow > Remote Desktop\n"
            "3. From command line:\n"
            "   - Test port: Test-NetConnection hostname -Port 3389 (PowerShell)\n"
            "4. 'The credentials did not work':\n"
            "   - Use full domain\\username or username@domain format\n"
            "   - For local accounts: .\\username or COMPUTERNAME\\username\n"
            "5. RDP black screen after connecting:\n"
            "   - Press Ctrl+Alt+End (RDP equivalent of Ctrl+Alt+Del)\n"
            "   - Kill wallpaper engine or display-related apps on remote\n"
            "   - Connect with reduced color depth: mstsc > Show Options > Display > 16-bit\n"
            "6. NLA (Network Level Authentication) errors:\n"
            "   - Target may require NLA but client doesn't support it\n"
            "   - Or CredSSP encryption oracle error: Apply the security update on both sides\n"
            "7. For RDP over internet: Use a VPN - never expose port 3389 to the internet directly"
        ),
    },
    {
        "category": "Software",
        "problem_title": "OneDrive sync issues or conflicts",
        "problem_description": "OneDrive shows sync errors, files not uploading/downloading, or shows file conflicts. Red X or sync pending icons on files.",
        "problem_keywords": "onedrive sync, onedrive error, onedrive conflict, sync pending, onedrive not syncing, onedrive red x",
        "solution_steps": (
            "1. Check OneDrive status:\n"
            "   - Click OneDrive icon in taskbar > check for sync errors\n"
            "   - Settings > Account > View sync problems\n"
            "2. Common sync fixes:\n"
            "   - Pause and resume sync: OneDrive icon > Pause > Resume\n"
            "   - Close and restart OneDrive\n"
            "3. File name issues:\n"
            "   - OneDrive doesn't support: * : < > ? \" | \\ /\n"
            "   - File path must be under 400 characters total\n"
            "   - Rename files/folders with unsupported characters\n"
            "4. Reset OneDrive:\n"
            "   - Win+R: %localappdata%\\Microsoft\\OneDrive\\onedrive.exe /reset\n"
            "   - If icon doesn't reappear: Re-run OneDrive from Start\n"
            "5. Conflicts:\n"
            "   - OneDrive creates a copy with your PC name appended\n"
            "   - Compare both files, keep the correct one\n"
            "   - Delete the duplicate\n"
            "6. Check storage:\n"
            "   - OneDrive has a storage limit (5GB free, 1TB with M365)\n"
            "   - Files On-Demand: Only download files when you open them\n"
            "7. For business: Check if admin policies restrict sync\n"
            "8. Relink OneDrive if account changed: Unlink this PC > sign in again"
        ),
    },
    {
        "category": "Software",
        "problem_title": "Excel file corrupt or won't open",
        "problem_description": "Excel file won't open, shows as corrupt, or opens with errors and missing data. May show 'The file is corrupt and cannot be opened'.",
        "problem_keywords": "excel corrupt, spreadsheet corrupt, excel won't open, xlsx corrupt, excel repair, recover excel",
        "solution_steps": (
            "1. Try Excel's built-in repair:\n"
            "   - Excel > File > Open > Browse to the file\n"
            "   - Click the dropdown on 'Open' button > 'Open and Repair'\n"
            "   - Try 'Repair' first, then 'Extract Data' if repair fails\n"
            "2. Try opening in Protected View:\n"
            "   - Create a new blank workbook\n"
            "   - Data > Get Data > From File > select the corrupt file\n"
            "3. Change file extension:\n"
            "   - Try renaming .xlsx to .xls or vice versa\n"
            "   - Try opening in LibreOffice Calc (handles some corruption better)\n"
            "4. Recover from temp files:\n"
            "   - Check: %appdata%\\Microsoft\\Excel\\\n"
            "   - Look for .xlk or .tmp files with similar names\n"
            "   - Check AutoRecover: File > Options > Save > AutoRecover file location\n"
            "5. Use previous version:\n"
            "   - Right-click file > Properties > Previous Versions\n"
            "   - Or check OneDrive/SharePoint version history\n"
            "6. For .xlsx files: Rename to .zip, extract, fix XML, re-zip\n"
            "   - Open the .zip > xl folder > check sheets for data\n"
            "7. Third-party tools: Stellar Repair for Excel, Recovery Toolbox"
        ),
    },
    {
        "category": "Software",
        "problem_title": "Windows Store apps won't install or update",
        "problem_description": "Microsoft Store apps fail to download, install, or update. May show error codes 0x80073CFB, 0x80004003, or downloads stuck at pending.",
        "problem_keywords": "microsoft store, store error, app install, store update, store download, store won't work, 0x80073CFB",
        "solution_steps": (
            "1. Reset Microsoft Store cache:\n"
            "   - Win+R: wsreset.exe > wait for Store to open\n"
            "2. Check date and time: Incorrect date causes store errors\n"
            "3. Run Windows Store troubleshooter:\n"
            "   - Settings > Update > Troubleshoot > Windows Store Apps\n"
            "4. Re-register Store:\n"
            "   - PowerShell (Admin):\n"
            "   - Get-AppXPackage *Microsoft.WindowsStore* | Foreach {Add-AppxPackage -DisableDevelopmentMode -Register \"$($_.InstallLocation)\\AppXManifest.xml\"}\n"
            "5. Re-register all Store apps:\n"
            "   - Get-AppXPackage | Foreach {Add-AppxPackage -DisableDevelopmentMode -Register \"$($_.InstallLocation)\\AppXManifest.xml\"}\n"
            "6. Check Windows Update:\n"
            "   - Store updates often depend on Windows updates\n"
            "   - Install all pending Windows updates\n"
            "7. Check proxy/VPN isn't interfering\n"
            "8. Sign out and sign back into the Store\n"
            "9. Reset Store app:\n"
            "   - Settings > Apps > Microsoft Store > Advanced Options > Reset"
        ),
    },
    {
        "category": "Software",
        "problem_title": "Microsoft Teams chat messages not sending or delayed",
        "problem_description": "Teams messages show a spinning circle, fail to send, or arrive delayed. Chat functionality is broken while calls may still work.",
        "problem_keywords": "teams chat, message not sent, teams delay, chat failed, teams spinning, chat not working, teams message",
        "solution_steps": (
            "1. Check Teams service status:\n"
            "   - Visit https://status.office365.com or admin.microsoft.com\n"
            "   - Check for Teams service incidents\n"
            "   - Teams outages affect chat before other features\n"
            "2. Clear Teams cache:\n"
            "   - Fully quit Teams (right-click tray icon > Quit)\n"
            "   - Delete: %appdata%\\Microsoft\\Teams\\Cache\n"
            "   - Delete: %appdata%\\Microsoft\\Teams\\blob_storage\n"
            "   - Delete: %appdata%\\Microsoft\\Teams\\databases\n"
            "   - Restart Teams\n"
            "3. For new Teams (Teams 2.0):\n"
            "   - Cache location: %localappdata%\\Packages\\MSTeams_8wekyb3d8bbwe\\LocalCache\n"
            "   - Clear the LocalCache folder\n"
            "4. Network check:\n"
            "   - Teams requires WebSocket connections\n"
            "   - Proxy/firewall may block Teams endpoints\n"
            "   - Required: *.teams.microsoft.com, *.skype.com on ports 80 and 443\n"
            "5. Sign out and back in:\n"
            "   - Teams > Profile > Sign Out\n"
            "   - Restart Teams and sign in again\n"
            "6. Reinstall Teams:\n"
            "   - Uninstall Teams from Settings > Apps\n"
            "   - Delete remaining cache folders\n"
            "   - Download and install latest version\n"
            "7. Use Teams Web (teams.microsoft.com) as a temporary workaround"
        ),
    },
    {
        "category": "Software",
        "problem_title": "Application crashes with 'insufficient memory' error",
        "problem_description": "Applications crash with out-of-memory errors even though the system has available RAM. Common with large Excel files, CAD, or media editing software.",
        "problem_keywords": "out of memory, insufficient memory, memory error, ram full, low memory, virtual memory, page file",
        "solution_steps": (
            "1. Check memory usage:\n"
            "   - Task Manager > Performance > Memory\n"
            "   - Note: Total, In use, and Available\n"
            "   - If Available is very low: Close other applications\n"
            "2. 32-bit vs 64-bit application:\n"
            "   - 32-bit applications can only use ~3.5 GB of RAM total\n"
            "   - Even on a 64-bit system with 32 GB RAM\n"
            "   - Install the 64-bit version of the application if available\n"
            "   - Check: Task Manager > Details > shows '32 bit' next to process name\n"
            "3. Virtual memory / Page file:\n"
            "   - System Properties > Advanced > Performance > Settings > Advanced\n"
            "   - Virtual Memory > Change\n"
            "   - Set a custom size: Initial = 1.5x RAM, Maximum = 3x RAM\n"
            "   - Or let Windows manage it automatically\n"
            "4. Close memory-heavy apps:\n"
            "   - Task Manager > sort by Memory usage\n"
            "   - Browser tabs are major memory consumers\n"
            "   - Close unused applications and browser tabs\n"
            "5. Memory leaks:\n"
            "   - If memory usage increases over time until crash\n"
            "   - Application has a memory leak - check for updates/patches\n"
            "   - Restart the application periodically as workaround\n"
            "6. Large file handling:\n"
            "   - Excel: Split large files, use Power Query for data\n"
            "   - Images/Video: Close other editing sessions\n"
            "7. Upgrade RAM if consistently running out of memory during normal work"
        ),
    },
    {
        "category": "Software",
        "problem_title": "Software license deactivated or activation server unreachable",
        "problem_description": "Software shows 'license expired' or 'activation failed' even though the license is valid. Cannot reach the activation server.",
        "problem_keywords": "license expired, activation failed, license server, software license, activation server, license key, deactivated",
        "solution_steps": (
            "1. Check license validity:\n"
            "   - Verify the license hasn't genuinely expired\n"
            "   - Check purchase/renewal dates with the vendor\n"
            "   - For subscription: Verify payment is current\n"
            "2. Network connectivity to activation server:\n"
            "   - Can the PC reach the internet? Check basic connectivity\n"
            "   - Firewall/proxy may block the activation server URL\n"
            "   - Whitelist the vendor's activation URLs\n"
            "3. System clock:\n"
            "   - If the system date/time is wrong, licenses may appear expired\n"
            "   - Settings > Time & Language > Set time automatically\n"
            "   - Sync with time server\n"
            "4. Re-activate:\n"
            "   - Deactivate the license first (if possible)\n"
            "   - Re-enter the license key\n"
            "   - Some software limits activations per key\n"
            "5. Hardware changes:\n"
            "   - Some licenses are tied to hardware (MAC address, CPU, motherboard)\n"
            "   - Hardware changes (new NIC, motherboard) may invalidate activation\n"
            "   - Contact vendor to transfer the license\n"
            "6. For on-premises license servers:\n"
            "   - Check if the license server is running\n"
            "   - Verify the client can reach the server on the required port\n"
            "   - Check server logs for license checkout failures\n"
            "7. Contact the vendor's support with your license key and error for reactivation"
        ),
    },
    {
        "category": "Software",
        "problem_title": "PDF files won't open or display incorrectly",
        "problem_description": "PDF files show blank pages, fail to open, or display garbled text. May affect specific PDFs or all PDF files.",
        "problem_keywords": "pdf won't open, pdf blank, pdf error, adobe reader, pdf display, pdf corrupt, pdf viewer",
        "solution_steps": (
            "1. Try a different PDF viewer:\n"
            "   - If using Edge/Chrome: Try Adobe Acrobat Reader\n"
            "   - If using Adobe Reader: Try Edge, Chrome, or Foxit Reader\n"
            "   - This determines if the issue is the viewer or the file\n"
            "2. Update the PDF viewer:\n"
            "   - Adobe Reader: Help > Check for Updates\n"
            "   - Chrome: Updates automatically\n"
            "   - Edge: Updates with Windows Update\n"
            "3. Repair Adobe Reader:\n"
            "   - Help > Repair Installation\n"
            "   - Or: Settings > Apps > Adobe Acrobat > Modify > Repair\n"
            "4. Set default PDF app:\n"
            "   - Settings > Apps > Default Apps > Choose by file type\n"
            "   - Find .pdf > select preferred viewer\n"
            "5. Protected Mode:\n"
            "   - Adobe Reader: Edit > Preferences > Security (Enhanced)\n"
            "   - If PDFs from network fail: Uncheck 'Enable Protected Mode at startup'\n"
            "   - Also check: 'Enable Enhanced Security' may block some features\n"
            "6. Corrupted PDF:\n"
            "   - If only one PDF fails: The file may be corrupted or incomplete\n"
            "   - Re-download or request the file again\n"
            "   - Partial downloads cause blank/broken PDFs\n"
            "7. Browser PDF viewer: If downloading PDFs from Chrome: Settings > Privacy > Site settings > PDF documents > Download instead of open"
        ),
    },
    {
        "category": "Software",
        "problem_title": "AutoCAD or design software extremely slow or freezing",
        "problem_description": "CAD/design software (AutoCAD, Revit, SolidWorks) runs very slowly, freezes during operations, or takes long to open files.",
        "problem_keywords": "autocad slow, cad freeze, solidworks slow, revit slow, design software, 3d software slow, rendering slow",
        "solution_steps": (
            "1. Check system requirements:\n"
            "   - CAD software has specific GPU/RAM requirements\n"
            "   - AutoCAD: Certified GPU list at autodesk.com\n"
            "   - Minimum: 16 GB RAM, SSD, dedicated GPU\n"
            "2. GPU driver:\n"
            "   - Install the Studio/Professional driver (not Game Ready)\n"
            "   - NVIDIA: nvidia.com/drivers > Professional\n"
            "   - AMD: AMD Pro drivers\n"
            "   - CAD software relies heavily on GPU acceleration\n"
            "3. Hardware acceleration:\n"
            "   - AutoCAD: Options > System > Graphics Performance\n"
            "   - Ensure hardware acceleration is ON\n"
            "   - If it's off with a dedicated GPU: Driver issue\n"
            "4. File optimization:\n"
            "   - Purge unused elements: PURGE command in AutoCAD\n"
            "   - Audit the drawing: AUDIT command\n"
            "   - Reduce xrefs and imported geometry\n"
            "5. Disk performance:\n"
            "   - Work from a local SSD, not network drive\n"
            "   - Copy files locally, edit, then save back to network\n"
            "   - Temp files: Set temp directory to SSD\n"
            "6. Antivirus exclusions:\n"
            "   - Exclude .dwg, .rvt, .sldprt file extensions\n"
            "   - Exclude the application folder and temp directory\n"
            "   - Real-time scanning significantly impacts CAD performance\n"
            "7. Reset the application to defaults if settings may be corrupted"
        ),
    },
    {
        "category": "Software",
        "problem_title": "Windows Defender conflicts with third-party software",
        "problem_description": "Windows Defender blocks or quarantines legitimate software. Application files are deleted or executables won't run due to false positive detections.",
        "problem_keywords": "defender block, false positive, quarantine, exclusion, defender conflict, antivirus block, windows security",
        "solution_steps": (
            "1. Check quarantine:\n"
            "   - Windows Security > Virus & threat protection > Protection history\n"
            "   - Look for recent 'Quarantined' or 'Blocked' items\n"
            "   - Click the item to see details and file path\n"
            "2. Restore from quarantine:\n"
            "   - In Protection history > click the item > Actions > Restore\n"
            "   - File will be restored to original location\n"
            "3. Add an exclusion:\n"
            "   - Windows Security > Virus & threat protection > Manage settings\n"
            "   - Scroll to Exclusions > Add or remove exclusions\n"
            "   - Add: File, Folder, File type, or Process exclusion\n"
            "   - Recommended: Exclude the application folder\n"
            "4. Submit false positive to Microsoft:\n"
            "   - microsoft.com/wdsi > Submit a file for analysis\n"
            "   - Reports help Microsoft fix the false positive in future updates\n"
            "5. Controlled folder access:\n"
            "   - If apps can't save files: Look at 'Ransomware protection'\n"
            "   - Controlled folder access > Allow an app through\n"
            "   - Add the application executable\n"
            "6. Real-time protection:\n"
            "   - Temporarily toggle off for testing (turns back on automatically)\n"
            "   - If the app works with it off: Need a specific exclusion\n"
            "   - Do NOT leave real-time protection disabled permanently\n"
            "7. Group Policy: Admins can manage exclusions centrally via GPO or Intune"
        ),
    },
    {
        "category": "Software",
        "problem_title": "Chrome or browser using too much RAM and CPU",
        "problem_description": "Web browser consumes excessive RAM (multiple GB) and high CPU even with few tabs. System becomes sluggish due to browser resource consumption.",
        "problem_keywords": "chrome ram, browser memory, chrome slow, high cpu browser, too many tabs, browser resources, chrome cpu",
        "solution_steps": (
            "1. Check per-tab usage:\n"
            "   - Chrome: Shift+Esc opens Chrome Task Manager\n"
            "   - Shows memory and CPU per tab and extension\n"
            "   - Sort by Memory to find the biggest consumers\n"
            "2. Close unnecessary tabs:\n"
            "   - Each tab uses 50-300 MB of RAM\n"
            "   - 20+ tabs can easily consume 4+ GB\n"
            "   - Use tab groups or bookmark unused tabs\n"
            "3. Disable extensions:\n"
            "   - chrome://extensions > disable unused extensions\n"
            "   - Ad blockers, password managers, and dev tools use resources\n"
            "   - Keep only essential extensions\n"
            "4. Chrome settings:\n"
            "   - Settings > Performance > Memory Saver: Enable\n"
            "   - This hibernates inactive tabs\n"
            "   - Settings > Performance > Energy Saver: Enable on battery\n"
            "5. Hardware acceleration:\n"
            "   - Settings > System > Use hardware acceleration: Toggle\n"
            "   - ON: Offloads rendering to GPU (usually better)\n"
            "   - OFF: May help if GPU driver is problematic\n"
            "6. Clear browsing data:\n"
            "   - Ctrl+Shift+Del > Clear cache, cookies, browsing data\n"
            "   - Accumulated cache can slow down the browser\n"
            "7. Try browser alternatives: Edge uses less RAM than Chrome, Firefox is also efficient"
        ),
    },
    {
        "category": "Software",
        "problem_title": "Visual Studio Code or IDE very slow to start",
        "problem_description": "Code editor or IDE takes very long to start, is sluggish when editing, or extensions cause freezes.",
        "problem_keywords": "vscode slow, ide slow, visual studio slow, code editor, extensions slow, intellisense slow, ide freeze",
        "solution_steps": (
            "1. Disable unused extensions:\n"
            "   - Extensions view > disable extensions you don't actively use\n"
            "   - Use workspace-specific extensions (only enabled for relevant projects)\n"
            "   - Check: @installed in extensions search\n"
            "2. Check which extensions are slow:\n"
            "   - VS Code: Ctrl+Shift+P > 'Developer: Show Running Extensions'\n"
            "   - Shows activation time per extension\n"
            "   - Anything above 1000ms significantly impacts startup\n"
            "3. Large workspace:\n"
            "   - Exclude unnecessary folders from search/watchers\n"
            "   - .vscode/settings.json: 'files.exclude' and 'files.watcherExclude'\n"
            "   - Exclude: node_modules, .git, build, dist, venv\n"
            "4. Settings optimization:\n"
            "   - Disable minimap: 'editor.minimap.enabled': false\n"
            "   - Reduce file watchers: 'files.watcherExclude'\n"
            "   - Disable telemetry: 'telemetry.telemetryLevel': 'off'\n"
            "5. VS Code cache:\n"
            "   - Corrupted cache can slow down VS Code\n"
            "   - Delete: %appdata%\\Code\\Cache\n"
            "   - Delete: %appdata%\\Code\\CachedData\n"
            "6. For Visual Studio (not Code):\n"
            "   - devenv /SafeMode (start without extensions)\n"
            "   - Clear component cache: %localappdata%\\Microsoft\\VisualStudio\n"
            "7. Hardware: SSD is essential for IDE performance - HDD causes major slowdowns"
        ),
    },
    {
        "category": "Software",
        "problem_title": "QuickBooks database server manager not running",
        "problem_description": "QuickBooks multi-user mode doesn't work because the Database Server Manager service is stopped or not installed on the server.",
        "problem_keywords": "quickbooks database, server manager, multi-user, quickbooks server, qbdbmgrn, quickbooks service, database manager",
        "solution_steps": (
            "1. Check the service:\n"
            "   - services.msc > look for 'QuickBooksDBXX' (XX = year/version)\n"
            "   - Should be Running and set to Automatic\n"
            "   - If stopped: Right-click > Start\n"
            "2. Install Database Server Manager:\n"
            "   - On the server/host PC: Run QuickBooks installer\n"
            "   - Select 'Custom' installation\n"
            "   - Check 'Database Server Manager' option\n"
            "3. Firewall ports:\n"
            "   - QuickBooks needs these ports open:\n"
            "   - TCP 8019 (QB 2020+), dynamic ports for older versions\n"
            "   - QuickBooks Database Server Manager port\n"
            "   - Run QuickBooks File Doctor to auto-configure firewall\n"
            "4. Scan folders:\n"
            "   - Open QuickBooks Database Server Manager\n"
            "   - Scan the folder where company files (.QBW) are stored\n"
            "   - This creates the .ND file needed for multi-user access\n"
            "5. Permissions:\n"
            "   - The QBDataServiceUserXX user needs full control over the company file folder\n"
            "   - Right-click folder > Properties > Security > Edit > Add the QB user\n"
            "6. File location:\n"
            "   - Company file should be on a local or mapped drive (not UNC path)\n"
            "   - Do NOT host the file on a NAS without official support\n"
            "7. QuickBooks File Doctor: Download from Intuit - fixes most connectivity issues"
        ),
    },
    {
        "category": "Software",
        "problem_title": "Java application not running or wrong Java version",
        "problem_description": "Java application fails to start or shows 'unsupported version' errors. Multiple Java versions installed cause conflicts.",
        "problem_keywords": "java version, jre, jdk, java not found, java error, wrong java, java conflict, java update",
        "solution_steps": (
            "1. Check installed Java versions:\n"
            "   - CMD: java -version (shows default version)\n"
            "   - Control Panel > Programs > look for Java entries\n"
            "   - Multiple versions may be installed\n"
            "2. Common version issues:\n"
            "   - App requires Java 8 but Java 11+ is installed\n"
            "   - App requires 64-bit but 32-bit Java is default\n"
            "   - Check application requirements documentation\n"
            "3. Set Java version:\n"
            "   - JAVA_HOME environment variable: System > Advanced > Environment Variables\n"
            "   - Set JAVA_HOME to the correct JDK/JRE path\n"
            "   - Update PATH to include %JAVA_HOME%\\bin\n"
            "4. Multiple Java installations:\n"
            "   - Remove unneeded Java versions from Control Panel\n"
            "   - Keep only the versions required by your applications\n"
            "   - Java Control Panel > Java tab shows installed JREs\n"
            "5. Java Control Panel settings:\n"
            "   - Security tab: Adjust security level if legacy apps are blocked\n"
            "   - Exception Site List: Add trusted application URLs\n"
            "6. Web browser Java (NPAPI):\n"
            "   - Modern browsers no longer support Java applets\n"
            "   - Use Internet Explorer 11 if Java applets are required\n"
            "   - Better: Ask vendor for a non-Java alternative\n"
            "7. Classpath issues: Set CLASSPATH environment variable if application requires specific JARs"
        ),
    },
    {
        "category": "Software",
        "problem_title": "VPN client software connection drops repeatedly",
        "problem_description": "VPN client connects but disconnects after a few minutes. Connection is unstable and reconnecting doesn't help long-term.",
        "problem_keywords": "vpn disconnect, vpn drops, vpn unstable, vpn reconnect, vpn client, vpn timeout, vpn connection",
        "solution_steps": (
            "1. Check VPN client version:\n"
            "   - Update to the latest version of the VPN client\n"
            "   - Common clients: Cisco AnyConnect, GlobalProtect, FortiClient, WireGuard\n"
            "   - Older versions may have bugs causing disconnects\n"
            "2. Network stability:\n"
            "   - VPN drops often caused by underlying network instability\n"
            "   - Test with ping -t to an external IP while on VPN\n"
            "   - Watch for timeouts or high latency spikes\n"
            "3. Timeout settings:\n"
            "   - VPN server may have an idle timeout\n"
            "   - Keep the connection active with periodic traffic\n"
            "   - Check VPN client: Settings > Keepalive/Dead Peer Detection\n"
            "4. MTU issues:\n"
            "   - VPN adds overhead, reducing effective MTU\n"
            "   - Try reducing MTU on the VPN adapter to 1300-1400\n"
            "   - netsh interface ipv4 set subinterface \"VPN Adapter\" mtu=1300\n"
            "5. Conflict with other software:\n"
            "   - Multiple VPN clients installed can conflict\n"
            "   - Windows Firewall or third-party firewall blocking VPN traffic\n"
            "   - Disable/uninstall other VPN clients\n"
            "6. Power management:\n"
            "   - Wi-Fi adapter power saving can disconnect VPN\n"
            "   - Device Manager > Wi-Fi > Power Management > uncheck 'Allow turn off'\n"
            "7. Try a different protocol: Switch between IKEv2, OpenVPN, WireGuard, or SSL"
        ),
    },
    {
        "category": "Software",
        "problem_title": "Printer driver software conflicts or spooler errors",
        "problem_description": "Print spooler crashes or shows errors after installing printer software. Multiple printer drivers may conflict with each other.",
        "problem_keywords": "print spooler, spooler error, spooler crash, printer driver conflict, spooler service, print driver, spoolsv",
        "solution_steps": (
            "1. Restart Print Spooler:\n"
            "   - services.msc > 'Print Spooler' > Restart\n"
            "   - Or CMD: net stop spooler; net start spooler\n"
            "2. Clear the print queue:\n"
            "   - Stop the Print Spooler service\n"
            "   - Delete all files in: C:\\Windows\\System32\\spool\\PRINTERS\n"
            "   - Start the Print Spooler service\n"
            "3. Remove conflicting drivers:\n"
            "   - printmanagement.msc > All Drivers\n"
            "   - Remove duplicate or old drivers\n"
            "   - Particularly watch for multiple versions of the same manufacturer\n"
            "4. Clean driver installation:\n"
            "   - Remove printer from Settings > Devices > Printers\n"
            "   - Remove driver from Print Management\n"
            "   - Uninstall printer software from Settings > Apps\n"
            "   - Restart and install fresh\n"
            "5. Type 3 vs Type 4 drivers:\n"
            "   - Type 3: Runs in spooler process (crash affects all printers)\n"
            "   - Type 4: Isolated (crash affects only that printer)\n"
            "   - When possible, use Type 4 drivers\n"
            "6. Event Viewer:\n"
            "   - System > source 'Print' or 'Spooler'\n"
            "   - Check which driver/DLL is causing the crash\n"
            "7. Driver isolation: Print Management > Driver > Isolated (runs driver in separate process)"
        ),
    },
    {
        "category": "Software",
        "problem_title": "Antivirus scan taking too long or high CPU",
        "problem_description": "Full antivirus scan takes hours, consumes 100% CPU, and makes the system unusable during scanning.",
        "problem_keywords": "antivirus slow, scan slow, antivirus cpu, scan taking long, defender scan, full scan, antivirus performance",
        "solution_steps": (
            "1. Schedule scans for off-hours:\n"
            "   - Windows Security > Virus & threat protection > Scan options\n"
            "   - Task Scheduler > Microsoft > Windows > Windows Defender\n"
            "   - Modify trigger to run at night or during lunch\n"
            "2. Use Quick Scan instead of Full:\n"
            "   - Quick Scan checks common malware locations only\n"
            "   - Full Scan checks every file on every drive (hours)\n"
            "   - Quick Scan daily + Full Scan weekly is sufficient\n"
            "3. Exclude safe folders:\n"
            "   - Large data drives with known-safe content\n"
            "   - Development folders (node_modules, .git, build)\n"
            "   - Virtual machine disk files\n"
            "   - Windows Security > Virus & threat > Manage settings > Exclusions\n"
            "4. Limit CPU usage:\n"
            "   - PowerShell: Set-MpPreference -ScanAvgCPULoadFactor 50 (limit to 50%)\n"
            "   - Default is 50%, but it can be set lower for less impact\n"
            "   - Lower value = longer scan but less performance impact\n"
            "5. SSD vs HDD:\n"
            "   - Full scans on HDD take much longer than SSD\n"
            "   - If multiple drives: Larger drives take proportionally longer\n"
            "6. Third-party antivirus:\n"
            "   - Check the antivirus settings for similar CPU/scheduling controls\n"
            "   - Ensure only ONE antivirus is active (don't run two simultaneously)\n"
            "7. Group Policy: Admins can set scan schedules and CPU limits via GPO"
        ),
    },
    {
        "category": "Software",
        "problem_title": "Office 365 apps not updating or update errors",
        "problem_description": "Microsoft 365 apps show 'Update Failed' or are stuck on an old version. Automatic updates don't seem to work.",
        "problem_keywords": "office update, office 365 update, update failed, office version, click to run, office outdated, update error",
        "solution_steps": (
            "1. Check current version:\n"
            "   - Any Office app > File > Account\n"
            "   - Shows: Version and Build number\n"
            "   - Update Channel: Monthly, Semi-Annual, etc.\n"
            "2. Manual update:\n"
            "   - File > Account > Update Options > Update Now\n"
            "   - If greyed out: Updates may be managed by IT\n"
            "3. Update from command line:\n"
            "   - Open elevated CMD\n"
            "   - cd \"C:\\Program Files\\Common Files\\Microsoft Shared\\ClickToRun\"\n"
            "   - OfficeC2RClient.exe /update user\n"
            "4. Click-to-Run service:\n"
            "   - services.msc > 'Microsoft Office Click-to-Run Service'\n"
            "   - Must be Running and set to Automatic\n"
            "   - Restart the service if stuck\n"
            "5. Network issues:\n"
            "   - Updates download from Office CDN (officecdn.microsoft.com)\n"
            "   - Ensure this URL isn't blocked by proxy/firewall\n"
            "   - Large updates (~1-2 GB) may fail on slow connections\n"
            "6. Repair Office:\n"
            "   - Settings > Apps > Microsoft 365 > Modify > Quick Repair\n"
            "   - If that fails: Online Repair (requires internet)\n"
            "7. Group Policy: Update channel and frequency can be set by admins via GPO or Intune"
        ),
    },
    {
        "category": "Software",
        "problem_title": "Database application (SQL/Access) connection timeout",
        "problem_description": "Application shows database connection timeout errors. Queries that used to work now fail with timeout exceptions.",
        "problem_keywords": "database timeout, sql timeout, connection timeout, query timeout, database slow, sql connection, access database",
        "solution_steps": (
            "1. Connection vs Query timeout:\n"
            "   - Connection timeout: Can't establish the connection at all\n"
            "   - Query timeout: Connected but query takes too long\n"
            "   - Different solutions for each\n"
            "2. Connection timeout:\n"
            "   - Check if the database server is reachable: ping servername\n"
            "   - Check port: Test-NetConnection -ComputerName server -Port 1433 (SQL)\n"
            "   - Firewall rules on the server may block connections\n"
            "3. Query timeout:\n"
            "   - The query is running too long\n"
            "   - Increase timeout in application/connection string\n"
            "   - Optimize the query: Add indexes, reduce data returned\n"
            "4. SQL Server specific:\n"
            "   - SQL Server Configuration Manager > TCP/IP must be enabled\n"
            "   - SQL Browser service must be running for named instances\n"
            "   - Check if SQL Server is set to allow remote connections\n"
            "5. Access database:\n"
            "   - Compact and Repair the database: Database Tools > Compact and Repair\n"
            "   - Large Access files (>1 GB) become very slow\n"
            "   - Consider migrating to SQL Server or Azure SQL\n"
            "6. Network latency:\n"
            "   - High latency between app and database causes timeouts\n"
            "   - tracert to the database server\n"
            "   - VPN connections add latency\n"
            "7. Increase timeout: Connection string > 'Connection Timeout=60' or 'CommandTimeout=120'"
        ),
    },
    {
        "category": "Software",
        "problem_title": "Windows font rendering or DPI scaling issues in applications",
        "problem_description": "Applications display blurry text, tiny fonts, or oversized UI elements due to DPI scaling. Common on high-resolution (4K) monitors.",
        "problem_keywords": "dpi scaling, blurry text, font rendering, 4k scaling, high dpi, fuzzy text, small text, display scaling",
        "solution_steps": (
            "1. Windows DPI scaling:\n"
            "   - Settings > System > Display > Scale and layout\n"
            "   - Recommended: 100% (1080p), 125% (1440p), 150-200% (4K)\n"
            "   - Use the recommended percentage\n"
            "2. Per-application DPI fix:\n"
            "   - Right-click the application .exe > Properties > Compatibility\n"
            "   - 'Change high DPI settings'\n"
            "   - Check 'Override high DPI scaling behavior'\n"
            "   - Scaling performed by: System (Enhanced)\n"
            "3. ClearType:\n"
            "   - Search 'ClearType' > 'Adjust ClearType text'\n"
            "   - Follow the wizard to tune font rendering\n"
            "   - Rerun after changing monitors\n"
            "4. Mixed DPI monitors:\n"
            "   - Windows handles mixed DPI monitors poorly for some apps\n"
            "   - Try: Settings > Display > Advanced scaling settings\n"
            "   - 'Let Windows try to fix apps so they're not blurry'\n"
            "5. Specific application fixes:\n"
            "   - Java apps: -Dsun.java2d.dpiaware=false\n"
            "   - Older .NET apps: Add dpiAware manifest\n"
            "   - Electron apps: Usually DPI-aware by default\n"
            "6. Remote Desktop:\n"
            "   - RDP scaling issues: See Remote Desktop scaling article\n"
            "7. Sign out and back in after changing scaling (some apps require it)"
        ),
    },
    {
        "category": "Software",
        "problem_title": "Java Runtime Environment version conflicts or not detected",
        "problem_description": "Applications requiring Java fail to launch, show 'Java not found' errors, or use the wrong Java version despite having JRE/JDK installed.",
        "problem_keywords": "java, jre, jdk, java version, java not found, java runtime, java conflict, java home",
        "solution_steps": (
            "1. Check installed Java versions:\n"
            "   - Command Prompt: java -version\n"
            "   - PowerShell: Get-Command java | Format-List\n"
            "   - Check both: C:\\Program Files\\Java and C:\\Program Files (x86)\\Java\n"
            "2. JAVA_HOME environment variable:\n"
            "   - System Properties > Environment Variables\n"
            "   - Set JAVA_HOME to correct JDK/JRE path\n"
            "   - Add %JAVA_HOME%\\bin to PATH\n"
            "3. PATH order matters:\n"
            "   - Multiple Java installations: PATH determines which runs\n"
            "   - Move desired Java path entry above others\n"
            "   - Remove old Java paths from PATH\n"
            "4. 32-bit vs 64-bit:\n"
            "   - Some apps require 32-bit Java specifically\n"
            "   - Both can coexist: Program Files (64-bit), Program Files (x86) (32-bit)\n"
            "5. Clean install: Uninstall all Java versions, reboot, install only the required version(s)"
        ),
    },
    {
        "category": "Software",
        "problem_title": "Windows Store apps fail to install or update",
        "problem_description": "Microsoft Store apps won't install, update, or download. Store shows error codes, gets stuck on 'Pending' or 'Starting download', or Store itself won't open.",
        "problem_keywords": "microsoft store, windows store, store error, app install, store pending, store download, wsreset, store update",
        "solution_steps": (
            "1. Reset Microsoft Store cache:\n"
            "   - Win+R > wsreset.exe > click OK\n"
            "   - Wait for blank command window to close and Store to open\n"
            "2. Check Windows Update:\n"
            "   - Store apps depend on Windows Update service\n"
            "   - Settings > Update & Security > Check for updates\n"
            "   - Install all pending updates\n"
            "3. Re-register Store:\n"
            "   - PowerShell (Admin):\n"
            "   - Get-AppxPackage Microsoft.WindowsStore | Foreach {Add-AppxPackage -Register \"$($_.InstallLocation)\\AppxManifest.xml\" -DisableDevelopmentMode}\n"
            "4. Check account:\n"
            "   - Sign out and back into Microsoft Store\n"
            "   - Ensure using correct Microsoft account\n"
            "   - Check: Settings > Accounts > Email & accounts\n"
            "5. Group Policy: Computer Config > Admin Templates > Windows Components > Store > check if 'Turn off the Store' is enabled (common in enterprise)"
        ),
    },
    {
        "category": "Software",
        "problem_title": "Software license activation or deactivation failures",
        "problem_description": "Software product activation fails, shows 'license expired' or 'activation limit reached'. Need to transfer license to new computer or reactivate after hardware change.",
        "problem_keywords": "license activation, product key, activation failed, license expired, license transfer, deactivate license, activation limit, product activation",
        "solution_steps": (
            "1. Common activation errors:\n"
            "   - 'Activation limit reached': Deactivate on old machine first\n"
            "   - 'Invalid product key': Check for typos, correct edition\n"
            "   - 'License expired': Renew subscription or enter new key\n"
            "2. Windows activation:\n"
            "   - Settings > Update & Security > Activation\n"
            "   - slmgr /ato (force activation attempt)\n"
            "   - slmgr /dlv (display license info)\n"
            "   - KMS: Ensure network connectivity to KMS server\n"
            "3. Office activation:\n"
            "   - File > Account > Activation status\n"
            "   - Sign out and sign back in with licensed account\n"
            "   - cscript ospp.vbs /dstatus (check license status)\n"
            "4. Transfer license:\n"
            "   - Deactivate on old machine before activating on new\n"
            "   - Some software: Online portal to manage device activations\n"
            "5. Contact vendor: If self-service fails, contact software vendor support with proof of purchase for manual activation reset"
        ),
    },
    {
        "category": "Software",
        "problem_title": "Browser extensions causing performance or security issues",
        "problem_description": "Browser runs slowly, displays unwanted ads, redirects searches, or shows security warnings after installing extensions. Potentially unwanted extensions affecting browser behavior.",
        "problem_keywords": "browser extension, chrome extension, edge addon, browser slow, adware, browser redirect, unwanted extension, browser hijack",
        "solution_steps": (
            "1. Identify problematic extensions:\n"
            "   - Chrome: chrome://extensions/\n"
            "   - Edge: edge://extensions/\n"
            "   - Firefox: about:addons\n"
            "   - Disable all extensions, re-enable one at a time\n"
            "2. Remove suspicious extensions:\n"
            "   - Look for: recently installed, unfamiliar names\n"
            "   - Check permissions: Extensions requesting excessive access\n"
            "   - Remove anything you didn't intentionally install\n"
            "3. Reset browser:\n"
            "   - Chrome: Settings > Reset settings > Restore to defaults\n"
            "   - Edge: Settings > Reset settings\n"
            "   - This removes extensions and resets settings but keeps bookmarks\n"
            "4. Enterprise policy:\n"
            "   - Group Policy: Force-install approved extensions only\n"
            "   - Block extension installs: ExtensionInstallBlocklist = *\n"
            "   - Allowlist specific extensions: ExtensionInstallAllowlist\n"
            "5. Anti-malware scan: Run full scan with Windows Defender or enterprise AV to catch browser-hijacking malware"
        ),
    },
]

DIAGNOSTIC_TREE = {
    "category": "Software",
    "root": {
        "title": "Software Troubleshooting",
        "node_type": "question",
        "question_text": "What type of software problem are you experiencing?",
        "children": [
            {
                "title": "Microsoft Office issues",
                "node_type": "question",
                "question_text": "What's wrong with Office?",
                "children": [
                    {
                        "title": "Office won't activate / shows Unlicensed",
                        "node_type": "solution",
                        "solution_text": "1. Sign in with correct Microsoft account: File > Account\n2. Clear credentials: Control Panel > Credential Manager > remove office/microsoft entries\n3. Reset licensing: Close all Office apps > re-sign in\n4. Repair Office: Settings > Apps > Microsoft Office > Modify > Quick Repair\n5. For M365: Use Microsoft Support and Recovery Assistant (SaRA)\n6. Uninstall and reinstall from office.com"
                    },
                    {
                        "title": "Office is slow or freezing",
                        "node_type": "solution",
                        "solution_text": "1. Disable add-ins: File > Options > Add-ins > COM Add-ins > disable all\n2. Move file to local drive (not network/cloud during editing)\n3. Repair Office: Settings > Apps > Office > Modify > Quick Repair\n4. Disable Protected View for internal files\n5. For Excel: Set calculation to Manual if many formulas\n6. Clear Office cache: %localappdata%\\Microsoft\\Office\\16.0\\OfficeFileCache\n7. Update Office to latest version"
                    },
                    {
                        "title": "Document is corrupt",
                        "node_type": "solution",
                        "solution_text": "1. Open and Repair: File > Open > select file > dropdown > Open and Repair\n2. Check AutoRecover location for backups: File > Options > Save\n3. Right-click file > Previous Versions\n4. Check OneDrive/SharePoint version history\n5. Try opening in LibreOffice\n6. For .xlsx: rename to .zip and extract data from xl/worksheets\n7. Use third-party repair tools as last resort"
                    }
                ]
            },
            {
                "title": "Application won't install",
                "node_type": "solution",
                "solution_text": "1. Run installer as Administrator\n2. Check for sufficient disk space\n3. If 'another installation in progress': Restart Windows Installer service\n4. Disable antivirus temporarily\n5. Try installing in Clean Boot: msconfig > disable non-Microsoft services\n6. Install required prerequisites (Visual C++, .NET, DirectX)\n7. Check installer log for specific errors\n8. Download fresh installer from official source"
            },
            {
                "title": "Application crashes / won't run",
                "node_type": "question",
                "question_text": "What error do you see?",
                "children": [
                    {
                        "title": "0xc000007b error",
                        "node_type": "solution",
                        "solution_text": "This is a 32/64-bit mismatch or missing runtime:\n1. Install ALL Visual C++ Redistributables (2010-2022, both x86 and x64)\n2. Install DirectX End-User Runtime from Microsoft\n3. Install .NET Framework (required version)\n4. Run sfc /scannow to repair system files\n5. Try the 32-bit version of the application if available\n6. Reinstall the application"
                    },
                    {
                        "title": "Other error or no error message",
                        "node_type": "solution",
                        "solution_text": "1. Update the application to latest version\n2. Run as Administrator\n3. Try Compatibility Mode: right-click > Properties > Compatibility\n4. Clear app cache in %appdata% and %localappdata%\n5. Check Event Viewer > Application log for crash details\n6. Reinstall Visual C++ Redistributables\n7. Run sfc /scannow\n8. Fully uninstall and reinstall the application\n9. Test in a new Windows user profile"
                    }
                ]
            },
            {
                "title": "Browser issues",
                "node_type": "solution",
                "solution_text": "1. Disable extensions: They are the #1 cause of browser issues\n2. Clear cache and cookies: Ctrl+Shift+Del > All time\n3. Disable hardware acceleration in browser settings\n4. Reset browser to defaults\n5. Check for adware/malware: Run Malwarebytes scan\n6. Update browser to latest version\n7. Try a different browser to compare\n8. If all browsers slow: Check network connection"
            },
            {
                "title": "Teams not working",
                "node_type": "solution",
                "solution_text": "1. Clear Teams cache:\n   - Close Teams completely\n   - Delete: %appdata%\\Microsoft\\Teams (old Teams)\n   - Or: %localappdata%\\Packages\\MSTeams_* (new Teams)\n2. Clear credentials in Credential Manager\n3. Disable GPU acceleration in Teams settings\n4. Check date/time is correct\n5. Test in browser: teams.microsoft.com\n6. Update Teams\n7. Fully uninstall, delete cache folders, reinstall"
            }
        ]
    }
}
