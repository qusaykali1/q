#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ==============================
#   OSINT TOOL – FINAL EDITION
#   Fixed & Hardened Version
# ==============================

import os
import sys
import socket
import platform
import time
import locale
import datetime
import requests

try:
    import psutil
except ImportError:
    psutil = None

import phonenumbers
from phonenumbers import carrier, geocoder, timezone

# ==============================
# COLORS
# ==============================
Bl = '\033[30m'
Re = '\033[1;31m'
Gr = '\033[1;32m'
Ye = '\033[1;33m'
Blu = '\033[1;34m'
Mage = '\033[1;35m'
Cy = '\033[1;36m'
Wh = '\033[1;37m'

# ==============================
# HEADERS (ANTI-BLOCK)
# ==============================
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Connection": "close"
}

# ==============================
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# ==============================
def banner():
    clear()
    print(f"""{Cy}
 ██████╗ ██╗   ██╗███████╗ █████╗ ██╗   ██╗
██╔═══██╗██║   ██║██╔════╝██╔══██╗╚██╗ ██╔╝
██║   ██║██║   ██║███████╗███████║ ╚████╔╝ 
██║▄▄ ██║██║   ██║╚════██║██╔══██║  ╚██╔╝  
╚██████╔╝╚██████╔╝███████║██║  ██║   ██║   
 ╚══▀▀═╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝   
{Wh}-----------------------------------------
{Ye} OSINT MULTI TOOL – FINAL STABLE BUILD
{Ye} Mode : LEGAL | PUBLIC DATA ONLY
{Wh}-----------------------------------------
""")

# ==============================
def sub_banner(title):
    clear()
    print(f"{Cy}========== {Gr}{title} {Cy}=========={Wh}")

# ==============================
def valid_public_ip(ip):
    private_prefixes = (
        "10.", "127.", "192.168.",
        "172.16.", "172.17.", "172.18.", "172.19.",
        "172.2", "169.254."
    )
    return not ip.startswith(private_prefixes)

# ==============================
def IP_Track():
    sub_banner("IP TRACKING")
    ip = input(f"\n{Wh}[+] Enter Target IP : {Gr}").strip()

    if not valid_public_ip(ip):
        print(f"{Re}[!] Private or Local IP – Not Traceable")
        return

    print(f"\n{Wh}========== IP INFORMATION =========={Gr}")

    apis = [
        f"https://ipwho.is/{ip}",
        f"https://ipinfo.io/{ip}/json",
        f"https://ipapi.co/{ip}/json/"
    ]

    for api in apis:
        try:
            r = requests.get(api, headers=HEADERS, timeout=10)
            if r.status_code != 200:
                continue

            data = r.json()

            if "success" in data and data["success"] is False:
                continue

            for k, v in data.items():
                print(f"{Wh}{k:<15}:{Gr} {v}")
            return

        except Exception:
            continue

    print(f"{Re}[!] All IP services failed (Blocked / Rate Limited)")

# ==============================
def showDeviceInfo():
    sub_banner("DEVICE INFORMATION")

    hostname = socket.gethostname()

    try:
        public_ip = requests.get(
            "https://api.ipify.org",
            headers=HEADERS,
            timeout=5
        ).text
    except:
        public_ip = "Unavailable"

    print(f"{Gr}Device Name     : {Wh}{hostname}")
    print(f"{Gr}Public IP      : {Wh}{public_ip}")
    print(f"{Gr}Local IP       : {Wh}{socket.gethostbyname(hostname)}")
    print(f"{Gr}OS             : {Wh}{platform.system()} {platform.release()}")
    print(f"{Gr}Architecture   : {Wh}{platform.machine()}")
    print(f"{Gr}Processor      : {Wh}{platform.processor()}")
    print(f"{Gr}Python Version : {Wh}{platform.python_version()}")
    print(f"{Gr}Language       : {Wh}{locale.getdefaultlocale()}")

    if psutil:
        mem = psutil.virtual_memory()
        print(f"{Gr}RAM Total      : {Wh}{round(mem.total/1024**3,2)} GB")
        print(f"{Gr}RAM Usage      : {Wh}{mem.percent}%")
        print(f"{Gr}CPU Cores      : {Wh}{psutil.cpu_count()}")

# ==============================
def phoneTracker():
    sub_banner("PHONE OSINT")
    num = input(f"\n{Wh}[+] Enter Phone (+CountryCode) : {Gr}")

    try:
        p = phonenumbers.parse(num)
        print(f"{Gr}Valid           : {Wh}{phonenumbers.is_valid_number(p)}")
        print(f"{Gr}Country Code    : {Wh}{p.country_code}")
        print(f"{Gr}Region          : {Wh}{phonenumbers.region_code_for_number(p)}")
        print(f"{Gr}Carrier         : {Wh}{carrier.name_for_number(p, 'en')}")
        print(f"{Gr}Location        : {Wh}{geocoder.description_for_number(p, 'en')}")
        print(f"{Gr}Timezones       : {Wh}{timezone.time_zones_for_number(p)}")
    except:
        print(f"{Re}[!] Invalid phone number")

# ==============================
def usernameSearch():
    sub_banner("USERNAME SEARCH")
    user = input(f"\n{Wh}[+] Enter Username : {Gr}").strip()

    sites = [
        "https://www.facebook.com/{}",
        "https://www.instagram.com/{}",
        "https://github.com/{}",
        "https://twitter.com/{}",
        "https://www.tiktok.com/@{}",
        "https://t.me/{}",
        "https://www.reddit.com/user/{}"
    ]

    for site in sites:
        url = site.format(user)
        try:
            r = requests.get(url, headers=HEADERS, timeout=5)
            if r.status_code == 200:
                print(f"{Gr}[FOUND] {Wh}{url}")
            else:
                print(f"{Re}[NONE ] {Wh}{url}")
        except:
            print(f"{Re}[ERR  ] {Wh}{url}")

# ==============================
def main():
    while True:
        banner()
        print(f"{Wh}[1] {Gr}IP Tracker")
        print(f"{Wh}[2] {Gr}My Device Info")
        print(f"{Wh}[3] {Gr}Phone OSINT")
        print(f"{Wh}[4] {Gr}Username Search")
        print(f"{Wh}[0] {Gr}Exit")

        choice = input(f"\n{Wh}[+] Select : ")

        if choice == "1":
            IP_Track()
        elif choice == "2":
            showDeviceInfo()
        elif choice == "3":
            phoneTracker()
        elif choice == "4":
            usernameSearch()
        elif choice == "0":
            sys.exit()
        else:
            print(f"{Re}[!] Invalid option")

        input(f"\n{Wh}Press Enter to continue...")

# ==============================
if __name__ == "__main__":
    main()
