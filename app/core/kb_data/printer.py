"""Printer troubleshooting articles and diagnostic tree."""

ARTICLES = [
    {
        "category": "Printer",
        "problem_title": "Printer shows Offline status",
        "problem_description": "The printer appears as 'Offline' in Windows despite being powered on and connected. Print jobs queue up but never print.",
        "problem_keywords": "printer offline, printer not printing, printer status offline, printer greyed out",
        "solution_steps": (
            "1. Check the physical connection (USB cable or network cable) and ensure the printer is powered on\n"
            "2. Open Settings > Devices > Printers & Scanners\n"
            "3. Click on the printer > Open print queue\n"
            "4. Click Printer menu > uncheck 'Use Printer Offline'\n"
            "5. If still offline, restart the Print Spooler service:\n"
            "   - Press Win+R, type services.msc, press Enter\n"
            "   - Find 'Print Spooler', right-click > Restart\n"
            "6. If on network, verify the printer's IP address hasn't changed:\n"
            "   - Print a network config page from the printer\n"
            "   - Update the printer port in Printer Properties > Ports\n"
            "7. Remove and re-add the printer if the above steps don't work"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Print Spooler service keeps stopping",
        "problem_description": "The Windows Print Spooler service crashes or stops automatically. Users cannot print and get error 'The print spooler service is not running'.",
        "problem_keywords": "print spooler, spooler crash, spooler stopped, cannot print, print service",
        "solution_steps": (
            "1. Clear the print queue folder:\n"
            "   - Stop Print Spooler: Run as Admin cmd > net stop spooler\n"
            "   - Delete all files in C:\\Windows\\System32\\spool\\PRINTERS\\\n"
            "   - Start Print Spooler: net start spooler\n"
            "2. If it keeps crashing, check for corrupt drivers:\n"
            "   - Open Print Management (printmanagement.msc)\n"
            "   - Go to All Drivers, remove any suspicious third-party drivers\n"
            "3. Run SFC scan: sfc /scannow (in elevated CMD)\n"
            "4. Check Event Viewer > Windows Logs > System for spooler crash details\n"
            "5. If a specific printer driver causes crashes, reinstall that printer with a fresh driver from manufacturer website\n"
            "6. As last resort, reset Print Spooler to defaults:\n"
            "   - Delete registry key: HKLM\\SYSTEM\\CurrentControlSet\\Control\\Print\\Printers (backup first)\n"
            "   - Restart Print Spooler service"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Printer printing blank pages",
        "problem_description": "The printer feeds paper through but pages come out completely blank or with very faint text.",
        "problem_keywords": "blank pages, empty print, no text, faint print, printer blank",
        "solution_steps": (
            "1. Check ink/toner levels - replace if low\n"
            "2. For inkjet printers:\n"
            "   - Run the printer's built-in head cleaning utility (usually in printer properties or printer's own menu)\n"
            "   - Run it 2-3 times if needed, then print a test page\n"
            "   - Check if nozzles are clogged - print nozzle check pattern\n"
            "3. For laser printers:\n"
            "   - Remove toner cartridge, gently shake side to side to redistribute toner\n"
            "   - Check if the sealing tape was removed from a new cartridge\n"
            "   - Check the drum unit for damage\n"
            "4. Verify the correct paper size and type are selected in print settings\n"
            "5. Try printing from a different application to rule out software issues\n"
            "6. Update or reinstall the printer driver from the manufacturer's website"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Cannot add network printer - Windows cannot connect",
        "problem_description": "When trying to add a shared network printer, Windows shows 'Windows cannot connect to the printer' with error 0x0000011b or similar.",
        "problem_keywords": "add printer, network printer, 0x0000011b, cannot connect printer, shared printer, printer error",
        "solution_steps": (
            "1. For error 0x0000011b (common after Windows update):\n"
            "   - On the PRINT SERVER: Open Registry Editor\n"
            "   - Navigate to HKLM\\SYSTEM\\CurrentControlSet\\Control\\Print\n"
            "   - Create DWORD value: RpcAuthnLevelPrivacyEnabled = 0\n"
            "   - Restart Print Spooler service\n"
            "2. Alternative fix: Install the printer driver locally first, then add the network printer\n"
            "3. Verify network connectivity to the print server: ping <server-name>\n"
            "4. Ensure File and Printer Sharing is enabled on both machines:\n"
            "   - Control Panel > Network and Sharing Center > Advanced sharing settings\n"
            "5. Check that the printer is shared and permissions allow Everyone or appropriate users\n"
            "6. If using IP: Add printer by TCP/IP address instead of browsing the network\n"
            "   - Use printer's IP address (print a config page from the printer to find it)"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Paper jam error but no paper stuck",
        "problem_description": "Printer displays 'Paper Jam' error but there is no visible paper stuck inside the printer.",
        "problem_keywords": "paper jam, ghost jam, false paper jam, paper feed error",
        "solution_steps": (
            "1. Turn off the printer and unplug it for 30 seconds\n"
            "2. Open all accessible doors and trays, look carefully for small paper scraps\n"
            "3. Check the following common jam locations:\n"
            "   - Paper input tray (remove tray completely)\n"
            "   - Under the toner/ink cartridge area\n"
            "   - Rear access panel / duplexer\n"
            "   - Output tray area and rollers\n"
            "4. Clean the paper feed rollers with a slightly damp lint-free cloth\n"
            "5. Check for worn paper feed rollers (smooth/shiny = need replacement)\n"
            "6. Make sure paper guides in the tray are snug but not too tight against the paper\n"
            "7. Try different paper - old/damp/curled paper causes false jams\n"
            "8. Plug in and turn on - if error persists, do a full power cycle (unplug for 60 seconds)\n"
            "9. Update firmware from manufacturer website"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Printer prints very slowly",
        "problem_description": "Print jobs take much longer than expected to complete. Printer pauses between pages or takes minutes to start printing.",
        "problem_keywords": "slow printing, printer slow, slow print, print speed, printing takes long",
        "solution_steps": (
            "1. Check print quality setting - change from 'Best' or 'High Quality' to 'Normal' or 'Draft'\n"
            "2. For network printers, check network connection quality:\n"
            "   - Use Ethernet instead of Wi-Fi if possible\n"
            "   - Check for IP conflicts\n"
            "3. Clear the print spooler queue:\n"
            "   - net stop spooler\n"
            "   - Delete files in C:\\Windows\\System32\\spool\\PRINTERS\\\n"
            "   - net start spooler\n"
            "4. Update the printer driver from manufacturer's website\n"
            "5. Check if bidirectional communication is causing delays:\n"
            "   - Printer Properties > Ports > Uncheck 'Enable bidirectional support'\n"
            "6. For large documents, check if 'Print directly to printer' helps:\n"
            "   - Printer Properties > Advanced > 'Print directly to the printer'\n"
            "7. Ensure the printer firmware is up to date\n"
            "8. Check printer's memory - complex documents may exceed printer memory"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Error 0x00000709 - Cannot set default printer",
        "problem_description": "Windows shows error 0x00000709 when trying to set a default printer, or the default printer keeps changing.",
        "problem_keywords": "0x00000709, default printer, cannot set default, printer changing",
        "solution_steps": (
            "1. Disable Windows managing default printer:\n"
            "   - Settings > Devices > Printers & Scanners\n"
            "   - Turn off 'Let Windows manage my default printer'\n"
            "2. Set default manually:\n"
            "   - Right-click the desired printer > Set as default\n"
            "3. If error persists, fix via registry:\n"
            "   - Open regedit as Administrator\n"
            "   - Go to HKCU\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Windows\n"
            "   - Change 'Device' value to your printer name (format: PrinterName,winspool,PortName)\n"
            "   - You may need to take ownership of this key first\n"
            "4. Remove all other printers temporarily, set default, then re-add them\n"
            "5. Run printer troubleshooter: Settings > Update & Security > Troubleshoot > Printer"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Printer driver installation fails or is unavailable",
        "problem_description": "Cannot install printer driver - installer fails, driver not compatible, or Windows cannot find the driver for the printer.",
        "problem_keywords": "driver install, printer driver, driver not found, driver incompatible, install fails",
        "solution_steps": (
            "1. Download the correct driver from the manufacturer's website:\n"
            "   - HP: support.hp.com\n"
            "   - Canon: usa.canon.com/support\n"
            "   - Epson: epson.com/Support\n"
            "   - Brother: support.brother.com\n"
            "   - Lexmark: support.lexmark.com\n"
            "2. Make sure you select the right OS version (Windows 10/11, 32-bit or 64-bit)\n"
            "3. If the manufacturer doesn't have a driver for your OS:\n"
            "   - Try the Windows built-in driver: Add Printer > Windows Update > select your model\n"
            "   - Try a 'Universal Print Driver' from the manufacturer (HP UPD, Ricoh UPD, etc.)\n"
            "4. If installer fails:\n"
            "   - Run as Administrator\n"
            "   - Temporarily disable antivirus\n"
            "   - Use Device Manager > Add legacy hardware > Install from disk\n"
            "5. For old printers with no modern driver:\n"
            "   - Try running the old installer in Compatibility Mode (right-click > Properties > Compatibility)\n"
            "   - Some old PostScript printers work with a generic PS driver"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Printer prints garbled text or symbols",
        "problem_description": "Printouts contain random characters, symbols, strange fonts, or jumbled text instead of the correct content.",
        "problem_keywords": "garbled text, random characters, symbols, wrong font, garbled print, corrupt print",
        "solution_steps": (
            "1. Cancel all current print jobs and clear the spooler:\n"
            "   - CMD (Admin): net stop spooler\n"
            "   - Delete files in C:\\Windows\\System32\\spool\\PRINTERS\\\n"
            "   - net start spooler\n"
            "2. Try printing from a different application - if garbled from one app only, it's a software issue\n"
            "3. Check if the correct driver is installed:\n"
            "   - Printer Properties > Advanced > Driver dropdown\n"
            "   - Should match your exact printer model\n"
            "4. Reinstall the printer driver:\n"
            "   - Remove the printer completely\n"
            "   - Download fresh driver from manufacturer\n"
            "   - Install and re-add the printer\n"
            "5. For PostScript printers, switch between PCL and PS driver (or vice versa)\n"
            "6. Check the data cable - a faulty USB cable can corrupt data\n"
            "7. Try printing a test page from Printer Properties - if that's garbled too, it's a driver or hardware issue\n"
            "8. Update printer firmware"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Printer duplex (double-sided) not working",
        "problem_description": "Double-sided printing option is greyed out, not available, or the printer only prints on one side even when duplex is selected.",
        "problem_keywords": "duplex, double-sided, two-sided, both sides, duplex not working, duplex greyed out",
        "solution_steps": (
            "1. Verify the printer supports automatic duplexing:\n"
            "   - Check printer specifications on manufacturer website\n"
            "   - Some printers only support manual duplex\n"
            "2. Enable duplex in the driver:\n"
            "   - Printer Properties > Device Settings > Installable Options > Duplex Unit: Installed\n"
            "3. Check print dialog:\n"
            "   - Print > Properties/Preferences > look for 'Print on Both Sides' or 'Duplex'\n"
            "   - Some applications hide this under 'Layout' or 'Finishing' tab\n"
            "4. If duplex unit is installed but not detected:\n"
            "   - Reinstall or update the printer driver\n"
            "   - Remove and re-add the printer\n"
            "5. For manual duplex: Print odd pages first, flip the stack, then print even pages\n"
            "6. Check paper type - some heavy/glossy paper cannot be duplexed\n"
            "7. Check printer's own menu for a duplex setting that may need enabling"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Printer shows wrong ink or toner levels",
        "problem_description": "Printer or software reports incorrect ink/toner levels - shows empty when cartridge is full, or shows full when ink is low.",
        "problem_keywords": "ink level, toner level, cartridge, wrong level, ink full, ink empty, cartridge error",
        "solution_steps": (
            "1. For non-OEM (third-party) cartridges:\n"
            "   - Many printers cannot accurately read third-party cartridge levels\n"
            "   - This is normal - the printer may show 'Unknown' or 'Empty'\n"
            "   - You can usually dismiss the warning and keep printing\n"
            "2. Reset the ink/toner counter:\n"
            "   - Some printers have a reset button or menu option\n"
            "   - Hold the cancel/stop button for 5 seconds on some models\n"
            "3. Clean the cartridge contacts:\n"
            "   - Remove cartridge, gently wipe the gold/copper contacts with a dry lint-free cloth\n"
            "   - Also wipe the contacts inside the printer where the cartridge sits\n"
            "4. Remove and reseat the cartridge firmly\n"
            "5. If using OEM cartridge and level is wrong:\n"
            "   - Try a different cartridge to test\n"
            "   - Update printer firmware\n"
            "   - The cartridge chip may be defective - contact manufacturer\n"
            "6. Some printer monitoring software (HP Smart, Epson Status Monitor) may show different levels than the printer display - trust the printer display"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Printer only prints part of the page or cuts off content",
        "problem_description": "Printout is missing content on one or more sides - text/images are cut off at the edges, or only half the page prints.",
        "problem_keywords": "cut off, partial print, missing content, margin, page size, scaling, truncated print",
        "solution_steps": (
            "1. Check paper size settings:\n"
            "   - Application print dialog > Page Setup > verify paper size matches loaded paper (A4 vs Letter)\n"
            "   - Printer Properties > Paper/Quality > verify correct size\n"
            "2. Check margins:\n"
            "   - Set margins to at least 6mm/0.25in on all sides\n"
            "   - Printers have a minimum non-printable area at edges\n"
            "3. Check scaling:\n"
            "   - Look for 'Fit to page' or 'Shrink to fit' option in print dialog\n"
            "   - Ensure scaling is at 100% or use 'Fit to printable area'\n"
            "4. For PDF files: Use Adobe Reader > Print > 'Fit' or 'Shrink oversize pages'\n"
            "5. Check the printer driver paper size matches the application:\n"
            "   - Printer Properties > Advanced > Printing Defaults > Paper size\n"
            "6. If bottom is cut off: The document may have content outside the printable area\n"
            "7. Try 'Print as Image' for PDF documents that have rendering issues"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Wireless printer not found on network",
        "problem_description": "Cannot discover or add a wireless printer. It doesn't show up in the printer search or network discovery.",
        "problem_keywords": "wireless printer, wifi printer, printer not found, discover printer, add wireless printer",
        "solution_steps": (
            "1. Verify the printer is connected to Wi-Fi:\n"
            "   - Check the printer's display for Wi-Fi icon or SSID\n"
            "   - Print a network config page from the printer's menu\n"
            "2. Ensure the computer and printer are on the SAME network:\n"
            "   - Both must be on the same SSID (not one on 2.4GHz and other on 5GHz if they're separate)\n"
            "   - Check IP: Both should be in the same subnet (e.g., 192.168.1.x)\n"
            "3. Restart the printer's Wi-Fi:\n"
            "   - Printer menu > Network/Wi-Fi > Disable Wi-Fi > Re-enable > Reconnect\n"
            "4. Add by IP address instead of discovery:\n"
            "   - Get printer's IP from its config page or display\n"
            "   - Windows: Add a printer > 'The printer I want isn't listed' > TCP/IP > enter IP\n"
            "5. Enable network discovery on your PC:\n"
            "   - Control Panel > Network and Sharing Center > Advanced sharing settings\n"
            "   - Turn on Network discovery\n"
            "6. Check firewall isn't blocking printer discovery (WSD/SNMP/Bonjour protocols)\n"
            "7. Try manufacturer's setup app (HP Smart, Epson Connect, Canon PRINT, etc.)"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Color printing not working - only prints in black and white",
        "problem_description": "Printer only produces black and white output even when color is selected. Color cartridges are installed.",
        "problem_keywords": "no color, black and white only, grayscale, color not printing, printer no color",
        "solution_steps": (
            "1. Check print settings:\n"
            "   - Print dialog > Properties > Color tab\n"
            "   - Change from 'Grayscale' or 'Monochrome' to 'Color'\n"
            "2. Check the printer driver defaults:\n"
            "   - Devices > Printers > right-click printer > Printing Preferences\n"
            "   - Look for Color/Grayscale setting - change to Color and Apply\n"
            "3. Verify color cartridges are installed and not empty:\n"
            "   - Check all color ink/toner levels\n"
            "   - Some printers default to B&W when any color cartridge is low\n"
            "4. For Group Policy restrictions (corporate environment):\n"
            "   - IT admin may have enforced B&W printing to save costs\n"
            "   - Check with IT admin\n"
            "5. Try printing a color test page:\n"
            "   - Printer Properties > Print Test Page (should be in color)\n"
            "   - If test page is B&W, check driver/printer settings\n"
            "6. Run the printer's own color calibration (from printer menu)\n"
            "7. Reinstall the printer driver if settings look correct but color still doesn't work"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Printer picking up multiple pages at once",
        "problem_description": "Printer feeds two or more pages at the same time, causing missed pages or jams.",
        "problem_keywords": "multiple pages, double feed, two pages, paper feed, sheets stuck together, feed roller",
        "solution_steps": (
            "1. Fan the paper stack before loading:\n"
            "   - Take out the paper, fan it to separate the sheets, then reload\n"
            "2. Don't overfill the paper tray - stay below the max fill line\n"
            "3. Check for static:\n"
            "   - Paper in dry environments sticks together\n"
            "   - Fan the paper or use anti-static paper\n"
            "4. Check paper quality:\n"
            "   - Use fresh, dry paper (not damp or wrinkled)\n"
            "   - Use the correct weight for your printer (usually 80gsm / 20lb)\n"
            "5. Clean the paper feed/pickup rollers:\n"
            "   - Use a slightly damp lint-free cloth\n"
            "   - If rollers are shiny/smooth, they may need replacement\n"
            "6. Check the separation pad:\n"
            "   - Located opposite the pickup roller\n"
            "   - If worn, pages won't separate properly - replace it\n"
            "7. Adjust paper guides to fit snugly (not too tight, not too loose)"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Printer error 50.x - Fuser error (HP/LaserJet)",
        "problem_description": "HP LaserJet printer shows Error 50.x (50.1, 50.2, 50.3, etc.) which is a fuser-related error. Printer stops working.",
        "problem_keywords": "error 50, fuser error, HP error, 50.1, 50.2, laserjet error, fuser",
        "solution_steps": (
            "1. Power cycle the printer:\n"
            "   - Turn off, unplug from power, wait 5 minutes\n"
            "   - Plug back in, turn on\n"
            "   - Waiting allows the fuser to cool completely\n"
            "2. Check the fuser unit:\n"
            "   - Open the rear or top access door\n"
            "   - Remove and reseat the fuser assembly\n"
            "   - Check for any visible damage or debris\n"
            "3. Error code meanings:\n"
            "   - 50.1: Low fuser temperature (fuser not heating up)\n"
            "   - 50.2: Fuser warmup service (slow to heat)\n"
            "   - 50.3: High fuser temperature (overheating)\n"
            "   - 50.4: Faulty fuser (drive circuit)\n"
            "4. Check the power source:\n"
            "   - Plug printer directly into wall outlet (not a power strip or UPS)\n"
            "   - Ensure the outlet provides consistent voltage\n"
            "5. If error persists after reseat and power cycle:\n"
            "   - The fuser unit likely needs replacement\n"
            "   - Order the correct fuser kit for your specific model\n"
            "6. Fuser replacement is usually a user-installable part - check your maintenance kit"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Streaks, lines, or marks on every printed page",
        "problem_description": "Every page has visible vertical or horizontal lines, streaks, smudges, or repeating marks/spots at regular intervals.",
        "problem_keywords": "streaks, lines, marks, spots, smudges, print quality, repeating marks, dirty print",
        "solution_steps": (
            "1. Identify the pattern:\n"
            "   - Repeating marks at regular intervals = drum or roller issue\n"
            "   - Single vertical line = scratch on drum or debris on scanner glass\n"
            "   - Horizontal bands = print head issue (inkjet) or transfer belt (laser)\n"
            "2. For laser printers:\n"
            "   - Remove toner cartridge and inspect the drum for scratches or marks\n"
            "   - Clean the drum gently with a dry lint-free cloth (never touch with fingers)\n"
            "   - If drum has visible damage, replace the drum unit\n"
            "   - Clean inside the printer with compressed air (avoid blowing toner everywhere)\n"
            "3. For inkjet printers:\n"
            "   - Run head cleaning from the printer's maintenance menu (2-3 times)\n"
            "   - Print alignment page\n"
            "   - If streaks persist, the print head may need replacement\n"
            "4. For copier/scanner lines: Clean the scanner glass and the white strip underneath the lid\n"
            "5. Check if the fuser film has marks (laser printers) - may need cleaning or replacement\n"
            "6. Replace toner or ink cartridge as a test (new cartridge = new drum on some models)"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Printer says it needs a new cartridge but cartridge is full",
        "problem_description": "Printer displays 'Replace cartridge' or 'Cartridge empty' error even though the cartridge was just installed or is clearly full.",
        "problem_keywords": "cartridge error, replace cartridge, cartridge not recognized, cartridge empty, new cartridge error",
        "solution_steps": (
            "1. Remove and reseat the cartridge:\n"
            "   - Take out the cartridge, wait 10 seconds, reinsert firmly until it clicks\n"
            "2. Clean the cartridge chip/contacts:\n"
            "   - Wipe the gold/copper contacts on the cartridge with a dry lint-free cloth\n"
            "   - Clean the matching contacts inside the printer\n"
            "3. For third-party/refilled cartridges:\n"
            "   - Some printers reject non-OEM cartridges\n"
            "   - Look for a firmware downgrade or 'Use cartridge anyway' option\n"
            "   - Some recent printer firmware updates block third-party cartridges\n"
            "4. Reset the cartridge counter:\n"
            "   - On some Brother printers: Hold the Cancel button for 5 seconds\n"
            "   - On some HP printers: Look for a 'cartridge protection' setting to disable\n"
            "5. Check if the cartridge is compatible with your specific printer model\n"
            "   - Same brand doesn't mean compatible - model number must match exactly\n"
            "6. If using OEM cartridge: Try a different cartridge from the same box (occasionally defective chips)\n"
            "7. Update or downgrade printer firmware as needed"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "PrintNightmare vulnerability and print issues after patching",
        "problem_description": "After installing Windows security updates for PrintNightmare (CVE-2021-34527), printing stops working, especially to shared network printers.",
        "problem_keywords": "PrintNightmare, CVE-2021-34527, print after update, printer patch, printer security update",
        "solution_steps": (
            "1. This is caused by security patches restricting how Windows handles printer drivers\n"
            "2. Fix for shared printers:\n"
            "   - On the PRINT SERVER, add this registry value:\n"
            "   - HKLM\\SYSTEM\\CurrentControlSet\\Control\\Print\n"
            "   - RpcAuthnLevelPrivacyEnabled (DWORD) = 0\n"
            "   - Restart Print Spooler service\n"
            "3. Pre-install the printer driver on the client PC:\n"
            "   - Download the correct driver from the manufacturer\n"
            "   - Install it locally\n"
            "   - Then add the network printer\n"
            "4. For Point and Print restrictions:\n"
            "   - Group Policy: Computer Config > Admin Templates > Printers\n"
            "   - 'Point and Print Restrictions' > Enable and configure\n"
            "   - Note: This can reduce security - discuss with your security team\n"
            "5. Keep systems patched - the security fixes are essential\n"
            "6. Consider using direct TCP/IP printing instead of shared printers\n"
            "7. Microsoft recommends keeping the patches and using the driver pre-install method"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Printer printing wrong colors - color mismatch",
        "problem_description": "Colors in the printout don't match what's shown on screen. Photos look wrong, reds look orange, blues look purple, etc.",
        "problem_keywords": "wrong colors, color mismatch, inaccurate color, color calibration, print colors different",
        "solution_steps": (
            "1. Understand that monitors (RGB) and printers (CMYK) display color differently - some mismatch is normal\n"
            "2. Run the printer's color calibration:\n"
            "   - Printer menu > Maintenance/Tools > Color Calibration\n"
            "   - Or from the printer driver: Maintenance tab > Calibrate\n"
            "3. Use the correct color profile:\n"
            "   - Printer Properties > Color Management > Add the manufacturer's ICC profile\n"
            "   - Download the correct ICC profile from the manufacturer website\n"
            "4. In the print dialog:\n"
            "   - Let the printer manage colors (not the application), or\n"
            "   - Let the application manage colors and disable color management in printer driver\n"
            "   - Don't use both at the same time (double-corrects colors)\n"
            "5. Print a test page with known colors to compare\n"
            "6. For photos: Use the paper type setting that matches your actual paper\n"
            "7. Check if any color cartridge is low - low ink/toner distorts colors\n"
            "8. Calibrate your monitor as well for best screen-to-print matching"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Printer error 49 - firmware error (HP)",
        "problem_description": "HP LaserJet displays '49 Error' on the control panel and won't print. The printer may reboot in a loop.",
        "problem_keywords": "49 error, hp firmware, hp error 49, laserjet error, firmware crash, printer loop",
        "solution_steps": (
            "1. Power cycle the printer:\n"
            "   - Turn off, unplug power cable for 30 seconds, plug back in\n"
            "   - Wait for full initialization\n"
            "2. If error returns when printing:\n"
            "   - A specific print job is causing the firmware crash\n"
            "   - Clear the print queue on the computer\n"
            "   - Cancel all jobs in print queue before turning printer back on\n"
            "3. Try printing a different document to confirm\n"
            "4. Check for firmware updates:\n"
            "   - Go to HP support website > enter printer model\n"
            "   - Download latest firmware and install via USB or network\n"
            "5. Check if PostScript or PCL driver issue:\n"
            "   - Switch from PS to PCL driver (or vice versa)\n"
            "   - Reinstall the print driver\n"
            "6. Disable advanced printing features in driver:\n"
            "   - Printer Properties > Advanced > uncheck 'Enable advanced printing features'\n"
            "7. If error 49.4C02 specifically: Usually a network communication error\n"
            "   - Disconnect network cable, power cycle, reconnect\n"
            "8. Reset printer to factory defaults via the control panel menu"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Printer tray not detected or wrong tray selected",
        "problem_description": "Printer reports 'Tray 2 not detected' or jobs keep printing from the wrong paper tray despite correct settings.",
        "problem_keywords": "tray not detected, wrong tray, paper tray, tray error, tray 2, paper source, tray missing",
        "solution_steps": (
            "1. Physical check:\n"
            "   - Remove and reseat the paper tray completely\n"
            "   - Check for any paper or debris blocking tray detection sensors\n"
            "   - Ensure the tray is pushed all the way in until it clicks\n"
            "2. Check tray settings on printer control panel:\n"
            "   - Go to Paper/Tray settings > Configure Tray\n"
            "   - Set the correct paper size and type for each tray\n"
            "3. To fix wrong tray being selected:\n"
            "   - Printer Properties (on PC) > Device Settings > Tray assignment\n"
            "   - Map paper sizes to specific trays\n"
            "   - Check 'Paper Source' in print dialog matches the desired tray\n"
            "4. In the print driver:\n"
            "   - Preferences > Paper/Quality > Paper Source\n"
            "   - Change from 'Automatically Select' to the specific tray\n"
            "5. For 'Tray not detected' errors:\n"
            "   - Power cycle the printer with tray removed, then reinsert\n"
            "   - Check tray pickup rollers are not worn\n"
            "   - Check tray solenoid (hardware may need service)\n"
            "6. Update or reinstall the driver with correct tray configuration"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Printer not waking from sleep mode",
        "problem_description": "Printer goes into sleep or power-save mode and won't respond to print jobs. Users have to manually press buttons to wake it.",
        "problem_keywords": "printer sleep, power save, won't wake, printer unresponsive, sleep mode, energy save, standby",
        "solution_steps": (
            "1. Adjust sleep mode settings:\n"
            "   - Printer control panel > Settings > Energy/Power Management\n"
            "   - Increase the sleep timer or set to 'Never' for busy offices\n"
            "   - Some printers: Settings > General > Eco Mode > Off\n"
            "2. Check Wake-on-LAN settings:\n"
            "   - Network settings on printer > Enable 'Wake on Network Activity'\n"
            "   - This allows incoming print jobs to wake the printer\n"
            "3. Firmware update:\n"
            "   - Sleep/wake bugs are common in printer firmware\n"
            "   - Update to the latest firmware from manufacturer website\n"
            "4. Driver settings:\n"
            "   - Open Printing Preferences > check for SNMP or bidirectional communication\n"
            "   - Enable SNMP so the driver can communicate status to wake the printer\n"
            "5. Network switch port:\n"
            "   - Some managed switches put ports to sleep\n"
            "   - Check 'Energy Efficient Ethernet' (EEE) on the switch port\n"
            "   - Disable EEE on the printer's switch port if needed\n"
            "6. USB printers: Check USB selective suspend in Windows\n"
            "   - Device Manager > USB > Power Management > uncheck 'Allow computer to turn off this device'"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Printer shows PCL XL error on every print",
        "problem_description": "When printing, a page comes out with 'PCL XL Error' text instead of the actual document. May say 'Subsystem: KERNEL' or 'IllegalOperatorSequence'.",
        "problem_keywords": "pcl xl error, pcl error, illegal operator, subsystem kernel, pcl xl, printer pcl, driver error",
        "solution_steps": (
            "1. Switch to a different driver type:\n"
            "   - If using PCL 6 driver: Switch to PCL 5 or PS (PostScript)\n"
            "   - Install the alternate driver from manufacturer's website\n"
            "   - Set it as the default printer\n"
            "2. Disable advanced printing features:\n"
            "   - Printer Properties > Advanced > uncheck 'Enable advanced printing features'\n"
            "   - This forces basic print rendering\n"
            "3. Print as Image:\n"
            "   - In the Print dialog > Advanced > check 'Print as Image'\n"
            "   - This converts the document to a bitmap (slower but works)\n"
            "4. Font-related PCL XL errors:\n"
            "   - Printer Properties > Advanced > Print Processor > change to RAW\n"
            "   - Or: Preferences > check 'Send TrueType as Bitmap'\n"
            "5. Update the printer driver:\n"
            "   - Uninstall old driver completely\n"
            "   - Download latest driver from manufacturer\n"
            "   - Install fresh\n"
            "6. If error only happens with specific documents:\n"
            "   - The document may have complex graphics or fonts\n"
            "   - Try saving as PDF first then printing the PDF\n"
            "7. Update printer firmware"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Scan to email or scan to folder not working",
        "problem_description": "Multifunction printer's scan-to-email or scan-to-network-folder feature has stopped working. Scans fail with authentication or connection errors.",
        "problem_keywords": "scan to email, scan to folder, scan error, mfp scan, scan smb, scanner email, scan network",
        "solution_steps": (
            "1. Scan to Email issues:\n"
            "   - Check SMTP server settings on the printer's web interface\n"
            "   - Common: smtp.office365.com, port 587, TLS enabled\n"
            "   - Verify the 'From' email address and credentials\n"
            "   - If using M365: May need an app password or SMTP relay connector\n"
            "   - Gmail: Enable 'Less secure apps' or use App Password\n"
            "2. Scan to Folder (SMB) issues:\n"
            "   - Verify the network path: \\\\servername\\sharename\\folder\n"
            "   - Check the username format: DOMAIN\\username or username@domain.com\n"
            "   - Test credentials by mapping the share from a PC first\n"
            "   - Check SMB version: Newer printers may not support SMB1\n"
            "   - On the server: Enable SMB2/3 and ensure the printer supports it\n"
            "3. After Windows updates:\n"
            "   - Microsoft may have disabled SMBv1 or changed guest access\n"
            "   - Registry: HKLM\\SYSTEM\\CurrentControlSet\\Services\\LanmanWorkstation\\Parameters\n"
            "   - AllowInsecureGuestAuth may need to be set to 1 (for older printers)\n"
            "4. Firewall:\n"
            "   - Ensure ports 445 (SMB) and 587/25 (SMTP) are not blocked\n"
            "5. Check DNS: Printer must resolve the server hostname\n"
            "   - Try using IP address instead of hostname in the scan config\n"
            "6. Test with a simple scan to USB first to rule out scanner hardware issues"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Printer queue shows jobs but nothing prints",
        "problem_description": "Print jobs appear in the Windows print queue and show 'Printing' status but nothing comes out of the printer physically.",
        "problem_keywords": "queue printing nothing, print job stuck, printing but nothing, phantom print, queue not clearing, print job no output",
        "solution_steps": (
            "1. Check the physical printer:\n"
            "   - Is it powered on and ready? (No error lights)\n"
            "   - Is there paper in the tray?\n"
            "   - Is the correct tray selected for the paper size?\n"
            "2. Check the connection:\n"
            "   - USB: Cable plugged in securely on both ends?\n"
            "   - Network: Can you ping the printer's IP?\n"
            "   - Wireless: Is the printer connected to the right network?\n"
            "3. Print a test page from the printer itself:\n"
            "   - Internal menu > Print Configuration/Test Page\n"
            "   - If this works: Problem is between PC and printer\n"
            "4. Clear and restart the print queue:\n"
            "   - net stop spooler\n"
            "   - Delete all files in C:\\Windows\\System32\\spool\\PRINTERS\\\n"
            "   - net start spooler\n"
            "5. Check the port configuration:\n"
            "   - Printer Properties > Ports > ensure correct IP/port is checked\n"
            "   - For network printers: The IP may have changed (DHCP)\n"
            "   - Set a static IP or DHCP reservation for the printer\n"
            "6. Try printing from a different application or a simple text file\n"
            "7. Remove and re-add the printer with the correct driver\n"
            "8. Check if 'Use Printer Offline' is accidentally enabled:\n"
            "   - Printer > See what's printing > Printer menu > uncheck 'Use Printer Offline'"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Printer producing faded or light prints",
        "problem_description": "Printed pages come out very light, faded, or washed out. Text is barely readable even though toner/ink levels appear adequate.",
        "problem_keywords": "faded print, light print, washed out, faint print, toner light, pale print, low density",
        "solution_steps": (
            "1. Check toner/ink levels:\n"
            "   - Even if the printer reports 'OK', the cartridge may be near-empty\n"
            "   - Remove and gently shake the toner cartridge side-to-side (laser printers)\n"
            "   - Replace if old\n"
            "2. Print density/darkness setting:\n"
            "   - Printer Preferences > Quality > increase Print Density\n"
            "   - Or on the printer control panel: Settings > Print Quality > Toner Density\n"
            "   - Increase from the default setting\n"
            "3. Check print quality mode:\n"
            "   - If set to 'Draft' or 'EconoMode': Change to 'Normal' or 'Best'\n"
            "   - Preferences > Quality > Quality Settings > Normal\n"
            "   - Disable EconoMode / Toner Save mode\n"
            "4. For laser printers:\n"
            "   - Clean the transfer roller\n"
            "   - Check the drum unit: May be worn or damaged\n"
            "   - Print a cleaning page: Maintenance > Cleaning Page\n"
            "5. For inkjet printers:\n"
            "   - Run nozzle check and head cleaning\n"
            "   - Check if the correct paper type is selected\n"
            "   - Print head alignment: Maintenance > Align Print Head\n"
            "6. Check paper quality:\n"
            "   - Damp paper causes fading - store paper in dry location\n"
            "   - Ensure paper matches the printer's paper type setting"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Printer communication error or bidirectional issues",
        "problem_description": "Getting 'Communication error', 'Printer not responding', or 'Error communicating with printer'. Bidirectional communication failures.",
        "problem_keywords": "communication error, bidirectional, printer not responding, communication failed, wsd error, snmp error",
        "solution_steps": (
            "1. Disable bidirectional communication:\n"
            "   - Printer Properties > Ports > uncheck 'Enable bidirectional support'\n"
            "   - This prevents the PC from querying the printer status\n"
            "   - Eliminates many communication timeouts\n"
            "2. Check SNMP settings:\n"
            "   - Printer Properties > Ports > Configure Port\n"
            "   - Uncheck 'SNMP Status Enabled' if causing issues\n"
            "   - Or update the SNMP community string to match the printer\n"
            "3. For WSD (Web Services for Devices) printers:\n"
            "   - WSD ports use discovery protocol that can be unreliable\n"
            "   - Remove the WSD printer and re-add using TCP/IP port instead\n"
            "   - Add Printer > TCP/IP > enter printer's IP address\n"
            "4. Check firewall:\n"
            "   - SNMP uses UDP 161/162\n"
            "   - WSD uses TCP 5357/5358\n"
            "   - Ensure these are not blocked\n"
            "5. Network connectivity:\n"
            "   - Ping the printer IP to verify reachability\n"
            "   - Check for IP changes - use static IP for the printer\n"
            "6. USB communication errors:\n"
            "   - Try a different USB cable (shorter is better)\n"
            "   - Try a different USB port on the PC\n"
            "   - Avoid USB hubs - connect directly to the computer"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Envelope printing issues - jamming or misfeeding",
        "problem_description": "Printer jams or misfeeds when trying to print envelopes. Envelopes may curl, stick together, or print with wrong orientation.",
        "problem_keywords": "envelope printing, envelope jam, envelope feed, envelope curl, envelope orientation, #10 envelope",
        "solution_steps": (
            "1. Proper envelope loading:\n"
            "   - Most printers: Load envelopes flap-side up or flap on the left\n"
            "   - Check the printer manual for your specific model\n"
            "   - Use the manual feed tray or designated envelope slot\n"
            "   - Do NOT overfill - load 5-10 envelopes at most\n"
            "2. Driver settings:\n"
            "   - Set paper size to the correct envelope size (e.g., #10, DL, C5)\n"
            "   - Set paper type to 'Envelope' or 'Heavy paper'\n"
            "   - Set the correct orientation (Landscape for most envelopes)\n"
            "3. Prevent curling:\n"
            "   - Use 'Low heat' or 'Envelope' mode in fuser settings\n"
            "   - For laser printers: Reduce fuser temperature via driver\n"
            "   - Open the rear output tray for a straight paper path\n"
            "4. Avoid:\n"
            "   - Envelopes with windows (plastic can melt in laser printers)\n"
            "   - Padded or clasp envelopes\n"
            "   - Envelopes with self-seal adhesive (heat can activate the glue)\n"
            "5. If jamming:\n"
            "   - Remove any curled or wrinkled envelopes before loading\n"
            "   - Fan the stack to separate envelopes before loading\n"
            "   - Adjust tray guides snugly (not too tight)"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Printer IP address keeps changing",
        "problem_description": "Network printer's IP address changes periodically, causing it to go offline. Users have to reconfigure the printer each time.",
        "problem_keywords": "ip address change, printer ip, dhcp printer, static ip, printer offline ip, ip changed",
        "solution_steps": (
            "1. Set a static IP on the printer:\n"
            "   - Access printer's web interface (Embedded Web Server)\n"
            "   - Browse to http://<current-printer-IP>\n"
            "   - Network > IPv4 Configuration > change from DHCP to Manual/Static\n"
            "   - Set an IP outside the DHCP range\n"
            "   - Set subnet mask, gateway, and DNS server\n"
            "2. Or use a DHCP reservation (preferred):\n"
            "   - Find the printer's MAC address: Network config page or printer menu\n"
            "   - On DHCP server: Create a reservation for that MAC address\n"
            "   - Printer keeps using DHCP but always gets the same IP\n"
            "3. Update the printer port on all PCs:\n"
            "   - Printer Properties > Ports > Configure Port\n"
            "   - Update the IP address to the new static/reserved IP\n"
            "   - Or use the printer's hostname instead of IP (more resilient)\n"
            "4. For GPO-deployed printers:\n"
            "   - Update the shared printer on the print server\n"
            "   - The port change will propagate to clients\n"
            "5. Prevent future issues:\n"
            "   - Always use either static IP or DHCP reservation for printers\n"
            "   - Document all printer IPs in an asset management system\n"
            "6. If using DNS: Create an A record for the printer hostname"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Print jobs deleted automatically before printing",
        "problem_description": "Print jobs are disappearing from the queue before they can be printed. Jobs appear briefly then vanish without any error message.",
        "problem_keywords": "jobs disappearing, auto delete, print job removed, queue cleared, jobs vanish, print deleted",
        "solution_steps": (
            "1. Check the print spooler event log:\n"
            "   - Event Viewer > Applications and Services > Microsoft > Windows > PrintService > Operational\n"
            "   - Look for events showing job deletion and the reason\n"
            "2. Common causes:\n"
            "   - Driver mismatch: Driver on PC doesn't match printer capabilities\n"
            "   - Corrupt driver: Uninstall and reinstall the print driver\n"
            "   - Paper size mismatch: Job requests a size the printer doesn't have\n"
            "3. Check print server settings (if using print server):\n"
            "   - Print Management > Printer > Properties > Advanced\n"
            "   - Check 'Keep printed documents' to see if jobs complete\n"
            "   - Check for any filters or redirections\n"
            "4. Antivirus interference:\n"
            "   - Some AV products scan the spool file and may quarantine it\n"
            "   - Add exclusion: C:\\Windows\\System32\\spool\\PRINTERS\\\n"
            "5. Permissions:\n"
            "   - Check the user has Print permission on the printer\n"
            "   - Printer Properties > Security > user should have 'Print' allow\n"
            "6. Try printing from a different application\n"
            "7. Try printing to a different printer to isolate the issue\n"
            "8. Disable and re-enable the printer, then test again"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Secure Print / PIN printing not releasing jobs",
        "problem_description": "User sends a secure/confidential print job with a PIN but cannot release it at the printer. Job doesn't appear at the printer panel.",
        "problem_keywords": "secure print, pin print, confidential print, release job, held job, pull print, follow-me print",
        "solution_steps": (
            "1. Check at the printer:\n"
            "   - Navigate to 'Stored Jobs' or 'Secure Print' or 'Held Jobs' on printer panel\n"
            "   - Enter the correct PIN code\n"
            "   - Jobs may be listed under the username\n"
            "2. If the job doesn't appear:\n"
            "   - Verify secure print was enabled in the driver:\n"
            "   - Print dialog > Printer Properties > Job Storage or Secure Print\n"
            "   - PIN must have been set before sending the job\n"
            "3. Printer storage issues:\n"
            "   - Printer may have run out of storage for held jobs\n"
            "   - Old held jobs may need to be deleted first\n"
            "   - Check printer memory: Some models have limited RAM for job storage\n"
            "4. For pull-print solutions (PaperCut, Equitrac, etc.):\n"
            "   - Check if the pull-print server is running\n"
            "   - Verify user badge/card is registered in the system\n"
            "   - Check the pull-print queue on the server\n"
            "5. Timeout:\n"
            "   - Stored jobs may expire after a set time (e.g., 24 hours)\n"
            "   - Resend the job and release promptly\n"
            "6. Verify the user is sending to the correct printer/queue"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Printer leaking toner inside the machine",
        "problem_description": "Toner is spilling inside the laser printer. Pages have toner smudges, dust, or loose toner on the back. Inside the printer is dirty.",
        "problem_keywords": "toner leak, toner spill, toner dust, dirty printer, toner inside, loose toner, smudge back",
        "solution_steps": (
            "1. Safety first:\n"
            "   - Turn off and unplug the printer\n"
            "   - Use a toner vacuum or damp cloth (NOT a regular vacuum - static risk)\n"
            "   - Wear gloves - toner is fine powder\n"
            "2. Check the toner cartridge:\n"
            "   - Remove it and inspect for cracks or damage\n"
            "   - Check the seal: Was the protective strip removed properly?\n"
            "   - Gently shake and check for loose toner falling out\n"
            "   - Replace cartridge if damaged\n"
            "3. Check the drum unit:\n"
            "   - Drum surface should be clean and smooth\n"
            "   - Scratches on drum can cause toner to not adhere properly\n"
            "   - Replace drum if worn out (separate from cartridge on some models)\n"
            "4. Check the waste toner container:\n"
            "   - Full waste toner can overflow and spill\n"
            "   - Replace the waste toner container\n"
            "5. Clean the transfer belt/roller:\n"
            "   - Toner residue on the transfer roller causes back-side smudges\n"
            "   - Use printer's built-in cleaning feature or replace the unit\n"
            "6. After cleaning:\n"
            "   - Print several blank pages to clear residual toner\n"
            "   - Run the built-in cleaning cycle\n"
            "7. If using non-OEM cartridges: Try switching to genuine manufacturer cartridges"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Printer driver causes computer to crash or BSOD",
        "problem_description": "Computer crashes with Blue Screen of Death when printing or when the printer driver is loaded. BSOD may reference printer-related files.",
        "problem_keywords": "printer bsod, printer crash, driver crash, blue screen printer, printer driver bsod, print crash",
        "solution_steps": (
            "1. Identify the crashing driver:\n"
            "   - Check BSOD dump files: C:\\Windows\\Minidump\\\n"
            "   - Use WinDbg or BlueScreenView to analyze\n"
            "   - Look for printer-related .sys files in the stack trace\n"
            "2. Remove the printer driver:\n"
            "   - Boot to Safe Mode if necessary\n"
            "   - Device Manager > Print queues > remove printer\n"
            "   - Print Management > Drivers > remove the driver package\n"
            "   - Or: printui /s /t2 > Drivers tab > Remove\n"
            "3. Clean up driver files:\n"
            "   - Delete driver files from C:\\Windows\\System32\\spool\\drivers\\\n"
            "   - net stop spooler, clean up, net start spooler\n"
            "4. Install fresh driver:\n"
            "   - Download the latest driver from the manufacturer website\n"
            "   - NOT the driver from Windows Update (may be outdated)\n"
            "   - Install and test printing\n"
            "5. If vendor driver also crashes:\n"
            "   - Try the Windows built-in 'Microsoft IPP Class Driver'\n"
            "   - This is a generic but stable driver\n"
            "6. Check for Windows updates that may have caused the conflict\n"
            "   - KB article may exist for the specific BSOD + printer combination\n"
            "7. As a workaround: Use a different connection method (e.g., IPP instead of WSD)"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Printer not detected via USB connection",
        "problem_description": "USB printer is physically connected but Windows doesn't detect it. No 'New device found' notification appears.",
        "problem_keywords": "usb printer not detected, usb printer, printer not found usb, plug and play, usb not recognized printer",
        "solution_steps": (
            "1. Basic checks:\n"
            "   - Try a different USB cable\n"
            "   - Try a different USB port (preferably on the back of PC)\n"
            "   - Avoid USB hubs - connect directly to the computer\n"
            "   - Restart both the printer and computer\n"
            "2. Check Device Manager:\n"
            "   - Device Manager > look for unknown devices or yellow exclamation marks\n"
            "   - Check under 'Universal Serial Bus controllers' and 'Print queues'\n"
            "   - Right-click unknown device > Update Driver\n"
            "3. USB driver issues:\n"
            "   - Device Manager > Universal Serial Bus controllers\n"
            "   - Right-click each 'USB Root Hub' > Properties > Power Management\n"
            "   - Uncheck 'Allow the computer to turn off this device to save power'\n"
            "4. Install the driver BEFORE connecting (some printers require this):\n"
            "   - Download driver from manufacturer website\n"
            "   - Run the installer first\n"
            "   - Connect USB cable when prompted\n"
            "5. Check USB Selective Suspend:\n"
            "   - Power Options > Change Plan Settings > Advanced\n"
            "   - USB settings > USB selective suspend > Disabled\n"
            "6. Check the USB cable:\n"
            "   - Must be USB 2.0 Type-B cable (standard printer cable)\n"
            "   - Cable should be under 5 meters for reliable operation\n"
            "   - Some USB-C printers need specific cables"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Printer making grinding or loud noises",
        "problem_description": "Printer is making unusual grinding, squealing, or clicking noises during printing or startup. Print quality may also be affected.",
        "problem_keywords": "printer noise, grinding noise, squealing, loud printer, clicking noise, printer squeak, mechanical noise",
        "solution_steps": (
            "1. Identify the noise source:\n"
            "   - Open covers and listen for where the noise is coming from\n"
            "   - During startup: Often the carriage or gear mechanism\n"
            "   - During printing: Usually rollers, gears, or the fuser\n"
            "2. Paper path check:\n"
            "   - Check for small paper scraps stuck in the paper path\n"
            "   - Open all covers and doors, check for foreign objects\n"
            "   - Use a flashlight to inspect thoroughly\n"
            "3. Roller maintenance:\n"
            "   - Pickup rollers: Clean with a damp lint-free cloth\n"
            "   - Worn rollers may squeak - replace if shiny/smooth\n"
            "   - Fuser rollers: Do not touch - very hot during operation\n"
            "4. For laser printers:\n"
            "   - Remove toner cartridge and drum, check for debris\n"
            "   - Check the drum gear for damage\n"
            "   - Reinstall and test\n"
            "5. For inkjet printers:\n"
            "   - Grinding on startup: Carriage mechanism may be jammed\n"
            "   - Gently move the print head carriage by hand (when off)\n"
            "   - Check carriage rail for debris\n"
            "   - Clean and lubricate the carriage rod with light oil\n"
            "6. If fuser area: Fuser unit may need replacement (service call)\n"
            "7. Check if the noise started after installing new cartridges - seat them properly"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Printer watermark or overlay appearing on every page",
        "problem_description": "Every printed page has an unwanted watermark like 'DRAFT', 'CONFIDENTIAL', company logo, or other overlay that wasn't in the document.",
        "problem_keywords": "watermark, draft watermark, overlay print, unwanted watermark, remove watermark, print header, confidential",
        "solution_steps": (
            "1. Check print driver settings:\n"
            "   - Printer Preferences > Effects or Watermark tab\n"
            "   - Remove or disable any configured watermark\n"
            "   - Check 'Header/Footer' settings and disable if present\n"
            "2. Check application settings:\n"
            "   - Word/Excel: Design tab > Watermark > Remove Watermark\n"
            "   - PDF: The watermark may be embedded in the PDF itself\n"
            "3. Check the printer's built-in overlay:\n"
            "   - Access printer web interface > Settings > Forms/Overlay\n"
            "   - Disable any stored overlay or form\n"
            "   - Some printers: Settings > Print > Form Overlay > Off\n"
            "4. Group Policy-applied watermarks:\n"
            "   - GPO may push watermark settings via printer preferences\n"
            "   - Check: Computer Config > Preferences > Printers\n"
            "   - Contact IT admin to modify the policy\n"
            "5. Secure printing solutions:\n"
            "   - PaperCut, Equitrac, etc. can add watermarks\n"
            "   - Check the print management software settings\n"
            "6. Print from a different computer to determine if it's:\n"
            "   - PC-specific (driver setting) or printer-specific (stored on printer)"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "AirPrint or mobile printing not working",
        "problem_description": "Cannot print from iPhone/iPad via AirPrint or from Android device. Printer doesn't appear in the mobile device's print list.",
        "problem_keywords": "airprint, mobile print, iphone print, ipad print, android print, mopria, wifi direct print",
        "solution_steps": (
            "1. Basic requirements:\n"
            "   - Phone and printer must be on the SAME Wi-Fi network\n"
            "   - Printer must support AirPrint (iOS) or Mopria (Android)\n"
            "   - Check manufacturer's specs for mobile printing support\n"
            "2. AirPrint (iOS):\n"
            "   - Verify AirPrint is enabled on the printer (web interface > Network > AirPrint)\n"
            "   - On iPhone: Open document > Share > Print > printer should appear\n"
            "   - If not: Restart the printer and the phone\n"
            "   - Check: Router must allow multicast/Bonjour traffic between devices\n"
            "3. Android printing:\n"
            "   - Install the Mopria Print Service from Play Store\n"
            "   - Or install the manufacturer's print plugin (HP Smart, Epson iPrint, etc.)\n"
            "   - Settings > Connected devices > Connection preferences > Printing\n"
            "   - Enable the print service\n"
            "4. Network isolation:\n"
            "   - Guest Wi-Fi networks often isolate devices from each other\n"
            "   - Move to the main corporate Wi-Fi\n"
            "   - Check AP/router: 'Client isolation' or 'AP isolation' must be disabled\n"
            "5. Wi-Fi Direct as an alternative:\n"
            "   - Enable Wi-Fi Direct on the printer\n"
            "   - Connect phone directly to printer's Wi-Fi Direct network\n"
            "   - Print without needing shared Wi-Fi\n"
            "6. Manufacturer's app:\n"
            "   - HP Smart, Canon PRINT, Epson iPrint, Brother iPrint&Scan\n"
            "   - These often work when AirPrint/Mopria doesn't"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Printer shows 'Door Open' error but all doors are closed",
        "problem_description": "Printer displays 'Door Open' or 'Cover Open' error even though all doors and covers are physically closed. Printer won't print.",
        "problem_keywords": "door open, cover open, door sensor, cover closed, false door error, interlock, printer door",
        "solution_steps": (
            "1. Open and close all doors firmly:\n"
            "   - Open every cover/door on the printer\n"
            "   - Check for anything blocking the door from closing completely\n"
            "   - Close each door until it clicks securely\n"
            "2. Check door sensors:\n"
            "   - Locate the sensor switches (small plastic levers or tabs)\n"
            "   - When the door closes, a lever should press a microswitch\n"
            "   - Check if any sensor lever is broken or bent\n"
            "   - Check for paper scraps near the sensor area\n"
            "3. Cartridge/toner seating:\n"
            "   - Remove toner cartridge and drum\n"
            "   - Reinsert carefully - improper seating can trigger 'door open'\n"
            "   - Some models: The cartridge must lock into place\n"
            "4. Clean the sensor contacts:\n"
            "   - Use compressed air to clean around door sensors\n"
            "   - Clean sensor contacts with a dry cloth\n"
            "5. Paper path obstructions:\n"
            "   - Check for jammed paper in the fuser or duplex area\n"
            "   - Even a small scrap can prevent proper closure detection\n"
            "6. Power cycle: Turn off, wait 30 seconds, turn on\n"
            "7. If sensor is physically broken: This requires a service call for replacement"
        ),
    },
    {
        "category": "Printer",
        "problem_title": "Printer ghosting - faint duplicate image on page",
        "problem_description": "Printed pages show a faint repeated image or 'ghost' of the content lower on the same page. Laser printer showing repeated patterns.",
        "problem_keywords": "ghosting, ghost image, repeat image, faint duplicate, drum ghost, image repeat, shadow print",
        "solution_steps": (
            "1. Identify the repeating distance:\n"
            "   - Measure the distance between the original and ghost image\n"
            "   - This helps identify which component is causing it:\n"
            "   - Drum: ~75mm repeat cycle\n"
            "   - Fuser: ~63mm repeat cycle\n"
            "   - Transfer roller: ~56mm repeat cycle\n"
            "2. Drum-related ghosting:\n"
            "   - The drum isn't discharging properly between rotations\n"
            "   - Replace the drum unit (or toner + drum if combined)\n"
            "   - Also check: Drum may be exposed to light - keep it covered\n"
            "3. Fuser-related ghosting:\n"
            "   - The fuser isn't hot enough to fully bond toner\n"
            "   - Check paper type setting: Heavier paper needs higher fuser temp\n"
            "   - Replace the fuser if worn out\n"
            "4. Print density:\n"
            "   - If printing very dark content, reduce print density slightly\n"
            "   - The excess toner transfers to subsequent pages\n"
            "5. Paper issues:\n"
            "   - Damp paper worsens ghosting - use fresh paper\n"
            "   - Match the paper type setting to actual paper weight\n"
            "6. Run the printer's cleaning cycle\n"
            "7. Print 10-20 blank pages to help clean the drum path"
        ),
    },
]


DIAGNOSTIC_TREE = {
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
                "title": "Print quality problems",
                "node_type": "question",
                "question_text": "What quality issue do you see?",
                "children": [
                    {
                        "title": "Blank pages",
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
                        "title": "Lines, streaks, or smudges",
                        "node_type": "solution",
                        "solution_text": "1. For inkjet:\n   - Run print head alignment from printer maintenance menu\n   - Run head cleaning 2-3 times\n   - Check for damaged or leaking cartridges\n2. For laser:\n   - The drum unit may be damaged - inspect for marks\n   - The fuser may be contaminated - clean or replace\n   - Remove toner cartridge and check for spilled toner\n3. For both types:\n   - Clean the paper feed rollers with a damp lint-free cloth\n   - Use correct paper type and quality (not too thin/thick/damp)\n   - Check print quality is set to 'Normal' or 'Best', not 'Draft'\n4. Try printing a test page and a photo - compare quality"
                    },
                    {
                        "title": "Wrong colors or missing colors",
                        "node_type": "solution",
                        "solution_text": "1. Run a nozzle/color check from printer maintenance\n2. Check each individual ink/toner cartridge level\n3. Replace the empty or nearly-empty color cartridge\n4. Run head cleaning cycle (for inkjet)\n5. Check print settings:\n   - Make sure 'Grayscale' or 'Black & White' is not selected\n   - Ensure correct color profile is selected\n6. Run the printer's color calibration from its menu\n7. Try printing from a different application to isolate the issue"
                    },
                    {
                        "title": "Text is blurry or faded",
                        "node_type": "solution",
                        "solution_text": "1. Check ink/toner levels - replace if low\n2. Change print quality setting from 'Draft' to 'Normal' or 'Best'\n3. For laser: Shake toner cartridge to redistribute remaining toner\n4. Run alignment: Printer Maintenance > Align Print Heads\n5. Check that the paper type setting matches the actual paper\n6. Ensure you're using the correct driver (not generic/universal)\n7. Download and install the latest driver from manufacturer website"
                    }
                ]
            },
            {
                "title": "Paper feed issues",
                "node_type": "question",
                "question_text": "What's happening with the paper?",
                "children": [
                    {
                        "title": "Paper jam / false paper jam",
                        "node_type": "solution",
                        "solution_text": "1. Turn off the printer and unplug it\n2. Open all available doors, trays, and panels\n3. Carefully remove any visible paper - pull in the direction of paper path (avoid tearing)\n4. Check these common locations:\n   - Paper input tray (remove tray completely)\n   - Under the toner/ink cartridge\n   - Rear access door / duplexer unit\n   - Output tray area\n5. Look for tiny paper scraps with a flashlight\n6. Clean the pickup rollers with a slightly damp cloth\n7. Prevent future jams:\n   - Fan the paper before loading\n   - Don't overfill the tray\n   - Use the correct paper weight\n   - Adjust paper guides snugly\n   - Store paper in a dry place"
                    },
                    {
                        "title": "Feeding multiple pages",
                        "node_type": "solution",
                        "solution_text": "1. Fan the paper stack before loading to separate sheets\n2. Don't overfill the tray - stay below the max line\n3. Use fresh, dry paper (damp or old paper sticks together)\n4. Clean the pickup and separation rollers with a damp cloth\n5. Check if the separation pad is worn (needs replacement)\n6. Adjust paper guides to fit snugly against the stack\n7. Try a different brand/quality of paper"
                    },
                    {
                        "title": "Not picking up paper at all",
                        "node_type": "solution",
                        "solution_text": "1. Check that paper is loaded correctly and aligned\n2. Check that the paper guides are properly adjusted\n3. Make sure the correct paper tray is selected in print settings\n4. Clean the pickup rollers with a slightly damp lint-free cloth\n5. If rollers look smooth/shiny (instead of slightly rough) they need replacement\n6. Check for any debris or small paper scraps blocking the feed mechanism\n7. Try a different paper tray if available"
                    }
                ]
            }
        ]
    }
}
