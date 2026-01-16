#!/usr/bin/python
# -*- coding: utf-8 -*-
# << CODE BY Qusay_kali
# Free Palestine 🇵🇸

import os, socket, platform, sys, time, requests, locale, subprocess, datetime

# التحقق من وجود المكتبات الأساسية
try:
    import phonenumbers
    from phonenumbers import carrier, geocoder, timezone
except ImportError:
    pass

try:
    import psutil
except ImportError:
    psutil = None

# إعداد الألوان الكاملة
Re = '\033[1;31m'; Gr = '\033[1;32m'; Ye = '\033[1;33m'
Blu = '\033[1;34m'; Cy = '\033[1;36m'; Wh = '\033[1;37m'

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
{Ye} [!] Support : Free Palestine 🇵🇸
{Ye} [!] Status  : Active (FULL 40 PLATFORMS)
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
{Wh}          ____________________________________
{Wh}          | {Cy}ACTION: {Gr}{title:<20}       {Wh}|
{Wh}          | {Cy}AUTHOR: {Wh}Qusay_kali                 {Wh}|
{Wh}          |____________________________________|
    """)

def IP_Track():
    sub_banner("IP TRACKING")
    ip = input(f"{Wh}\n [+] Enter Target IP : {Gr}")
    print(f'\n {Wh}============= {Gr}DEEP IP DATA {Wh}=============')
    try:
        url = f"http://ip-api.com/json/{ip}?fields=66846719"
        data = requests.get(url, headers=HEADERS, timeout=10).json()
        if data.get('status') == 'success':
            for i, (k, v) in enumerate(data.items(), 1):
                print(f" {Wh}{i:<2}. {k.replace('_',' ').capitalize():<20}:{Gr} {v}")
        else:
            print(f"{Ye} [!] Switching to Backup Server...")
            alt = requests.get(f"https://ipwho.is/{ip}", timeout=10).json()
            if alt.get('success'):
                fields = ["country", "city", "region", "isp", "latitude", "longitude", "timezone"]
                for i, field in enumerate(fields, 1):
                    print(f" {Wh}{i:<2}. {field.capitalize():<20}:{Gr} {alt.get(field)}")
            else: print(f"{Re} [!] IP Not Found.")
    except: print(f"{Re} [!] Connection Error. Check Network.")

def TrackLu():
    sub_banner("USER SEARCH (40)")
    user = input(f"\n {Wh} [+] Target Username : {Gr}")
    
    # قائمة الـ 40 منصة كاملة
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
        {"url": "https://open.spotify.com/user/{}", "name": "Spotify"},
        {"url": "https://www.medium.com/@{}", "name": "Medium"},
        {"url": "https://www.behance.net/{}", "name": "Behance"},
        {"url": "https://www.quora.com/profile/{}", "name": "Quora"},
        {"url": "https://www.vimeo.com/{}", "name": "Vimeo"},
        {"url": "https://www.soundcloud.com/{}", "name": "SoundCloud"},
        {"url": "https://www.vk.com/{}", "name": "VK"},
        {"url": "https://www.steamcommunity.com/id/{}", "name": "Steam"},
        {"url": "https://www.roblox.com/user.aspx?username={}", "name": "Roblox"},
        {"url": "https://www.dailymotion.com/{}", "name": "DailyMotion"},
        {"url": "https://www.flickr.com/people/{}", "name": "Flickr"},
        {"url": "https://www.imgur.com/user/{}", "name": "Imgur"},
        {"url": "https://www.patreon.com/{}", "name": "Patreon"},
        {"url": "https://www.deviantart.com/{}", "name": "DeviantArt"},
        {"url": "https://www.about.me/{}", "name": "About.me"},
        {"url": "https://www.mixcloud.com/{}", "name": "Mixcloud"},
        {"url": "https://www.keybase.io/{}", "name": "Keybase"},
        {"url": "https://www.issuu.com/{}", "name": "Issuu"},
        {"url": "https://www.wattpad.com/user/{}", "name": "Wattpad"},
        {"url": "https://www.last.fm/user/{}", "name": "Last.fm"},
        {"url": "https://www.ok.ru/{}", "name": "Odnoklassniki"},
        {"url": "https://www.bitbucket.org/{}", "name": "Bitbucket"},
        {"url": "https://www.etsy.com/shop/{}", "name": "Etsy"},
        {"url": "https://www.reverbnation.com/{}", "name": "ReverbNation"},
        {"url": "https://www.behance.net/{}", "name": "Behance"},
        {"url": "https://www.dribbble.com/{}", "name": "Dribbble"},
        {"url": "https://www.crunchyroll.com/user/{}", "name": "Crunchyroll"}
    ]
    
    print(f"\n {Wh}========== {Gr}SCANNING 40 PLATFORMS {Wh}==========")
    for site in platforms:
        try:
            r = requests.get(site['url'].format(user), headers=HEADERS, timeout=5)
            if r.status_code == 200:
                print(f" {Wh}[{Gr} FOUND {Wh}] {site['name']:<12} -> {Gr}{site['url'].format(user)}")
            else:
                print(f" {Wh}[{Re} NONE {Wh}] {site['name']:<12} : Not Found")
        except: pass

def showDevice30():
    sub_banner("DEVICE AUDIT")
    hostname = socket.gethostname()
    try: pub_ip = requests.get('https://api.ipify.org/', timeout=5).text
    except: pub_ip = "Offline"
    has_ps = 'psutil' in sys.modules
    mem = psutil.virtual_memory() if has_ps else None
    info = [
        ("Device Name", hostname), ("Public IP", pub_ip), ("Local IP", socket.gethostbyname(hostname)),
        ("OS System", platform.system()), ("OS Release", platform.release()), ("Architecture", platform.machine()),
        ("RAM Total", f"{round(mem.total/(1024**3),2)} GB" if mem else "N/A"), ("RAM Usage", f"{mem.percent}%" if mem else "N/A"),
        ("CPU Cores", psutil.cpu_count() if has_ps else "N/A"), ("Battery", f"{psutil.sensors_battery().percent}%" if has_ps and psutil.sensors_battery() else "N/A")
    ]
    for i, (k, v) in enumerate(info, 1):
        print(f" {Wh}{i:<2}. {k:<20}:{Gr} {v}")

def phone30():
    sub_banner("PHONE OSINT")
    num = input(f"{Wh}\n [+] Enter Phone (Ex +962xxxx): {Gr}")
    try:
        p = phonenumbers.parse(num, None)
        data = [
            ("Country Code", p.country_code), ("National Num", p.national_number),
            ("Carrier", carrier.name_for_number(p, 'en')), ("Location", geocoder.description_for_number(p, 'ar')),
            ("Timezone", timezone.time_zones_for_number(p)), ("Valid Number", phonenumbers.is_valid_number(p))
        ]
        for i, (k, v) in enumerate(data, 1):
            print(f" {Wh}{i:<2}. {k:<20}:{Gr} {v}")
    except: print(f"{Re} [!] Parsing Error.")

def main():
    while True:
        banner()
        print(f"{Wh}[ 1 ] {Gr}IP Tracker\n{Wh}[ 2 ] {Gr}Device Information\n{Wh}[ 3 ] {Gr}Phone Tracker\n{Wh}[ 4 ] {Gr}Username Search (40 Platforms)\n{Wh}[ 0 ] {Gr}Exit")
        c = input(f"{Wh}\n [ + ] Select Option : ")
        if c == '1': IP_Track()
        elif c == '2': showDevice30()
        elif c == '3': phone30()
        elif c == '4': TrackLu()
        elif c == '0': sys.exit()
        input(f"\n{Wh}Press Enter to return...");

if __name__ == "__main__": main()
