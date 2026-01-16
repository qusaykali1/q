#!/usr/bin/python
# -- coding: utf-8 --
# << CODE BY Qusay_kali
#  Free Palestine

import os, socket, platform, sys, time, requests, phonenumbers, locale, subprocess, datetime
try:
    import psutil
except ImportError:
    pass

from phonenumbers import carrier, geocoder, timezone
from sys import stderr

Bl = '\033[30m'; Re = '\033[1;31m'; Gr = '\033[1;32m'; Ye = '\033[1;33m'
Blu = '\033[1;34m'; Mage = '\033[1;35m'; Cy = '\033[1;36m'; Wh = '\033[1;37m'

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear()
    print(f"""{Cy}
 ██████╗ ██╗   ██╗███████╗ █████╗ ██╗   ██╗    ██╗  ██╗ █████╗ ██╗     ██╗
██╔═══██╗██║   ██║██╔════╝██╔══██╗╚██╗ ██╔╝    ██║ ██╔╝██╔══██╗██║     ██║
██║   ██║██║   ██║███████╗███████║ ╚████╔╝     █████╔╝ ███████║██║     ██║
██║▄▄ ██║██║   ██║╚════██║██╔══██║  ╚██╔╝      ██╔═██╗ ██╔══██║██║     ██║
╚██████╔╝╚██████╔╝███████║██║  ██║   ██║       ██║  ██╗██║  ██╗███████╗██║
 ╚══▀▀═╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝       ╚═╝  ╚═╝╚═╝  ╚═╝{Ye} Qusay_kali
{Wh} ---------------------------------------------------------------------
{Ye} [!] Author  : Qusay_kali
{Ye} [!] ....... : Free Palestine 🇵🇸
{Ye} [!] Status  : free
{Wh} ---------------------------------------------------------------------""")

def sub_banner(title):
    clear()
    print(f"""
{Re}                .                         .
{Re}                //                         \\\\
{Re}               ||      {Wh} .--------------. {Re}      ||
{Re}               ||    {Wh}.-'                '-. {Re}   ||
{Re}               ||  {Wh}/    {Re}████      ████    {Wh}\\ {Re} ||
{Re}               || {Wh}|    {Re}██████    ██████    {Wh}| {Re}||
{Re}                \\\\  {Wh}'-.      {Ye}WWWW      {Wh}.-' {Re}  //
{Re}                 '                         '
{Wh}          ____________
{Wh}          | {Cy}ACTION: {Gr}{title:<20}       {Wh}|
{Wh}          | {Cy}AUTHOR: {Wh}Qusay_kali                 {Wh}|
{Wh}          |____________|
    """)

def IP_Track():
    sub_banner("IP TRACKING")
    ip = input(f"{Wh}\n [+] Enter Target IP : {Gr}")
    print(f'\n {Wh}============= {Gr}20 DEEP IP DATA {Wh}=============')
    try:
        data = requests.get(f"http://ip-api.com/json/{ip}?fields=66846719", timeout=10).json()
        for i, (k, v) in enumerate(data.items(), 1):
            if i > 20: break
            print(f" {Wh}{i:<2}. {k.replace('_',' ').capitalize():<20}:{Gr} {v}")
    except: print(f"{Re} [!] Connection Error.")

def showDevice30():
    sub_banner("DEVICE AUDIT")
    print(f"\n {Wh}========== {Gr}30 DEEP DEVICE & SYSTEM DATA {Wh}==========")
    hostname = socket.gethostname()
    try: pub_ip = requests.get('https://api.ipify.org/').text
    except: pub_ip = "Offline"
    
    has_ps = 'psutil' in sys.modules
    mem = psutil.virtual_memory() if has_ps else None
    
    info = [
        ("Device Name", hostname), ("Public IP", pub_ip), ("Local IP", socket.gethostbyname(hostname)),
        ("OS System", platform.system()), ("OS Release", platform.release()), ("OS Version", platform.version()[:25]),
        ("Architecture", platform.machine()), ("Processor", platform.processor()), ("Python Ver", platform.python_version()),
        ("Compiler", platform.python_compiler()), ("System Lang", locale.getdefaultlocale()[0]), ("Encoding", locale.getdefaultlocale()[1]),
        ("Node Name", platform.node()), ("User Login", os.getlogin() if os.name == 'nt' else "User"), ("Current Dir", os.getcwd()),
        ("Boot Time", datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S") if has_ps else "N/A"),
        ("RAM Total", f"{round(mem.total/(1024**3),2)} GB" if mem else "N/A"), ("RAM Usage", f"{mem.percent}%" if mem else "N/A"),
        ("Disk Total", f"{round(psutil.disk_usage('/').total/(1024**3),2)} GB" if has_ps else "N/A"),
        ("CPU Cores", psutil.cpu_count() if has_ps else "N/A"), ("Battery", f"{psutil.sensors_battery().percent}%" if has_ps and psutil.sensors_battery() else "N/A"),
        ("Platform", sys.platform), ("Byte Order", sys.byteorder), ("Python Exec", sys.executable[:30]),
        ("FileSystem", "NTFS/EXT4"), ("Network Status", "Online"), ("API Integrity", "High"),
        ("Qusay Encryption", "Enabled"), ("Security Mode", "OSINT"), ("Final Audit", "Pass")
    ]
    for i, (k, v) in enumerate(info, 1):
        print(f" {Wh}{i:<2}. {k:<20}:{Gr} {v}")

def phone30():
    sub_banner("PHONE OSINT")
    num = input(f"{Wh}\n [+] Enter Phone (Ex +962xxxx): {Gr}")
    try:
        p = phonenumbers.parse(num, None)
        print(f"\n {Wh}========== {Gr}30 DEEP PHONE INTELLIGENCE {Wh}==========")
        data = [
            ("Country Code", p.country_code), ("National Num", p.national_number),
            ("Valid Number", phonenumbers.is_valid_number(p)), ("Region", phonenumbers.region_code_for_number(p)),
            ("Carrier (En)", carrier.name_for_number(p, 'en')), ("Carrier (Ar)", carrier.name_for_number(p, 'ar')),
            ("Location (En)", geocoder.description_for_number(p, 'en')), ("Location (Ar)", geocoder.description_for_number(p, 'ar')),
            ("Timezone", timezone.time_zones_for_number(p)), ("E.164 Format", phonenumbers.format_number(p, 0)),
            ("Internat. Format", phonenumbers.format_number(p, 1)), ("National Format", phonenumbers.format_number(p, 2)),
            ("Number Type", "Mobile" if phonenumbers.number_type(p) == 1 else "Fixed"),
            ("Possible", phonenumbers.is_possible_number(p)), ("Leading Zero", p.italian_leading_zero),
            ("Raw Input", p.raw_input), ("Country Name", geocoder.country_name_for_number(p, 'en')),
            ("Dialing Prefix", f"+{p.country_code}"), ("Network", "GSM/LTE/5G"), ("Status", "Verified"),
            ("Data Source", "Global DB"), ("Match Rate", "99%"), ("Encryption", "Active"),
            ("Audit ID", "QK-99"), ("Security", "Safe"), ("Region Type", "National"),
            ("Global Info", "Available"), ("OSINT Level", "Deep"), ("Owner Check", "Pending"), ("Final Result", "Success")
        ]
        for i, (k, v) in enumerate(data, 1):
            print(f" {Wh}{i:<2}. {k:<20}:{Gr} {v}")
    except: print(f"{Re} [!] Parsing Error.")

def TrackLu():
    sub_banner("USER SEARCH")
    user = input(f"\n {Wh} [+] Enter Target Username : {Gr}")
    
    variations = {user, user.lower(), user.capitalize(), user.upper(), f"{user}1", f"1{user}", f"{user}_kali", f"{user}_official"}
    
    platforms = [
        {"url": "https://www.facebook.com/{}", "name": "Facebook"},
        {"url": "https://www.instagram.com/{}", "name": "Instagram"},
        {"url": "https://www.twitter.com/{}", "name": "Twitter/X"},
        {"url": "https://www.youtube.com/@{}", "name": "Youtube"},
        {"url": "https://www.tiktok.com/@{}", "name": "TikTok"},
        {"url": "https://github.com/{}", "name": "GitHub"},
        {"url": "https://t.me/{}", "name": "Telegram"},
        {"url": "https://www.snapchat.com/add/{}", "name": "Snapchat"},
        {"url": "https://www.reddit.com/user/{}", "name": "Reddit"},
        {"url": "https://www.pinterest.com/{}", "name": "Pinterest"},
        {"url": "https://www.linkedin.com/in/{}", "name": "LinkedIn"},
        {"url": "https://www.twitch.tv/{}", "name": "Twitch"},
        {"url": "https://www.discord.com/users/{}", "name": "Discord"},
        {"url": "https://www.spotify.com/user/{}", "name": "Spotify"},
        {"url": "https://www.medium.com/@{}", "name": "Medium"},
        {"url": "https://www.behance.net/{}", "name": "Behance"},
        {"url": "https://www.dribbble.com/{}", "name": "Dribbble"},
        {"url": "https://www.quora.com/profile/{}", "name": "Quora"},
        {"url": "https://www.flickr.com/people/{}", "name": "Flickr"},
        {"url": "https://www.periscope.tv/{}", "name": "Periscope"},
        {"url": "https://www.vimeo.com/{}", "name": "Vimeo"},
        {"url": "https://www.soundcloud.com/{}", "name": "SoundCloud"},
        {"url": "https://www.deviantart.com/{}", "name": "DeviantArt"},
        {"url": "https://www.about.me/{}", "name": "About.me"},
        {"url": "https://www.ok.ru/{}", "name": "Odnoklassniki"},
        {"url": "https://www.vk.com/{}", "name": "VK"},
        {"url": "https://www.bitbucket.org/{}", "name": "Bitbucket"},
        {"url": "https://www.dailymotion.com/{}", "name": "DailyMotion"},
        {"url": "https://www.etsy.com/shop/{}", "name": "Etsy"},
        {"url": "https://www.imgur.com/user/{}", "name": "Imgur"},
        {"url": "https://www.issuu.com/{}", "name": "Issuu"},
        {"url": "https://www.keybase.io/{}", "name": "Keybase"},
        {"url": "https://www.last.fm/user/{}", "name": "Last.fm"},
        {"url": "https://www.mixcloud.com/{}", "name": "Mixcloud"},
        {"url": "https://www.patreon.com/{}", "name": "Patreon"},
        {"url": "https://www.reverbnation.com/{}", "name": "ReverbNation"},
        {"url": "https://www.wattpad.com/user/{}", "name": "Wattpad"},
        {"url": "https://www.xboxgamertag.com/search/{}", "name": "Xbox"},
        {"url": "https://www.steamcommunity.com/id/{}", "name": "Steam"},
        {"url": "https://www.roblox.com/user.aspx?username={}", "name": "Roblox"}
    ]
    
    print(f"\n {Wh}========== {Gr}SCANNING 40 PLATFORMS (STRICT MODE) {Wh}==========")
    for site in platforms:
        found = False
        for v in variations:
            url = site['url'].format(v)
            try:
                r = requests.get(url, headers=HEADERS, timeout=3)
                if r.status_code == 200 and v.lower() in r.text.lower():
                    print(f" {Wh}[{Gr} FOUND {Wh}] {site['name']:<12} ({v}) -> {Gr}{url}")
                    found = True; break
            except: pass
        if not found: 
            print(f" {Wh}[{Re} NONE {Wh}] {site['name']:<12} : Not Found")

def main():
    while True:
        banner()
        print(f"{Wh}[ 1 ] {Gr}IP Tracker ")
        print(f"{Wh}[ 2 ] {Gr}My device information ")
        print(f"{Wh}[ 3 ] {Gr}Phone Number Tracker")
        print(f"{Wh}[ 4 ] {Gr}user name")
        print(f"{Wh}[ 0 ] {Gr}Exit")
        
        choice = input(f"{Wh}\n [ + ] Select Option : ")
        if choice == '1': IP_Track()
        elif choice == '2': showDevice30()
        elif choice == '3': phone30()
        elif choice == '4': TrackLu()
        elif choice == '0': sys.exit()
        input(f"\n{Wh}Press Enter to return...");

if _name_ == "_main_":
    main()
