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
    {
        "category": "Windows",
        "problem_title": "Blue Screen DRIVER_IRQL_NOT_LESS_OR_EQUAL (ndis.sys)",
        "problem_description": "BSOD referencing ndis.sys or a network-related driver. Often occurs after waking from sleep or connecting to network.",
        "problem_keywords": "ndis.sys bsod, driver irql, network driver crash, ndis crash, blue screen network, ndis bsod",
        "solution_steps": (
            "1. Update network adapter drivers:\n"
            "   - Device Manager > Network adapters\n"
            "   - Right-click adapter > Update Driver\n"
            "   - Better: Download latest from manufacturer (Intel, Realtek, Broadcom)\n"
            "2. Disable power management on the NIC:\n"
            "   - Device Manager > Network adapter > Properties > Power Management\n"
            "   - Uncheck 'Allow the computer to turn off this device'\n"
            "3. Check for VPN/firewall software conflicts:\n"
            "   - Third-party VPN clients may install conflicting NDIS filter drivers\n"
            "   - Try uninstalling VPN client temporarily\n"
            "4. Disable offloading features:\n"
            "   - Device Manager > Network adapter > Properties > Advanced\n"
            "   - Disable: Large Send Offload, TCP Checksum Offload, RSS\n"
            "5. Run driver verifier to identify the problematic driver:\n"
            "   - verifier (run limited testing mode)\n"
            "6. sfc /scannow and DISM /Online /Cleanup-Image /RestoreHealth\n"
            "7. If recent Windows update caused it: Uninstall the update from Recovery"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Windows Explorer Shell keeps restarting",
        "problem_description": "The Windows taskbar, desktop icons, and Start menu keep disappearing and reappearing. Explorer.exe is crashing and restarting in a loop.",
        "problem_keywords": "explorer crash, explorer restart, taskbar disappear, shell crash, explorer.exe, desktop flashing",
        "solution_steps": (
            "1. Check Event Viewer:\n"
            "   - Application log > filter by 'Application Error' source\n"
            "   - Look for explorer.exe crashes - note the faulting module\n"
            "2. Common faulting modules:\n"
            "   - ntdll.dll: System corruption, run sfc /scannow\n"
            "   - shell32.dll: Shell extension conflict\n"
            "   - Third-party DLL: Identify and uninstall the application\n"
            "3. Disable shell extensions:\n"
            "   - Download ShellExView (NirSoft) to see all shell extensions\n"
            "   - Disable all non-Microsoft extensions\n"
            "   - Re-enable one by one to find the culprit\n"
            "4. Safe Mode test:\n"
            "   - If explorer is stable in Safe Mode: Third-party software conflict\n"
            "   - Clean boot: msconfig > Services > Hide Microsoft > Disable All\n"
            "5. Check for corrupted thumbnail cache:\n"
            "   - Delete: %localappdata%\\Microsoft\\Windows\\Explorer\\thumbcache_*\n"
            "   - Restart explorer\n"
            "6. Reset Windows shell:\n"
            "   - Create new user account and test if explorer works there\n"
            "   - If yes: User profile is corrupted\n"
            "7. sfc /scannow and DISM /Online /Cleanup-Image /RestoreHealth"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Windows 10 to 11 upgrade failing",
        "problem_description": "Upgrade to Windows 11 fails with compatibility errors about TPM 2.0, Secure Boot, CPU, or other requirements during installation.",
        "problem_keywords": "windows 11 upgrade, tpm 2.0, secure boot, upgrade fail, windows 11 requirements, compatibility, win11",
        "solution_steps": (
            "1. Check requirements:\n"
            "   - Run the PC Health Check app from Microsoft\n"
            "   - Requirements: TPM 2.0, Secure Boot, 64-bit CPU (8th gen Intel+/Ryzen 2000+)\n"
            "   - 4 GB RAM minimum, 64 GB storage\n"
            "2. Enable TPM 2.0:\n"
            "   - Restart > BIOS/UEFI settings (Del/F2)\n"
            "   - Intel: Look for 'Intel PTT' under Security or Advanced\n"
            "   - AMD: Look for 'AMD fTPM' under Security\n"
            "   - Enable it and save/exit\n"
            "3. Enable Secure Boot:\n"
            "   - BIOS/UEFI > Boot or Security section\n"
            "   - Set 'Secure Boot' to Enabled\n"
            "   - Note: Drive must be GPT (not MBR) for Secure Boot\n"
            "   - Check disk type: diskmgmt.msc > right-click disk > Properties > Volumes\n"
            "4. If CPU not supported:\n"
            "   - Windows 11 officially requires specific CPUs\n"
            "   - The hardware does not meet Microsoft's requirements\n"
            "   - Consider staying on Windows 10 (supported until Oct 2025)\n"
            "5. If upgrade fails midway:\n"
            "   - Check C:\\$WINDOWS.~BT\\Sources\\Panther\\setupact.log for error details\n"
            "   - Free up 20+ GB of disk space\n"
            "   - Disconnect non-essential USB devices\n"
            "   - Disable antivirus during upgrade"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Windows event log full or not recording events",
        "problem_description": "Event Viewer shows 'The log file is full' or events are missing. System may have stopped recording important audit and error events.",
        "problem_keywords": "event log full, event viewer, event log, log file full, security log, audit log, events missing",
        "solution_steps": (
            "1. Check log sizes:\n"
            "   - Event Viewer > Windows Logs > right-click each log > Properties\n"
            "   - Note the log size and maximum size\n"
            "2. Increase maximum log size:\n"
            "   - Right-click log > Properties > Maximum log size\n"
            "   - Recommended: Security: 256 MB, System/Application: 64 MB\n"
            "3. Set log behavior:\n"
            "   - 'Overwrite events as needed' (default - recommended for most)\n"
            "   - 'Archive the log when full' (for compliance requirements)\n"
            "   - 'Do not overwrite events' (causes 'log full' error)\n"
            "4. Clear old logs:\n"
            "   - Right-click the log > Clear Log > Save And Clear (to archive first)\n"
            "   - Or just Clear if you don't need old events\n"
            "5. Via Group Policy:\n"
            "   - Computer Config > Admin Templates > Windows Components > Event Log Service\n"
            "   - Set maximum log size and retention method per log\n"
            "6. PowerShell to manage logs:\n"
            "   - wevtutil gl Security (view config)\n"
            "   - wevtutil sl Security /ms:268435456 (set max size to 256MB)\n"
            "7. Check if audit policies are generating excessive events:\n"
            "   - auditpol /get /category:* (view all audit policies)"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Windows not detecting second hard drive or SSD",
        "problem_description": "A second hard drive or SSD is installed but doesn't appear in File Explorer. May show in BIOS but not in Windows.",
        "problem_keywords": "second drive, disk not showing, new ssd, drive missing, disk management, initialize disk, unallocated",
        "solution_steps": (
            "1. Check Disk Management:\n"
            "   - diskmgmt.msc > look for the drive at the bottom\n"
            "   - If it shows as 'Not Initialized': Right-click > Initialize Disk\n"
            "   - Choose GPT (recommended for drives > 2TB) or MBR\n"
            "2. If it shows as 'Unallocated':\n"
            "   - Right-click the unallocated space > New Simple Volume\n"
            "   - Follow the wizard to format and assign a drive letter\n"
            "3. If no drive letter:\n"
            "   - Right-click the volume > Change Drive Letter and Paths\n"
            "   - Assign a letter\n"
            "4. If drive doesn't appear in Disk Management:\n"
            "   - Check BIOS: Is the drive detected there?\n"
            "   - Check physical connections: SATA cable and power cable\n"
            "   - Try a different SATA port on the motherboard\n"
            "5. For NVMe drives:\n"
            "   - Check if NVMe is enabled in BIOS\n"
            "   - M.2 slot may share bandwidth with SATA ports (disabling one)\n"
            "   - Install NVMe driver if needed (Intel RST or Samsung NVMe)\n"
            "6. Device Manager:\n"
            "   - Disk drives > check if the drive is listed\n"
            "   - If yellow exclamation: Right-click > Update Driver\n"
            "7. For USB external drives: Try different USB port, update USB drivers"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Print Screen / screenshot not working",
        "problem_description": "Pressing Print Screen key doesn't capture screenshots. Snipping Tool or Win+Shift+S not working either.",
        "problem_keywords": "screenshot, print screen, snipping tool, screen capture, prtsc, win shift s, screenshot not working",
        "solution_steps": (
            "1. Check Print Screen key:\n"
            "   - Some laptops: Need Fn+PrtSc combination\n"
            "   - PrtSc saves to clipboard - paste in Paint to see it\n"
            "   - Win+PrtSc: Saves directly to Pictures\\Screenshots folder\n"
            "2. Snipping Tool / Snip & Sketch:\n"
            "   - Win+Shift+S should open the snipping toolbar\n"
            "   - If not working: Reset the app\n"
            "   - Settings > Apps > Snipping Tool > Advanced > Reset\n"
            "3. Check for keyboard shortcuts conflict:\n"
            "   - OneDrive may intercept PrtSc: OneDrive Settings > Backup > uncheck 'Automatically save screenshots'\n"
            "   - Third-party screenshot tools may capture the key\n"
            "   - Gaming software (GeForce Experience, Xbox Game Bar) may intercept\n"
            "4. Fix via Registry:\n"
            "   - HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\n"
            "   - Set 'ScreenshotIndex' DWORD value\n"
            "5. Reinstall Snipping Tool:\n"
            "   - PowerShell: Get-AppxPackage *SnippingTool* | Remove-AppxPackage\n"
            "   - Then reinstall from Microsoft Store\n"
            "6. Try alternative methods:\n"
            "   - Win+G (Xbox Game Bar) > Capture\n"
            "   - Alt+PrtSc to capture active window only"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Windows PIN or fingerprint login stopped working",
        "problem_description": "Windows Hello PIN, fingerprint, or facial recognition stopped working after an update. Back to password-only login.",
        "problem_keywords": "windows hello, pin login, fingerprint, facial recognition, biometric, hello not working, pin error",
        "solution_steps": (
            "1. Reset the PIN:\n"
            "   - Settings > Accounts > Sign-in options > PIN (Windows Hello)\n"
            "   - Click 'I forgot my PIN' and follow the prompts\n"
            "   - Requires the account password\n"
            "2. Clear PIN data:\n"
            "   - Delete the folder: C:\\Windows\\ServiceProfiles\\LocalService\\AppData\\Local\\Microsoft\\Ngc\n"
            "   - Requires admin permissions (take ownership first)\n"
            "   - Restart and set up PIN again\n"
            "3. For fingerprint:\n"
            "   - Settings > Accounts > Sign-in options > Fingerprint\n"
            "   - Remove all fingerprints and re-enroll\n"
            "   - Update fingerprint reader driver from Device Manager\n"
            "   - Check: Device Manager > Biometric devices\n"
            "4. Check required services:\n"
            "   - services.msc > 'Windows Biometric Service' > Running\n"
            "   - 'Microsoft Passport' service > Running\n"
            "   - 'Credential Manager' service > Running\n"
            "5. Group Policy check:\n"
            "   - Computer Config > Admin Templates > System > Logon\n"
            "   - 'Turn on convenience PIN sign-in' should be Enabled or Not Configured\n"
            "6. TPM issues:\n"
            "   - tpm.msc > check TPM status\n"
            "   - PIN uses TPM - if TPM has errors, clear and reinitialize"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Scheduled Task won't run or runs at wrong time",
        "problem_description": "Windows Task Scheduler tasks are not executing at the configured times, or run at unexpected times. Manual run may work fine.",
        "problem_keywords": "scheduled task, task scheduler, task not running, wrong time, scheduled job, task trigger, cron",
        "solution_steps": (
            "1. Check task status:\n"
            "   - Task Scheduler > check 'Last Run Result'\n"
            "   - 0x0: Success\n"
            "   - 0x1: Incorrect function (check the action/command)\n"
            "   - 0x41301: Currently running\n"
            "   - 0x41303: Task not yet run\n"
            "   - 0x800710E0: The operator or admin has refused the request\n"
            "2. Check 'Run whether user is logged on or not':\n"
            "   - Task Properties > General > Security options\n"
            "   - This must be selected for tasks to run when nobody is logged in\n"
            "   - Requires storing the password\n"
            "3. Check the user account:\n"
            "   - The run-as account must have 'Log on as a batch job' right\n"
            "   - Local Security Policy > User Rights Assignment\n"
            "   - If password changed: Update the task password\n"
            "4. Conditions tab:\n"
            "   - Uncheck 'Start only if AC power' (for laptops)\n"
            "   - Uncheck 'Start only if network is available' if not needed\n"
            "   - Check 'Wake the computer' if needed\n"
            "5. Wrong time execution:\n"
            "   - Check timezone on the server/PC\n"
            "   - Check if trigger is set to UTC or local time\n"
            "   - Review trigger schedule carefully\n"
            "6. History tab: Enable Task Scheduler history for debugging:\n"
            "   - Task Scheduler > Action > Enable All Tasks History"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Night Light or color settings not working",
        "problem_description": "Windows Night Light feature not turning on/off, color calibration is wrong, or display colors look oversaturated or washed out.",
        "problem_keywords": "night light, color calibration, display color, color temperature, oversaturated, color profile, night mode",
        "solution_steps": (
            "1. Night Light not working:\n"
            "   - Settings > System > Display > Night Light\n"
            "   - Toggle off and back on\n"
            "   - Set schedule: Sunset to Sunrise or custom times\n"
            "   - May require Location Services to be enabled for sunset/sunrise\n"
            "2. Night Light greyed out:\n"
            "   - Update the display/graphics driver\n"
            "   - Some older or basic display drivers don't support Night Light\n"
            "   - Check: Device Manager > Display adapters > update driver\n"
            "3. Color calibration:\n"
            "   - Search 'Calibrate display color' > follow the wizard\n"
            "   - Adjusts gamma, brightness, contrast, and color balance\n"
            "   - Or: dccw.exe from Run dialog\n"
            "4. Wrong color profile:\n"
            "   - Settings > System > Display > Advanced display settings\n"
            "   - Color Management > select monitor > Add/remove profiles\n"
            "   - Use the manufacturer's ICC profile\n"
            "5. Graphics driver color settings:\n"
            "   - Intel: Intel Graphics Command Center > Display > Color\n"
            "   - NVIDIA: NVIDIA Control Panel > Display > Adjust desktop color\n"
            "   - AMD: AMD Adrenalin > Display > Color settings\n"
            "   - Reset all to defaults if colors are off\n"
            "6. HDR issues: Settings > Display > HDR > toggle off if causing problems"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Windows Services failing to start at boot",
        "problem_description": "One or more Windows services fail to start automatically. Applications dependent on these services don't work until services are manually started.",
        "problem_keywords": "service failed, service not starting, automatic service, service timeout, service error 1053, dependency",
        "solution_steps": (
            "1. Check the service error:\n"
            "   - services.msc > find the service > Properties\n"
            "   - Note the startup type and current status\n"
            "   - Check Event Viewer > System for service errors at boot time\n"
            "2. Service dependencies:\n"
            "   - Service Properties > Dependencies tab\n"
            "   - All dependent services must start first\n"
            "   - If a dependency fails, the service can't start\n"
            "3. Error 1053 (Service did not respond in time):\n"
            "   - Registry: HKLM\\SYSTEM\\CurrentControlSet\\Control\n"
            "   - Increase 'ServicesPipeTimeout' DWORD to 60000 (60 seconds)\n"
            "   - Slow disks or extensive startup can cause timeouts\n"
            "4. Set startup type:\n"
            "   - Automatic: Starts at boot\n"
            "   - Automatic (Delayed Start): Starts after other services (better for slow PCs)\n"
            "   - Try changing to Delayed Start if it fails with Automatic\n"
            "5. Log On account:\n"
            "   - Service Properties > Log On tab\n"
            "   - Try 'Local System' account if a specific account fails\n"
            "   - If using a domain account: Verify password hasn't changed\n"
            "6. Repair service registration:\n"
            "   - sc config ServiceName start= auto\n"
            "   - sfc /scannow to repair system files\n"
            "7. For third-party service: Reinstall the application"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Clipboard not working or can't copy/paste",
        "problem_description": "Copy and paste (Ctrl+C/Ctrl+V) stops working. Clipboard is empty when trying to paste, or content doesn't transfer between applications.",
        "problem_keywords": "clipboard, copy paste, ctrl c, ctrl v, clipboard empty, can't paste, copy not working",
        "solution_steps": (
            "1. Restart clipboard:\n"
            "   - Open Task Manager > find 'rdpclip.exe' or 'Windows Explorer'\n"
            "   - End task on rdpclip.exe (if on Remote Desktop)\n"
            "   - Restart Windows Explorer: Task Manager > Details > explorer.exe > End Task > File > New Task > explorer.exe\n"
            "2. Clear clipboard:\n"
            "   - Win+V > Clear All\n"
            "   - Or: cmd > echo off | clip\n"
            "   - Settings > System > Clipboard > Clear clipboard data\n"
            "3. Check Clipboard service:\n"
            "   - services.msc > 'ClipSVC' (Clipboard User Service) > Running\n"
            "   - Restart the service if needed\n"
            "4. Remote Desktop clipboard issues:\n"
            "   - RDP session: rdpclip.exe handles clipboard sync\n"
            "   - Kill rdpclip.exe in Task Manager and restart it\n"
            "   - RDP settings: Local Resources > Clipboard must be checked\n"
            "5. Application-specific:\n"
            "   - Some applications lock the clipboard while using it\n"
            "   - Try copying from/to a different application (e.g., Notepad)\n"
            "   - Close apps one by one to find the culprit\n"
            "6. Enable clipboard history:\n"
            "   - Settings > System > Clipboard > Clipboard history: On\n"
            "   - Win+V to see clipboard history"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Windows hibernation or sleep mode not working",
        "problem_description": "Computer won't sleep, won't hibernate, wakes from sleep immediately, or won't wake from sleep properly.",
        "problem_keywords": "sleep mode, hibernate, won't sleep, wake from sleep, power, standby, sleep not working",
        "solution_steps": (
            "1. Won't go to sleep:\n"
            "   - powercfg /requests (shows what's preventing sleep)\n"
            "   - Common: Media player, downloads, USB devices\n"
            "   - powercfg /requestsoverride (override specific blockers)\n"
            "2. Wakes immediately after sleeping:\n"
            "   - powercfg /lastwake (shows what woke the PC)\n"
            "   - Common culprits: Network adapter, mouse, keyboard\n"
            "   - Device Manager > Network adapter > Properties > Power Management\n"
            "   - Uncheck 'Allow this device to wake the computer'\n"
            "   - Do the same for mouse if it's too sensitive\n"
            "3. Hibernate not available:\n"
            "   - CMD (admin): powercfg /hibernate on\n"
            "   - Add Hibernate to power menu: Power Options > Choose what power buttons do\n"
            "   - Check: Requires enough disk space for hiberfil.sys (RAM size)\n"
            "4. Won't wake from sleep (black screen):\n"
            "   - Update graphics driver\n"
            "   - Try: Press any key, move mouse, press power button briefly\n"
            "   - Disable 'Fast Startup': Power Options > Choose what power buttons do > Change settings > uncheck 'Turn on fast startup'\n"
            "5. Sleep/hibernate troubleshooter:\n"
            "   - powercfg /energy (generates energy report)\n"
            "   - Check the report for warnings and errors\n"
            "6. BIOS: Check sleep/suspend settings (S3 vs Modern Standby)"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Windows fonts missing, corrupted, or not displaying",
        "problem_description": "Fonts appear as boxes or squares, certain applications show wrong fonts, or custom installed fonts are missing after an update.",
        "problem_keywords": "fonts missing, font corrupted, boxes instead of text, missing characters, font install, font not showing",
        "solution_steps": (
            "1. Rebuild font cache:\n"
            "   - services.msc > 'Windows Font Cache Service' > Stop\n"
            "   - Delete: C:\\Windows\\ServiceProfiles\\LocalService\\AppData\\Local\\FontCache\\*\n"
            "   - Delete: C:\\Windows\\System32\\FNTCACHE.DAT\n"
            "   - Restart the font cache service and restart the PC\n"
            "2. Restore default fonts:\n"
            "   - Settings > Personalization > Fonts > Related settings > Font settings\n"
            "   - 'Restore default font settings'\n"
            "3. Check font folder:\n"
            "   - C:\\Windows\\Fonts should contain the system fonts\n"
            "   - If fonts were deleted: Copy from a working PC or Windows ISO\n"
            "   - sfc /scannow restores missing system files including fonts\n"
            "4. Install custom fonts:\n"
            "   - Right-click .ttf or .otf file > Install\n"
            "   - Or drag into C:\\Windows\\Fonts\n"
            "   - 'Install for all users' requires admin rights\n"
            "5. Group Policy font restrictions:\n"
            "   - Computer Config > Admin Templates > Network > Fonts\n"
            "   - 'Enable font providers' may be disabled\n"
            "   - 'Download fonts over metered connections' may block fonts\n"
            "6. For boxes/squares appearing:\n"
            "   - Missing Unicode fonts needed for the language\n"
            "   - Settings > Time & Language > Language > Add language packs needed"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Disk Check (CHKDSK) needed or running at every boot",
        "problem_description": "Windows prompts to run disk check or CHKDSK runs automatically at every boot. May indicate disk errors or improper shutdowns.",
        "problem_keywords": "chkdsk, disk check, check disk, chkdsk every boot, disk error, file system error, chkdsk stuck",
        "solution_steps": (
            "1. Run CHKDSK manually:\n"
            "   - CMD (admin): chkdsk C: /f /r\n"
            "   - /f: Fix errors, /r: Locate bad sectors and recover data\n"
            "   - Will schedule for next reboot on boot drive\n"
            "   - Let it complete fully - do NOT interrupt\n"
            "2. CHKDSK running every boot:\n"
            "   - Check dirty bit: fsutil dirty query C:\n"
            "   - If 'Dirty': Run chkdsk /f to fix errors and clear the bit\n"
            "   - Registry check: HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\n"
            "   - 'BootExecute' should show 'autocheck autochk *' (not additional entries)\n"
            "3. CHKDSK stuck at a percentage:\n"
            "   - Stage 4 and 5 can take hours on large drives\n"
            "   - Do NOT interrupt - let it finish\n"
            "   - If truly stuck (24+ hours): Power cycle and run again\n"
            "4. Check the SMART health of the drive:\n"
            "   - Use CrystalDiskInfo to check for hardware errors\n"
            "   - Repeated CHKDSK needs often means the drive is failing\n"
            "   - Back up data immediately if SMART shows warnings\n"
            "5. For SSDs:\n"
            "   - chkdsk /f is fine on SSDs (skip /r as it's for bad sectors)\n"
            "   - SSD wear: Check Total Bytes Written in CrystalDiskInfo\n"
            "6. After CHKDSK: Review the log in Event Viewer > Application > Event ID 26212 (Wininit)"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Remote Desktop scaling or display issues",
        "problem_description": "Remote Desktop session shows tiny text, blurry display, wrong resolution, or DPI scaling issues on high-resolution monitors.",
        "problem_keywords": "rdp scaling, rdp resolution, rdp blurry, remote desktop display, rdp dpi, rdp small text, rdp monitor",
        "solution_steps": (
            "1. Adjust RDP display settings before connecting:\n"
            "   - mstsc > Show Options > Display tab\n"
            "   - Resolution slider: Set to desired resolution or 'Full Screen'\n"
            "   - Check 'Use all my monitors for remote session' if multi-monitor\n"
            "2. Smart sizing:\n"
            "   - In the RDP window: System menu > Smart Sizing\n"
            "   - This scales the remote desktop to fit the window\n"
            "3. DPI scaling fix:\n"
            "   - Right-click mstsc.exe > Properties > Compatibility\n"
            "   - Change high DPI settings > Override high DPI scaling\n"
            "   - Scaling performed by: System\n"
            "4. RDP file settings for custom DPI:\n"
            "   - Edit the .rdp file in Notepad\n"
            "   - Add: desktopscalefactor:i:125 (or 150, 200 etc.)\n"
            "   - Add: smart sizing:i:1\n"
            "5. Dynamic resolution:\n"
            "   - Windows 10+ supports dynamic resolution in RDP\n"
            "   - Resizing the RDP window should change the remote resolution\n"
            "   - If not working: Check Group Policy on the remote server\n"
            "6. Multi-monitor:\n"
            "   - mstsc /multimon (command line to enable multi-monitor)\n"
            "   - Requires same DPI across monitors for best results"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Windows Installer service errors (MSI failures)",
        "problem_description": "Applications fail to install or uninstall with Windows Installer errors. MSI packages show error codes like 1603, 1722, or 'The Windows Installer Service could not be accessed'.",
        "problem_keywords": "msi error, windows installer, error 1603, error 1722, installer service, msiexec, install failed",
        "solution_steps": (
            "1. Check Windows Installer service:\n"
            "   - services.msc > 'Windows Installer' > should be Manual or Running\n"
            "   - If stopped: Start it\n"
            "   - If won't start: msiexec /regserver (re-register the service)\n"
            "2. Error 1603 (Fatal error during installation):\n"
            "   - Check Windows Temp folder: %TEMP%\\MSI*.LOG\n"
            "   - Common: Not enough disk space, permissions, or locked files\n"
            "   - Try running installer as administrator\n"
            "   - Close all running applications first\n"
            "3. Error 1722 (Problem with Windows Installer package):\n"
            "   - The .msi package has a problem with a custom action\n"
            "   - Try re-downloading the installer\n"
            "   - Run in compatibility mode\n"
            "4. Cannot uninstall:\n"
            "   - Use Microsoft's Program Install/Uninstall Troubleshooter\n"
            "   - Available from support.microsoft.com\n"
            "   - Fixes broken uninstall registrations\n"
            "5. Re-register Windows Installer:\n"
            "   - CMD (admin): msiexec /unregister then msiexec /regserver\n"
            "6. Install logging for debugging:\n"
            "   - msiexec /i package.msi /l*vx install.log\n"
            "   - Review install.log for the specific error\n"
            "7. sfc /scannow to repair system files"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Disk encryption with BitLocker causing boot delay",
        "problem_description": "Computer takes much longer to boot after BitLocker encryption was enabled. Startup may show 'Preparing BitLocker' or just be very slow.",
        "problem_keywords": "bitlocker slow boot, bitlocker encrypting, bitlocker startup, slow encryption, bitlocker preparing, boot delay",
        "solution_steps": (
            "1. Check encryption status:\n"
            "   - manage-bde -status C:\n"
            "   - If 'Encryption in Progress': The drive is still encrypting\n"
            "   - This is normal - initial encryption can take hours\n"
            "   - Boot will be slower until encryption completes\n"
            "2. While encryption is in progress:\n"
            "   - Do NOT interrupt or power off during encryption\n"
            "   - manage-bde -status shows percentage complete\n"
            "   - Normal activities can continue - encryption runs in background\n"
            "3. After encryption completes but still slow:\n"
            "   - BitLocker decryption at boot adds about 5-10 seconds\n"
            "   - Check if TPM is working: tpm.msc\n"
            "   - Without TPM: BitLocker uses password/USB key (slower)\n"
            "4. Optimize boot:\n"
            "   - Ensure Fast Startup is enabled\n"
            "   - Check BIOS boot order: Remove unnecessary boot devices\n"
            "   - SSD + TPM: BitLocker overhead should be minimal\n"
            "   - HDD: Expect more noticeable slowdown\n"
            "5. If boot is extremely slow (minutes):\n"
            "   - Check Event Viewer for BitLocker errors\n"
            "   - Check SMART health of the drive\n"
            "   - Update BIOS/firmware\n"
            "6. To pause encryption temporarily:\n"
            "   - manage-bde -pause C: (resume later with manage-bde -resume C:)"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Windows Sandbox or Hyper-V not available",
        "problem_description": "Cannot enable Windows Sandbox or Hyper-V. The feature doesn't appear in Windows Features or gives an error about virtualization.",
        "problem_keywords": "windows sandbox, hyper-v, virtualization, hypervisor, sandbox not available, vt-x, amd-v",
        "solution_steps": (
            "1. Check Windows edition:\n"
            "   - Windows Sandbox: Requires Pro or Enterprise (not Home)\n"
            "   - Hyper-V: Requires Pro, Enterprise, or Education (not Home)\n"
            "   - Check: winver (shows edition)\n"
            "2. Enable virtualization in BIOS:\n"
            "   - Restart > BIOS/UEFI settings\n"
            "   - Intel: Enable 'Intel Virtualization Technology' (VT-x)\n"
            "   - AMD: Enable 'AMD-V' or 'SVM Mode'\n"
            "   - Save and exit\n"
            "3. Enable the Windows feature:\n"
            "   - Control Panel > Programs > Turn Windows features on or off\n"
            "   - Check 'Hyper-V' (all sub-items)\n"
            "   - Check 'Windows Sandbox'\n"
            "   - Restart when prompted\n"
            "4. Check virtualization status:\n"
            "   - Task Manager > Performance > CPU\n"
            "   - 'Virtualization: Enabled' should show at the bottom\n"
            "   - If 'Disabled': Go to BIOS (step 2)\n"
            "5. Conflicts:\n"
            "   - VirtualBox/VMware may conflict with Hyper-V\n"
            "   - Choose one hypervisor or enable WHP (Windows Hypervisor Platform)\n"
            "   - bcdedit /set hypervisorlaunchtype auto (enable Hyper-V)\n"
            "6. For nested virtualization (VM inside VM):\n"
            "   - The host must also have Hyper-V enabled\n"
            "   - Enable nested virtualization on the VM"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Windows Sandbox or Hyper-V feature not available",
        "problem_description": "Windows Sandbox or Hyper-V option is grayed out in Windows Features, won't enable, or gives errors about virtualization not supported despite having a compatible CPU.",
        "problem_keywords": "windows sandbox, hyper-v, virtualization, windows features, sandbox not available, hyper-v grayed out, vt-x, slat",
        "solution_steps": (
            "1. Check requirements:\n"
            "   - Windows 10/11 Pro, Enterprise, or Education (not Home)\n"
            "   - 64-bit processor with SLAT (Second Level Address Translation)\n"
            "   - Minimum 4GB RAM (8GB+ recommended)\n"
            "   - systeminfo | findstr /i \"Hyper-V\"\n"
            "2. Enable in BIOS:\n"
            "   - Enter BIOS/UEFI (usually F2, F10, DEL at boot)\n"
            "   - Intel: Enable VT-x / Intel Virtualization Technology\n"
            "   - AMD: Enable AMD-V / SVM Mode\n"
            "   - Save and exit\n"
            "3. Enable Windows features:\n"
            "   - Control Panel > Programs > Turn Windows features on or off\n"
            "   - Check: Hyper-V, Windows Sandbox, Virtual Machine Platform\n"
            "   - Or PowerShell: Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V-All\n"
            "4. Conflict with other hypervisors:\n"
            "   - VirtualBox/VMware may conflict with Hyper-V\n"
            "   - bcdedit /set hypervisorlaunchtype auto (enable Hyper-V)\n"
            "   - bcdedit /set hypervisorlaunchtype off (disable for other hypervisors)\n"
            "5. Reboot required after enabling any virtualization feature"
        ),
    },
    {
        "category": "Windows",
        "problem_title": "Windows event log full or event log service errors",
        "problem_description": "Windows Event Viewer shows 'event log is full' warnings, events not being recorded, or Event Log service failing to start. Critical for security auditing and troubleshooting.",
        "problem_keywords": "event log, event viewer, log full, event log service, windows log, security log, audit log, log size",
        "solution_steps": (
            "1. Check log sizes:\n"
            "   - Event Viewer > Windows Logs\n"
            "   - Right-click each log > Properties\n"
            "   - Shows: Current size, maximum size, overwrite policy\n"
            "2. Increase log size:\n"
            "   - Right-click log > Properties > Maximum log size\n"
            "   - Recommended: Security 1GB+, Application 256MB, System 256MB\n"
            "   - Set overwrite policy: 'Overwrite events as needed'\n"
            "3. Clear old logs:\n"
            "   - Right-click log > Clear Log\n"
            "   - Save before clearing: 'Save and Clear'\n"
            "   - PowerShell: wevtutil cl Security\n"
            "4. Group Policy settings:\n"
            "   - Computer Config > Admin Templates > Windows Components > Event Log Service\n"
            "   - Set max log sizes and retention method per log\n"
            "   - Security log: 'Do not overwrite' for compliance\n"
            "5. Event Log service: If service won't start, check %SystemRoot%\\System32\\winevt\\Logs\\ folder permissions (SYSTEM needs Full Control)"
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
