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
    {
        "category": "Backup & Recovery",
        "problem_title": "Backup job running too long and overlapping schedule",
        "problem_description": "Backup jobs take longer than the backup window and overlap with the next scheduled run. This causes performance issues during business hours.",
        "problem_keywords": "backup slow, backup window, backup duration, long backup, backup overlap, backup performance, slow backup",
        "solution_steps": (
            "1. Identify the bottleneck:\n"
            "   - Is it source disk I/O? (Reading from production server)\n"
            "   - Is it network bandwidth? (Transferring to backup target)\n"
            "   - Is it target disk I/O? (Writing to backup storage)\n"
            "   - Check backup software logs for timing breakdown\n"
            "2. Use incremental backups:\n"
            "   - Full backup: Copies everything (slowest)\n"
            "   - Incremental: Only changed blocks since last backup (fastest)\n"
            "   - Differential: Changed since last full (middle ground)\n"
            "   - Schedule: Full weekly + incremental daily\n"
            "3. Change block tracking:\n"
            "   - VMware CBT (Changed Block Tracking) dramatically speeds VM backups\n"
            "   - Hyper-V RCT (Resilient Change Tracking)\n"
            "   - If CBT/RCT was reset: First incremental will be slow\n"
            "4. Network optimization:\n"
            "   - Dedicated backup LAN/VLAN (separate from production traffic)\n"
            "   - 10 GbE between backup server and targets\n"
            "   - Enable backup software compression and deduplication\n"
            "5. Exclude unnecessary data:\n"
            "   - Temp files, page files, recycle bin\n"
            "   - Browser caches, Windows Update cache\n"
            "   - Non-essential log files\n"
            "6. Parallel processing:\n"
            "   - Most backup software can run multiple jobs simultaneously\n"
            "   - Balance: Too many parallel jobs = resource contention\n"
            "   - Start with 2-4 concurrent jobs and adjust\n"
            "7. Stagger schedules: Don't start all backup jobs at the same time"
        ),
    },
    {
        "category": "Backup & Recovery",
        "problem_title": "Backup verification and restore test failed",
        "problem_description": "Backup verification or test restore shows corrupted data, incomplete restore, or restore fails entirely despite backup logs showing success.",
        "problem_keywords": "backup verification, restore test, backup integrity, test restore, corrupted backup, backup check, verify backup",
        "solution_steps": (
            "1. Why test restores matter:\n"
            "   - A backup is worthless if it can't be restored\n"
            "   - Backup software reports 'success' based on job completion\n"
            "   - Doesn't verify data readability or application consistency\n"
            "2. Automated verification:\n"
            "   - Veeam SureBackup: Boots VMs from backup to verify\n"
            "   - Tests: VM boots, application responds, network connectivity\n"
            "   - Runs in isolated network (no production impact)\n"
            "3. Manual restore test:\n"
            "   - Monthly: Restore a random file from backup and verify contents\n"
            "   - Quarterly: Full server restore to test hardware/VM\n"
            "   - Document: Time to restore, any issues encountered\n"
            "4. Common restore failures:\n"
            "   - Missing backup chain: Incremental requires all prior incrementals + full\n"
            "   - Backup media rotation: Tape/disk not available\n"
            "   - Expired retention: Backup was deleted by retention policy\n"
            "   - Encryption key lost: Encrypted backups unrecoverable without key\n"
            "5. Database restore testing:\n"
            "   - SQL/Exchange: Restore to a test server or recovery database\n"
            "   - Verify database integrity: DBCC CHECKDB (SQL Server)\n"
            "   - Test: Can you query data? Are all tables present?\n"
            "6. Bare-metal recovery test:\n"
            "   - Restore OS + applications to new/blank hardware\n"
            "   - Verify: Driver compatibility, application functionality\n"
            "   - Document the process (for disaster recovery runbook)\n"
            "7. Tracking: Maintain a restore test log with date, scope, result, and time-to-restore"
        ),
    },
    {
        "category": "Backup & Recovery",
        "problem_title": "Cloud backup (Azure/AWS) upload slow or failing",
        "problem_description": "Backup to cloud storage (Azure Blob, AWS S3, Wasabi, Backblaze) is extremely slow, times out, or fails consistently with network or authentication errors.",
        "problem_keywords": "cloud backup, azure backup, aws backup, s3 backup, cloud upload, offsite backup, slow upload, cloud storage",
        "solution_steps": (
            "1. Check internet bandwidth:\n"
            "   - Run a speed test to the cloud region\n"
            "   - 10 Mbps upload = ~100 GB per day maximum\n"
            "   - 100 Mbps upload = ~1 TB per day maximum\n"
            "   - Calculate: Is your data smaller than daily upload capacity?\n"
            "2. Bandwidth throttling:\n"
            "   - Backup software may have upload speed limits\n"
            "   - Check: Backup settings > Network > throttle/bandwidth limit\n"
            "   - Schedule: Full speed off-hours, throttled during business\n"
            "3. Authentication errors:\n"
            "   - Azure: Check storage account access keys or SAS tokens\n"
            "   - AWS: Check IAM access key and secret key\n"
            "   - Tokens/keys may have expired or been rotated\n"
            "4. Network errors:\n"
            "   - Timeout: Increase connection timeout in backup software\n"
            "   - Firewall: Ensure outbound HTTPS (443) is allowed\n"
            "   - Proxy: Configure backup software to use web proxy if required\n"
            "5. Initial seed:\n"
            "   - First backup to cloud is always the largest (full backup)\n"
            "   - Consider: Azure Data Box or AWS Snowball for initial seed >10 TB\n"
            "   - After initial seed: Incremental backups are much smaller\n"
            "6. Compression/deduplication:\n"
            "   - Enable compression before upload (reduces data sent)\n"
            "   - WAN acceleration (if using Veeam Cloud Connect)\n"
            "   - Source-side dedup reduces upload volume\n"
            "7. Multi-part upload: Ensure backup software uses chunked/multi-part upload for large files"
        ),
    },
    {
        "category": "Backup & Recovery",
        "problem_title": "Exchange mailbox or email recovery from backup",
        "problem_description": "User needs a deleted email or mailbox recovered from backup. Need to restore specific items without restoring the entire Exchange database.",
        "problem_keywords": "exchange recovery, mailbox restore, email recovery, exchange backup, item recovery, deleted email, exchange restore",
        "solution_steps": (
            "1. Check Deleted Items first:\n"
            "   - Outlook > Deleted Items folder > search for the email\n"
            "   - If not there: Recover Deleted Items option in Outlook\n"
            "   - Online: outlook.office.com > Deleted Items > Recover items\n"
            "2. Exchange retention policy:\n"
            "   - Deleted Items retention: Default 14-30 days in Exchange Online\n"
            "   - Items are in 'Recoverable Items' folder during this period\n"
            "   - Admin: Search-Mailbox or Compliance eDiscovery to find items\n"
            "3. Exchange Online (M365):\n"
            "   - Admin: Exchange Admin Center > Recipients > Mailboxes\n"
            "   - Select user > Mailbox > Manage litigation hold\n"
            "   - eDiscovery: Compliance Center > Content Search\n"
            "4. Deleted mailbox:\n"
            "   - Exchange Online: Soft-deleted mailboxes retained 30 days\n"
            "   - Restore: Connect-ExchangeOnline; Undo-SoftDeletedMailbox\n"
            "   - On-premises: Mailbox retained per deleted mailbox retention\n"
            "5. Granular restore from backup:\n"
            "   - Veeam Explorer for Exchange: Browse backup > find specific email\n"
            "   - Restore directly to the user's mailbox\n"
            "   - No need to restore entire database\n"
            "6. Full database restore:\n"
            "   - If granular restore not available: Restore Exchange DB to recovery database\n"
            "   - New-MailboxRestoreRequest to copy items from recovery DB to production\n"
            "   - This is complex and time-consuming\n"
            "7. Prevention: Enable litigation hold or full retention policies for critical mailboxes"
        ),
    },
    {
        "category": "Backup & Recovery",
        "problem_title": "Active Directory disaster recovery procedure",
        "problem_description": "Active Directory Domain Controller has failed catastrophically or AD database is corrupted. Need to restore AD to a functional state.",
        "problem_keywords": "ad recovery, domain controller restore, active directory backup, ad disaster, dc restore, ad corruption, ntds dit",
        "solution_steps": (
            "1. Assess the situation:\n"
            "   - How many DCs exist? If multiple: Other DCs still functioning\n"
            "   - Single DC failure: AD is still online via other DCs\n"
            "   - All DCs down: Critical - AD restore needed immediately\n"
            "2. If other DCs exist:\n"
            "   - AD replicates across DCs - no restore needed\n"
            "   - Rebuild failed DC: Install Windows Server > dcpromo > replicate\n"
            "   - Or restore from backup and let replication catch up\n"
            "3. Authoritative vs Non-authoritative restore:\n"
            "   - Non-authoritative: Restore backup then let replication update it\n"
            "   - Authoritative: Restore and FORCE other DCs to accept this data\n"
            "   - Use authoritative when object was deleted and replicated to all DCs\n"
            "4. Non-authoritative restore steps:\n"
            "   - Boot DC into DSRM (Directory Services Restore Mode)\n"
            "   - F8 during boot > DSRM\n"
            "   - wbadmin get versions (find backup)\n"
            "   - wbadmin start systemstaterecovery -version:backup_version\n"
            "   - Reboot > AD will replicate from other DCs\n"
            "5. Authoritative restore:\n"
            "   - After non-authoritative restore, before reboot:\n"
            "   - ntdsutil > activate instance ntds > authoritative restore\n"
            "   - restore object/subtree as needed\n"
            "   - This increments the version number so other DCs accept this data\n"
            "6. AD Recycle Bin:\n"
            "   - If enabled: Restore deleted objects without backup\n"
            "   - Get-ADObject -Filter {isDeleted -eq $true} -IncludeDeletedObjects\n"
            "   - Restore-ADObject -Identity <objectGUID>\n"
            "   - Default retention: 180 days\n"
            "7. Prevention: Minimum 2 DCs per domain, regular System State backups, enable AD Recycle Bin"
        ),
    },
    {
        "category": "Backup & Recovery",
        "problem_title": "Virtual machine snapshot/checkpoint management issues",
        "problem_description": "VM snapshots/checkpoints are growing too large, causing disk space issues, or reverting a snapshot causes data loss or application corruption.",
        "problem_keywords": "vm snapshot, checkpoint, snapshot too large, revert snapshot, snapshot management, vmware snapshot, hyper-v checkpoint",
        "solution_steps": (
            "1. Snapshots are NOT backups:\n"
            "   - Snapshots capture a point-in-time state\n"
            "   - They grow continuously (delta/differencing disk)\n"
            "   - Long-running snapshots degrade performance and risk corruption\n"
            "   - Best practice: Delete snapshots within 72 hours\n"
            "2. Snapshot growing too large:\n"
            "   - Every write to the VM goes to the snapshot delta file\n"
            "   - Active database servers: Snapshots grow very fast (GBs/day)\n"
            "   - Monitor snapshot size: VMware (datastore browser), Hyper-V (checkpoint files)\n"
            "3. Deleting/merging snapshots:\n"
            "   - VMware: Snapshot Manager > Delete (merges delta back to base VMDK)\n"
            "   - Hyper-V: Delete checkpoint (merges .avhdx into parent VHD)\n"
            "   - Large snapshots take time to merge (disk I/O intensive)\n"
            "   - Schedule merge during maintenance window\n"
            "4. Reverting a snapshot:\n"
            "   - All changes AFTER the snapshot are lost permanently\n"
            "   - Applications may be in an inconsistent state\n"
            "   - Databases: Require crash recovery after revert\n"
            "   - Confirm with stakeholders before reverting\n"
            "5. Stuck/orphaned snapshots:\n"
            "   - VMware: Consolidate disks if snapshot files exist but Snapshot Manager is empty\n"
            "   - Virtual Machine > Snapshot > Consolidate\n"
            "   - Hyper-V: Manually merge .avhdx files if checkpoint is orphaned\n"
            "6. Quiescing:\n"
            "   - VMware quiesced snapshot: Flushes app memory to disk before snapshot\n"
            "   - Requires VMware Tools and running VSS inside the VM\n"
            "   - Application-consistent vs crash-consistent snapshots\n"
            "7. Policy: Implement monitoring alerts for snapshots older than 24-48 hours"
        ),
    },
    {
        "category": "Backup & Recovery",
        "problem_title": "Tape backup library or drive errors",
        "problem_description": "Tape backup jobs fail due to tape drive errors, media write failures, or tape library mechanical issues. Tapes may be unreadable or rejected.",
        "problem_keywords": "tape backup, tape drive, tape error, lto, tape library, tape media, tape write error, tape failure",
        "solution_steps": (
            "1. Check tape drive status:\n"
            "   - Device Manager: Tape drive should show no errors\n"
            "   - Backup software: Check tape drive status and error logs\n"
            "   - LED indicators on the drive: Check vendor documentation for codes\n"
            "2. Media errors:\n"
            "   - 'Media write error' or 'Bad tape': The tape itself may be damaged\n"
            "   - Try a new tape from a different batch\n"
            "   - If multiple tapes fail: Drive may need cleaning\n"
            "3. Clean the drive:\n"
            "   - Use ONLY the recommended cleaning tape for your drive model\n"
            "   - LTO: Universal cleaning cartridge (limited number of uses)\n"
            "   - Most drives have a cleaning indicator LED\n"
            "   - Clean every 20-30 tape mounts or when indicator lights\n"
            "4. Tape compatibility:\n"
            "   - LTO drives read/write current generation and read one generation back\n"
            "   - LTO-9 drive: Reads/writes LTO-9, reads LTO-8\n"
            "   - Can't use tapes from 3+ generations back\n"
            "5. Library mechanical issues:\n"
            "   - Robotic arm may fail to pick/place tapes\n"
            "   - Barcode reader may not scan tape labels\n"
            "   - Power cycle the library\n"
            "   - Reinventory: Backup software > Library > Inventory\n"
            "6. Driver and firmware:\n"
            "   - Update tape drive firmware from manufacturer\n"
            "   - Update HBA (host bus adapter) drivers and firmware\n"
            "   - Ensure backup software supports the drive model\n"
            "7. Rotation: Retire tapes after vendor-recommended number of passes (typically 200-300)"
        ),
    },
    {
        "category": "Backup & Recovery",
        "problem_title": "SQL Server database restore to point-in-time",
        "problem_description": "Need to restore a SQL Server database to a specific point in time (e.g., just before accidental data deletion) using transaction log backups.",
        "problem_keywords": "sql restore, point in time, transaction log, sql backup, database restore, sql recovery, log restore, pitr",
        "solution_steps": (
            "1. Requirements for point-in-time restore:\n"
            "   - Database must be in FULL recovery model (not SIMPLE)\n"
            "   - Must have: Full backup + all transaction log backups up to the desired point\n"
            "   - Check: SELECT name, recovery_model_desc FROM sys.databases\n"
            "2. Identify the time:\n"
            "   - When exactly did the data loss occur?\n"
            "   - Review application logs, user reports, SQL audit logs\n"
            "   - Restore to just BEFORE the damaging event\n"
            "3. Restore sequence:\n"
            "   - Restore the latest full backup WITH NORECOVERY:\n"
            "   - RESTORE DATABASE dbname FROM DISK='full.bak' WITH NORECOVERY\n"
            "   - Restore each log backup in order WITH NORECOVERY:\n"
            "   - RESTORE LOG dbname FROM DISK='log1.trn' WITH NORECOVERY\n"
            "4. Final restore with STOPAT:\n"
            "   - Restore the last log backup to the exact time:\n"
            "   - RESTORE LOG dbname FROM DISK='logN.trn' WITH RECOVERY, STOPAT='2024-01-15 14:30:00'\n"
            "   - Database is now at the state of that exact timestamp\n"
            "5. Restore to different database:\n"
            "   - Best practice: Restore as a different database name first\n"
            "   - WITH MOVE to different file locations\n"
            "   - Verify the data, then copy/merge needed data to production\n"
            "6. Tail-log backup:\n"
            "   - Before restoring: Take a tail-log backup of the current database\n"
            "   - BACKUP LOG dbname TO DISK='tail.trn' WITH NORECOVERY\n"
            "   - This captures transactions since the last log backup\n"
            "7. Prevention: Ensure transaction log backups run every 15-30 minutes for important databases"
        ),
    },
    {
        "category": "Backup & Recovery",
        "problem_title": "Backup storage capacity running out",
        "problem_description": "Backup storage (NAS, SAN, disk repository) is running low on space. New backups fail with 'not enough space' errors.",
        "problem_keywords": "backup storage full, backup space, storage capacity, backup repository, not enough space, backup disk full, retention",
        "solution_steps": (
            "1. Check current usage:\n"
            "   - Backup software dashboard: Storage utilization percentage\n"
            "   - NAS/SAN management: Volume capacity\n"
            "   - What's consuming the most space?\n"
            "2. Review retention policy:\n"
            "   - Current retention may be keeping too many restore points\n"
            "   - Example: 30 daily + 12 monthly + 7 yearly = significant storage\n"
            "   - Consider reducing: 14 daily + 6 monthly + 2 yearly\n"
            "   - Align with business/compliance requirements\n"
            "3. Deduplication:\n"
            "   - Enable deduplication on backup storage\n"
            "   - Typical savings: 50-80% for file server backups\n"
            "   - Windows Server Data Deduplication\n"
            "   - Or backup software built-in dedup (Veeam, Commvault)\n"
            "4. Compression:\n"
            "   - Enable backup compression if not already active\n"
            "   - Typical savings: 30-50% reduction\n"
            "   - Software compression uses CPU, hardware compression uses backup device\n"
            "5. Clean up orphaned backups:\n"
            "   - Old backup jobs that were deleted but data remains\n"
            "   - Backup software: Run storage cleanup/maintenance\n"
            "   - Check for manually copied files consuming space\n"
            "6. Tiered storage:\n"
            "   - Recent backups: Fast storage (SSD/SAS)\n"
            "   - Older backups: Cheaper storage (SATA/cloud)\n"
            "   - Archive backups: Tape or cold cloud storage (cheapest)\n"
            "7. Capacity planning: Track storage growth rate and purchase additional capacity proactively"
        ),
    },
    {
        "category": "Backup & Recovery",
        "problem_title": "File server data recovery after accidental deletion",
        "problem_description": "User or admin accidentally deleted a large number of files from the file server. Need to recover files from various recovery methods before using backup.",
        "problem_keywords": "file recovery, accidental deletion, deleted files, file restore, recycle bin, shadow copy, previous versions",
        "solution_steps": (
            "1. Check Recycle Bin first:\n"
            "   - Server Recycle Bin: Check the recycle bin on the server\n"
            "   - Network share: Recycle Bin behavior depends on configuration\n"
            "   - By default: Files deleted from network shares bypass recycle bin\n"
            "   - Enable: Server-side recycle bin (not default on Windows)\n"
            "2. Previous Versions (Shadow Copies):\n"
            "   - Right-click folder > Properties > Previous Versions tab\n"
            "   - Shows point-in-time snapshots if Volume Shadow Copy is enabled\n"
            "   - Can restore individual files or entire folders\n"
            "   - This is the fastest recovery method\n"
            "3. Shadow Copy configuration:\n"
            "   - Must be enabled BEFORE the deletion occurs\n"
            "   - Server Manager > File and Storage Services > configure\n"
            "   - Set schedule: Every 2-4 hours during business hours\n"
            "   - Allocate sufficient shadow copy storage (10-20% of volume)\n"
            "4. Full backup restore:\n"
            "   - If Shadow Copies not available: Restore from backup\n"
            "   - Identify the most recent backup before the deletion\n"
            "   - Restore to an alternate location to avoid overwriting current data\n"
            "   - Then merge/copy needed files to production\n"
            "5. Partial restore:\n"
            "   - Most backup software allows browsing and selecting specific files\n"
            "   - Veeam: File Level Restore from backup\n"
            "   - Windows Server Backup: wbadmin start recovery -itemType:File\n"
            "6. Data recovery tools (last resort):\n"
            "   - If no backup or shadow copies: Third-party recovery tools\n"
            "   - STOP writing to the volume immediately (prevents overwrite)\n"
            "   - Tools: Recuva, Disk Drill, R-Studio\n"
            "   - Success rate varies depending on time since deletion\n"
            "7. Prevention: Enable Shadow Copies, configure server-side recycle bin, frequent backups"
        ),
    },
    {
        "category": "Backup & Recovery",
        "problem_title": "Disaster recovery site failover testing and procedures",
        "problem_description": "DR site failover test is planned or an actual disaster requires failover. Need procedures for activating backup site and verifying services.",
        "problem_keywords": "disaster recovery, dr failover, dr test, failover site, business continuity, dr plan, rpo, rto, site failover",
        "solution_steps": (
            "1. DR planning (before disaster):\n"
            "   - Document RTO (Recovery Time Objective): How fast must we recover?\n"
            "   - Document RPO (Recovery Point Objective): How much data can we lose?\n"
            "   - Example: RTO=4 hours, RPO=1 hour (max 1 hour of data loss)\n"
            "2. DR test preparation:\n"
            "   - Schedule test during low-impact period\n"
            "   - Notify all stakeholders\n"
            "   - Document: Test scope, participating systems, success criteria\n"
            "   - Have rollback plan ready\n"
            "3. Failover steps (common):\n"
            "   - Activate replication targets (Hyper-V Replica, VMware SRM, Zerto)\n"
            "   - Update DNS records to point to DR site\n"
            "   - Verify Active Directory (DC at DR site must be reachable)\n"
            "   - Test network connectivity between DR site and remaining services\n"
            "4. Application verification:\n"
            "   - Start critical applications in priority order\n"
            "   - Test: Can users access email, file shares, LOB applications?\n"
            "   - Verify database connections and data integrity\n"
            "   - Test inbound/outbound external communications\n"
            "5. Communication:\n"
            "   - Notify staff of DR activation and new access procedures\n"
            "   - External communications: Customer/partner notification\n"
            "   - Status page or email updates on recovery progress\n"
            "6. Failback:\n"
            "   - After primary site restored: Reverse replication from DR to primary\n"
            "   - Schedule failback during maintenance window\n"
            "   - Verify all data is synced before switching back\n"
            "7. Documentation: After each test, document what worked, what failed, and update DR plan"
        ),
    },
    {
        "category": "Backup & Recovery",
        "problem_title": "Windows Server bare metal recovery (BMR) from backup",
        "problem_description": "A Windows Server has completely failed (hardware failure, OS corruption). Need to restore the entire server from a bare metal backup to new hardware.",
        "problem_keywords": "bare metal, bmr, server restore, full recovery, hardware failure, os restore, complete restore, server rebuild",
        "solution_steps": (
            "1. What is Bare Metal Recovery:\n"
            "   - Restores the entire server: OS, applications, data, configuration\n"
            "   - Requires a BMR-capable backup (includes system state + all volumes)\n"
            "   - Can restore to same or different hardware\n"
            "2. Prerequisites:\n"
            "   - BMR backup must exist (Windows Server Backup or third-party)\n"
            "   - Windows Server installation media (same version as backup)\n"
            "   - Access to backup media (external drive, network share, tape)\n"
            "   - New hardware with sufficient disk space\n"
            "3. Windows Server Backup BMR:\n"
            "   - Boot from Windows Server installation media\n"
            "   - Click 'Repair your computer' (bottom left)\n"
            "   - Troubleshoot > System Image Recovery\n"
            "   - Select the backup location and image\n"
            "   - Follow wizard to restore all volumes\n"
            "4. Different hardware:\n"
            "   - Windows may not boot on different hardware (driver mismatch)\n"
            "   - After BMR: May need to inject storage/NIC drivers\n"
            "   - Third-party tools (Veeam) handle dissimilar hardware better\n"
            "5. Veeam BMR:\n"
            "   - Boot from Veeam Recovery Media ISO\n"
            "   - Connect to Veeam Backup repository\n"
            "   - Select the server backup and restore point\n"
            "   - Disk mapping: Map backup disks to new hardware disks\n"
            "   - Automatic driver injection for new hardware\n"
            "6. Post-restore:\n"
            "   - Verify all services start correctly\n"
            "   - Check event logs for driver or service errors\n"
            "   - If DC: Verify AD replication (repadmin /replsummary)\n"
            "   - Update BIOS/firmware on new hardware\n"
            "7. Virtual alternative: Restore as a VM instead of physical (P2V) for faster recovery"
        ),
    },
    {
        "category": "Backup & Recovery",
        "problem_title": "OneDrive or SharePoint file recovery and version restore",
        "problem_description": "User needs to recover deleted files from OneDrive or SharePoint, or restore a previous version of a document that was overwritten or corrupted.",
        "problem_keywords": "onedrive recovery, sharepoint recovery, version history, deleted file, recycle bin, file version, restore file",
        "solution_steps": (
            "1. OneDrive Recycle Bin:\n"
            "   - OneDrive.com > Recycle Bin (left sidebar)\n"
            "   - Files are kept in recycle bin for 93 days\n"
            "   - Select files > Restore (returns to original location)\n"
            "2. Second-stage Recycle Bin:\n"
            "   - If deleted from first recycle bin:\n"
            "   - Site Collection Recycle Bin (admin access)\n"
            "   - SharePoint admin center > Sites > select site > Recycle Bin\n"
            "   - Also retained for 93 days total (from initial deletion)\n"
            "3. Version History:\n"
            "   - OneDrive/SharePoint automatically keeps version history\n"
            "   - Right-click file > Version History\n"
            "   - View, download, or restore any previous version\n"
            "   - Default: 500 versions kept\n"
            "4. OneDrive 'Restore your OneDrive':\n"
            "   - For ransomware or mass changes: OneDrive.com > Settings > Restore your OneDrive\n"
            "   - Restores entire OneDrive to any point in the last 30 days\n"
            "   - Shows activity timeline to pick the right point\n"
            "5. SharePoint Library restore:\n"
            "   - SharePoint site > Settings > Restore this library\n"
            "   - Same as OneDrive restore but for document libraries\n"
            "   - 30-day rolling window\n"
            "6. Admin recovery:\n"
            "   - If beyond recycle bin retention: Need third-party backup\n"
            "   - Veeam for M365, AvePoint, Druva, etc.\n"
            "   - Microsoft does NOT provide long-term backup of M365 data\n"
            "7. Retention policies: Use Microsoft Purview retention policies for compliance-based retention"
        ),
    },
    {
        "category": "Backup & Recovery",
        "problem_title": "Backup encryption and security best practices",
        "problem_description": "Need to implement or troubleshoot backup encryption. Concerns about backup data being stolen, encryption key management, or compliance requirements.",
        "problem_keywords": "backup encryption, encrypted backup, encryption key, backup security, key management, compliance, data protection",
        "solution_steps": (
            "1. Why encrypt backups:\n"
            "   - Backups contain all your sensitive data\n"
            "   - If backup media is stolen/lost: Data is exposed\n"
            "   - Compliance: HIPAA, PCI-DSS, GDPR require data protection\n"
            "   - Encrypt backups at rest AND in transit\n"
            "2. Encryption types:\n"
            "   - Software encryption: Backup software encrypts data (uses CPU)\n"
            "   - Hardware encryption: Tape drive or disk controller encrypts\n"
            "   - AES-256 is the standard for backup encryption\n"
            "3. Key management:\n"
            "   - CRITICAL: If you lose the encryption key, backup is UNRECOVERABLE\n"
            "   - Store keys separately from backup data\n"
            "   - Multiple key custodians (no single point of failure)\n"
            "   - Document key recovery procedures\n"
            "4. Windows Server Backup:\n"
            "   - Supports backup password protection\n"
            "   - BitLocker on backup drives adds encryption at rest\n"
            "5. Veeam encryption:\n"
            "   - Backup job settings > Storage > Enable backup file encryption\n"
            "   - Password is used to derive the encryption key\n"
            "   - Enterprise Manager stores encrypted passwords for recovery\n"
            "6. Cloud backup encryption:\n"
            "   - Azure Backup: Encrypted by default (service-managed keys)\n"
            "   - Option: Customer-managed keys in Azure Key Vault\n"
            "   - AWS: S3 server-side encryption (SSE-S3, SSE-KMS, SSE-C)\n"
            "7. Testing: Regularly test restoring encrypted backups to verify key/password still works"
        ),
    },
    {
        "category": "Backup & Recovery",
        "problem_title": "Backup agent or client not connecting to backup server",
        "problem_description": "Backup agent installed on a server or workstation can't communicate with the central backup server. Jobs fail with 'agent not responding' errors.",
        "problem_keywords": "backup agent, agent offline, agent not responding, backup client, agent connection, agent error, agent communication",
        "solution_steps": (
            "1. Check agent service:\n"
            "   - On the protected machine: Services.msc\n"
            "   - Find the backup agent service (e.g., Veeam Agent, Acronis Agent)\n"
            "   - Ensure it's running with 'Automatic' startup\n"
            "   - If stopped: Start it and check event logs for errors\n"
            "2. Network connectivity:\n"
            "   - Can the agent reach the backup server? ping backup-server\n"
            "   - Check specific ports:\n"
            "   - Veeam: TCP 6160, 6162 (agent ports)\n"
            "   - Acronis: TCP 9876, 7780\n"
            "   - Test: Test-NetConnection -ComputerName backup-server -Port 6160\n"
            "3. Firewall:\n"
            "   - Windows Firewall may block agent communication\n"
            "   - Check: Inbound rules for the backup agent on the protected machine\n"
            "   - Check: Network firewall between the machine and backup server\n"
            "4. Agent version:\n"
            "   - Agent version must be compatible with backup server version\n"
            "   - After backup server upgrade: Update agents to match\n"
            "   - Check vendor documentation for compatibility matrix\n"
            "5. Certificate/authentication:\n"
            "   - Agent may use certificates for authentication to the server\n"
            "   - Expired certificates: Agent can't authenticate\n"
            "   - Re-register the agent with the backup server\n"
            "6. DNS resolution:\n"
            "   - Agent may use hostname to reach backup server\n"
            "   - If DNS is failing: Agent can't find the server\n"
            "   - Add backup server IP to hosts file as workaround\n"
            "7. Reinstall: If all else fails, uninstall and reinstall the backup agent"
        ),
    },
    {
        "category": "Backup & Recovery",
        "problem_title": "RAID array degraded or failed drive replacement",
        "problem_description": "Server RAID array shows degraded status due to a failed drive. Need to replace the drive and rebuild the array without data loss.",
        "problem_keywords": "raid degraded, failed drive, raid rebuild, disk replacement, raid array, hot spare, drive failure, raid recovery",
        "solution_steps": (
            "1. Identify the failure:\n"
            "   - RAID controller management utility (Dell PERC, HP Smart Array)\n"
            "   - Or: Server front panel LEDs (amber LED = failed drive)\n"
            "   - Note: Drive slot number, model, size, speed\n"
            "2. RAID levels and tolerance:\n"
            "   - RAID 1 (mirror): Survives 1 drive failure\n"
            "   - RAID 5: Survives 1 drive failure\n"
            "   - RAID 6: Survives 2 drive failures\n"
            "   - RAID 10: Survives 1 drive per mirror pair\n"
            "   - RAID 0: NO redundancy - any failure = total data loss\n"
            "3. Hot swap replacement:\n"
            "   - Most server RAID supports hot swap (no downtime)\n"
            "   - Pull the failed drive carefully (correct slot!)\n"
            "   - Insert the replacement drive (same size or larger, same speed)\n"
            "   - RAID controller should automatically start rebuild\n"
            "4. Rebuild process:\n"
            "   - Rebuild can take hours to days depending on array size\n"
            "   - During rebuild: Performance is degraded, NO redundancy\n"
            "   - DO NOT reboot or power off during rebuild\n"
            "   - If another drive fails during rebuild: Possible data loss\n"
            "5. Replacement drive requirements:\n"
            "   - Same size or larger than the failed drive\n"
            "   - Same interface (SAS/SATA/NVMe) and speed\n"
            "   - Preferably same model/firmware\n"
            "   - Use enterprise/server-grade drives (not desktop drives)\n"
            "6. Hot spare:\n"
            "   - Configure a hot spare drive that auto-replaces on failure\n"
            "   - Rebuild starts immediately without human intervention\n"
            "   - Reduces risk window significantly\n"
            "7. After rebuild: Verify array status is 'Optimal' and run a consistency check"
        ),
    },
    {
        "category": "Backup & Recovery",
        "problem_title": "Backup compliance and audit reporting",
        "problem_description": "Need to generate backup compliance reports for auditors. Must prove that backups run successfully, meet retention requirements, and restore tests are performed.",
        "problem_keywords": "backup compliance, audit report, backup report, retention compliance, backup sla, regulatory, backup documentation",
        "solution_steps": (
            "1. What auditors typically ask for:\n"
            "   - Backup success rates (last 30/90/365 days)\n"
            "   - Backup retention schedules and evidence of compliance\n"
            "   - Restore test results and frequency\n"
            "   - Encryption of backup data at rest and in transit\n"
            "   - Offsite/disaster recovery copy\n"
            "2. Backup success reports:\n"
            "   - Most backup software has built-in reporting\n"
            "   - Veeam ONE: Detailed reports on success/failure/warning\n"
            "   - Export reports as PDF for audit evidence\n"
            "   - Include: Job name, schedule, last successful run, data protected\n"
            "3. Retention evidence:\n"
            "   - Document your retention policy (e.g., daily 30 days, monthly 12 months)\n"
            "   - Show backup software configuration matching the policy\n"
            "   - Demonstrate that restore points exist for the required retention period\n"
            "4. Restore test documentation:\n"
            "   - Log every restore test: Date, scope, result, time to restore\n"
            "   - Include: What was restored and verification of data integrity\n"
            "   - Recommendation: Monthly file-level test, quarterly full server test\n"
            "5. Regulatory requirements:\n"
            "   - HIPAA: Backup and disaster recovery plan required\n"
            "   - PCI-DSS: Regular backup testing, encrypted media handling\n"
            "   - SOX: Data retention and backup integrity\n"
            "   - GDPR: Right to erasure may conflict with backup retention\n"
            "6. Automated monitoring:\n"
            "   - Set up email alerts for backup failures\n"
            "   - Dashboard showing real-time backup status\n"
            "   - Weekly backup summary report to IT management\n"
            "7. Documentation: Maintain a Backup Policy document reviewed annually with management sign-off"
        ),
    },
    {
        "category": "Backup & Recovery",
        "problem_title": "Backup software agent crashes or stops responding",
        "problem_description": "Backup agent service crashes during backup jobs, becomes unresponsive, or fails to start. Backup jobs show 'agent not available' or 'communication error' status.",
        "problem_keywords": "backup agent, agent crash, backup service, agent unresponsive, agent not available, backup client, agent communication",
        "solution_steps": (
            "1. Check agent service:\n"
            "   - services.msc > find backup agent service\n"
            "   - Status should be Running\n"
            "   - If stopped: Try to start manually\n"
            "   - Set startup type to Automatic\n"
            "2. Agent logs:\n"
            "   - Check application event log for agent errors\n"
            "   - Agent log directory (varies by product)\n"
            "   - Look for: memory errors, access denied, certificate errors\n"
            "3. Resource issues:\n"
            "   - Agent crash during backup: Check available memory\n"
            "   - Large backup sets can exhaust agent memory\n"
            "   - Increase agent memory allocation in config\n"
            "   - Check disk space on temp/cache location\n"
            "4. Agent update:\n"
            "   - Outdated agent versions have known bugs\n"
            "   - Update agent to latest version from backup server\n"
            "   - Check compatibility matrix with OS version\n"
            "5. Reinstall agent: Uninstall agent, delete agent config folder, reboot, reinstall agent, re-register with backup server"
        ),
    },
    {
        "category": "Backup & Recovery",
        "problem_title": "Incremental or differential backup chain broken",
        "problem_description": "Incremental or differential backups failing because the backup chain is broken. Restore fails due to missing incremental links. Backup software requests a new full backup.",
        "problem_keywords": "incremental backup, differential backup, backup chain, broken chain, full backup required, backup dependency, restore chain",
        "solution_steps": (
            "1. Understanding backup chains:\n"
            "   - Full: Complete copy of all data\n"
            "   - Differential: Changes since last FULL backup\n"
            "   - Incremental: Changes since last ANY backup\n"
            "   - Incremental chain: Full + all incrementals needed for restore\n"
            "2. Broken chain causes:\n"
            "   - Full backup was deleted or corrupted\n"
            "   - An incremental in the chain is missing\n"
            "   - Backup media was removed or lost\n"
            "   - Retention policy deleted a link in the chain\n"
            "3. Recovery:\n"
            "   - Run a new full backup immediately\n"
            "   - This starts a fresh chain\n"
            "   - Keep old broken chain until new chain has valid restore points\n"
            "4. Prevention:\n"
            "   - Schedule periodic full backups (weekly minimum)\n"
            "   - Synthetic full: Backup software merges incrementals into new full\n"
            "   - Protect full backups from premature deletion\n"
            "5. Retention policy: Set retention to keep at least one full backup plus all its dependents together, never delete a full that has active incrementals"
        ),
    },
    {
        "category": "Backup & Recovery",
        "problem_title": "Email or mailbox backup and granular restore issues",
        "problem_description": "Can't backup or restore individual emails, mailboxes, or calendar items. Exchange or M365 mailbox backup failing, or granular mailbox restore showing errors.",
        "problem_keywords": "mailbox backup, email restore, exchange backup, granular restore, mailbox recovery, m365 backup, email backup, pst restore",
        "solution_steps": (
            "1. Exchange on-premises backup:\n"
            "   - Windows Server Backup: Full Exchange-aware backup\n"
            "   - Third-party: Veeam, Commvault, Veritas for granular restore\n"
            "   - Exchange Recovery Database for individual mailbox restore\n"
            "2. M365/Exchange Online backup:\n"
            "   - Microsoft native: Retention policies and Litigation Hold\n"
            "   - Third-party backup recommended: Veeam for M365, Afi, Spanning\n"
            "   - eDiscovery: Search and export mailbox content\n"
            "3. Granular restore steps:\n"
            "   - Mount backup to recovery database\n"
            "   - New-MailboxRestoreRequest to merge items to target mailbox\n"
            "   - Or: Export to PST > import specific items\n"
            "4. PST backup/restore:\n"
            "   - Export: Outlook > File > Open & Export > Import/Export\n"
            "   - Import: Same path, select 'Import from another file'\n"
            "   - PowerShell: New-MailboxExportRequest for bulk operations\n"
            "5. Retention vs backup: Configure M365 retention policies (Security & Compliance > Data lifecycle management) as first line of defense, supplement with third-party backup"
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
