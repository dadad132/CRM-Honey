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
