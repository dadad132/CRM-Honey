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
    {
        "category": "Hardware",
        "problem_title": "CMOS battery dead or BIOS settings keep resetting",
        "problem_description": "Computer loses BIOS settings after powering off. Date/time resets, boot order changes back to default, or 'CMOS checksum error' appears.",
        "problem_keywords": "cmos battery, bios reset, cmos error, bios settings lost, date reset, cmos checksum, cr2032",
        "solution_steps": (
            "1. Symptoms of dead CMOS battery:\n"
            "   - Date/time resets to a past date on every boot\n"
            "   - BIOS settings revert to defaults after power off\n"
            "   - 'CMOS Checksum Error' on boot\n"
            "   - System may beep or show warnings\n"
            "2. Replace the CMOS battery:\n"
            "   - Power off and unplug the computer\n"
            "   - Open the case and locate the CR2032 battery on the motherboard\n"
            "   - Note the orientation (+/- side)\n"
            "   - Remove the old battery and insert a new CR2032\n"
            "3. After replacement:\n"
            "   - Power on, enter BIOS (Del/F2 during boot)\n"
            "   - Reconfigure settings: boot order, date/time, SATA mode\n"
            "   - Save and exit\n"
            "4. Battery life:\n"
            "   - CMOS batteries last 3-7 years typically\n"
            "   - Desktop PCs: Easy to replace (accessible on motherboard)\n"
            "   - Laptops: May be soldered or require disassembly\n"
            "5. If settings still reset after new battery:\n"
            "   - Check the battery holder for corrosion, clean with isopropyl alcohol\n"
            "   - Motherboard damage possible if the holder is broken\n"
            "6. BIOS update:\n"
            "   - Flash the BIOS to latest version from motherboard manufacturer\n"
            "   - Corrupted BIOS can also cause settings loss"
        ),
    },
    {
        "category": "Hardware",
        "problem_title": "Computer randomly shuts down without warning",
        "problem_description": "PC powers off suddenly without any blue screen or warning. May happen during heavy use, or seemingly at random.",
        "problem_keywords": "random shutdown, sudden power off, pc turns off, unexpected shutdown, no warning, power failure, shuts off",
        "solution_steps": (
            "1. Check for overheating:\n"
            "   - Download HWMonitor or Core Temp\n"
            "   - CPU temps above 95-100°C trigger emergency shutdown\n"
            "   - GPU temps above 100-110°C also cause shutdowns\n"
            "   - Clean fans and heatsinks with compressed air\n"
            "2. Power supply (PSU) issues:\n"
            "   - Insufficient wattage for the components\n"
            "   - Aging PSU with failing capacitors\n"
            "   - Check: Does it happen under heavy load (gaming, rendering)?\n"
            "   - Try a different/higher wattage PSU to test\n"
            "3. Check Event Viewer:\n"
            "   - System log > look for 'Kernel-Power' Event ID 41\n"
            "   - This indicates unexpected shutdown (no clean shutdown event)\n"
            "4. RAM issues:\n"
            "   - Run Windows Memory Diagnostic (mdsched.exe)\n"
            "   - Or run MemTest86 overnight\n"
            "   - Try removing one stick at a time\n"
            "5. Power outlet:\n"
            "   - Loose power cable or faulty outlet\n"
            "   - Use a UPS (Uninterruptible Power Supply)\n"
            "   - Avoid daisy-chaining power strips\n"
            "6. Check power settings:\n"
            "   - Settings > Power & Sleep > ensure not set to turn off\n"
            "   - powercfg /energy to check power configuration\n"
            "7. For laptops: Test with AC power only (remove battery if possible)"
        ),
    },
    {
        "category": "Hardware",
        "problem_title": "Docking station not detecting all peripherals",
        "problem_description": "USB docking station or Thunderbolt dock doesn't detect all connected monitors, USB devices, or network adapter. Some peripherals work but others don't.",
        "problem_keywords": "docking station, dock, thunderbolt dock, usb dock, peripherals, dock not working, displaylink, dock monitors",
        "solution_steps": (
            "1. Power and connections:\n"
            "   - Ensure the dock has its power adapter connected (most docks need external power)\n"
            "   - Check the cable between laptop and dock (USB-C/Thunderbolt cable)\n"
            "   - Try a different USB-C/Thunderbolt port on the laptop\n"
            "2. Dock firmware:\n"
            "   - Check manufacturer website for dock firmware updates\n"
            "   - Dell, Lenovo, HP all have dock firmware update utilities\n"
            "   - Firmware updates fix many compatibility issues\n"
            "3. Drivers:\n"
            "   - DisplayLink docks: Install/update DisplayLink driver\n"
            "   - Thunderbolt docks: Install Thunderbolt driver and approve the device\n"
            "   - Check Device Manager for any 'Unknown Device' entries\n"
            "4. Monitor issues:\n"
            "   - Check dock's video output limits (some only support 1 external monitor)\n"
            "   - USB-C docks may support fewer monitors than Thunderbolt docks\n"
            "   - Resolution/refresh rate may be limited through dock\n"
            "5. USB devices:\n"
            "   - Try connecting USB device directly to laptop (bypass dock)\n"
            "   - If works directly: Dock USB hub may have power or bandwidth issue\n"
            "   - Avoid using high-bandwidth devices through dock USB hubs\n"
            "6. Ethernet:\n"
            "   - Dock ethernet adapter needs drivers (usually auto-install)\n"
            "   - Check Device Manager > Network Adapters for dock NIC\n"
            "   - Some docks have Realtek or ASIX NIC requiring specific drivers\n"
            "7. Reset dock: Disconnect power and laptop cable for 30 seconds, reconnect power first then laptop"
        ),
    },
    {
        "category": "Hardware",
        "problem_title": "Laptop lid close action not working correctly",
        "problem_description": "Laptop doesn't sleep, hibernate, or stay on when the lid is closed as configured. May sleep at wrong times or not wake when reopened.",
        "problem_keywords": "lid close, laptop lid, close lid, sleep on close, hibernate lid, lid action, laptop wake",
        "solution_steps": (
            "1. Configure lid close action:\n"
            "   - Control Panel > Power Options > Choose what closing the lid does\n"
            "   - Set for both 'On battery' and 'Plugged in'\n"
            "   - Options: Do nothing, Sleep, Hibernate, Shut down\n"
            "2. If laptop sleeps when it shouldn't:\n"
            "   - Set lid close action to 'Do nothing'\n"
            "   - Also check: Power Options > Change plan settings > Advanced\n"
            "   - Look for 'Display' > 'Turn off display on lid close'\n"
            "3. External monitor clamshell mode:\n"
            "   - To use laptop with lid closed and external monitor:\n"
            "   - Set lid close action to 'Do nothing'\n"
            "   - Must have external keyboard and mouse connected\n"
            "   - Connect external monitor before closing lid\n"
            "4. Won't wake when lid opens:\n"
            "   - Check: Power Options > Change plan settings > Advanced\n"
            "   - Power buttons and lid > Lid open action\n"
            "   - Update chipset and ACPI drivers\n"
            "5. Lid switch:\n"
            "   - The lid has a magnetic sensor that detects open/close\n"
            "   - If malfunctioning: May falsely trigger sleep\n"
            "   - Check if a magnet (case, phone) near the laptop triggers it\n"
            "6. BIOS: Some laptops have lid-related ACPI settings in BIOS\n"
            "7. Group Policy: In domain environments, power settings may be enforced"
        ),
    },
    {
        "category": "Hardware",
        "problem_title": "Hard drive clicking sound or unusual noises",
        "problem_description": "Hard drive is making clicking, grinding, or buzzing noises. Drive may still be working or may be failing to read/write data.",
        "problem_keywords": "hdd clicking, hard drive noise, grinding sound, click of death, drive clicking, hard drive dying, hdd sound",
        "solution_steps": (
            "1. Identify the sound:\n"
            "   - Clicking (repetitive): Head crash or failing read/write heads\n"
            "   - Grinding: Physical contact between heads and platter\n"
            "   - Buzzing/whining: Motor issue or normal spindle noise\n"
            "   - Single click on power up: Normal\n"
            "2. Check SMART status immediately:\n"
            "   - Download CrystalDiskInfo (free)\n"
            "   - Check for 'Caution' or 'Bad' health status\n"
            "   - Critical attributes: Reallocated Sectors, Current Pending, Uncorrectable\n"
            "3. BACK UP DATA NOW:\n"
            "   - If clicking is repetitive, the drive may fail at any moment\n"
            "   - Copy the most important data first\n"
            "   - Use robocopy /MIR for quick backup\n"
            "   - Don't defragment a failing drive\n"
            "4. Power supply issue:\n"
            "   - Insufficient power can cause clicking in HDDs\n"
            "   - Try a different SATA power cable\n"
            "   - Check if too many drives on one power rail\n"
            "5. If drive won't mount:\n"
            "   - Try connecting to a different computer as a secondary drive\n"
            "   - Use a USB-to-SATA adapter\n"
            "   - Professional data recovery may be needed for critical data\n"
            "6. For SSDs:\n"
            "   - SSDs are silent - clicking usually comes from another component\n"
            "   - Check fans, other HDDs, or the PSU\n"
            "7. Replace the drive: If SMART shows bad health, replace immediately"
        ),
    },
    {
        "category": "Hardware",
        "problem_title": "USB hub or USB devices not getting enough power",
        "problem_description": "USB devices connected through a hub keep disconnecting or don't work at all. External drives may fail to spin up.",
        "problem_keywords": "usb power, usb hub, power surge, usb disconnect, usb drive, not enough power, powered hub",
        "solution_steps": (
            "1. USB power limits:\n"
            "   - USB 2.0 port: 500mA max (0.5A)\n"
            "   - USB 3.0 port: 900mA max (0.9A)\n"
            "   - Unpowered hubs share the host port's power budget\n"
            "   - External HDDs may need 500-900mA each\n"
            "2. Symptoms of insufficient power:\n"
            "   - 'USB Device Not Recognized' or 'Power Surge on Hub Port'\n"
            "   - Devices disconnect intermittently\n"
            "   - External drives make clicking sounds\n"
            "3. Solution: Use a powered USB hub:\n"
            "   - Get a USB hub with its own power adapter\n"
            "   - Each port can then deliver full power\n"
            "   - Connect power-hungry devices to the powered hub\n"
            "4. Connect directly to PC:\n"
            "   - Bypass the hub for devices needing more power\n"
            "   - Use rear USB ports (directly on motherboard) for better power\n"
            "   - Front panel ports often have weaker power delivery\n"
            "5. Check USB power settings:\n"
            "   - Device Manager > Universal Serial Bus controllers > USB Root Hub\n"
            "   - Properties > Power tab > shows power usage per device\n"
            "   - Power Management tab > uncheck 'Allow the computer to turn off'\n"
            "6. For external drives:\n"
            "   - Use the Y-cable (dual USB connectors) if provided\n"
            "   - Or use a drive with its own power adapter\n"
            "7. USB-C/Thunderbolt: Can deliver up to 15W (3A at 5V) per port"
        ),
    },
    {
        "category": "Hardware",
        "problem_title": "CPU fan running at full speed constantly",
        "problem_description": "Computer fan runs at maximum speed and is very loud even when the system is idle. Fan speed doesn't adjust based on temperature.",
        "problem_keywords": "fan loud, cpu fan, fan full speed, noisy fan, fan control, fan always on, fan speed",
        "solution_steps": (
            "1. Check CPU temperature:\n"
            "   - Download HWMonitor, Core Temp, or HWiNFO\n"
            "   - Idle temps should be 30-50°C\n"
            "   - If temps are high: Fan is running fast for a reason (see overheating)\n"
            "2. Clean the fan and heatsink:\n"
            "   - Dust buildup reduces cooling efficiency\n"
            "   - Power off > open case > use compressed air\n"
            "   - Clean the heatsink fins where dust accumulates\n"
            "3. BIOS fan control:\n"
            "   - Enter BIOS > Hardware Monitor or Fan Control section\n"
            "   - Set fan mode to 'Auto' or 'Smart Fan' (not 'Full Speed')\n"
            "   - Adjust the fan curve: lower RPM at lower temps\n"
            "4. Windows fan control:\n"
            "   - SpeedFan (software) can control some fans\n"
            "   - Manufacturer tools: Dell Command, Lenovo Vantage, HP OMEN\n"
            "5. Fan header:\n"
            "   - CPU fans should be connected to the CPU_FAN header (4-pin PWM)\n"
            "   - If connected to a case fan header: May not have speed control\n"
            "   - 3-pin fans use voltage control (less precise)\n"
            "6. Check for high CPU usage:\n"
            "   - Task Manager > CPU usage while idle\n"
            "   - Background processes, malware, or updates may cause high CPU\n"
            "7. Replace thermal paste: If temps are high after cleaning, reapply thermal paste"
        ),
    },
    {
        "category": "Hardware",
        "problem_title": "Laptop touchpad not responding or erratic behavior",
        "problem_description": "Laptop touchpad doesn't work at all or the cursor jumps around erratically. Gestures like two-finger scroll may have stopped working.",
        "problem_keywords": "touchpad, trackpad, cursor jumping, touchpad not working, touchpad disabled, gestures, synaptics",
        "solution_steps": (
            "1. Check if touchpad is disabled:\n"
            "   - Function key toggle: Fn+F6/F7/F8 (varies by manufacturer)\n"
            "   - Look for a touchpad icon on the function keys\n"
            "   - Some laptops have a physical switch or double-tap corner to toggle\n"
            "2. Windows settings:\n"
            "   - Settings > Devices > Touchpad\n"
            "   - Ensure 'Touchpad' toggle is On\n"
            "   - Check: 'Leave touchpad on when a mouse is connected'\n"
            "   - If you have a USB mouse plugged in, touchpad may be auto-disabled\n"
            "3. Update touchpad driver:\n"
            "   - Device Manager > Mice and other pointing devices\n"
            "   - Or: Human Interface Devices > check for touchpad entry\n"
            "   - Update or download from laptop manufacturer (Synaptics, ELAN, Precision)\n"
            "4. Erratic cursor/jumping:\n"
            "   - Clean the touchpad surface (oils and moisture affect it)\n"
            "   - Adjust touchpad sensitivity: Settings > Devices > Touchpad > Sensitivity\n"
            "   - Check: Palm rejection should be enabled\n"
            "5. Gestures not working:\n"
            "   - Settings > Devices > Touchpad > scroll down to gestures\n"
            "   - Configure Three-finger and Four-finger gestures\n"
            "   - Precision touchpad drivers required for all gestures\n"
            "6. Reinstall driver:\n"
            "   - Device Manager > Uninstall touchpad device\n"
            "   - Check 'Delete the driver software'\n"
            "   - Restart to auto-install, or install manufacturer driver\n"
            "7. BIOS: Some BIOS settings can disable the touchpad - check Advanced or Input"
        ),
    },
    {
        "category": "Hardware",
        "problem_title": "Network card (NIC) failing or dropping link",
        "problem_description": "Built-in network card loses link intermittently, shows errors, or the NIC is not detected at all. May work after restart but fails again.",
        "problem_keywords": "nic failing, network card, ethernet card, nic error, link down, network adapter hardware, nic not detected",
        "solution_steps": (
            "1. Check adapter status:\n"
            "   - Device Manager > Network adapters\n"
            "   - Yellow exclamation: Driver issue or hardware error\n"
            "   - Red X: Disabled (right-click > Enable)\n"
            "   - Missing: Hardware not detected\n"
            "2. Check link LED:\n"
            "   - Ethernet port should have link light (green or amber)\n"
            "   - No light: Cable, port, or NIC hardware failure\n"
            "   - Flashing: Normal activity\n"
            "3. Driver update:\n"
            "   - Download latest NIC driver from motherboard/laptop manufacturer\n"
            "   - Intel, Realtek, or Broadcom depending on the NIC\n"
            "   - Completely uninstall old driver, install new one\n"
            "4. Check Event Viewer:\n"
            "   - System > errors from 'e1express', 'e1iexpress', or 'Netwtw'\n"
            "   - Link up/down messages indicate physical or hardware issue\n"
            "   - Repeated errors suggest failing NIC\n"
            "5. Reset NIC:\n"
            "   - Device Manager > NIC > Uninstall device > Restart\n"
            "   - Or: netsh interface set interface 'Ethernet' admin=disable\n"
            "   - Then: netsh interface set interface 'Ethernet' admin=enable\n"
            "6. If built-in NIC is dead:\n"
            "   - USB Ethernet adapter as a workaround\n"
            "   - PCIe network card replacement (desktops)\n"
            "   - Check warranty for replacement\n"
            "7. Test with Linux live USB: If NIC works in Linux, it's a driver issue in Windows"
        ),
    },
    {
        "category": "Hardware",
        "problem_title": "Computer beep codes at startup",
        "problem_description": "Computer beeps during startup and doesn't boot. Beep codes (short and long beeps) indicate hardware issues detected by POST (Power-On Self Test).",
        "problem_keywords": "beep code, post beep, startup beep, no boot beep, bios beep, motherboard beep, post error",
        "solution_steps": (
            "1. Count the beep pattern:\n"
            "   - Note: number of beeps, short vs long, and pauses\n"
            "   - Pattern varies by BIOS manufacturer (AMI, Award, Phoenix, Dell, HP)\n"
            "2. Common AMI BIOS beep codes:\n"
            "   - 1 short: Normal POST (all good)\n"
            "   - 2 short: Memory (RAM) error\n"
            "   - 3 short: Memory test failed\n"
            "   - 5 short: CPU error\n"
            "   - Continuous short: Power supply or motherboard issue\n"
            "3. Common Dell beep codes:\n"
            "   - 1-3-2 (1 beep, 3 beeps, 2 beeps): Memory failure\n"
            "   - 1-3-3: Motherboard chipset error\n"
            "   - Varies by model - look up specific Dell model\n"
            "4. For RAM errors (most common):\n"
            "   - Power off, unplug\n"
            "   - Reseat RAM sticks (remove and firmly reinsert)\n"
            "   - Try one stick at a time in the first slot\n"
            "   - Clean contacts with an eraser if necessary\n"
            "5. For GPU errors:\n"
            "   - Reseat the graphics card\n"
            "   - Ensure power cables to GPU are connected\n"
            "   - Try the integrated GPU (remove discrete card)\n"
            "6. No beep at all (and no display):\n"
            "   - Check if PC speaker/buzzer is connected to motherboard\n"
            "   - PSU may not be powering the board\n"
            "   - Try paper clip test on PSU (if experienced)\n"
            "7. Look up the specific beep code for your BIOS/manufacturer online"
        ),
    },
    {
        "category": "Hardware",
        "problem_title": "Laptop not charging or charge stops at certain percentage",
        "problem_description": "Laptop battery doesn't charge, charges very slowly, or stops charging at a percentage below 100%. Charger may or may not be detected.",
        "problem_keywords": "not charging, battery, charge stops, slow charge, charger not detected, plugged in not charging, battery limit",
        "solution_steps": (
            "1. Check basic connections:\n"
            "   - Verify charger is fully plugged in at both ends\n"
            "   - Check the charging LED on the laptop\n"
            "   - Try a different outlet\n"
            "2. Battery health check:\n"
            "   - powercfg /batteryreport (generates a battery health report)\n"
            "   - Open the HTML report and check 'Design Capacity' vs 'Full Charge Capacity'\n"
            "   - If Full Charge < 50% of Design: Battery needs replacement\n"
            "3. Charge limit feature:\n"
            "   - Many laptops limit charging to 80% for battery longevity\n"
            "   - Lenovo Vantage > Battery > Conservation Mode\n"
            "   - Dell > BIOS > Power > Primary Battery Charge Configuration\n"
            "   - ASUS > MyASUS > Battery Health Charging\n"
            "4. Wrong charger wattage:\n"
            "   - Using a lower wattage charger than required\n"
            "   - USB-C chargers must deliver enough watts for the laptop\n"
            "   - Check laptop requirements vs charger output\n"
            "5. Reset battery:\n"
            "   - For removable batteries: Remove battery, hold power 30 seconds, reinsert\n"
            "   - For internal batteries: Power off, hold power button 15 seconds\n"
            "6. Driver reset:\n"
            "   - Device Manager > Batteries > 'Microsoft ACPI-Compliant Control Method Battery'\n"
            "   - Uninstall > Restart > Windows reinstalls it\n"
            "7. BIOS update: Some charging issues are fixed by BIOS updates"
        ),
    },
    {
        "category": "Hardware",
        "problem_title": "Thunderbolt or USB-C device not recognized",
        "problem_description": "Thunderbolt dock, eGPU, or USB-C device not recognized or not working when connected. May charge but not transfer data.",
        "problem_keywords": "thunderbolt, usb-c, usb c, dock not working, egpu, thunderbolt device, usb-c not working, type-c",
        "solution_steps": (
            "1. Check port capability:\n"
            "   - Not all USB-C ports support Thunderbolt\n"
            "   - Not all USB-C ports support video (DP Alt Mode)\n"
            "   - Check laptop specs for port capabilities\n"
            "   - Thunderbolt port has a lightning bolt icon\n"
            "2. Approve the device:\n"
            "   - Thunderbolt devices may require approval\n"
            "   - Thunderbolt Control Center (Intel) > Approve new device\n"
            "   - Settings > Thunderbolt > Approve device\n"
            "3. Update Thunderbolt drivers:\n"
            "   - Download from Intel or laptop manufacturer\n"
            "   - Also update NVM firmware for Thunderbolt controller\n"
            "   - Device Manager > System devices > Thunderbolt Controller\n"
            "4. Cable quality:\n"
            "   - Not all USB-C cables support Thunderbolt/USB4\n"
            "   - Use the cable that came with the device\n"
            "   - Active cables may be required for longer runs\n"
            "   - USB 2.0 cables won't support USB 3.x speeds\n"
            "5. Power delivery:\n"
            "   - If the device charges but no data: Cable may be charge-only\n"
            "   - eGPU requires significant power delivery\n"
            "6. BIOS settings:\n"
            "   - Some BIOSes have Thunderbolt security levels\n"
            "   - Set to 'User Authorization' or 'No Security' for automatic connection\n"
            "7. Firmware: Update dock/device firmware from the manufacturer"
        ),
    },
    {
        "category": "Hardware",
        "problem_title": "Projector or conference room display connection issues",
        "problem_description": "Laptop won't display on projector or conference room TV. HDMI/VGA/wireless connection established but no image appears or resolution is wrong.",
        "problem_keywords": "projector, conference room, presentation, hdmi projector, display connect, vga, wireless display, miracast",
        "solution_steps": (
            "1. Check input source:\n"
            "   - Projector/TV must be set to the correct input (HDMI 1, VGA, etc.)\n"
            "   - Use the projector's remote or buttons to change input\n"
            "2. Switch display mode:\n"
            "   - Win+P > select Duplicate, Extend, or Second screen only\n"
            "   - Try each option\n"
            "   - Default is 'PC screen only' which won't send to projector\n"
            "3. Cable/adapter check:\n"
            "   - Try a different HDMI/VGA cable\n"
            "   - For USB-C to HDMI: Ensure adapter supports your resolution\n"
            "   - VGA is analog - use HDMI/DP when possible for better quality\n"
            "4. Resolution issues:\n"
            "   - The projector may not support your laptop's default resolution\n"
            "   - Temporarily lower resolution: Settings > Display > Resolution\n"
            "   - Most projectors: Optimal at 1920x1080 or 1280x720\n"
            "5. Wireless display (Miracast):\n"
            "   - Win+K to connect to wireless display\n"
            "   - Both devices must support Miracast\n"
            "   - Must be on the same network (or using Wi-Fi Direct)\n"
            "6. Update display driver:\n"
            "   - Old GPU drivers may not support certain resolutions or connections\n"
            "   - Update from NVIDIA/AMD/Intel\n"
            "7. Presentation timer: Use Presenter View in PowerPoint for notes on laptop screen"
        ),
    },
    {
        "category": "Hardware",
        "problem_title": "Keyboard keys stuck or registering wrong characters",
        "problem_description": "Keyboard types wrong characters, keys repeat uncontrollably, or specific keys are stuck. May be physical or software issue.",
        "problem_keywords": "wrong characters, key stuck, keyboard wrong, key repeat, sticky keys, keyboard input, key mapping",
        "solution_steps": (
            "1. Check keyboard layout:\n"
            "   - Settings > Time & Language > Language\n"
            "   - Verify the correct keyboard layout is selected (e.g., US QWERTY)\n"
            "   - Win+Space toggles between installed keyboard layouts\n"
            "   - Remove extra layouts that could accidentally activate\n"
            "2. Physically stuck keys:\n"
            "   - Turn keyboard upside down and gently shake\n"
            "   - Use compressed air to blow out debris\n"
            "   - For laptops: Carefully pry up the key cap and clean underneath\n"
            "3. Disable Filter Keys and Sticky Keys:\n"
            "   - Settings > Accessibility > Keyboard\n"
            "   - Turn off 'Sticky Keys' and 'Filter Keys'\n"
            "   - Filter Keys can cause keys to appear stuck or ignored\n"
            "4. Key repeat settings:\n"
            "   - Control Panel > Keyboard > Speed tab\n"
            "   - Adjust 'Repeat delay' (longer) and 'Repeat rate' (slower)\n"
            "5. Driver reset:\n"
            "   - Device Manager > Keyboards > Uninstall device\n"
            "   - Restart to reinstall\n"
            "   - For USB keyboards: Try a different USB port\n"
            "6. Liquid damage:\n"
            "   - If liquid was spilled: Power off immediately\n"
            "   - Flip upside down, let dry 24-48 hours\n"
            "   - Individual keys may need replacement\n"
            "7. Test with on-screen keyboard: Settings > Accessibility > Keyboard > On-Screen Keyboard"
        ),
    },
    {
        "category": "Hardware",
        "problem_title": "Multiple monitors different refresh rates or tearing",
        "problem_description": "Multi-monitor setup has screen tearing, stuttering, or one monitor runs at the wrong refresh rate. Mixed refresh rate monitors cause issues.",
        "problem_keywords": "refresh rate, screen tearing, multi monitor, vsync, freesync, g-sync, 144hz, mixed refresh",
        "solution_steps": (
            "1. Check current refresh rates:\n"
            "   - Settings > System > Display > Advanced display settings\n"
            "   - Select each monitor and check the refresh rate\n"
            "   - Set each to its maximum supported rate\n"
            "2. Set refresh rate properly:\n"
            "   - Right-click desktop > Display settings > Advanced display > Refresh rate dropdown\n"
            "   - If the desired rate isn't listed: Update GPU driver\n"
            "   - Check cable: HDMI 2.0+ or DP 1.2+ for higher refresh rates\n"
            "3. Mixed refresh rates:\n"
            "   - Running 60Hz and 144Hz monitors together can cause stuttering\n"
            "   - This is a known issue with Windows compositor\n"
            "   - Workaround: Set all monitors to the same refresh rate if possible\n"
            "   - Or: Use 'Hardware-accelerated GPU scheduling' (Settings > Display > Graphics)\n"
            "4. Screen tearing:\n"
            "   - Enable VSync in game/application settings\n"
            "   - Use FreeSync (AMD) or G-Sync (NVIDIA) if monitor supports it\n"
            "   - NVIDIA Control Panel > Manage 3D settings > V-Sync\n"
            "5. GPU driver settings:\n"
            "   - NVIDIA: NVIDIA Control Panel > Change Resolution > select correct for each\n"
            "   - AMD: AMD Adrenalin > Display > per-monitor settings\n"
            "6. Restart GPU driver: Win+Ctrl+Shift+B (screen flashes, resets driver)\n"
            "7. Cable requirement: 4K@60Hz needs HDMI 2.0 or DP 1.2, 4K@120Hz needs HDMI 2.1 or DP 1.4"
        ),
    },
    {
        "category": "Hardware",
        "problem_title": "Printer paper jam that keeps recurring",
        "problem_description": "Printer jams paper repeatedly in the same area. Clearing the jam temporarily fixes it but it jams again within a few pages.",
        "problem_keywords": "paper jam, recurring jam, printer jam, paper stuck, feed roller, pickup roller, jam error",
        "solution_steps": (
            "1. Clear the current jam completely:\n"
            "   - Open all doors/covers indicated by the printer\n"
            "   - Pull paper gently in the direction of paper travel\n"
            "   - Check for small torn pieces left behind\n"
            "   - Close all covers firmly\n"
            "2. Check paper quality:\n"
            "   - Use recommended paper weight (75-90 gsm for most printers)\n"
            "   - Don't use damp, wrinkled, or curled paper\n"
            "   - Fan the paper stack before loading (separates sheets)\n"
            "   - Don't overfill the paper tray\n"
            "3. Clean pickup rollers:\n"
            "   - Open the tray and locate the rubber pickup rollers\n"
            "   - Clean with a lint-free cloth dampened with water\n"
            "   - Worn/shiny rollers need replacement\n"
            "4. Check paper guides:\n"
            "   - Tray paper guides should snugly fit the paper size\n"
            "   - Too loose: Paper feeds at an angle\n"
            "   - Too tight: Paper can't feed at all\n"
            "5. Duplex unit:\n"
            "   - If jams occur during double-sided printing\n"
            "   - Remove and clean the duplex unit\n"
            "   - Some paper types don't work well with duplex\n"
            "6. Fuser area:\n"
            "   - Jams near the output: Fuser may be worn\n"
            "   - Fuser kits have a page life (e.g., 200K pages)\n"
            "   - Professional replacement may be needed\n"
            "7. Firmware update: Check manufacturer website for printer firmware"
        ),
    },
    {
        "category": "Hardware",
        "problem_title": "Desktop PC won't power on at all",
        "problem_description": "Pressing the power button does nothing. No fans spin, no LEDs light up, and no display output. Complete absence of any power signs.",
        "problem_keywords": "won't turn on, no power, dead pc, power button, no response, pc dead, won't start, no lights",
        "solution_steps": (
            "1. Check power source:\n"
            "   - Verify the outlet works (plug in a phone charger or lamp)\n"
            "   - Check power strip/surge protector is on\n"
            "   - Verify the power cable is firmly seated at both ends\n"
            "2. PSU switch:\n"
            "   - Check the power supply switch on the back (I = On, O = Off)\n"
            "   - Some PSUs have a voltage selector (ensure it matches your country)\n"
            "   - Try toggling the PSU switch off/on\n"
            "3. Power button test:\n"
            "   - The front panel power button may be disconnected\n"
            "   - Open the case and locate the motherboard power header pins\n"
            "   - Briefly touch the two PWR_SW pins with a screwdriver to jump-start\n"
            "   - If it starts: Power button or front panel cable is faulty\n"
            "4. PSU test:\n"
            "   - Disconnect all cables from motherboard\n"
            "   - Paperclip test: Short the green wire to any black wire on the 24-pin\n"
            "   - If PSU fan doesn't spin: PSU is dead, replace it\n"
            "5. Minimal boot test:\n"
            "   - Disconnect everything except: CPU, 1 stick of RAM, CPU cooler, power\n"
            "   - Try to power on\n"
            "   - Add components back one by one to find the short\n"
            "6. Check for shorts:\n"
            "   - Loose standoff behind motherboard can short\n"
            "   - Stray screws or metal objects in the case\n"
            "7. Motherboard LED: Many motherboards have a standby LED - if it's not lit, power isn't reaching the board"
        ),
    },
    {
        "category": "Hardware",
        "problem_title": "Laptop trackpad gestures or sensitivity not working",
        "problem_description": "Laptop touchpad gestures (two-finger scroll, pinch zoom, three-finger swipe) not working, touchpad too sensitive or not sensitive enough, or touchpad stops working after driver update.",
        "problem_keywords": "trackpad, touchpad, gesture, touchpad sensitivity, two finger scroll, touchpad not working, precision touchpad, synaptics",
        "solution_steps": (
            "1. Check touchpad settings:\n"
            "   - Settings > Bluetooth & Devices > Touchpad\n"
            "   - Ensure touchpad is enabled\n"
            "   - Check: 'Leave touchpad on when a mouse is connected'\n"
            "2. Gestures configuration:\n"
            "   - Precision touchpad: Settings > Touchpad > scroll, tap, gestures\n"
            "   - Three-finger gestures: Swipe, tap actions configurable\n"
            "   - Four-finger gestures available on supported hardware\n"
            "3. Sensitivity adjustment:\n"
            "   - Settings > Touchpad > Touchpad sensitivity\n"
            "   - Options: Most sensitive, High, Medium, Low\n"
            "   - Palm detection: Helps prevent accidental touches while typing\n"
            "4. Driver issues:\n"
            "   - Device Manager > Mice and other pointing devices\n"
            "   - Update or roll back touchpad driver\n"
            "   - Precision Touchpad driver vs Synaptics/ELAN driver\n"
            "   - Download latest from laptop manufacturer's site\n"
            "5. Function key: Many laptops have Fn+F-key to enable/disable touchpad (look for touchpad icon on function keys)"
        ),
    },
    {
        "category": "Hardware",
        "problem_title": "USB devices frequently disconnecting and reconnecting",
        "problem_description": "USB devices keep disconnecting and reconnecting with the Windows notification sound. Affects mice, keyboards, drives, or other USB peripherals. May show 'USB device not recognized' intermittently.",
        "problem_keywords": "usb disconnect, usb reconnect, usb dropped, usb intermittent, usb not recognized, usb power, usb hub disconnect",
        "solution_steps": (
            "1. USB power management:\n"
            "   - Device Manager > Universal Serial Bus controllers\n"
            "   - Each USB Root Hub > Properties > Power Management\n"
            "   - Uncheck 'Allow the computer to turn off this device to save power'\n"
            "2. USB Selective Suspend:\n"
            "   - Control Panel > Power Options > Change plan settings > Advanced\n"
            "   - USB settings > USB selective suspend setting > Disabled\n"
            "3. Physical checks:\n"
            "   - Try different USB port (front vs back)\n"
            "   - Try without USB hub (direct to PC)\n"
            "   - Check cable for damage\n"
            "   - Clean USB ports with compressed air\n"
            "4. USB hub power:\n"
            "   - Unpowered hubs can't supply enough current\n"
            "   - Use powered USB hub for power-hungry devices\n"
            "   - Don't daisy-chain hubs\n"
            "5. Driver fix: Uninstall all USB controllers in Device Manager, reboot (Windows reinstalls them automatically)"
        ),
    },
    {
        "category": "Hardware",
        "problem_title": "Desktop or laptop fan running constantly at high speed",
        "problem_description": "Computer fans running at full speed constantly, creating excessive noise. May indicate overheating, dust buildup, failed thermal management, or BIOS fan control issues.",
        "problem_keywords": "fan noise, fan speed, loud fan, fan running, overheating fan, fan control, cpu fan, thermal",
        "solution_steps": (
            "1. Check temperatures:\n"
            "   - Task Manager: Performance tab shows CPU temperature (Win11)\n"
            "   - HWMonitor or Core Temp for detailed temps\n"
            "   - CPU normal: 30-50C idle, 60-80C load\n"
            "   - If >90C: Overheating problem\n"
            "2. High CPU usage:\n"
            "   - Task Manager: Check for processes using high CPU\n"
            "   - Common: Windows Update, antivirus scan, malware\n"
            "   - Fix the CPU issue and fans will quiet down\n"
            "3. Dust cleaning:\n"
            "   - Power off and unplug\n"
            "   - Use compressed air to blow out vents and fans\n"
            "   - Laptops: Clean intake and exhaust vents\n"
            "   - Desktop: Open case, clean CPU heatsink and case fans\n"
            "4. Thermal paste:\n"
            "   - If cleaning doesn't help, thermal paste may need replacing\n"
            "   - Desktop: Remove CPU cooler, clean old paste, apply new\n"
            "   - Laptop: More complex, may need professional service\n"
            "5. BIOS fan settings: Check BIOS for fan curve settings, reset to defaults if custom settings were changed"
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
