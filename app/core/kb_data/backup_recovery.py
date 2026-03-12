"""Backup, recovery, and disaster recovery articles and diagnostic tree."""

ARTICLES = [
    {
        "category": "Backup & Recovery",
        "problem_title": "Windows backup has stopped working",
        "problem_description": "Windows built-in backup (File History or Backup and Restore) has stopped running or shows errors. Users are not protected against data loss.",
        "problem_keywords": "windows backup, file history, backup stopped, backup error, backup and restore, backup not running",
        "solution_steps": (
            "1. Check File History status:\n"
            "   - Settings > Update & Security > Backup\n"
            "   - Is File History turned on? Is the backup drive connected?\n"
            "2. Common File History issues:\n"
            "   - Backup drive full: Free up space or use a larger drive\n"
            "   - Backup drive disconnected: Reconnect and restart File History\n"
            "   - Error 'We found errors': Settings > Backup > More options > See advanced settings > Run now\n"
            "3. Restart File History service:\n"
            "   - services.msc > File History Service > Restart\n"
            "   - Also restart: Windows Search (indexing can affect backup)\n"
            "4. For 'Backup and Restore (Windows 7)':\n"
            "   - Control Panel > Backup and Restore > Check backup settings\n"
            "   - Remove old schedule and create new one\n"
            "   - Check Event Viewer > Application for backup errors\n"
            "5. Re-enable File History:\n"
            "   - Turn off File History\n"
            "   - Disconnect backup drive\n"
            "   - Reconnect drive\n"
            "   - Turn on File History and select the drive\n"
            "6. Alternative: Use OneDrive Known Folder Protection for cloud backup\n"
            "   - OneDrive > Settings > Backup > Manage backup\n"
            "   - Protects Desktop, Documents, Pictures to the cloud"
        ),
    },
    {
        "category": "Backup & Recovery",
        "problem_title": "Deleted files recovery from backup",
        "problem_description": "User accidentally deleted important files and needs to recover them from backup or other recovery methods.",
        "problem_keywords": "deleted files, recover files, file recovery, undelete, restore files, accidental delete, lost files",
        "solution_steps": (
            "1. Check Recycle Bin first:\n"
            "   - Desktop > Recycle Bin > find files > right-click > Restore\n"
            "   - Restores to original location\n"
            "2. Check File History:\n"
            "   - Navigate to the folder where files were\n"
            "   - Right-click > Properties > Previous Versions\n"
            "   - Or: Control Panel > File History > Restore personal files\n"
            "   - Browse to the date before deletion\n"
            "3. Check OneDrive:\n"
            "   - OneDrive web > Recycle Bin (keeps files for 93 days)\n"
            "   - OneDrive > Version History on the folder\n"
            "4. Check SharePoint:\n"
            "   - Site > Recycle Bin (first stage: 93 days)\n"
            "   - Site Collection Admin > Second-stage Recycle Bin\n"
            "5. Check shadow copies (if available on server):\n"
            "   - Right-click folder > Properties > Previous Versions\n"
            "   - Requires Volume Shadow Copy to be configured\n"
            "6. Use data recovery tools (if not backed up):\n"
            "   - STOP writing to the drive immediately\n"
            "   - Recuva (free): Scans for recoverable files\n"
            "   - TestDisk/PhotoRec: Open source recovery\n"
            "   - Professional data recovery: For critical business data\n"
            "7. For server files: Check the most recent server backup\n"
            "   - Windows Server Backup or third-party backup solution\n"
            "8. Prevention: Set up regular automated backups"
        ),
    },
    {
        "category": "Backup & Recovery",
        "problem_title": "System Image restore for complete PC recovery",
        "problem_description": "Computer won't boot or is severely corrupted. Need to restore from a system image backup to recover the entire machine.",
        "problem_keywords": "system image, restore image, pc recovery, system restore image, bare metal, complete restore, disk image",
        "solution_steps": (
            "1. Boot from Windows installation media:\n"
            "   - Insert USB/DVD with Windows installer\n"
            "   - Boot from it (F12/F2/Del to access boot menu)\n"
            "   - Select 'Repair your computer'\n"
            "2. Restore from system image:\n"
            "   - Troubleshoot > Advanced options > System Image Recovery\n"
            "   - Connect the backup drive if external\n"
            "   - Windows will find the latest system image\n"
            "   - Select the image and follow prompts\n"
            "3. If image not detected:\n"
            "   - Ensure backup drive is connected and detected in BIOS\n"
            "   - Try different USB port\n"
            "   - Check if the drive uses GPT/MBR matching the target disk\n"
            "4. Creating a system image (for future use):\n"
            "   - Control Panel > Backup and Restore > Create a system image\n"
            "   - Choose destination: External drive, network, or DVD\n"
            "   - Select drives to include\n"
            "   - Also create a System Repair Disc\n"
            "5. Important notes:\n"
            "   - System image restores the ENTIRE drive (overwrites everything)\n"
            "   - Cannot restore individual files from a system image\n"
            "   - Target disk must be same size or larger than original\n"
            "6. Alternative recovery: Windows Reset\n"
            "   - Settings > Recovery > Reset this PC > Keep my files\n"
            "   - Reinstalls Windows but preserves user files"
        ),
    },
    {
        "category": "Backup & Recovery",
        "problem_title": "Third-party backup software errors (Veeam, Acronis)",
        "problem_description": "Enterprise backup solution (Veeam, Acronis, or similar) is reporting job failures, VSS errors, or unable to complete backup jobs.",
        "problem_keywords": "veeam error, acronis error, backup job failed, enterprise backup, vss backup error, backup software",
        "solution_steps": (
            "1. Check backup job logs:\n"
            "   - Open the backup software console\n"
            "   - Review the failed job > Session details\n"
            "   - Note the specific error message\n"
            "2. VSS (Volume Shadow Copy) errors:\n"
            "   - Most common cause of backup failures\n"
            "   - On the machine being backed up:\n"
            "   - vssadmin list writers (check for failed writers)\n"
            "   - Restart the service associated with the failed writer\n"
            "   - net stop vss && net start vss\n"
            "3. Storage/repository issues:\n"
            "   - Backup repository full: Free up space\n"
            "   - Network share unreachable: Check connectivity\n"
            "   - Check for disk errors on backup storage\n"
            "4. Veeam-specific:\n"
            "   - Check VBR console > Infrastructure > verify backup proxy is online\n"
            "   - Check repository maintenance tasks\n"
            "   - Run health check on backup files: Edit job > Storage > Health Check\n"
            "   - Update Veeam to latest patch\n"
            "5. Acronis-specific:\n"
            "   - Check Acronis Management Console for task details\n"
            "   - Verify agent is running on target machine\n"
            "   - Check Acronis service: services.msc > Acronis Agent\n"
            "6. Connection/authentication issues:\n"
            "   - Verify backup account has admin rights on target\n"
            "   - Check if password was changed\n"
            "   - Verify firewall ports for backup software\n"
            "7. After fixing: Run the job manually to verify it completes"
        ),
    },
    {
        "category": "Backup & Recovery",
        "problem_title": "Ransomware recovery from backups",
        "problem_description": "Need to restore systems and data after a ransomware attack. Must ensure backups are clean before restoring.",
        "problem_keywords": "ransomware recovery, restore ransomware, backup restore, ransomware restore, disaster recovery, data restore",
        "solution_steps": (
            "1. DO NOT restore until threat is contained:\n"
            "   - Ensure all infected machines are isolated\n"
            "   - Identify the ransomware variant\n"
            "   - Determine the infection timeline (when it started)\n"
            "2. Verify backup integrity:\n"
            "   - Backups from BEFORE the infection date are needed\n"
            "   - Ransomware may have been dormant for weeks\n"
            "   - Scan backup files with updated antivirus before restoring\n"
            "   - Test restore to isolated environment first\n"
            "3. Check if backups are affected:\n"
            "   - Ransomware may encrypt backup files too\n"
            "   - Check backup storage for encrypted/modified files\n"
            "   - Air-gapped or immutable backups should be safe\n"
            "   - Cloud backups with versioning can roll back to clean version\n"
            "4. Restoration order:\n"
            "   - Domain Controllers first (if affected)\n"
            "   - DNS servers\n"
            "   - Critical application servers\n"
            "   - File servers\n"
            "   - User workstations last\n"
            "5. For each restore:\n"
            "   - Wipe the machine completely (new disk image)\n"
            "   - Install clean OS and apply all patches\n"
            "   - Restore data from verified clean backup\n"
            "   - Change all passwords before reconnecting to network\n"
            "6. Post-recovery:\n"
            "   - Monitor all systems for re-infection\n"
            "   - Implement better backup strategy (3-2-1 rule: 3 copies, 2 media, 1 offsite)\n"
            "   - Add immutable backup storage"
        ),
    },
    {
        "category": "Backup & Recovery",
        "problem_title": "Hard drive failing - emergency data recovery",
        "problem_description": "Hard drive is making clicking noises, showing SMART errors, or becoming inaccessible. Need to recover data before it fails completely.",
        "problem_keywords": "hard drive failing, hdd clicking, smart error, drive dying, data recovery, disk failure, drive recovery",
        "solution_steps": (
            "1. STOP using the drive immediately:\n"
            "   - Every read/write operation may worsen the failure\n"
            "   - If it's the boot drive: Shut down the computer\n"
            "2. Check SMART status:\n"
            "   - Use CrystalDiskInfo (free) to check drive health\n"
            "   - Look for: Reallocated Sectors, Current Pending Sectors, Uncorrectable Errors\n"
            "   - Yellow = Warning, Red = Critical\n"
            "3. Create a disk image FIRST:\n"
            "   - Clone the failing drive to a healthy drive before trying recovery\n"
            "   - Use ddrescue (Linux) for best results with failing drives\n"
            "   - Or use Clonezilla to create a disk image\n"
            "   - Work with the clone, not the failing original\n"
            "4. Data recovery from the image:\n"
            "   - Mount the disk image on a working PC\n"
            "   - Copy important files: Documents, Desktop, Downloads, AppData\n"
            "   - Use Recuva or R-Studio if file system is damaged\n"
            "5. For SSDs:\n"
            "   - SSDs don't click but can fail suddenly\n"
            "   - SMART shows: Wear Leveling Count, Percentage Used\n"
            "   - Recovery from SSDs is harder than HDDs due to encryption\n"
            "6. Professional recovery:\n"
            "   - If clicking or not detecting: Professional clean room recovery\n"
            "   - Costs $300-$1500+ depending on severity\n"
            "   - Do NOT open the drive yourself\n"
            "7. Prevention: Implement automated backups and SMART monitoring\n"
            "   - Replace drives showing SMART warnings proactively"
        ),
    },
    {
        "category": "Backup & Recovery",
        "problem_title": "System Restore to previous state",
        "problem_description": "Computer started misbehaving after a driver or software install. Need to use System Restore to revert Windows to a previous good state.",
        "problem_keywords": "system restore, restore point, roll back, undo changes, previous state, restore windows, rollback",
        "solution_steps": (
            "1. Open System Restore:\n"
            "   - Search 'Create a restore point' > System Restore\n"
            "   - Or: rstrui.exe from Run dialog\n"
            "2. Select a restore point:\n"
            "   - Choose a date BEFORE the problem started\n"
            "   - Click 'Scan for affected programs' to see what will change\n"
            "   - This shows which programs and drivers will be removed/restored\n"
            "3. Run the restore:\n"
            "   - Computer will restart automatically\n"
            "   - Process takes 15-45 minutes\n"
            "   - Do NOT interrupt the process (can cause corruption)\n"
            "4. If Windows won't boot:\n"
            "   - Boot from Windows installation media\n"
            "   - Troubleshoot > Advanced options > System Restore\n"
            "   - Select restore point from the list\n"
            "5. If System Restore fails:\n"
            "   - Try in Safe Mode: Boot to Safe Mode then run rstrui.exe\n"
            "   - Try a different (older) restore point\n"
            "   - Check disk space: System Restore needs temporary space\n"
            "   - Run: sfc /scannow then retry\n"
            "6. Important notes:\n"
            "   - System Restore does NOT delete personal files\n"
            "   - It DOES remove apps installed after the restore point date\n"
            "   - It DOES revert system settings, drivers, and registry\n"
            "7. Enable restore points:\n"
            "   - System Properties > System Protection > Configure > Turn on\n"
            "   - Set max disk usage (5-10% is usually sufficient)"
        ),
    },
    {
        "category": "Backup & Recovery",
        "problem_title": "OneDrive or SharePoint version history restore",
        "problem_description": "User accidentally overwrote a file with bad data or needs to restore a previous version. File is stored in OneDrive or SharePoint.",
        "problem_keywords": "version history, restore version, previous version, onedrive restore, sharepoint restore, file version, undo changes file",
        "solution_steps": (
            "1. Restore a previous version in OneDrive:\n"
            "   - Right-click the file > Version history\n"
            "   - Or: OneDrive web > right-click file > Version history\n"
            "   - Browse versions by date\n"
            "   - Click the version to preview it\n"
            "   - Click 'Restore' to replace current with this version\n"
            "2. Restore in SharePoint:\n"
            "   - Navigate to document library\n"
            "   - Click ... (more) next to file > Version history\n"
            "   - Click the dropdown next to the version > Restore\n"
            "3. OneDrive 'Restore your OneDrive' (bulk restore):\n"
            "   - OneDrive web > Settings (gear) > Options > Restore your OneDrive\n"
            "   - Choose a date to restore everything to\n"
            "   - Useful after ransomware or mass file changes\n"
            "   - Works for up to 30 days back\n"
            "4. For deleted files:\n"
            "   - OneDrive web > Recycle Bin (keeps files 93 days)\n"
            "   - SharePoint > Recycle Bin > Second-stage Recycle Bin (admin)\n"
            "5. Version history settings:\n"
            "   - SharePoint: Library Settings > Versioning Settings\n"
            "   - Set number of major versions to keep (default varies)\n"
            "   - Enable: Create major AND minor versions for important libraries\n"
            "6. For Office files: Version history is also accessible within the Office app\n"
            "   - File > Info > Version History"
        ),
    },
    {
        "category": "Backup & Recovery",
        "problem_title": "Backup strategy planning (3-2-1 rule)",
        "problem_description": "Need to set up or improve a backup strategy for the organization. Looking for best practices and recommendations.",
        "problem_keywords": "backup strategy, 3-2-1 backup, backup plan, backup best practice, backup design, disaster recovery plan",
        "solution_steps": (
            "1. The 3-2-1 Backup Rule:\n"
            "   - 3 copies of your data (1 primary + 2 backups)\n"
            "   - 2 different types of media (e.g., local disk + cloud)\n"
            "   - 1 copy offsite (cloud or remote location)\n"
            "2. Identify what to back up:\n"
            "   - Critical: Servers, databases, email, file shares\n"
            "   - Important: User documents (if not in OneDrive/SharePoint)\n"
            "   - Configuration: Firewall rules, switch configs, GPO backups\n"
            "   - System state: Active Directory, certificates\n"
            "3. Set backup frequency:\n"
            "   - Servers: Daily full or daily incremental + weekly full\n"
            "   - Databases: Hourly transaction logs + daily full\n"
            "   - File servers: Daily incremental + weekly full\n"
            "   - Workstations: Continuous via OneDrive/File History\n"
            "4. Define retention:\n"
            "   - Daily backups: Keep 7 days\n"
            "   - Weekly backups: Keep 4 weeks\n"
            "   - Monthly backups: Keep 12 months\n"
            "   - Yearly backups: Keep 3-7 years (regulatory dependent)\n"
            "5. Test your backups regularly:\n"
            "   - Monthly: Test restore of individual files\n"
            "   - Quarterly: Test full system restore\n"
            "   - Document the testing results\n"
            "   - Untested backups are NOT backups\n"
            "6. Consider immutable backups:\n"
            "   - Cannot be deleted or modified after creation\n"
            "   - Protects against ransomware encrypting backups\n"
            "   - Veeam Hardened Repository, AWS S3 Object Lock, Azure Immutable Blob"
        ),
    },
]

DIAGNOSTIC_TREE = {
    "category": "Backup & Recovery",
    "root": {
        "title": "Backup & Recovery Troubleshooting",
        "node_type": "question",
        "question_text": "What backup or recovery issue do you need help with?",
        "children": [
            {
                "title": "Need to recover deleted or lost files",
                "node_type": "question",
                "question_text": "Where were the files stored?",
                "children": [
                    {
                        "title": "Local PC (Desktop, Documents, Downloads)",
                        "node_type": "solution",
                        "solution_text": "1. Check Recycle Bin first\n2. Right-click folder > Previous Versions (File History)\n3. Check OneDrive Recycle Bin if Known Folder Protection was on\n4. If not backed up: Use Recuva or TestDisk (STOP using the drive first)\n5. For critical data: Consider professional data recovery\n6. Prevention: Enable File History or OneDrive backup"
                    },
                    {
                        "title": "OneDrive or SharePoint",
                        "node_type": "solution",
                        "solution_text": "1. OneDrive/SharePoint: Check Recycle Bin (93 days retention)\n2. Version History: Right-click file > Version history > restore a previous version\n3. Bulk restore: OneDrive web > Settings > Restore your OneDrive (up to 30 days)\n4. SharePoint admin: Check Second-stage Recycle Bin\n5. Contact admin if beyond retention period"
                    },
                    {
                        "title": "File server / network share",
                        "node_type": "solution",
                        "solution_text": "1. Check if shadow copies are enabled: Right-click > Previous Versions\n2. Check server backup using Windows Server Backup or third-party tool\n3. Restore from most recent backup before deletion date\n4. Check Recycle Bin on the file server\n5. For critical data: Contact backup administrator"
                    }
                ]
            },
            {
                "title": "Backup job is failing",
                "node_type": "question",
                "question_text": "What type of backup?",
                "children": [
                    {
                        "title": "Windows built-in backup",
                        "node_type": "solution",
                        "solution_text": "1. File History: Check backup drive is connected\n2. Restart File History Service\n3. Turn off and re-enable File History with the backup drive\n4. Check for disk space on backup drive\n5. Alternative: Use OneDrive Known Folder Protection"
                    },
                    {
                        "title": "Server / enterprise backup (Veeam, Acronis)",
                        "node_type": "solution",
                        "solution_text": "1. Check job logs for specific error\n2. VSS errors: vssadmin list writers > restart failed services > net stop vss && net start vss\n3. Check backup storage space\n4. Verify credentials/permissions on target\n5. Run backup manually to test\n6. Update backup software to latest version"
                    }
                ]
            },
            {
                "title": "Need to restore entire PC / system",
                "node_type": "solution",
                "solution_text": "1. If PC boots: Settings > Recovery > Reset this PC > Keep my files\n2. If PC won't boot: Boot from Windows USB > Repair > System Restore\n3. For system image: Boot from Windows USB > Troubleshoot > System Image Recovery\n4. For enterprise: Use deployment tools (SCCM/Intune Autopilot) to reimage\n5. After restore: Run Windows Update, reinstall missing apps\n6. Restore user data from backup"
            },
            {
                "title": "Need help setting up backups",
                "node_type": "solution",
                "solution_text": "1. Follow 3-2-1 rule: 3 copies, 2 media types, 1 offsite\n2. For workstations: Enable OneDrive Known Folder Protection + File History\n3. For servers: Daily backups with weekly full + daily incremental\n4. Set retention: 7 daily + 4 weekly + 12 monthly\n5. Test restores monthly\n6. Consider immutable backups for ransomware protection\n7. Document your backup plan and recovery procedures"
            }
        ]
    }
}
