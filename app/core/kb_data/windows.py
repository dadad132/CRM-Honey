"""Windows OS troubleshooting articles and diagnostic tree."""

ARTICLES = [
    {
        "category": "Windows",
        "problem_title": "Blue Screen KERNEL_DATA_INPAGE_ERROR",
        "problem_description": "Computer crashes with blue screen showing KERNEL_DATA_INPAGE_ERROR (0x0000007A). May happen during boot or randomly during use.",
        "problem_keywords": "blue screen, BSOD, KERNEL_DATA_INPAGE_ERROR, 0x0000007A, crash, disk error",
        "solution_steps": (
            "1. This error usually indicates a disk or RAM problem\n"
            "2. Check disk health:\n"
            "   - Open CMD as Admin: chkdsk C: /f /r\n"
            "   - Reboot to run the scan\n"
            "   - Check SMART status: wmic diskdrive get status\n"
            "3. Test RAM:\n"
            "   - Run Windows Memory Diagnostic: mdsched.exe\n"
            "   - Choose 'Restart now and check for problems'\n"
            "4. Check for driver issues:\n"
            "   - Boot into Safe Mode (hold Shift while clicking Restart)\n"
            "   - If stable in Safe Mode, a driver is likely the cause\n"
            "   - Update storage controller and disk drivers\n"
            "5. Check Event Viewer for disk errors:\n"
            "   - Look for Event ID 7, 11, or 51 under System log\n"
            "6. If disk is failing, back up data immediately and replace the drive\n"
            "7. Disable pagefile temporarily to test: System Properties > Advanced > Performance > Virtual Memory"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Blue Screen IRQL_NOT_LESS_OR_EQUAL",
        "problem_description": "Windows crashes with IRQL_NOT_LESS_OR_EQUAL blue screen error. Often happens after installing new hardware or drivers.",
        "problem_keywords": "blue screen, IRQL_NOT_LESS_OR_EQUAL, BSOD, driver crash, 0x0000000A",
        "solution_steps": (
            "1. This is almost always a driver issue\n"
            "2. If it started after a recent change, undo that change:\n"
            "   - Boot Safe Mode (hold Shift + Restart > Troubleshoot > Startup Settings)\n"
            "   - Uninstall recently added drivers or software\n"
            "3. Update drivers (especially network, graphics, and chipset):\n"
            "   - Open Device Manager > right-click each device > Update driver\n"
            "   - Download latest drivers from manufacturer website\n"
            "4. Run Driver Verifier to find the faulting driver:\n"
            "   - CMD (Admin): verifier /standard /all\n"
            "   - Reboot - Windows will crash and identify the bad driver\n"
            "   - Disable verifier after: verifier /reset\n"
            "5. Check for Windows updates\n"
            "6. Run SFC: sfc /scannow\n"
            "7. Run DISM: DISM /Online /Cleanup-Image /RestoreHealth\n"
            "8. Test RAM with Windows Memory Diagnostic (mdsched.exe)"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Blue Screen CRITICAL_PROCESS_DIED",
        "problem_description": "Windows shows CRITICAL_PROCESS_DIED blue screen. Computer may enter a boot loop or crash repeatedly.",
        "problem_keywords": "blue screen, CRITICAL_PROCESS_DIED, boot loop, BSOD, cannot boot",
        "solution_steps": (
            "1. Boot into Safe Mode:\n"
            "   - Power on, force power off 3 times to trigger WinRE\n"
            "   - Troubleshoot > Advanced > Startup Settings > Enable Safe Mode\n"
            "2. In Safe Mode:\n"
            "   - Uninstall recent Windows updates: Settings > Update > View update history > Uninstall\n"
            "   - Uninstall recently installed software\n"
            "   - Update all drivers\n"
            "3. Run system file repair:\n"
            "   - CMD (Admin): sfc /scannow\n"
            "   - Then: DISM /Online /Cleanup-Image /RestoreHealth\n"
            "4. Check disk: chkdsk C: /f /r\n"
            "5. Use System Restore:\n"
            "   - WinRE > Troubleshoot > Advanced > System Restore\n"
            "   - Pick a restore point before the issue started\n"
            "6. If still failing, run Startup Repair:\n"
            "   - WinRE > Troubleshoot > Advanced > Startup Repair\n"
            "7. Last resort: Reset PC keeping files:\n"
            "   - Settings > Recovery > Reset this PC > Keep my files"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Blue Screen WHEA_UNCORRECTABLE_ERROR",
        "problem_description": "Blue screen with WHEA_UNCORRECTABLE_ERROR stop code. Often related to hardware failures - CPU, RAM, or hard drive.",
        "problem_keywords": "WHEA_UNCORRECTABLE_ERROR, BSOD, hardware error, 0x00000124, CPU error, overheating",
        "solution_steps": (
            "1. WHEA errors typically indicate a real hardware fault\n"
            "2. Check for overheating:\n"
            "   - Clean dust from CPU fan, case fans, and heatsink\n"
            "   - Monitor CPU temperature with HWiNFO64 or Core Temp\n"
            "   - CPU above 90°C under load = cooling problem\n"
            "   - Replace thermal paste if dried out\n"
            "3. Test RAM:\n"
            "   - Run mdsched.exe (Windows Memory Diagnostic)\n"
            "   - For extended test: Download and run MemTest86 (boots from USB)\n"
            "   - If errors found: replace faulty RAM stick\n"
            "4. Check disk health:\n"
            "   - CMD: wmic diskdrive get status\n"
            "   - Install CrystalDiskInfo for detailed SMART data\n"
            "5. If overclocked:\n"
            "   - Reset CPU/RAM to default speeds in BIOS\n"
            "   - Overclocking is a common cause of WHEA errors\n"
            "6. Update BIOS/UEFI from manufacturer website\n"
            "7. Update chipset drivers\n"
            "8. Check Event Viewer > System for WHEA-Logger events with hardware details"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Blue Screen PAGE_FAULT_IN_NONPAGED_AREA",
        "problem_description": "Blue screen crash with PAGE_FAULT_IN_NONPAGED_AREA. May mention a specific driver file (.sys) as the cause.",
        "problem_keywords": "PAGE_FAULT_IN_NONPAGED_AREA, BSOD, blue screen, 0x00000050, bad RAM, driver fault",
        "solution_steps": (
            "1. Note the driver file name mentioned on the blue screen (e.g., ntfs.sys, win32k.sys)\n"
            "2. If a specific .sys file is named:\n"
            "   - Search online for which driver/software owns that file\n"
            "   - Update or uninstall that driver/software\n"
            "3. Test RAM - this BSOD is commonly caused by faulty memory:\n"
            "   - Run mdsched.exe > Restart and check\n"
            "   - If errors found, test each RAM stick individually\n"
            "4. Run SFC and DISM:\n"
            "   - sfc /scannow\n"
            "   - DISM /Online /Cleanup-Image /RestoreHealth\n"
            "5. Check disk: chkdsk C: /f /r\n"
            "6. Disable automatic pagefile and set a fixed size:\n"
            "   - System Properties > Advanced > Performance > Virtual Memory > Custom size\n"
            "7. Boot to Safe Mode and test stability - if stable, a driver is the cause\n"
            "8. Use WinDbg to analyze the crash dump file (C:\\Windows\\Minidump\\) for exact cause"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Blue Screen SYSTEM_SERVICE_EXCEPTION",
        "problem_description": "Blue screen with SYSTEM_SERVICE_EXCEPTION, often mentioning driver files like ks.sys, dxgkrnl.sys, ntfs.sys, or win32k.sys.",
        "problem_keywords": "SYSTEM_SERVICE_EXCEPTION, BSOD, ks.sys, dxgkrnl.sys, ntfs.sys, 0x0000003B",
        "solution_steps": (
            "1. Note the driver name on the BSOD (e.g., dxgkrnl.sys = display driver)\n"
            "2. Common culprits and fixes:\n"
            "   - dxgkrnl.sys / dxgmms1.sys: Update graphics driver from NVIDIA/AMD/Intel\n"
            "   - ks.sys: Webcam or audio driver issue - update or disable\n"
            "   - ntfs.sys: Disk issue - run chkdsk C: /f /r\n"
            "   - win32k.sys: Display or font issue - update Windows and display driver\n"
            "   - netio.sys: Network driver issue - update network adapter driver\n"
            "3. Update all drivers to latest version from manufacturer\n"
            "4. Run SFC: sfc /scannow\n"
            "5. Run DISM: DISM /Online /Cleanup-Image /RestoreHealth\n"
            "6. Check for recently installed software and uninstall it\n"
            "7. Update Windows to latest version\n"
            "8. If caused by antivirus: temporarily uninstall third-party antivirus"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Windows Update stuck or failing",
        "problem_description": "Windows Update downloads get stuck at a percentage, fail with error codes, or the update keeps retrying and failing.",
        "problem_keywords": "windows update, update stuck, update failed, update error, 0x80070002, 0x80073712, 0x800f081f",
        "solution_steps": (
            "1. Run the Windows Update Troubleshooter:\n"
            "   - Settings > Update & Security > Troubleshoot > Windows Update\n"
            "2. Reset Windows Update components:\n"
            "   - Open CMD as Admin and run:\n"
            "   - net stop wuauserv\n"
            "   - net stop cryptSvc\n"
            "   - net stop bits\n"
            "   - net stop msiserver\n"
            "   - ren C:\\Windows\\SoftwareDistribution SoftwareDistribution.old\n"
            "   - ren C:\\Windows\\System32\\catroot2 catroot2.old\n"
            "   - net start wuauserv\n"
            "   - net start cryptSvc\n"
            "   - net start bits\n"
            "   - net start msiserver\n"
            "3. Repair system files:\n"
            "   - sfc /scannow\n"
            "   - DISM /Online /Cleanup-Image /RestoreHealth\n"
            "4. Free up disk space (at least 20GB on C: drive)\n"
            "5. Temporarily disable antivirus\n"
            "6. Download the update manually from Microsoft Update Catalog (catalog.update.microsoft.com)\n"
            "7. Check the C:\\Windows\\Logs\\CBS\\CBS.log for specific error details"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Windows Update error 0x80070005 - Access Denied",
        "problem_description": "Windows Update fails with error 0x80070005 (E_ACCESSDENIED). Updates cannot be downloaded or installed.",
        "problem_keywords": "0x80070005, access denied, windows update error, update permission, update access denied",
        "solution_steps": (
            "1. Run Windows Update as Administrator:\n"
            "   - You must be logged in as a local Administrator\n"
            "2. Reset Windows Update permissions:\n"
            "   - CMD (Admin):\n"
            "   - net stop wuauserv\n"
            "   - icacls C:\\Windows\\SoftwareDistribution /reset /T /C\n"
            "   - net start wuauserv\n"
            "3. Check the Windows Update service account:\n"
            "   - services.msc > Windows Update > Properties > Log On tab\n"
            "   - Should be 'Local System' - change if different\n"
            "4. Run the System File Checker:\n"
            "   - sfc /scannow\n"
            "5. Check that the date and time are correct\n"
            "6. Temporarily disable third-party antivirus\n"
            "7. Check Group Policy:\n"
            "   - gpedit.msc > Computer Config > Admin Templates > Windows Components > Windows Update\n"
            "   - Ensure no restrictive policies are set\n"
            "8. Re-register DLL files:\n"
            "   - CMD (Admin): regsvr32 wuapi.dll && regsvr32 wuaueng.dll && regsvr32 wups.dll"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Computer running very slow",
        "problem_description": "Windows is running extremely slowly. Applications take a long time to open, high disk or CPU usage in Task Manager.",
        "problem_keywords": "slow computer, slow pc, high cpu, high disk, 100% disk, slow performance, lag",
        "solution_steps": (
            "1. Open Task Manager (Ctrl+Shift+Esc) and check which process uses the most CPU/Disk/Memory\n"
            "2. If disk is at 100%:\n"
            "   - Disable Superfetch/SysMain: services.msc > SysMain > Disable\n"
            "   - Disable Windows Search indexer: services.msc > Windows Search > Disable\n"
            "   - Check disk health: wmic diskdrive get status\n"
            "   - Consider upgrading to SSD if using HDD\n"
            "3. Disable startup programs:\n"
            "   - Task Manager > Startup tab > Disable unnecessary programs\n"
            "4. Run disk cleanup:\n"
            "   - Type 'Disk Cleanup' > Clean up system files > Check all boxes\n"
            "5. Check for malware:\n"
            "   - Run Windows Defender full scan\n"
            "   - Download and run Malwarebytes free scan\n"
            "6. Disable visual effects:\n"
            "   - System Properties > Advanced > Performance > Adjust for best performance\n"
            "7. Check RAM usage - if consistently above 80%, consider adding more RAM\n"
            "8. Uninstall programs you don't use\n"
            "9. Run SFC: sfc /scannow\n"
            "10. Defragment HDD (not SSD): dfrgui.exe"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Start Menu not opening or not working",
        "problem_description": "Clicking the Start button does nothing. Start Menu won't open, or opens but freezes/crashes immediately.",
        "problem_keywords": "start menu, start button, start not working, taskbar, start broken",
        "solution_steps": (
            "1. Quick fix - restart Windows Explorer:\n"
            "   - Ctrl+Shift+Esc > find Windows Explorer > right-click > Restart\n"
            "2. Re-register Start Menu apps:\n"
            "   - Open PowerShell as Admin:\n"
            "   - Get-AppXPackage -AllUsers | Foreach {Add-AppxPackage -DisableDevelopmentMode -Register \"$($_.InstallLocation)\\AppXManifest.xml\"}\n"
            "3. Run SFC and DISM:\n"
            "   - CMD (Admin): sfc /scannow\n"
            "   - DISM /Online /Cleanup-Image /RestoreHealth\n"
            "4. Create a new user profile to test:\n"
            "   - Settings > Accounts > Family & other users > Add someone\n"
            "   - If Start works on new profile, the old profile is corrupt\n"
            "5. Check and fix Windows indexing:\n"
            "   - services.msc > Windows Search > Restart\n"
            "6. Sign out and sign back in\n"
            "7. Last resort: Create new local admin account, copy data, delete old profile"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Black screen after login",
        "problem_description": "After entering password, user sees a black screen with only a cursor visible. Desktop, taskbar, and icons don't appear.",
        "problem_keywords": "black screen, no desktop, cursor only, black screen after login, no taskbar",
        "solution_steps": (
            "1. Try Ctrl+Shift+Esc to open Task Manager\n"
            "   - If it opens: File > Run new task > explorer.exe > check 'Create this task with administrative privileges'\n"
            "2. If Task Manager doesn't open, try Ctrl+Alt+Del > Sign out, then sign back in\n"
            "3. Boot into Safe Mode:\n"
            "   - Force power off 3 times to trigger WinRE\n"
            "   - Troubleshoot > Advanced > Startup Settings > Safe Mode with Networking\n"
            "4. In Safe Mode:\n"
            "   - Uninstall graphics/display driver, reboot to let Windows install generic one\n"
            "   - Disable Fast Startup: Control Panel > Power Options > Choose what power buttons do > Change currently unavailable settings > Uncheck 'Turn on fast startup'\n"
            "5. Rename or delete: C:\\Users\\<username>\\AppData\\Local\\Packages\\Microsoft.Windows.ShellExperienceHost\n"
            "6. Run sfc /scannow in Safe Mode\n"
            "7. Try System Restore to a working point\n"
            "8. Check for recent Windows updates and uninstall the latest one"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "DLL file missing or not found errors",
        "problem_description": "Application shows 'The program can't start because XXXX.dll is missing from your computer' or 'Entry point not found in DLL'.",
        "problem_keywords": "dll missing, dll not found, dll error, missing dll, vcruntime, msvcp, api-ms-win",
        "solution_steps": (
            "1. First identify which DLL is missing and which program needs it\n"
            "2. Install/repair Microsoft Visual C++ Redistributables:\n"
            "   - Download all versions (2010, 2012, 2013, 2015-2022) from Microsoft\n"
            "   - Install both x86 and x64 versions\n"
            "   - This fixes most vcruntime140.dll, msvcp140.dll type errors\n"
            "3. For .NET DLL errors, install/repair .NET Framework:\n"
            "   - Download from Microsoft, or use: DISM /Online /Enable-Feature /FeatureName:NetFx3\n"
            "4. Run SFC to repair system DLLs: sfc /scannow\n"
            "5. Reinstall the application that's showing the error\n"
            "6. If DirectX related: Install DirectX End-User Runtime from Microsoft\n"
            "7. NEVER download DLLs from random websites - this is a major security risk\n"
            "8. Check if the application needs to be run as Administrator"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Windows activation error or not genuine",
        "problem_description": "Windows shows 'Activate Windows' watermark, or gives 'Windows is not genuine' error. Features may be limited.",
        "problem_keywords": "activate windows, not genuine, activation error, product key, license, 0xC004C003",
        "solution_steps": (
            "1. Check current activation status:\n"
            "   - CMD: slmgr /xpr (shows license status)\n"
            "   - CMD: slmgr /dli (shows detailed license info)\n"
            "2. Open Settings > Update & Security > Activation\n"
            "3. If you have a product key: Click 'Change product key' and enter it\n"
            "4. If it was previously activated (hardware change):\n"
            "   - Settings > Activation > Troubleshoot\n"
            "   - 'I changed hardware on this device recently'\n"
            "   - Sign in with the Microsoft account linked to the license\n"
            "5. For volume license (KMS) issues:\n"
            "   - Verify KMS server is reachable: nslookup -type=srv _vlmcs._tcp\n"
            "   - Re-activate: slmgr /ato\n"
            "6. If multi-activation (MAK) key:\n"
            "   - CMD (Admin): slmgr /ipk <MAK-KEY>\n"
            "   - slmgr /ato\n"
            "7. Run: slmgr /rearm to reset the activation timer (works up to 3 times)"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "File Explorer not responding or crashing",
        "problem_description": "Windows File Explorer freezes, shows 'Not Responding', or crashes when opening folders or right-clicking files.",
        "problem_keywords": "file explorer, explorer crash, explorer not responding, folder freeze, explorer.exe",
        "solution_steps": (
            "1. Quick fix - restart Explorer:\n"
            "   - Ctrl+Shift+Esc > Windows Explorer > Restart\n"
            "2. Clear Explorer history:\n"
            "   - Open File Explorer > View > Options > Clear File Explorer history\n"
            "3. Disable Quick Access:\n"
            "   - File Explorer Options > General > Open to 'This PC' instead of Quick Access\n"
            "   - Uncheck both options under Privacy\n"
            "4. Disable Preview Pane: View > Preview Pane (toggle off)\n"
            "5. Check for corrupt shell extensions:\n"
            "   - Download ShellExView (NirSoft) to find and disable third-party extensions\n"
            "6. Run SFC: sfc /scannow\n"
            "7. Clear thumbnail cache:\n"
            "   - Disk Cleanup > check 'Thumbnails'\n"
            "   - Or CMD: del /f /s /q %LocalAppData%\\Microsoft\\Windows\\Explorer\\thumbcache_*.db\n"
            "8. Check for problematic context menu entries (right-click handlers)\n"
            "9. Update display/graphics driver"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Windows Defender won't turn on or is disabled",
        "problem_description": "Windows Security / Defender shows 'Real-time protection is off' and won't turn back on. Threat protection may be greyed out.",
        "problem_keywords": "windows defender, defender disabled, real-time protection, antivirus off, security center, windows security",
        "solution_steps": (
            "1. Check for third-party antivirus:\n"
            "   - Another antivirus (Norton, McAfee, Kaspersky, etc.) disables Defender automatically\n"
            "   - If you want Defender, fully uninstall the third-party antivirus first\n"
            "   - Use the vendor's official removal tool for complete uninstall\n"
            "2. Check Group Policy:\n"
            "   - gpedit.msc > Computer Config > Admin Templates > Windows Components > Microsoft Defender Antivirus\n"
            "   - 'Turn off Microsoft Defender Antivirus' should be 'Not Configured' or 'Disabled'\n"
            "3. Check registry:\n"
            "   - HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\n"
            "   - Delete 'DisableAntiSpyware' key if it exists (set to 0 or delete)\n"
            "4. Restart the Windows Security Center service:\n"
            "   - services.msc > Security Center > Restart\n"
            "5. Update Windows - sometimes an update fixes Defender\n"
            "6. Run: sfc /scannow\n"
            "7. Reset Windows Security: Get-AppxPackage Microsoft.SecHealthUI -AllUsers | Reset-AppxPackage\n"
            "8. Check if Tamper Protection is enabled in Windows Security > Virus & threat protection settings"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Disk space running low on C: drive",
        "problem_description": "C: drive is critically low on space. Windows shows 'Low Disk Space' warning. System may become slow or unstable.",
        "problem_keywords": "low disk space, C drive full, disk space, storage full, free space, disk cleanup",
        "solution_steps": (
            "1. Run Disk Cleanup as Administrator:\n"
            "   - Search 'Disk Cleanup' > Clean up system files > check all boxes\n"
            "   - This removes: Windows Update cache, old Windows installations, temp files, thumbnails\n"
            "2. Clear temporary files:\n"
            "   - Settings > System > Storage > Temporary files > Remove files\n"
            "   - Or delete contents of: %TEMP% and C:\\Windows\\Temp\n"
            "3. Empty the Recycle Bin\n"
            "4. Uninstall unused programs:\n"
            "   - Settings > Apps > sort by size > uninstall large unused programs\n"
            "5. Move large files (Downloads, Videos, etc.) to another drive\n"
            "6. Disable hibernation (frees space = your RAM size):\n"
            "   - CMD (Admin): powercfg -h off\n"
            "7. Reduce System Restore space:\n"
            "   - System Properties > System Protection > Configure > reduce Max Usage\n"
            "8. Use Storage Sense: Settings > System > Storage > Storage Sense > On\n"
            "9. Check for large WinSxS folder:\n"
            "   - DISM /Online /Cleanup-Image /StartComponentCleanup\n"
            "10. If still low, consider upgrading to a larger drive or adding a second drive"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Computer keeps restarting on its own",
        "problem_description": "Windows restarts unexpectedly without warning. May happen during use, at random intervals, or in a restart loop.",
        "problem_keywords": "restart loop, keeps restarting, unexpected restart, auto restart, computer restarting",
        "solution_steps": (
            "1. Disable automatic restart on crash to see the error:\n"
            "   - System Properties > Advanced > Startup and Recovery > Settings\n"
            "   - Uncheck 'Automatically restart'\n"
            "2. Check for overheating:\n"
            "   - Clean dust from fans, heatsink, vents\n"
            "   - Monitor temperatures with HWiNFO64\n"
            "   - CPU > 90°C or GPU > 95°C = thermal shutdown\n"
            "3. Check Event Viewer:\n"
            "   - System log > filter by Critical and Error\n"
            "   - Look for Event ID 41 (Kernel-Power) = unexpected shutdown\n"
            "4. Check for Windows Update:\n"
            "   - Restarts for updates can seem random\n"
            "   - Settings > Update > Active hours > set your work hours\n"
            "5. Test power supply:\n"
            "   - Failing PSU causes random restarts\n"
            "   - Try a different PSU or test with a PSU tester\n"
            "6. Test RAM: mdsched.exe\n"
            "7. Update all drivers and BIOS\n"
            "8. Check for malware with full scan\n"
            "9. If all else fails, check reliability history: Control Panel > Reliability Monitor"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "System Restore failed or not working",
        "problem_description": "System Restore fails with errors, or there are no restore points available. Cannot restore to a previous state.",
        "problem_keywords": "system restore, restore failed, no restore points, system restore error, 0x80070091",
        "solution_steps": (
            "1. Run System Restore in Safe Mode:\n"
            "   - Safe Mode may have fewer conflicts\n"
            "   - Boot to Safe Mode > run rstrui.exe\n"
            "2. Choose a different restore point:\n"
            "   - System Restore > 'Choose a different restore point' > check 'Show more restore points'\n"
            "3. Ensure System Protection is turned on:\n"
            "   - System Properties > System Protection > Configure\n"
            "   - Turn on system protection, set disk space to at least 5%\n"
            "4. Check disk space: System Restore needs free space to create/restore points\n"
            "5. Disable antivirus temporarily before attempting restore\n"
            "6. Error 0x80070091: A folder may be blocking the restore\n"
            "   - Try renaming the WindowsApps folder in Safe Mode\n"
            "7. Repair system files first, then try restore:\n"
            "   - sfc /scannow\n"
            "   - DISM /Online /Cleanup-Image /RestoreHealth\n"
            "8. If all else fails, use 'Reset this PC' keeping your files:\n"
            "   - Settings > Recovery > Reset this PC > Keep my files"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Windows Task Scheduler not running tasks",
        "problem_description": "Scheduled tasks don't execute at the specified time. Tasks show as 'Ready' but never start, or show error codes.",
        "problem_keywords": "task scheduler, scheduled task, task not running, task failed, task scheduler error",
        "solution_steps": (
            "1. Check the task's status and last run result in Task Scheduler:\n"
            "   - Last Run Result 0x0 = success\n"
            "   - 0x1 = task failed/incorrect path\n"
            "   - 0x41301 = task is currently running\n"
            "   - 0x41303 = task has not run yet\n"
            "2. Verify the trigger settings:\n"
            "   - Is the schedule correct? Check time, date, and frequency\n"
            "   - Is the trigger enabled?\n"
            "3. Check 'Run with highest privileges' if the task needs admin access\n"
            "4. Verify 'Run whether user is logged on or not':\n"
            "   - This requires the user's password to be stored\n"
            "   - Re-enter credentials: task Properties > Change User or Group\n"
            "5. Check the 'Start in' field:\n"
            "   - Must be the directory containing the script/program\n"
            "   - Use full paths for both the program and Start in\n"
            "6. Check Conditions tab:\n"
            "   - Uncheck 'Start only if the computer is on AC power' if needed\n"
            "   - Check 'Wake the computer to run this task' if needed\n"
            "7. Verify the Task Scheduler service is running: services.msc\n"
            "8. Check Event Viewer > Task Scheduler operational log for details"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Windows Safe Mode - How to boot into it",
        "problem_description": "Need to access Safe Mode for troubleshooting but not sure how. Various methods to enter Safe Mode on Windows 10/11.",
        "problem_keywords": "safe mode, boot safe mode, safe mode windows 10, safe mode windows 11, safe boot, F8",
        "solution_steps": (
            "Method 1 - From Settings (if Windows is running):\n"
            "   1. Settings > Update & Security > Recovery\n"
            "   2. Under 'Advanced startup' click 'Restart now'\n"
            "   3. Troubleshoot > Advanced > Startup Settings > Restart\n"
            "   4. Press F4 (Safe Mode), F5 (Safe Mode with Networking), or F6 (with CMD)\n\n"
            "Method 2 - Hold Shift + Restart:\n"
            "   1. Click Start > Power\n"
            "   2. Hold Shift key and click Restart\n"
            "   3. Follow: Troubleshoot > Advanced > Startup Settings > Restart\n\n"
            "Method 3 - From login screen:\n"
            "   1. Click Power icon on login screen\n"
            "   2. Hold Shift and click Restart\n"
            "   3. Follow same steps as Method 2\n\n"
            "Method 4 - If Windows won't boot:\n"
            "   1. Force power off 3 times during boot (press and hold power button)\n"
            "   2. This triggers Windows Recovery Environment (WinRE)\n"
            "   3. Troubleshoot > Advanced > Startup Settings > Restart\n\n"
            "Method 5 - Using msconfig (for repeated Safe Mode boots):\n"
            "   1. Win+R > msconfig > Boot tab\n"
            "   2. Check 'Safe boot' > OK > Restart\n"
            "   3. Remember to uncheck it when done troubleshooting"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Right-click context menu is very slow to appear",
        "problem_description": "When right-clicking on desktop, files, or folders, there's a long delay (5-30 seconds) before the context menu appears.",
        "problem_keywords": "right click slow, context menu slow, right click delay, context menu hang, right click freeze",
        "solution_steps": (
            "1. Identify the problematic shell extension:\n"
            "   - Download ShellExView from NirSoft (free tool)\n"
            "   - Sort by 'Type' column and look at 'Context Menu' entries\n"
            "   - Disable non-Microsoft entries one at a time and test\n"
            "2. Common culprits:\n"
            "   - Cloud sync apps (Dropbox, OneDrive, Google Drive - context menu handlers)\n"
            "   - Antivirus 'Scan with...' entries\n"
            "   - GPU control panel entries (NVIDIA, AMD)\n"
            "   - WinRAR/7-Zip context menu\n"
            "3. Disable Windows 11 'Show more options' delay:\n"
            "   - Registry: HKCU\\Software\\Classes\\CLSID\\\n"
            "   - Create key: {86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\\InprocServer32\n"
            "   - Set (Default) value to empty > restart Explorer\n"
            "4. If right-click slow only on desktop:\n"
            "   - Check for corrupt desktop icons or shortcuts\n"
            "   - Move items off desktop to a folder\n"
            "5. Check for network paths in context menu:\n"
            "   - 'Send to' folder may contain broken network shortcuts\n"
            "   - Check: shell:sendto and remove broken shortcuts"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Recycle Bin corrupted or not working",
        "problem_description": "Cannot empty Recycle Bin, shows wrong size, deleted files not appearing in Bin, or getting 'The Recycle Bin is corrupted' error.",
        "problem_keywords": "recycle bin, corrupted recycle bin, cannot delete, recycle bin error, trash, empty recycle bin",
        "solution_steps": (
            "1. Reset the Recycle Bin:\n"
            "   - CMD (Admin): rd /s /q C:\\$Recycle.Bin\n"
            "   - Restart the computer\n"
            "   - Windows will recreate the Recycle Bin automatically\n"
            "2. For each additional drive, reset its bin too:\n"
            "   - rd /s /q D:\\$Recycle.Bin (replace D: with your drive letter)\n"
            "3. If 'corrupted' error appears:\n"
            "   - The above reset command is the fix\n"
            "   - If it says 'Access Denied', boot to Safe Mode and try again\n"
            "4. Run disk check: chkdsk C: /f\n"
            "5. If files aren't appearing in Recycle Bin:\n"
            "   - Check Recycle Bin Properties: Right-click Bin > Properties\n"
            "   - Ensure 'Don't move files to Recycle Bin' is NOT checked\n"
            "   - Check the size limit isn't too small\n"
            "6. For files deleted from network drives: they bypass Recycle Bin (instant delete)\n"
            "7. Run SFC: sfc /scannow"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Windows time keeps changing or is wrong",
        "problem_description": "Computer clock shows the wrong time. Time resets after restart, drifts over time, or jumps to a different timezone.",
        "problem_keywords": "wrong time, clock wrong, time changing, time reset, CMOS battery, time sync, timezone",
        "solution_steps": (
            "1. Check timezone:\n"
            "   - Settings > Time & Language > Date & Time\n"
            "   - Verify timezone is correct\n"
            "   - Turn on 'Set time automatically' and 'Set time zone automatically'\n"
            "2. Sync time manually:\n"
            "   - CMD (Admin): w32tm /resync\n"
            "   - Or Settings > Date & Time > Sync now\n"
            "3. If time resets on every restart:\n"
            "   - The CMOS battery is dead (small coin-cell battery on motherboard)\n"
            "   - Replace the CR2032 battery (desktop) or service the laptop\n"
            "4. Verify Windows Time service:\n"
            "   - services.msc > Windows Time > Startup type: Automatic > Start\n"
            "5. Configure NTP server:\n"
            "   - CMD (Admin): w32tm /config /manualpeerlist:time.windows.com /syncfromflags:manual /reliable:yes /update\n"
            "   - Restart Windows Time: net stop w32time && net start w32time\n"
            "6. For domain-joined PCs: Time syncs with domain controller automatically\n"
            "   - Check DC time is correct\n"
            "   - Kerberos requires time within 5 minutes of DC\n"
            "7. If dual-booting with Linux: Linux uses UTC, Windows uses local time - this causes conflicts"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Windows Search not finding files or not working",
        "problem_description": "Windows Search in Start Menu or File Explorer returns no results, wrong results, or the search bar is not responding.",
        "problem_keywords": "windows search, search not working, search bar, find files, search broken, cortana search",
        "solution_steps": (
            "1. Restart Windows Search service:\n"
            "   - services.msc > Windows Search > Restart\n"
            "2. Rebuild the search index:\n"
            "   - Settings > Search > Searching Windows > Advanced Search Indexer Settings\n"
            "   - Click 'Advanced' > Rebuild > OK\n"
            "   - This takes time (30 min to several hours depending on file count)\n"
            "3. Run the Search troubleshooter:\n"
            "   - Settings > Update > Troubleshoot > Search and Indexing\n"
            "4. Reset Windows Search via PowerShell (Admin):\n"
            "   - Get-AppXPackage -Name Microsoft.Windows.Search | Reset-AppxPackage\n"
            "5. Check indexed locations:\n"
            "   - Indexing Options > Modify > make sure your important folders are included\n"
            "6. For File Explorer search:\n"
            "   - Use wildcards: *.xlsx to find Excel files\n"
            "   - Click 'Search options' > change between 'Current folder' and 'All subfolders'\n"
            "7. If search hangs: End the SearchApp.exe or SearchHost.exe process in Task Manager"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Application says 'This app can't run on your PC'",
        "problem_description": "When trying to run an application, Windows shows 'This app can't run on your PC' or 'Check with the software publisher'.",
        "problem_keywords": "app cant run, not compatible, check with publisher, incompatible app, x86 x64, arm",
        "solution_steps": (
            "1. Check if you're running the correct version:\n"
            "   - 32-bit (x86) app on 64-bit Windows: Should work\n"
            "   - 64-bit (x64) app on 32-bit Windows: Won't work - need 32-bit version\n"
            "   - Check your system: Settings > System > About > System type\n"
            "2. For ARM-based Windows (Surface Pro X, etc.):\n"
            "   - Only ARM64 and x86 (32-bit) apps work\n"
            "   - 64-bit x64 apps may not work on older ARM versions\n"
            "3. Check if SmartScreen is blocking the app:\n"
            "   - Right-click the .exe > Properties > Unblock checkbox > Apply\n"
            "4. The file may be corrupted - redownload from the official source\n"
            "5. Try running in Compatibility Mode:\n"
            "   - Right-click > Properties > Compatibility > Run in compatibility mode for older Windows\n"
            "6. Check the file type:\n"
            "   - .msi installer may need to be run instead of a .exe\n"
            "   - File may not actually be an executable\n"
            "7. For very old 16-bit applications: They don't run on 64-bit Windows at all"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Windows Firewall blocking application or port",
        "problem_description": "An application can't connect to the network or internet because Windows Firewall is blocking it. Need to add an exception.",
        "problem_keywords": "firewall blocking, firewall exception, allow through firewall, firewall rule, port blocked, windows firewall",
        "solution_steps": (
            "1. Allow an app through the firewall:\n"
            "   - Control Panel > Windows Defender Firewall > Allow an app through firewall\n"
            "   - Click 'Change settings' > 'Allow another app' > Browse to the .exe\n"
            "   - Check both 'Private' and 'Public' if needed\n"
            "2. Create a port rule:\n"
            "   - Windows Defender Firewall > Advanced settings\n"
            "   - Inbound Rules > New Rule > Port\n"
            "   - TCP or UDP > enter port number > Allow the connection\n"
            "3. Create a program rule:\n"
            "   - Advanced settings > Inbound Rules > New Rule > Program\n"
            "   - Browse to the executable > Allow the connection\n"
            "4. For outbound rules (less common):\n"
            "   - Same process but under 'Outbound Rules'\n"
            "5. Check if the app is being blocked:\n"
            "   - Event Viewer > Windows Logs > Security > filter for Event ID 5157\n"
            "6. Temporarily disable firewall to test (not recommended long-term):\n"
            "   - CMD (Admin): netsh advfirewall set allprofiles state off\n"
            "   - Re-enable: netsh advfirewall set allprofiles state on\n"
            "7. Group Policy may override local firewall settings - check with IT admin"
        ),
    },
]


DIAGNOSTIC_TREE = {
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
                        "solution_text": "1. Check power connections:\n   - Is the power cable plugged in? Try a different outlet\n   - For laptop: Is the adapter plugged in and showing a charge light?\n   - For desktop: Is the power supply switch ON (I = ON, O = OFF)?\n2. Test the outlet with another device (e.g., phone charger)\n3. For laptop:\n   - Remove battery (if removable), hold power button 30 seconds\n   - Plug in AC adapter without battery and try to start\n   - Try a different charger if available\n4. For desktop:\n   - Check all internal power connections\n   - Listen for any fans or clicks when pressing power\n   - Unplug all USB devices and try again\n5. If motherboard has LED indicator, check its status\n6. This is likely a hardware failure - power supply, motherboard, or battery"
                    },
                    {
                        "title": "Lights/fans come on but no display",
                        "node_type": "solution",
                        "solution_text": "1. Check monitor:\n   - Is it turned on? Check the power light\n   - Is the right input selected (HDMI, DP, etc.)?\n   - Try a different cable\n2. Listen for any beep codes (beeping patterns = diagnostic codes)\n3. Try with only one RAM stick at a time (test each slot)\n4. Reset CMOS/BIOS:\n   - Unplug PC, remove CMOS battery for 30 seconds, replace, try again\n5. Remove all USB devices, extra drives, and peripherals\n6. For laptop: Connect an external monitor to test\n7. For desktop with discrete GPU:\n   - Try connecting monitor to motherboard video port\n   - Reseat the graphics card\n8. If fans spin then PC shuts off quickly: Possible CPU or RAM issue"
                    },
                    {
                        "title": "Shows error message on screen",
                        "node_type": "solution",
                        "solution_text": "1. Note the exact error message\n2. 'Operating System Not Found' / 'No Boot Device':\n   - Check boot order in BIOS (press F2/F12/DEL during startup)\n   - Ensure the hard drive is listed\n   - If not listed: Drive may be disconnected or failed\n3. 'BOOTMGR is missing':\n   - Boot from Windows USB > Repair > Command Prompt\n   - Run: bootrec /fixmbr && bootrec /fixboot && bootrec /rebuildbcd\n4. 'Your PC ran into a problem' loop:\n   - Enter WinRE > System Restore or Startup Repair\n5. 'Preparing Automatic Repair' loop:\n   - WinRE > Command Prompt > sfc /scannow /offbootdir=C:\\ /offwindir=C:\\Windows\n6. BIOS/UEFI screen only:\n   - Check boot device priority\n   - Disable Secure Boot if needed"
                    }
                ]
            },
            {
                "title": "Computer is very slow",
                "node_type": "question",
                "question_text": "When did the slowness start?",
                "children": [
                    {
                        "title": "Always been slow / gradually worse",
                        "node_type": "solution",
                        "solution_text": "1. Open Task Manager (Ctrl+Shift+Esc)\n2. If Disk is at 100%:\n   - #1 fix: Upgrade to SSD if using HDD\n   - Disable SysMain: services.msc > SysMain > Disabled\n   - Disable Windows Search indexer temporarily\n3. Reduce startup programs:\n   - Task Manager > Startup > disable unnecessary programs\n4. Check RAM usage:\n   - If consistently >80%, need more RAM\n   - 4GB is minimum, 8GB recommended, 16GB for heavy use\n5. Clean up disk: Disk Cleanup > Clean up system files\n6. Uninstall unused programs\n7. Run malware scan (Windows Defender + Malwarebytes free)\n8. Disable visual effects:\n   - System Properties > Advanced > Performance > Adjust for best performance\n9. Check temperature: Overheating causes throttling\n10. Consider reinstalling Windows for very old PCs"
                    },
                    {
                        "title": "Suddenly became slow recently",
                        "node_type": "solution",
                        "solution_text": "1. Check Task Manager for high CPU/Memory/Disk process\n2. Check for recently installed software or updates\n   - Uninstall anything installed around when slowness started\n3. Run malware scan immediately:\n   - Windows Defender full scan\n   - Download and run Malwarebytes free scan\n4. Check for crypto-mining malware (high CPU from unknown processes)\n5. Check for disk errors:\n   - CMD: chkdsk C: /f (requires reboot)\n   - Check SMART: wmic diskdrive get status\n6. Check for Windows Updates downloading in background\n7. Run sfc /scannow to repair system files\n8. Use System Restore to go back to before the slowness\n9. Check if antivirus is running a full scan in background"
                    }
                ]
            },
            {
                "title": "Windows Update problems",
                "node_type": "solution",
                "solution_text": "1. Run Windows Update Troubleshooter:\n   - Settings > Update > Troubleshoot\n2. Reset update components:\n   - CMD (Admin):\n   - net stop wuauserv\n   - net stop bits\n   - ren C:\\Windows\\SoftwareDistribution SoftwareDistribution.old\n   - net start wuauserv\n   - net start bits\n3. Run sfc /scannow then DISM /Online /Cleanup-Image /RestoreHealth\n4. Check disk space (need 20GB+ free)\n5. Try downloading the update manually from Microsoft Update Catalog\n6. Disable VPN/proxy temporarily\n7. Check Windows Update log: C:\\Windows\\Logs\\CBS\\CBS.log"
            },
            {
                "title": "Black screen / no desktop after login",
                "node_type": "solution",
                "solution_text": "1. Press Ctrl+Shift+Esc to open Task Manager\n   - File > Run new task > explorer.exe\n2. If Task Manager won't open: Ctrl+Alt+Del > Sign out, sign back in\n3. Boot to Safe Mode and:\n   - Uninstall graphics driver, reboot\n   - Disable Fast Startup in Power Options\n4. Run sfc /scannow in Safe Mode\n5. Try System Restore\n6. Check for Windows updates to uninstall"
            }
        ]
    }
}
