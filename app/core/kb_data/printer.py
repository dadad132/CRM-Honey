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
