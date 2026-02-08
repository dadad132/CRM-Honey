"""
Bubbles AI Enhancement Module
Advanced features for the Bubbles support assistant
"""
import re
import json
import random
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any

# ============================================================================
# FRUSTRATION DETECTION
# ============================================================================

FRUSTRATION_INDICATORS = {
    # High frustration (level 4-5)
    'high': {
        'patterns': [
            r'!!!+',  # Multiple exclamation marks
            r'\?\?\?+',  # Multiple question marks
            r'HELP+',  # Caps HELP
            r'PLEASE+',  # Caps PLEASE
            r'NOT WORKING',  # Caps complaints
            r'STILL (NOT|DOESN\'T|WON\'T|CANT)',  # Still broken
        ],
        'words': [
            'frustrated', 'frustrating', 'annoyed', 'annoying', 'angry', 'furious',
            'ridiculous', 'unacceptable', 'terrible', 'horrible', 'awful', 'useless',
            'waste of time', 'give up', 'giving up', 'had enough', 'sick of',
            'fed up', 'done with', 'hate this', 'hate it', 'so annoying',
            'nothing works', 'never works', 'always broken', 'piece of junk',
            'stupid', 'dumb', 'idiotic'
        ],
        'level': 5
    },
    # Medium frustration (level 2-3)
    'medium': {
        'patterns': [
            r'still (not|doesn\'t|won\'t|cant)',  # Still having issues
            r'tried everything',
            r'nothing (works|helps)',
            r'already tried',
            r'again and again',
        ],
        'words': [
            'confused', 'confusing', 'difficult', 'struggling', 'stuck',
            'problem', 'issue', 'trouble', 'keeps happening', 'again',
            'still', 'yet', 'same issue', 'same problem', 'not again',
            'come on', 'seriously', 'really', 'ugh', 'argh', 'sigh'
        ],
        'level': 3
    },
    # Low frustration (level 1)
    'low': {
        'patterns': [
            r'help',
            r'can\'t figure',
            r'don\'t understand',
        ],
        'words': [
            'help', 'please', 'need', 'want', 'trying', 'attempted'
        ],
        'level': 1
    }
}

EMPATHY_RESPONSES = {
    5: [  # High frustration
        "I can tell this has been really frustrating - and I'm truly sorry you're going through this. 💜 Let me try my absolute best to help you right now.",
        "I hear you, and I'm so sorry this has been such a struggle. 😔 You shouldn't have to deal with this. Let me see what I can do to make this better.",
        "I completely understand your frustration - technology issues are the worst! 🫧 I'm here for you, and let's work through this together step by step.",
        "Oh no, I can see this has been really difficult. 😟 Please know I'm taking this seriously and I want to help resolve this for you right away.",
        "I'm really sorry you're having such a hard time with this. 💔 Let's take a breath and tackle this together - I won't give up until we find a solution!",
    ],
    4: [
        "I can see this is frustrating - let me help! 💜 I'll do my best to find a solution for you.",
        "I understand how annoying this must be. 🫧 Let's work through this together.",
        "I'm sorry you're dealing with this! Let me see what I can do to help. 💪",
        "That does sound frustrating. 😊 I'm here to help - let's figure this out!",
    ],
    3: [
        "I understand - let me help you with that! 🫧",
        "No worries, let's figure this out together! 💜",
        "I'm here to help! Let's see what we can do. 😊",
        "I've got you - let's work through this! 🌟",
    ],
    2: [
        "Let me help you with that! 🫧",
        "I can definitely help with this! 💜",
        "No problem - I'm here to assist! 😊",
    ],
    1: [
        "Sure, I can help! 🫧",
        "Let me look into that for you! 💜",
        "I'd be happy to help! 😊",
    ]
}


def detect_frustration(message: str) -> Dict[str, Any]:
    """Detect user frustration level from message"""
    message_lower = message.lower()
    message_upper = message  # Keep original for caps detection
    
    detected_level = 0
    indicators_found = []
    
    # Check for ALL CAPS (more than 50% caps in a message over 10 chars)
    if len(message) > 10:
        caps_ratio = sum(1 for c in message if c.isupper()) / len(message.replace(' ', ''))
        if caps_ratio > 0.5:
            detected_level = max(detected_level, 4)
            indicators_found.append('ALL_CAPS')
    
    # Check each frustration level
    for level_name, level_data in FRUSTRATION_INDICATORS.items():
        # Check patterns
        for pattern in level_data['patterns']:
            if re.search(pattern, message_upper if level_name == 'high' else message_lower, re.IGNORECASE):
                detected_level = max(detected_level, level_data['level'])
                indicators_found.append(f"pattern:{pattern}")
        
        # Check words
        for word in level_data['words']:
            if word in message_lower:
                detected_level = max(detected_level, level_data['level'])
                indicators_found.append(f"word:{word}")
    
    # Get appropriate empathy response
    empathy_response = None
    if detected_level >= 3:
        empathy_response = random.choice(EMPATHY_RESPONSES.get(detected_level, EMPATHY_RESPONSES[3]))
    
    return {
        'level': detected_level,
        'indicators': indicators_found[:5],  # Limit to 5
        'empathy_response': empathy_response,
        'should_escalate': detected_level >= 5
    }


# ============================================================================
# INTERACTIVE TROUBLESHOOTING FLOWS
# ============================================================================

TROUBLESHOOTING_FLOWS = {
    'printer': {
        'name': 'Printer Troubleshooting',
        'start_question': "Let's troubleshoot your printer step by step! 🖨️\n\nFirst, is your printer **powered on** with lights showing?",
        'quick_replies': [
            {'text': '✅ Yes, lights are on', 'value': 'printer_on', 'next': 'printer_on'},
            {'text': '❌ No lights at all', 'value': 'printer_off', 'next': 'printer_power'},
            {'text': '⚠️ Error light is on', 'value': 'printer_error', 'next': 'printer_error_check'}
        ],
        'steps': {
            'printer_on': {
                'message': "Good! The printer has power. 👍\n\nIs the printer showing **\"Offline\"** on your computer?",
                'quick_replies': [
                    {'text': '✅ Yes, shows Offline', 'value': 'yes', 'next': 'printer_offline'},
                    {'text': '❌ No, shows Ready', 'value': 'no', 'next': 'printer_ready'},
                    {'text': '❓ Not sure how to check', 'value': 'unsure', 'next': 'printer_check_status'}
                ]
            },
            'printer_power': {
                'message': "No lights means no power. Let's check:\n\n1️⃣ Is the power cable **firmly plugged in** at both ends?\n2️⃣ Is the power outlet working? Try plugging in a phone charger to test.\n3️⃣ Is there a power **switch** on the printer?\n\nDid any of these help?",
                'quick_replies': [
                    {'text': '✅ Fixed! It\'s on now', 'value': 'fixed', 'next': 'success'},
                    {'text': '❌ Still no power', 'value': 'no', 'next': 'printer_power_fail'}
                ]
            },
            'printer_error_check': {
                'message': "An error light usually means there's a specific issue. Common causes:\n\n🔴 **Paper jam** - Open all covers and check for stuck paper\n🟠 **Low ink/toner** - Check ink levels\n🟡 **Paper tray empty** - Add paper\n\nWhat does the error seem to be?",
                'quick_replies': [
                    {'text': '📄 Paper jam', 'value': 'jam', 'next': 'paper_jam'},
                    {'text': '🖨️ Out of ink', 'value': 'ink', 'next': 'ink_issue'},
                    {'text': '📋 No paper', 'value': 'paper', 'next': 'paper_empty'},
                    {'text': '❓ Unknown error', 'value': 'unknown', 'next': 'printer_unknown_error'}
                ]
            },
            'printer_offline': {
                'message': "Let's fix the offline status:\n\n1️⃣ Right-click your printer → **See what's printing**\n2️⃣ Click **Printer** menu at top\n3️⃣ **Uncheck** \"Use Printer Offline\"\n4️⃣ Try printing again\n\nDid that work?",
                'quick_replies': [
                    {'text': '✅ Yes, it\'s printing!', 'value': 'yes', 'next': 'success'},
                    {'text': '❌ Still offline', 'value': 'no', 'next': 'printer_restart'},
                    {'text': '❓ Can\'t find that option', 'value': 'help', 'next': 'printer_detailed_steps'}
                ]
            },
            'printer_restart': {
                'message': "Let's try a full restart:\n\n1️⃣ **Turn OFF** the printer\n2️⃣ **Unplug** the power cable\n3️⃣ Wait **30 seconds**\n4️⃣ **Plug back in** and turn ON\n5️⃣ **Restart** your computer too\n\nTry printing now!",
                'quick_replies': [
                    {'text': '✅ Working now!', 'value': 'yes', 'next': 'success'},
                    {'text': '❌ Still not working', 'value': 'no', 'next': 'escalate'}
                ]
            },
            'paper_jam': {
                'message': "⚠️ **IMPORTANT: Turn OFF the printer first!**\n\nThen:\n1️⃣ Open all accessible doors/covers\n2️⃣ Look for paper - check front, back, and sides\n3️⃣ Pull paper **slowly and straight** - don't yank!\n4️⃣ Remove ALL torn pieces\n5️⃣ Close covers and turn printer back on\n\nWas there paper stuck inside?",
                'quick_replies': [
                    {'text': '✅ Found and removed it!', 'value': 'yes', 'next': 'success'},
                    {'text': '❌ No paper found but still says jam', 'value': 'no', 'next': 'hidden_jam'},
                    {'text': '⚠️ Paper is stuck, won\'t come out', 'value': 'stuck', 'next': 'escalate_jam'}
                ]
            },
            'hidden_jam': {
                'message': "Sometimes small pieces hide inside. Try:\n\n1️⃣ Check the **paper tray** - remove all paper and look inside\n2️⃣ Open the **back panel** if your printer has one\n3️⃣ Look near the **ink/toner area**\n4️⃣ Check for a small piece caught on rollers\n\n💡 Even a tiny piece of paper can cause a jam error!",
                'quick_replies': [
                    {'text': '✅ Found it!', 'value': 'yes', 'next': 'success'},
                    {'text': '❌ Still can\'t find anything', 'value': 'no', 'next': 'escalate'}
                ]
            },
            'success': {
                'message': "🎉 **Wonderful!** I'm so glad that worked!\n\nIs there anything else I can help you with today?",
                'quick_replies': [
                    {'text': '🖨️ Another printer issue', 'value': 'printer', 'next': 'restart'},
                    {'text': '💻 Different issue', 'value': 'other', 'next': 'new_issue'},
                    {'text': '👋 No, all good!', 'value': 'done', 'next': 'goodbye'}
                ],
                'is_success': True
            },
            'escalate': {
                'message': "I've tried my best but this might need hands-on help from our tech team. 🔧\n\n**Don't worry!** I'll include all the steps we've tried so they don't have to start from scratch.",
                'quick_replies': [
                    {'text': '🎫 Create Support Ticket', 'value': 'ticket', 'action': 'create_ticket'},
                    {'text': '🔄 Let me try again', 'value': 'retry', 'next': 'restart'}
                ],
                'is_escalation': True
            },
            'escalate_jam': {
                'message': "⚠️ **Don't force it!** Pulling too hard can damage the printer.\n\nOur tech team can safely remove stuck paper. I'll create a ticket with all the details.",
                'quick_replies': [
                    {'text': '🎫 Create Support Ticket', 'value': 'ticket', 'action': 'create_ticket'}
                ],
                'is_escalation': True
            }
        }
    },
    'wifi': {
        'name': 'WiFi Troubleshooting',
        'start_question': "Let's fix your WiFi! 📶\n\nCan you see **any WiFi networks** when you look at available connections?",
        'quick_replies': [
            {'text': '✅ Yes, I see networks', 'value': 'see_networks', 'next': 'wifi_see'},
            {'text': '❌ No networks showing', 'value': 'no_networks', 'next': 'wifi_none'},
            {'text': '⚠️ Connected but no internet', 'value': 'no_internet', 'next': 'wifi_no_internet'}
        ],
        'steps': {
            'wifi_see': {
                'message': "Good! Can you see **your network** in the list? (Your router's name)",
                'quick_replies': [
                    {'text': '✅ Yes, I see my network', 'value': 'yes', 'next': 'wifi_connect'},
                    {'text': '❌ My network isn\'t showing', 'value': 'no', 'next': 'wifi_hidden'}
                ]
            },
            'wifi_none': {
                'message': "No networks at all usually means WiFi is turned off.\n\n**Try these:**\n1️⃣ Look for a WiFi **function key** (F1-F12 with a WiFi icon)\n2️⃣ Check for a physical **WiFi switch** on your laptop\n3️⃣ Click the WiFi icon → toggle **WiFi ON**\n\nDo you see networks now?",
                'quick_replies': [
                    {'text': '✅ Yes! Networks appeared', 'value': 'yes', 'next': 'wifi_see'},
                    {'text': '❌ Still nothing', 'value': 'no', 'next': 'wifi_adapter'}
                ]
            },
            'wifi_no_internet': {
                'message': "Connected but no internet? Let's check:\n\n1️⃣ Can **other devices** connect and use internet?\n2️⃣ Try opening a website (not just apps)",
                'quick_replies': [
                    {'text': '✅ Other devices work fine', 'value': 'others_work', 'next': 'wifi_this_device'},
                    {'text': '❌ Nothing has internet', 'value': 'nothing_works', 'next': 'wifi_router_issue'}
                ]
            },
            'wifi_connect': {
                'message': "Let's reconnect properly:\n\n1️⃣ Click on your network\n2️⃣ Click **Forget** or **Disconnect**\n3️⃣ Reconnect and enter password **carefully**\n\n💡 Passwords are case-sensitive!\n\nDid it connect?",
                'quick_replies': [
                    {'text': '✅ Connected!', 'value': 'yes', 'next': 'success'},
                    {'text': '❌ Wrong password error', 'value': 'password', 'next': 'wifi_password'},
                    {'text': '❌ Just won\'t connect', 'value': 'no', 'next': 'wifi_restart'}
                ]
            },
            'wifi_restart': {
                'message': "**The Magic Reset** (works 80% of the time!):\n\n1️⃣ **Unplug** your router/modem\n2️⃣ Wait **30 seconds** (full 30!)\n3️⃣ **Plug back in**\n4️⃣ Wait **2 minutes** for it to fully restart\n5️⃣ Try connecting again\n\nDid that help?",
                'quick_replies': [
                    {'text': '✅ Yes! It\'s working!', 'value': 'yes', 'next': 'success'},
                    {'text': '❌ Still won\'t connect', 'value': 'no', 'next': 'escalate'}
                ]
            },
            'wifi_router_issue': {
                'message': "If **nothing** has internet, the issue is likely your router or ISP.\n\n**Try this:**\n1️⃣ **Unplug** router AND modem (if separate)\n2️⃣ Wait **1 minute**\n3️⃣ Plug in **modem first**, wait for lights\n4️⃣ Then plug in **router**\n5️⃣ Wait 2-3 minutes\n\nIs internet back on any device?",
                'quick_replies': [
                    {'text': '✅ Yes, internet is back!', 'value': 'yes', 'next': 'success'},
                    {'text': '❌ Still no internet anywhere', 'value': 'no', 'next': 'isp_issue'}
                ]
            },
            'isp_issue': {
                'message': "If nothing works after router restart, it might be:\n\n🔸 **ISP outage** - Check your provider's website or call them\n🔸 **Router failure** - Lights abnormal?\n🔸 **Account issue** - Bill paid?\n\nThis is likely outside my expertise. You may need to contact your internet provider.",
                'quick_replies': [
                    {'text': '📞 I\'ll contact ISP', 'value': 'isp', 'next': 'goodbye'},
                    {'text': '🎫 Create Support Ticket', 'value': 'ticket', 'action': 'create_ticket'}
                ]
            },
            'success': {
                'message': "🎉 **Excellent!** Your WiFi is back in action!\n\nIs there anything else you need help with?",
                'quick_replies': [
                    {'text': '📶 Another WiFi issue', 'value': 'wifi', 'next': 'restart'},
                    {'text': '💻 Different issue', 'value': 'other', 'next': 'new_issue'},
                    {'text': '👋 No thanks!', 'value': 'done', 'next': 'goodbye'}
                ],
                'is_success': True
            },
            'escalate': {
                'message': "This is a tricky one! 🔧 Our tech team should take a look.\n\nI'll include everything we tried so they can pick up where we left off.",
                'quick_replies': [
                    {'text': '🎫 Create Support Ticket', 'value': 'ticket', 'action': 'create_ticket'},
                    {'text': '🔄 Let me try again', 'value': 'retry', 'next': 'restart'}
                ],
                'is_escalation': True
            }
        }
    },
    'email': {
        'name': 'Email Troubleshooting',
        'start_question': "Let's fix your email! 📧\n\nWhat's happening with your email?",
        'quick_replies': [
            {'text': '📤 Can\'t send emails', 'value': 'send', 'next': 'email_send'},
            {'text': '📥 Not receiving emails', 'value': 'receive', 'next': 'email_receive'},
            {'text': '🔐 Can\'t log in', 'value': 'login', 'next': 'email_login'},
            {'text': '🐌 Email is very slow', 'value': 'slow', 'next': 'email_slow'}
        ],
        'steps': {
            'email_send': {
                'message': "Can't send? Let's check:\n\nAre your emails **stuck in the Outbox**?",
                'quick_replies': [
                    {'text': '✅ Yes, stuck in Outbox', 'value': 'yes', 'next': 'email_outbox'},
                    {'text': '❌ Getting an error', 'value': 'error', 'next': 'email_error'},
                    {'text': '❓ Where is Outbox?', 'value': 'help', 'next': 'email_outbox_help'}
                ]
            },
            'email_outbox': {
                'message': "Stuck emails usually mean:\n\n1️⃣ **Large attachment** - over 25MB? Try cloud sharing instead\n2️⃣ **Connection issue** - Are you online?\n3️⃣ **Email stuck** - Delete it and recreate\n\n**Try this:**\n• Open Outbox\n• Delete the stuck email\n• Recreate and send again\n\nDid that work?",
                'quick_replies': [
                    {'text': '✅ Yes, sent!', 'value': 'yes', 'next': 'success'},
                    {'text': '❌ Still won\'t send', 'value': 'no', 'next': 'email_restart'}
                ]
            },
            'email_receive': {
                'message': "Not receiving emails? Let's check:\n\n1️⃣ Check your **Spam/Junk** folder\n2️⃣ Is your **mailbox full**?\n3️⃣ Have someone send a test email now\n\nDid you find anything in Spam?",
                'quick_replies': [
                    {'text': '✅ Found it in Spam!', 'value': 'spam', 'next': 'email_spam'},
                    {'text': '📫 Mailbox is full', 'value': 'full', 'next': 'email_full'},
                    {'text': '❌ Not in Spam either', 'value': 'no', 'next': 'email_not_receiving'}
                ]
            },
            'email_login': {
                'message': "Can't log in? Let's troubleshoot:\n\n1️⃣ Check **Caps Lock** is OFF\n2️⃣ Type password in Notepad first to see it\n3️⃣ Try the **\"Forgot Password\"** link\n\nWhat happens when you try to log in?",
                'quick_replies': [
                    {'text': '🔑 Wrong password error', 'value': 'password', 'next': 'email_password'},
                    {'text': '🔒 Account locked', 'value': 'locked', 'next': 'email_locked'},
                    {'text': '❓ Other error', 'value': 'other', 'next': 'email_login_error'}
                ]
            },
            'email_password': {
                'message': "For password reset:\n\n1️⃣ Go to your email provider's login page\n2️⃣ Click **\"Forgot Password\"**\n3️⃣ Check for reset email (check Spam too!)\n4️⃣ Create a new password\n\n💡 Make it strong: 12+ characters, mix of letters, numbers, symbols!",
                'quick_replies': [
                    {'text': '✅ Reset successful!', 'value': 'yes', 'next': 'success'},
                    {'text': '❌ Can\'t get reset email', 'value': 'no', 'next': 'escalate'}
                ]
            },
            'success': {
                'message': "🎉 **Great!** Your email should be working now!\n\nNeed help with anything else?",
                'quick_replies': [
                    {'text': '📧 Another email issue', 'value': 'email', 'next': 'restart'},
                    {'text': '💻 Different issue', 'value': 'other', 'next': 'new_issue'},
                    {'text': '👋 All set, thanks!', 'value': 'done', 'next': 'goodbye'}
                ],
                'is_success': True
            },
            'escalate': {
                'message': "Email issues can be tricky to diagnose remotely. 📧\n\nLet me connect you with our tech team who can check your settings directly.",
                'quick_replies': [
                    {'text': '🎫 Create Support Ticket', 'value': 'ticket', 'action': 'create_ticket'},
                    {'text': '🔄 Let me try again', 'value': 'retry', 'next': 'restart'}
                ],
                'is_escalation': True
            }
        }
    },
    'slow_computer': {
        'name': 'Slow Computer Troubleshooting',
        'start_question': "Let's speed up your computer! 🚀\n\nIs it slow **all the time** or only when doing certain things?",
        'quick_replies': [
            {'text': '🐢 Always slow', 'value': 'always', 'next': 'always_slow'},
            {'text': '🎯 Slow with specific programs', 'value': 'specific', 'next': 'specific_slow'},
            {'text': '🌐 Only internet is slow', 'value': 'internet', 'next': 'internet_slow'},
            {'text': '🏁 Slow to start up', 'value': 'startup', 'next': 'startup_slow'}
        ],
        'steps': {
            'always_slow': {
                'message': "Have you tried **restarting** recently?\n\n(A proper restart, not just closing the lid)",
                'quick_replies': [
                    {'text': '✅ Yes, already restarted', 'value': 'yes', 'next': 'check_resources'},
                    {'text': '❌ Let me try that', 'value': 'no', 'next': 'do_restart'}
                ]
            },
            'do_restart': {
                'message': "Please **restart your computer now** (Start → Restart, not Shut Down).\n\nLet me know when you're back!",
                'quick_replies': [
                    {'text': '✅ Done, back now', 'value': 'done', 'next': 'restart_result'}
                ]
            },
            'restart_result': {
                'message': "Is it faster now?",
                'quick_replies': [
                    {'text': '✅ Yes, much better!', 'value': 'yes', 'next': 'success'},
                    {'text': '❌ Still slow', 'value': 'no', 'next': 'check_resources'}
                ]
            },
            'check_resources': {
                'message': "Let's see what's using your resources:\n\n1️⃣ Press **Ctrl + Shift + Esc** (Task Manager)\n2️⃣ Click **\"More details\"** if needed\n3️⃣ Look at **CPU** and **Memory** columns\n\nIs anything using over 80%?",
                'quick_replies': [
                    {'text': '📈 High CPU usage', 'value': 'cpu', 'next': 'high_cpu'},
                    {'text': '💾 High Memory usage', 'value': 'memory', 'next': 'high_memory'},
                    {'text': '💿 High Disk usage', 'value': 'disk', 'next': 'high_disk'},
                    {'text': '✅ All looks normal', 'value': 'normal', 'next': 'check_storage'}
                ]
            },
            'high_cpu': {
                'message': "High CPU! Look at what's using it:\n\n• **A program you recognize?** → Close it and restart it\n• **\"System\"** or \"Windows\"? → Might be updating\n• **Unknown program?** → Could be malware\n\nTry closing the high-usage program. Did that help?",
                'quick_replies': [
                    {'text': '✅ Yes, faster now!', 'value': 'yes', 'next': 'success'},
                    {'text': '❌ Can\'t close it', 'value': 'no', 'next': 'force_close'},
                    {'text': '⚠️ Worried about malware', 'value': 'malware', 'next': 'malware_check'}
                ]
            },
            'check_storage': {
                'message': "Let's check storage space:\n\n1️⃣ Open **File Explorer**\n2️⃣ Look at your **C: drive**\n3️⃣ Is it mostly **red** (low space)?\n\nYou need at least 15-20% free space!",
                'quick_replies': [
                    {'text': '🔴 Almost full!', 'value': 'full', 'next': 'storage_full'},
                    {'text': '🟢 Plenty of space', 'value': 'ok', 'next': 'other_causes'}
                ]
            },
            'storage_full': {
                'message': "Low storage slows everything down!\n\n**Quick cleanup:**\n1️⃣ Empty **Recycle Bin**\n2️⃣ Clear **Downloads** folder\n3️⃣ Run **Disk Cleanup** (search for it)\n\nCan you free up some space?",
                'quick_replies': [
                    {'text': '✅ Made some space, faster now!', 'value': 'yes', 'next': 'success'},
                    {'text': '❓ Need help cleaning up', 'value': 'help', 'next': 'cleanup_help'},
                    {'text': '❌ Still slow', 'value': 'no', 'next': 'escalate'}
                ]
            },
            'success': {
                'message': "🎉 **Excellent!** Glad your computer is running better!\n\n💡 **Tip:** Restart your computer weekly to keep it fast!\n\nAnything else you need?",
                'quick_replies': [
                    {'text': '🖥️ Another speed issue', 'value': 'slow', 'next': 'restart'},
                    {'text': '💻 Different issue', 'value': 'other', 'next': 'new_issue'},
                    {'text': '👋 No, thanks!', 'value': 'done', 'next': 'goodbye'}
                ],
                'is_success': True
            },
            'escalate': {
                'message': "Persistent slowness might need deeper investigation. 🔍\n\nOur tech team can check for:\n• Failing hardware\n• Hidden malware\n• Driver issues\n• System optimization",
                'quick_replies': [
                    {'text': '🎫 Create Support Ticket', 'value': 'ticket', 'action': 'create_ticket'},
                    {'text': '🔄 Let me try more things', 'value': 'retry', 'next': 'restart'}
                ],
                'is_escalation': True
            }
        }
    }
}


def get_troubleshooting_flow(issue_type: str) -> Optional[Dict]:
    """Get the troubleshooting flow for an issue type"""
    return TROUBLESHOOTING_FLOWS.get(issue_type)


def get_flow_step(flow_name: str, step_name: str) -> Optional[Dict]:
    """Get a specific step from a troubleshooting flow"""
    flow = TROUBLESHOOTING_FLOWS.get(flow_name)
    if flow and step_name in flow.get('steps', {}):
        return flow['steps'][step_name]
    return None


# ============================================================================
# SMART FOLLOW-UP QUESTIONS
# ============================================================================

CLARIFYING_QUESTIONS = {
    'device_type': {
        'question': "What type of device is having the issue?",
        'quick_replies': [
            {'text': '💻 Desktop Computer', 'value': 'desktop'},
            {'text': '💻 Laptop', 'value': 'laptop'},
            {'text': '🖨️ Printer', 'value': 'printer'},
            {'text': '📱 Phone/Tablet', 'value': 'mobile'},
            {'text': '🖥️ Monitor/Display', 'value': 'display'},
            {'text': '🔌 Other', 'value': 'other'}
        ]
    },
    'when_started': {
        'question': "When did this problem start?",
        'quick_replies': [
            {'text': '📅 Today', 'value': 'today'},
            {'text': '📆 This week', 'value': 'this_week'},
            {'text': '🗓️ Longer than a week', 'value': 'longer'},
            {'text': '❓ Not sure', 'value': 'unknown'}
        ]
    },
    'changes_made': {
        'question': "Did anything change before this started? (New software, updates, etc.)",
        'quick_replies': [
            {'text': '📥 Installed something new', 'value': 'new_install'},
            {'text': '🔄 Recent update', 'value': 'update'},
            {'text': '⚡ Power outage/issue', 'value': 'power'},
            {'text': '❌ Nothing changed', 'value': 'nothing'},
            {'text': '❓ Not sure', 'value': 'unknown'}
        ]
    },
    'error_message': {
        'question': "Are you seeing any error messages?",
        'quick_replies': [
            {'text': '✅ Yes, there\'s an error', 'value': 'yes'},
            {'text': '❌ No error message', 'value': 'no'},
            {'text': '📸 Let me take a screenshot', 'value': 'screenshot'}
        ]
    },
    'tried_restarting': {
        'question': "Have you tried restarting the device yet?",
        'quick_replies': [
            {'text': '✅ Yes, already restarted', 'value': 'yes'},
            {'text': '❌ No, not yet', 'value': 'no'},
            {'text': '🔄 Multiple times', 'value': 'multiple'}
        ]
    }
}


# ============================================================================
# VIDEO TUTORIAL LINKS
# ============================================================================

VIDEO_TUTORIALS = {
    'printer_jam': {
        'title': 'How to Clear a Paper Jam',
        'description': 'Watch how to safely clear paper jams from most printers',
        'links': [
            {'name': 'HP Printers', 'url': 'https://www.youtube.com/results?search_query=hp+printer+paper+jam+fix'},
            {'name': 'Canon Printers', 'url': 'https://www.youtube.com/results?search_query=canon+printer+paper+jam+fix'},
            {'name': 'Brother Printers', 'url': 'https://www.youtube.com/results?search_query=brother+printer+paper+jam+fix'},
            {'name': 'Epson Printers', 'url': 'https://www.youtube.com/results?search_query=epson+printer+paper+jam+fix'},
        ]
    },
    'wifi_reset': {
        'title': 'How to Reset Your WiFi Router',
        'description': 'Quick guide to properly restart your router',
        'links': [
            {'name': 'Router Reset Guide', 'url': 'https://www.youtube.com/results?search_query=how+to+reset+wifi+router'},
        ]
    },
    'windows_cleanup': {
        'title': 'Speed Up Your Windows Computer',
        'description': 'Free up space and improve performance',
        'links': [
            {'name': 'Windows 10/11 Cleanup', 'url': 'https://www.youtube.com/results?search_query=windows+disk+cleanup+speed+up'},
        ]
    },
    'password_reset': {
        'title': 'How to Reset Your Password',
        'description': 'Step-by-step password recovery guides',
        'links': [
            {'name': 'Microsoft Account', 'url': 'https://www.youtube.com/results?search_query=microsoft+account+password+reset'},
            {'name': 'Google Account', 'url': 'https://www.youtube.com/results?search_query=google+account+password+reset'},
        ]
    },
    'outlook_issues': {
        'title': 'Fix Outlook Problems',
        'description': 'Common Outlook fixes and troubleshooting',
        'links': [
            {'name': 'Outlook Not Working', 'url': 'https://www.youtube.com/results?search_query=outlook+not+working+fix'},
            {'name': 'Outlook Sync Issues', 'url': 'https://www.youtube.com/results?search_query=outlook+not+syncing+fix'},
        ]
    }
}


def get_video_tutorial(topic: str) -> Optional[Dict]:
    """Get video tutorial links for a topic"""
    return VIDEO_TUTORIALS.get(topic)


# ============================================================================
# RETURNING USER MEMORY
# ============================================================================

def get_welcome_back_message(user_history: Dict) -> Optional[str]:
    """Generate a welcome back message for returning users"""
    if not user_history:
        return None
    
    last_issue = user_history.get('last_issue')
    was_resolved = user_history.get('was_resolved')
    last_visit = user_history.get('last_visit')
    
    messages = []
    
    if last_issue:
        if was_resolved:
            messages = [
                f"Welcome back! 👋 Last time I helped you with **{last_issue}**. Hope it's still working well! What can I help you with today?",
                f"Hey, good to see you again! 🫧 Your **{last_issue}** issue from before - is everything still okay? What brings you back?",
                f"Hello again! 💜 I remember helping you with **{last_issue}**. What can I assist you with this time?",
            ]
        else:
            messages = [
                f"Welcome back! 👋 I see we were working on **{last_issue}** before. Are you still having that issue, or is this something new?",
                f"Hey again! 🫧 Last time you mentioned **{last_issue}** - should we continue from there or start fresh?",
                f"Hello! 💜 I remember you had a **{last_issue}** issue. Want to continue troubleshooting that, or is this different?",
            ]
    else:
        messages = [
            "Welcome back! 👋 Great to see you again! What can I help you with today?",
            "Hey, you're back! 🫧 What can Bubbles help you with this time?",
            "Hello again! 💜 Ready to help - what's on your mind?",
        ]
    
    return random.choice(messages)


# ============================================================================
# AUTO-FILL TICKET HELPER
# ============================================================================

def generate_ticket_prefill(conversation_data: Dict) -> Dict:
    """Generate pre-filled ticket data from conversation"""
    prefill = {
        'subject': '',
        'description': '',
        'steps_tried': [],
        'category': 'general',
        'priority': 'normal'
    }
    
    # Extract issue from conversation
    initial_problem = conversation_data.get('initial_problem', '')
    if initial_problem:
        # Create a subject
        if len(initial_problem) <= 100:
            prefill['subject'] = initial_problem
        else:
            prefill['subject'] = initial_problem[:97] + '...'
    
    # Build description
    description_parts = []
    
    if initial_problem:
        description_parts.append(f"**Original Issue:**\n{initial_problem}")
    
    # Add conversation history
    history = conversation_data.get('conversation_history', [])
    if history:
        description_parts.append("\n**Conversation with Bubbles:**")
        for msg in history[-10:]:  # Last 10 messages
            role = "Customer" if msg.get('role') == 'user' else "Bubbles"
            content = msg.get('content', '')[:200]  # Limit length
            description_parts.append(f"- {role}: {content}")
    
    # Add steps tried
    steps = conversation_data.get('steps_tried', [])
    if steps:
        prefill['steps_tried'] = steps
        description_parts.append(f"\n**Steps Already Tried:**")
        for step in steps:
            description_parts.append(f"- {step}")
    
    # Detect category
    category_keywords = {
        'printer': ['printer', 'print', 'paper', 'ink', 'toner'],
        'network': ['wifi', 'internet', 'network', 'connect', 'ethernet'],
        'email': ['email', 'outlook', 'mail', 'send', 'inbox'],
        'password': ['password', 'login', 'locked', 'account'],
        'computer': ['slow', 'freeze', 'crash', 'computer', 'laptop'],
        'display': ['screen', 'monitor', 'display', 'resolution']
    }
    
    problem_lower = initial_problem.lower()
    for category, keywords in category_keywords.items():
        if any(kw in problem_lower for kw in keywords):
            prefill['category'] = category
            break
    
    # Detect priority based on frustration and urgency words
    urgent_words = ['urgent', 'asap', 'emergency', 'critical', 'deadline', 'important', 'meeting']
    if any(word in problem_lower for word in urgent_words):
        prefill['priority'] = 'high'
    
    frustration = conversation_data.get('frustration_level', 0)
    if frustration >= 4:
        prefill['priority'] = 'high'
    
    prefill['description'] = '\n'.join(description_parts)
    
    return prefill


# ============================================================================
# SYSTEM STATUS CHECK (Placeholder for integration)
# ============================================================================

KNOWN_ISSUES = []  # This would be populated from a database or API

def check_known_issues(issue_type: str) -> Optional[Dict]:
    """Check if there are any known system issues"""
    # This is a placeholder - in production, this would check a database
    # or external monitoring system for known outages
    
    # For demo purposes, return None (no known issues)
    # You could add entries like:
    # KNOWN_ISSUES.append({
    #     'type': 'email',
    #     'title': 'Email Server Maintenance',
    #     'description': 'Email servers are undergoing maintenance until 5 PM',
    #     'affected': ['email', 'outlook'],
    #     'expected_resolution': '5:00 PM today'
    # })
    
    for issue in KNOWN_ISSUES:
        if issue_type in issue.get('affected', []):
            return issue
    
    return None


def get_status_message(issue_type: str) -> Optional[str]:
    """Get a status message if there are known issues"""
    known = check_known_issues(issue_type)
    if known:
        return f"""⚠️ **Known Issue Alert**

**{known['title']}**

{known['description']}

Expected resolution: {known.get('expected_resolution', 'Unknown')}

This might be affecting your issue. Would you still like to troubleshoot?"""
    return None
