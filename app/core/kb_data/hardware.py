"""Hardware troubleshooting articles and diagnostic tree."""

ARTICLES = [
    {
        "category": "Hardware",
        "problem_title": "External monitor not detected or no signal",
        "problem_description": "External monitor shows 'No Signal' or is not detected by the computer. Monitor may flash or remain black when connected.",
        "problem_keywords": "monitor no signal, external monitor, display not detected, second monitor, no display, hdmi no signal, displayport",
        "solution_steps": (
            "1. Check basic connections:\n"
            "   - Ensure cable is firmly connected at both ends\n"
            "   - Try a different cable (cables go bad)\n"
            "   - Try a different port on the computer and monitor\n"
            "2. Select correct input on monitor:\n"
            "   - Use monitor's physical buttons to select HDMI/DP/VGA input\n"
            "3. Detect the display in Windows:\n"
            "   - Settings > System > Display > Detect\n"
            "   - Or press Win+P and select 'Extend' or 'Duplicate'\n"
            "4. Update or reinstall graphics driver:\n"
            "   - Device Manager > Display adapters > Update driver\n"
            "   - Or download latest from NVIDIA/AMD/Intel website\n"
            "5. Check resolution settings:\n"
            "   - The monitor may not support the resolution Windows is trying to output\n"
            "   - In Safe Mode, lower the resolution\n"
            "6. For USB-C/Thunderbolt monitors:\n"
            "   - Not all USB-C ports support video output\n"
            "   - Check if your port has DisplayPort Alt Mode or Thunderbolt\n"
            "7. For docking stations:\n"
            "   - Update docking station firmware and drivers\n"
            "   - Try connecting directly to laptop (bypassing dock)\n"
            "8. Test the monitor with another computer to rule out monitor failure"
        ),
    },
    {
        "category": "Hardware",
        "problem_title": "USB device not recognized",
        "problem_description": "USB device shows 'USB Device Not Recognized' notification or doesn't appear at all when plugged in. May apply to drives, keyboards, mice, etc.",
        "problem_keywords": "usb not recognized, usb error, usb device, usb not working, unknown device, usb drive, usb port",
        "solution_steps": (
            "1. Try basic troubleshooting:\n"
            "   - Unplug and replug the device\n"
            "   - Try a different USB port (preferably directly on the PC, not a hub)\n"
            "   - Try on another computer to test the device itself\n"
            "2. Restart the USB controller:\n"
            "   - Device Manager > Universal Serial Bus controllers\n"
            "   - Right-click each 'USB Root Hub' > Disable, then Enable\n"
            "3. Uninstall and re-detect:\n"
            "   - Device Manager > find the device (may show with yellow !) > Uninstall\n"
            "   - Unplug device, wait 10 seconds, plug back in\n"
            "4. Update USB drivers:\n"
            "   - Device Manager > USB Root Hub > Update driver\n"
            "   - Install chipset driver from motherboard manufacturer\n"
            "5. Disable USB Selective Suspend:\n"
            "   - Control Panel > Power Options > Change plan settings > Advanced\n"
            "   - USB settings > USB selective suspend > Disabled\n"
            "6. For USB drives:\n"
            "   - Check Disk Management (diskmgmt.msc) - the drive may need a drive letter\n"
            "   - Right-click > Change Drive Letter and Paths > Add\n"
            "7. Check for power issues:\n"
            "   - USB ports provide limited power\n"
            "   - External HDDs may need a powered USB hub"
        ),
    },
    {
        "category": "Hardware",
        "problem_title": "No audio / no sound from speakers or headphones",
        "problem_description": "Computer produces no sound. Speakers or headphones are connected but no audio plays. Volume icon may show issues.",
        "problem_keywords": "no sound, no audio, speakers not working, headphones no sound, audio not working, sound missing, volume",
        "solution_steps": (
            "1. Check the obvious:\n"
            "   - Is volume muted? Click speaker icon in taskbar\n"
            "   - Is volume turned up on the physical speakers/headphones?\n"
            "   - Are speakers plugged in / turned on?\n"
            "2. Check the correct output device:\n"
            "   - Right-click speaker icon > Sound settings\n"
            "   - Under 'Output', select the correct device\n"
            "   - Or: Right-click speaker icon > Open Volume mixer > verify app volumes\n"
            "3. Run Windows audio troubleshooter:\n"
            "   - Settings > Update > Troubleshoot > Playing Audio\n"
            "4. Restart audio services:\n"
            "   - services.msc > Windows Audio > Restart\n"
            "   - Also restart: Windows Audio Endpoint Builder\n"
            "5. Update audio driver:\n"
            "   - Device Manager > Sound, video and game controllers\n"
            "   - Right-click audio device > Update driver\n"
            "   - Or download from manufacturer (Realtek, IDT, Conexant)\n"
            "6. Reinstall audio driver:\n"
            "   - Device Manager > right-click > Uninstall device > check 'Delete driver'\n"
            "   - Restart - Windows will reinstall\n"
            "7. Check BIOS: Onboard audio may be disabled in BIOS\n"
            "8. For HDMI audio: Display > set HDMI audio as default output device"
        ),
    },
    {
        "category": "Hardware",
        "problem_title": "Keyboard keys not working or typing wrong characters",
        "problem_description": "Some keyboard keys don't work, type the wrong character, or the entire keyboard is unresponsive. May type numbers instead of letters.",
        "problem_keywords": "keyboard not working, wrong characters, keyboard error, keys not typing, num lock, keyboard language, keyboard layout",
        "solution_steps": (
            "1. If letters produce numbers (e.g., pressing U gives 4):\n"
            "   - NumLock is ON for the laptop keyboard\n"
            "   - Press Fn + NumLock (or dedicated NumLock key) to turn it off\n"
            "2. If wrong characters (e.g., Z and Y swapped):\n"
            "   - Wrong keyboard layout!\n"
            "   - Settings > Time & Language > Language\n"
            "   - Click on your language > Options > add/change keyboard layout\n"
            "   - Quick switch: Win+Space to toggle layout\n"
            "3. If some keys don't work:\n"
            "   - Test with On-Screen Keyboard: search 'osk' in Start\n"
            "   - If on-screen keyboard works fine, it's a hardware issue with the physical keyboard\n"
            "   - For external keyboard: try different USB port or replace keyboard\n"
            "   - For laptop: check for debris under keys, or external keyboard as workaround\n"
            "4. If no keys work at all:\n"
            "   - Unplug and replug (for USB keyboards)\n"
            "   - Try a different USB port\n"
            "   - Check Device Manager for driver issues\n"
            "   - Update or reinstall keyboard drivers\n"
            "5. Check Filter Keys isn't enabled: Settings > Accessibility > Keyboard\n"
            "6. Check Sticky Keys isn't causing issues: Turn off in same settings"
        ),
    },
    {
        "category": "Hardware",
        "problem_title": "Mouse cursor freezing, jumping, or not moving",
        "problem_description": "Mouse cursor freezes, jumps around the screen, moves erratically, or stops working entirely. Touchpad may also exhibit issues.",
        "problem_keywords": "mouse not working, cursor freezing, mouse jumping, touchpad not working, mouse lag, cursor stuck, mouse frozen",
        "solution_steps": (
            "1. For USB/wireless mouse:\n"
            "   - Unplug and replug (try different USB port)\n"
            "   - Replace batteries in wireless mouse\n"
            "   - Check wireless receiver isn't blocked or too far away\n"
            "   - Clean the sensor on the bottom of the mouse\n"
            "   - Try on a different surface (avoid glass or reflective surfaces)\n"
            "2. For Bluetooth mouse:\n"
            "   - Turn off and on the mouse\n"
            "   - Remove and re-pair: Settings > Bluetooth > remove device > pair again\n"
            "3. For laptop touchpad:\n"
            "   - Check if touchpad is disabled: Look for Fn + touchpad toggle key\n"
            "   - Check Settings > Devices > Touchpad > toggle On\n"
            "   - Some laptops disable touchpad when external mouse is connected\n"
            "4. Update mouse/touchpad driver:\n"
            "   - Device Manager > Mice and other pointing devices > Update driver\n"
            "   - For touchpad: download from laptop manufacturer (Synaptics, ELAN, etc.)\n"
            "5. If cursor jumps/drifts:\n"
            "   - Reduce mouse sensitivity: Settings > Devices > Mouse > Pointer speed\n"
            "   - Disable 'Enhance pointer precision'\n"
            "6. For a completely frozen cursor:\n"
            "   - Try Tab and Enter keys to navigate\n"
            "   - Ctrl+Alt+Del > restart computer\n"
            "   - In Safe Mode, test if mouse works (driver issue test)"
        ),
    },
    {
        "category": "Hardware",
        "problem_title": "Laptop battery not charging or draining fast",
        "problem_description": "Laptop shows 'Plugged in, not charging' or battery drains very quickly. Battery percentage doesn't increase when connected to power.",
        "problem_keywords": "battery not charging, plugged in not charging, battery drain, laptop battery, battery fast drain, charging problem",
        "solution_steps": (
            "1. 'Plugged in, not charging':\n"
            "   - Remove battery (if removable), hold power 30 seconds, reinsert\n"
            "   - Try a different power outlet\n"
            "   - Check the charger and cable for damage\n"
            "2. Reset the battery driver:\n"
            "   - Device Manager > Batteries > Microsoft ACPI-Compliant Control Method Battery\n"
            "   - Right-click > Uninstall > restart computer\n"
            "   - Windows will reinstall the driver\n"
            "3. Check battery health:\n"
            "   - CMD (Admin): powercfg /batteryreport\n"
            "   - Open the generated report at C:\\Users\\<username>\\battery-report.html\n"
            "   - Compare 'Design Capacity' vs 'Full Charge Capacity'\n"
            "   - If Full Charge is less than 40% of Design, battery needs replacement\n"
            "4. For fast drain:\n"
            "   - Check battery report for high drain apps\n"
            "   - Reduce screen brightness\n"
            "   - Turn off Bluetooth and Wi-Fi when not needed\n"
            "   - Close unnecessary background apps\n"
            "   - Power plan: Settings > System > Power > Best power efficiency\n"
            "5. BIOS update may fix charging issues (download from manufacturer)\n"
            "6. If using non-original charger: It may not provide enough wattage\n"
            "7. Check for battery conservation mode in manufacturer software (Lenovo Vantage, Dell Power Manager)"
        ),
    },
    {
        "category": "Hardware",
        "problem_title": "Hard drive clicking or making noise",
        "problem_description": "Hard drive is making clicking, grinding, or beeping noises. Drive may not be detected or is showing slow performance.",
        "problem_keywords": "hard drive clicking, drive noise, hard drive grinding, drive beeping, hdd noise, hard drive failing, click of death",
        "solution_steps": (
            "1. CRITICAL: A clicking hard drive is likely failing\n"
            "   - Back up data IMMEDIATELY if the drive is still accessible\n"
            "   - Copy important files to an external drive, USB, or cloud storage\n"
            "2. Check SMART status:\n"
            "   - CMD: wmic diskdrive get status\n"
            "   - Install CrystalDiskInfo (free) for detailed health status\n"
            "   - If it shows 'Caution' or 'Bad': Drive is failing\n"
            "3. Listen to the sounds:\n"
            "   - Rhythmic clicking (click of death): Head crash - drive is failing\n"
            "   - Grinding: Physical damage - drive is failing\n"
            "   - Beeping: Motor seized - drive is failing\n"
            "   - Occasional soft clicks: Normal head parking\n"
            "4. If drive is not detected:\n"
            "   - Try different SATA cable and port\n"
            "   - Try in a USB enclosure on another PC\n"
            "   - Do NOT open the drive (needs cleanroom for data recovery)\n"
            "5. For data recovery on a failed drive:\n"
            "   - Professional data recovery services (expensive but effective)\n"
            "   - NEVER run chkdsk or format on a clicking drive\n"
            "   - Software recovery: Only if drive is still detectable (try ddrescue on Linux)\n"
            "6. Replacement: Replace with SSD for better speed, reliability, and no noise"
        ),
    },
    {
        "category": "Hardware",
        "problem_title": "SSD not detected or suddenly disappeared",
        "problem_description": "SSD is not showing in Windows or BIOS. May have disappeared suddenly after working fine. BIOS may not detect the drive.",
        "problem_keywords": "ssd not detected, ssd disappeared, ssd not showing, nvme not detected, m.2 not showing, ssd bios, ssd missing",
        "solution_steps": (
            "1. Check if SSD shows in BIOS:\n"
            "   - Restart > Enter BIOS (F2/Del) > look for Storage/Drives section\n"
            "   - If not in BIOS: hardware connection issue\n"
            "2. For SATA SSD:\n"
            "   - Reseat the SATA data cable and power cable\n"
            "   - Try a different SATA port on the motherboard\n"
            "   - Try a different SATA cable\n"
            "3. For M.2/NVMe SSD:\n"
            "   - Reseat the M.2 drive (remove and reinsert)\n"
            "   - Check if the M.2 slot supports NVMe or only SATA\n"
            "   - Some motherboards share bandwidth between M.2 and SATA ports\n"
            "   - Check motherboard manual for M.2 slot compatibility\n"
            "4. If SSD is in BIOS but not Windows:\n"
            "   - Open Disk Management (diskmgmt.msc)\n"
            "   - The SSD may appear as 'Unallocated' or 'Not Initialized'\n"
            "   - Initialize and format it (WARNING: this erases all data)\n"
            "   - If it was previously working, there may be a partition/file system issue\n"
            "5. Update storage controller drivers\n"
            "6. Update SSD firmware from manufacturer's website (Samsung Magician, Crucial Storage Executive)\n"
            "7. If SSD randomly disappears: It may be overheating - check with CrystalDiskInfo"
        ),
    },
    {
        "category": "Hardware",
        "problem_title": "Computer overheating - high temperatures",
        "problem_description": "Computer is very hot to touch. CPU or GPU temperatures are too high. May experience thermal throttling, shutdowns, or crashes.",
        "problem_keywords": "overheating, hot computer, high temperature, thermal throttle, cpu hot, gpu hot, fan loud, thermal shutdown",
        "solution_steps": (
            "1. Monitor temperatures:\n"
            "   - Install HWiNFO64 (free) or Core Temp\n"
            "   - Normal idle: CPU 30-50°C, GPU 30-45°C\n"
            "   - Normal load: CPU 60-80°C, GPU 65-85°C\n"
            "   - Concerning: CPU > 90°C, GPU > 95°C\n"
            "2. Clean dust:\n"
            "   - Power off and unplug the computer\n"
            "   - Use compressed air to blow dust from:\n"
            "   - CPU heatsink/fan, GPU heatsink/fan, case fans, vents\n"
            "   - For laptops: Blow into the exhaust vents\n"
            "3. Improve airflow:\n"
            "   - Don't block vents (laptop on bed/pillow = blocked vents)\n"
            "   - Use a laptop cooling pad\n"
            "   - For desktop: Ensure proper cable management, add case fans\n"
            "4. Replace thermal paste:\n"
            "   - If CPU is 3+ years old, thermal paste may have dried out\n"
            "   - Clean old paste with isopropyl alcohol, apply new (pea-sized dot)\n"
            "5. Check fans are spinning:\n"
            "   - If a fan isn't spinning: replace it\n"
            "   - Check fan curves in BIOS or manufacturer software\n"
            "6. Reduce CPU load:\n"
            "   - Power plan to 'Balanced' (not High Performance)\n"
            "   - Limit max CPU state: Power Options > Advanced > Processor > Max = 90%\n"
            "7. In extreme cases: Repaste CPU, replace thermal pads, or replace heatsink"
        ),
    },
    {
        "category": "Hardware",
        "problem_title": "Docking station not working properly",
        "problem_description": "Laptop docking station has issues: monitors not displaying, USB devices not working, Ethernet not connecting, or intermittent disconnections.",
        "problem_keywords": "docking station, dock not working, dock display, dock usb, thunderbolt dock, usb-c dock, laptop dock",
        "solution_steps": (
            "1. Basic troubleshooting:\n"
            "   - Unplug dock from laptop, wait 10 seconds, reconnect\n"
            "   - Restart the laptop with the dock connected\n"
            "   - Try a different USB-C/Thunderbolt cable if using an external dock\n"
            "2. Update dock firmware:\n"
            "   - Download firmware update from dock manufacturer\n"
            "   - Dell: Dell Dock Update utility\n"
            "   - Lenovo: Lenovo System Update\n"
            "   - HP: HP Firmware Installer\n"
            "3. Update drivers:\n"
            "   - Thunderbolt driver (for Thunderbolt docks)\n"
            "   - DisplayLink driver (for USB docks that use DisplayLink)\n"
            "   - Graphics driver (for display issues)\n"
            "   - USB driver/chipset driver\n"
            "4. For display issues:\n"
            "   - Check display cable connections on dock\n"
            "   - Win+P > Extend or Duplicate\n"
            "   - Some docks limit the number/resolution of monitors\n"
            "5. For USB issues through dock:\n"
            "   - Connect device directly to laptop to test\n"
            "   - Check if dock has enough power delivery for all connected devices\n"
            "6. For Ethernet through dock:\n"
            "   - Check if dock Ethernet driver is installed\n"
            "   - Try: ipconfig /release && ipconfig /renew\n"
            "7. Power delivery: Ensure dock provides enough wattage for your laptop"
        ),
    },
    {
        "category": "Hardware",
        "problem_title": "Webcam not working or not detected",
        "problem_description": "Built-in or external webcam is not working. Camera shows black screen, is not detected, or shows an error in video applications.",
        "problem_keywords": "webcam not working, camera not detected, webcam black, camera error, video call, teams camera, zoom camera",
        "solution_steps": (
            "1. Check camera privacy settings:\n"
            "   - Settings > Privacy > Camera > Allow apps to access camera > ON\n"
            "   - Check that the specific app is enabled below\n"
            "2. Check for physical camera cover/switch:\n"
            "   - Many laptops have a physical privacy shutter over the camera\n"
            "   - Some have a function key (Fn + camera key) to toggle camera\n"
            "3. Check if another app is using the camera:\n"
            "   - Only one app can use the camera at a time\n"
            "   - Close other video apps (Teams, Zoom, Skype, etc.)\n"
            "4. Update the camera driver:\n"
            "   - Device Manager > Cameras (or Imaging devices)\n"
            "   - Right-click > Update driver\n"
            "   - Or uninstall > restart to let Windows reinstall\n"
            "5. Test in the Camera app:\n"
            "   - Open the built-in 'Camera' app from Start\n"
            "   - If it works there but not in Teams/Zoom: app settings issue\n"
            "6. Check Device Manager:\n"
            "   - If camera shows with yellow ! : driver issue\n"
            "   - If camera is missing: may be disabled in BIOS\n"
            "7. For external USB webcam:\n"
            "   - Try different USB port\n"
            "   - Install manufacturer's driver/software\n"
            "8. Check antivirus: Some security software blocks camera access"
        ),
    },
    {
        "category": "Hardware",
        "problem_title": "Bluetooth not working or device won't pair",
        "problem_description": "Bluetooth adapter not working, devices won't pair, connected device keeps disconnecting, or Bluetooth toggle is missing.",
        "problem_keywords": "bluetooth not working, bluetooth pair, bluetooth missing, bluetooth disconnect, bluetooth driver, bt not working",
        "solution_steps": (
            "1. Check Bluetooth is enabled:\n"
            "   - Settings > Bluetooth & Devices > toggle On\n"
            "   - Check for physical Bluetooth switch or Fn key toggle\n"
            "   - Check Airplane mode is OFF\n"
            "2. If Bluetooth toggle is missing:\n"
            "   - Device Manager > Bluetooth > check for adapter\n"
            "   - If no Bluetooth section: driver not installed or adapter disabled\n"
            "   - Check if disabled in BIOS\n"
            "3. Restart Bluetooth:\n"
            "   - Device Manager > Bluetooth adapter > Disable > Enable\n"
            "   - Or: services.msc > Bluetooth Support Service > Restart\n"
            "4. Remove and re-pair device:\n"
            "   - Settings > Bluetooth > device > Remove\n"
            "   - Put the device in pairing mode\n"
            "   - Add Bluetooth device > reconnect\n"
            "5. Update Bluetooth driver:\n"
            "   - Download from laptop/adapter manufacturer\n"
            "   - Don't rely on Windows Update for Bluetooth drivers\n"
            "6. For audio devices (headphones/speakers):\n"
            "   - After pairing, set as default audio device\n"
            "   - Right-click speaker icon > Sound settings > Output\n"
            "7. If random disconnects:\n"
            "   - Disable power management: Device Manager > BT adapter > Properties > Power Management\n"
            "   - Uncheck 'Allow computer to turn off this device'"
        ),
    },
    {
        "category": "Hardware",
        "problem_title": "RAM errors or computer beeping on startup",
        "problem_description": "Computer beeps during startup and doesn't boot, or shows random errors, blue screens, and crashes that point to RAM issues.",
        "problem_keywords": "ram error, memory error, beep codes, pc beeping, ram failure, memory test, bad ram, ram beep",
        "solution_steps": (
            "1. Interpret beep codes:\n"
            "   - One short beep: Normal POST (all good)\n"
            "   - Repeating short beeps: RAM not detected or failed\n"
            "   - Long continuous beep: RAM failure\n"
            "   - Pattern varies by BIOS manufacturer (AMI, Award, Phoenix)\n"
            "   - Check your motherboard manual for specific beep codes\n"
            "2. Reseat RAM:\n"
            "   - Power off and unplug the computer\n"
            "   - Remove all RAM sticks\n"
            "   - Clean contacts with a clean eraser or isopropyl alcohol\n"
            "   - Reseat firmly until clips snap into place\n"
            "3. Test individual sticks:\n"
            "   - If multiple sticks: test one at a time\n"
            "   - Try each stick in each slot to find bad stick or slot\n"
            "4. Run memory diagnostic:\n"
            "   - mdsched.exe > Restart and check for problems\n"
            "   - For thorough testing: MemTest86 (boot from USB, free)\n"
            "   - Run for at least 4 passes (may take hours)\n"
            "5. Check RAM compatibility:\n"
            "   - New RAM must match: DDR generation, speed, and voltage\n"
            "   - Check motherboard QVL (Qualified Vendor List)\n"
            "   - Mixed brands/speeds can cause instability\n"
            "6. Check BIOS settings:\n"
            "   - XMP/DOCP may need to be enabled for rated speed\n"
            "   - If RAM was overclocked, reset to default\n"
            "7. Replace faulty RAM stick"
        ),
    },
    {
        "category": "Hardware",
        "problem_title": "Power supply unit (PSU) issues - random shutdowns",
        "problem_description": "Computer randomly shuts off without warning (not restart, just off). May fail to turn on, or turns on briefly then dies.",
        "problem_keywords": "power supply, psu failure, random shutdown, pc turns off, pc won't turn on, power issue, psu, power off",
        "solution_steps": (
            "1. Signs of PSU failure:\n"
            "   - PC shuts off suddenly without restart\n"
            "   - PC won't turn on at all (no lights, no fans)\n"
            "   - PC turns on briefly then dies\n"
            "   - Burning smell from the back of the case\n"
            "   - Random crashes/BSODs under heavy load\n"
            "2. Quick test (paperclip test):\n"
            "   - Disconnect PSU from motherboard\n"
            "   - On the 24-pin ATX connector, bridge green wire (PS_ON) to any black wire (Ground)\n"
            "   - If PSU fan spins: PSU can provide basic power\n"
            "   - This only tests basic function, not quality of power\n"
            "3. Check power:\n"
            "   - Is the outlet working? Test with another device\n"
            "   - Is PSU switch on (I = ON, O = OFF)?\n"
            "   - Try a different power cable\n"
            "4. Check for overloading:\n"
            "   - Calculate total system power draw (use pcpartpicker.com)\n"
            "   - PSU should be rated 20-30% above total draw\n"
            "   - New GPU may exceed PSU capacity\n"
            "5. Check internal connections:\n"
            "   - Reseat all PSU cables (24-pin, 8-pin CPU, GPU power)\n"
            "6. For accurate testing: Use a PSU tester (cheap tool, ~$20)\n"
            "   - Tests all voltage rails for correct output\n"
            "7. Replace PSU if failing - don't try to repair them (capacitors store dangerous charge)"
        ),
    },
    {
        "category": "Hardware",
        "problem_title": "Laptop screen flickering or display issues",
        "problem_description": "Laptop screen flickers, has horizontal/vertical lines, shows discolored patches, or goes dim/bright randomly.",
        "problem_keywords": "screen flicker, display flicker, laptop screen, screen lines, screen dim, brightness flicker, lcd issue",
        "solution_steps": (
            "1. Determine if it's hardware or software:\n"
            "   - Open Task Manager (Ctrl+Shift+Esc)\n"
            "   - If Task Manager flickers too: it's a driver issue\n"
            "   - If Task Manager doesn't flicker (but other things do): it's an app issue\n"
            "2. For driver-related flickering:\n"
            "   - Update display driver from manufacturer (NVIDIA/AMD/Intel)\n"
            "   - If update started the problem: Roll back the driver in Device Manager\n"
            "   - Uninstall driver with DDU (Display Driver Uninstaller) and reinstall\n"
            "3. For app-related flickering:\n"
            "   - Disable hardware acceleration in the problem app\n"
            "   - Update the application\n"
            "   - Common culprits: antivirus, Norton, iCloud, older apps\n"
            "4. Check display cable (hardware):\n"
            "   - Open and close the lid slowly - if flickering changes, cable is loose\n"
            "   - The LVDS or eDP cable inside the hinge may be damaged\n"
            "5. For random brightness changes:\n"
            "   - Disable adaptive brightness: Settings > Display > Brightness > uncheck 'Change brightness automatically'\n"
            "   - Disable Content Adaptive Brightness (CABC) if present\n"
            "6. For horizontal/vertical lines:\n"
            "   - Connect an external monitor - if lines are only on laptop screen: LCD or cable issue\n"
            "   - If on both screens: GPU issue\n"
            "7. Refresh rate: Try changing display refresh rate to see if it helps"
        ),
    },
    {
        "category": "Hardware",
        "problem_title": "Headphone jack not working - no audio from 3.5mm port",
        "problem_description": "Plugging headphones or speakers into the 3.5mm audio jack produces no sound. Windows may not detect the device.",
        "problem_keywords": "headphone jack, audio jack, 3.5mm, headphones not working, no sound headphones, jack not working",
        "solution_steps": (
            "1. Test the headphones on another device (phone, tablet) to confirm they work\n"
            "2. Check the correct output is selected:\n"
            "   - Right-click speaker icon in taskbar > Sound settings\n"
            "   - Select the headphone/speaker output device\n"
            "3. Try Windows audio troubleshooter:\n"
            "   - Settings > Update > Troubleshoot > Playing Audio\n"
            "4. Check Realtek Audio Console (if installed):\n"
            "   - Open Realtek Audio Console from taskbar or Start\n"
            "   - Check if the jack is detected and configured correctly\n"
            "   - Front panel vs rear panel jack settings\n"
            "5. Reinstall audio driver:\n"
            "   - Device Manager > Sound controllers > Uninstall device\n"
            "   - Check 'Delete the driver software'\n"
            "   - Restart to let Windows reinstall\n"
            "   - Or install latest Realtek driver from manufacturer\n"
            "6. Disable audio enhancements:\n"
            "   - Sound settings > Device properties > Additional device properties\n"
            "   - Enhancements tab > Disable all\n"
            "7. Check physical jack:\n"
            "   - Look for dust or lint in the port - use compressed air to clean\n"
            "   - Check if jack is loose or damaged\n"
            "8. For front panel jacks (desktop): Check internal cable from case to motherboard"
        ),
    },
]

DIAGNOSTIC_TREE = {
    "category": "Hardware",
    "root": {
        "title": "Hardware Troubleshooting",
        "node_type": "question",
        "question_text": "What type of hardware issue are you experiencing?",
        "children": [
            {
                "title": "Display / Monitor issues",
                "node_type": "question",
                "question_text": "What's wrong with the display?",
                "children": [
                    {
                        "title": "External monitor shows no signal",
                        "node_type": "solution",
                        "solution_text": "1. Check cable is firmly connected at both ends\n2. Select correct input on monitor (HDMI/DP/VGA button)\n3. Try Win+P > Extend or Duplicate\n4. Try a different cable\n5. Update graphics driver\n6. For USB-C: verify port supports video (DisplayPort Alt Mode)\n7. Test monitor on another computer\n8. For docking stations: update dock firmware"
                    },
                    {
                        "title": "Screen flickering or has lines",
                        "node_type": "solution",
                        "solution_text": "1. Open Task Manager - does Task Manager flicker too?\n   - Yes: Display driver issue - update or roll back driver\n   - No: An application is causing it\n2. Update display driver from manufacturer\n3. Connect external monitor to test:\n   - Lines on external too: GPU problem\n   - Lines only on laptop screen: LCD or cable issue\n4. Check if adaptive brightness is causing flicker\n5. Try changing refresh rate"
                    }
                ]
            },
            {
                "title": "Audio / Sound problems",
                "node_type": "question",
                "question_text": "What's the audio problem?",
                "children": [
                    {
                        "title": "No sound at all",
                        "node_type": "solution",
                        "solution_text": "1. Check volume isn't muted (taskbar speaker icon)\n2. Check correct output device is selected:\n   - Right-click speaker > Sound settings > Output device\n3. Check physical connections and speaker power\n4. Run audio troubleshooter\n5. Restart Windows Audio service (services.msc)\n6. Reinstall audio driver:\n   - Device Manager > Sound > Uninstall > restart\n7. Check if onboard audio is disabled in BIOS"
                    },
                    {
                        "title": "Headphones/jack not working",
                        "node_type": "solution",
                        "solution_text": "1. Test headphones on another device\n2. Check output device is set to headphones\n3. Check Realtek Audio Console for jack detection\n4. Reinstall audio driver\n5. Disable audio enhancements\n6. Clean the audio jack with compressed air\n7. For front panel: check internal cable connection"
                    }
                ]
            },
            {
                "title": "USB device issues",
                "node_type": "solution",
                "solution_text": "1. Try different USB port (use port directly on PC)\n2. Test device on another computer\n3. Device Manager > USB Root Hub > Disable then Enable\n4. Uninstall device in Device Manager > unplug > replug\n5. Disable USB Selective Suspend in Power Options\n6. For USB drives: check Disk Management for drive letter\n7. Update chipset/USB drivers from motherboard manufacturer"
            },
            {
                "title": "Keyboard or Mouse problems",
                "node_type": "solution",
                "solution_text": "Keyboard:\n1. If typing numbers instead of letters: Turn off NumLock (Fn+NumLock)\n2. If wrong characters: Change keyboard layout (Win+Space)\n3. Test with On-Screen Keyboard (search 'osk')\n4. Check Filter Keys / Sticky Keys are disabled\n\nMouse:\n1. Try different USB port or replace batteries\n2. Clean the sensor\n3. For Bluetooth: remove and re-pair\n4. Update driver from Device Manager\n5. Disable power management on USB root hub"
            },
            {
                "title": "Computer overheating",
                "node_type": "solution",
                "solution_text": "1. Monitor temps with HWiNFO64 or Core Temp\n   - CPU > 90°C = overheating\n   - GPU > 95°C = overheating\n2. Clean dust from fans and vents with compressed air\n3. Ensure vents aren't blocked (don't use laptop on bed/pillow)\n4. Use a laptop cooling pad\n5. Replace thermal paste (if 3+ years old)\n6. Check all fans are spinning\n7. Set power plan to Balanced\n8. Limit max CPU state to 90% in power options"
            },
            {
                "title": "Hard drive / SSD problems",
                "node_type": "solution",
                "solution_text": "1. Check drive health:\n   - CMD: wmic diskdrive get status\n   - Use CrystalDiskInfo for detailed SMART data\n2. Clicking/grinding HDD: BACK UP DATA NOW - drive is failing\n3. SSD not detected:\n   - Reseat the drive (SATA cable or M.2 slot)\n   - Check BIOS for drive detection\n   - Check Disk Management in Windows\n4. Run chkdsk C: /f /r for file system errors\n5. Update SSD firmware from manufacturer\n6. Replace failing drives with SSD"
            },
            {
                "title": "Battery / Power issues",
                "node_type": "solution",
                "solution_text": "For laptop battery:\n1. Reset battery driver: Device Manager > Batteries > Uninstall > restart\n2. Generate battery report: powercfg /batteryreport\n3. If Full Charge < 40% of Design Capacity: replace battery\n\nFor desktop power:\n1. Check power cable and outlet\n2. Check PSU switch is ON\n3. Reseat internal power cables (24-pin, CPU, GPU)\n4. Test PSU with tester tool or paperclip test\n5. Calculate if PSU wattage is sufficient for your components\n6. Replace PSU if faulty"
            }
        ]
    }
}
