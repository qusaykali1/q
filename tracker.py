# CODE BY Qusay_kali
# Free Palestine 🇵🇸
import os
import socket
import platform
import sys
import time
import requests
import locale
import datetime
import json
import re
import uuid
import asyncio
import aiohttp

try:
    import psutil
except ImportError:
    psutil = None

try:
    from geopy.geocoders import Nominatim
except ImportError:
    Nominatim = None

import phonenumbers
from phonenumbers import carrier, geocoder, timezone

# Colors
Bl='\033[30m'; Re='\033[1;31m'; Gr='\033[1;32m'; Ye='\033[1;33m'
Blu='\033[1;34m'; Mage='\033[1;35m'; Cy='\033[1;36m'; Wh='\033[1;37m'
PAL_EN = f"{Re}P{Gr}A{Wh}L{Bl}E{Re}S{Gr}T{Wh}I{Bl}N{Re}E{Wh}"
FREE_PAL = f"{Gr} {PAL_EN} 🇵🇸{Wh}"
HEADERS={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

def clear():
    os.system("cls" if os.name=="nt" else "clear")

def banner():
    clear()
    print(f"""{Cy}
                                                                                      
  ██╗██████╗      ████████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗    
  ██║██╔══██╗     ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗   
  ██║██████╔╝█████╗  ██║   ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝   
  ██║██╔═══╝ ╚════╝  ██║   ██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗   
  ██║██║             ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║   
  ╚═╝╚═╝             ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ {Re}Qusay_kali{Wh}                                                                         
------------------------------------------------------------
{Gr} {Ye}Instagram : @qusay_kali | {Cy}palestin {Ye}| {Ye}youtube : @Qusay_kali
{Wh}------------------------------------------------------------""")

def sub_banner(title=""):
    clear()
    print(f"""
{Re}                 .                         .
{Re}                //                         \\\\
{Re}               //               🇵🇸          \\\\
{Re}              ||      {Wh} .--------------. {Re}    ||
{Re}              ||    {Wh}.-'                '-. {Re} ||
{Re}              ||  {Wh}/    {Re}████      ████    {Wh}\\ {Re} ||
{Re}              || {Wh}|    {Re}██████    ██████    {Wh}| {Re}||
{Re}              || {Wh}|    {Re}██████    ██████    {Wh}| {Re}||
{Re}              ||  {Wh}\\    {Re}████      ████    {Wh}/ {Re} ||
{Re}               \\\\  {Wh}'-.      {Ye}WWWW      {Wh}.-' {Re}  //
{Re}                \\\\    {Wh}'--------------' {Re}    //
{Re}                 '                          '
{Wh}          ________________________________________
{Wh}         | {Cy}  version {Wh}: {Re}1.0 {Wh}                    |
{Wh}         | {Wh}------------------------------------{Wh}|
{Wh}         | {Gr}  AUTHOR: {Wh}Qusay_kali                {Wh}|
{Wh}         | {Gr}  MODULE: {Wh}CYBER SECURITY            {Wh}|
{Wh}         |_____________________________________|
    """)

def filter_p(val):
    bad = ["Israel", "IL", "israel"]
    if any(x in str(val) for x in bad):
        return FREE_PAL
    return val

def get_mac():
    try:
        mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        return mac.upper()
    except:
        return "Unknown"

def IP_Track():
    sub_banner("IP TRACKER ")
    ip=input(f"{Wh}[+] Target IP : {Gr}").strip()
    
    apis = [
        f"http://ip-api.com/json/{ip}",
        f"https://ipapi.co/{ip}/json/",
        f"https://ipwho.is/{ip}",
        f"https://ipinfo.io/{ip}/json"
    ]
    
    all_data = {}
    for api in apis:
        try:
            r = requests.get(api, headers=HEADERS, timeout=8).json()
            if isinstance(r, dict) and r.get("status") != "fail":
                all_data.update(r)
        except:
            pass
    
    if all_data:
        print(f"\n{Wh}========== DETAILED IP INFORMATION (MERGED) ==========\n")
        for i, (k, v) in enumerate(all_data.items(), 1):
            if i > 50: break
            v = filter_p(v)
            print(f"{Wh}{i:02}. {k:<20}:{Gr} {v}")
        if "lat" in all_data and "lon" in all_data:
            print(f"{Wh}Google Maps:{Gr} https://www.google.com/maps?q={all_data['lat']},{all_data['lon']}")
    else:
        print(f"{Re}[!] No IP data found")

def device_info():
    sub_banner("Device Inmformation ")
    host=socket.gethostname()
    address_full = "N/A"
    try:
        geo_r = requests.get("https://ipwho.is/", timeout=10).json()
        if geo_r.get("success"):
            pub_ip = geo_r.get("ip")
            lat = geo_r.get("latitude")
            lon = geo_r.get("longitude")
            city = geo_r.get("city")
            country = filter_p(geo_r.get("country"))
            maps_link = f"https://www.google.com/maps?q={lat},{lon}"
           
            if Nominatim:
                try:
                    geolocator = Nominatim(user_agent="Qusay_kali_Audit")
                    location = geolocator.reverse(f"{lat}, {lon}")
                    address_full = filter_p(location.address) if location else "Not Found"
                except:
                    address_full = "Geopy Service Timeout"
        else:
            pub_ip = requests.get("https://api.ipify.org", timeout=5).text
            lat = lon = city = country = maps_link = "N/A"
    except:
        pub_ip = "Offline"
        lat = lon = city = country = maps_link = "Error"
    mem=psutil.virtual_memory() if psutil else None
    disk=psutil.disk_usage("/") if psutil else None
    mac_addr = get_mac()
    info=[
        ("Hostname", host),
        ("MAC Address", mac_addr),
        ("Public IP", pub_ip),
        ("Local IP", socket.gethostbyname(host)),
        ("Country", country),
        ("City", city),
        ("Latitude", lat),
        ("Longitude", lon),
        ("Full Address", address_full),
        ("Maps Link", maps_link),
        ("OS", platform.system()),
        ("OS Release", platform.release()),
        ("OS Version", platform.version()),
        ("Architecture", platform.machine()),
        ("Processor", platform.processor()),
        ("CPU Cores", psutil.cpu_count() if psutil else "N/A"),
        ("RAM Total", f"{round(mem.total/1e9,2)} GB" if mem else "N/A"),
        ("RAM Usage", f"{mem.percent}%" if mem else "N/A"),
        ("Disk Total", f"{round(disk.total/1e9,2)} GB" if disk else "N/A"),
        ("Disk Usage", f"{disk.percent}%" if disk else "N/A"),
        ("Boot Time", datetime.datetime.fromtimestamp(psutil.boot_time()) if psutil else "N/A"),
        ("Python Version", platform.python_version()),
        ("User", os.getenv("USER") or os.getenv("USERNAME")),
        ("Working Dir", os.getcwd()),
        ("Timezone", time.tzname),
        ("Battery", f"{psutil.sensors_battery().percent}%" if psutil and psutil.sensors_battery() else "N/A"),
        ("Uptime", f"{round((time.time()-psutil.boot_time())/3600, 2)} Hours" if psutil else "N/A"),
        ("Network Status", "Online" if pub_ip != "Offline" else "Offline"),
        ("Security Mode", "OSINT"),
        ("Final Check", "CLEAN")
    ]
    print(f"\n{Wh}========== DEVICE & LOCATION INFO ==========\n")
    for i,(k,v) in enumerate(info,1):
        print(f"{Wh}{i:02}. {k:<18}:{Gr} {v}")

def phone_osint():
    sub_banner("Phone Number")
    num=input(f"{Wh}[+] Phone (+962xxxxxx): {Gr}").strip()
   
    if not num.startswith('+'): num = '+' + num
   
    try:
        p=phonenumbers.parse(num,None)
        if not phonenumbers.is_possible_number(p) and not num.startswith('+972'):
            print(f"{Re}[!] Invalid Phone Number")
            return
    except:
        print(f"{Re}[!] Parsing Error"); return
    carrier_name=carrier.name_for_number(p,"en") or "Unknown"
    region_name=filter_p(geocoder.description_for_number(p,"en"))
    country_name=filter_p(geocoder.country_name_for_number(p, "en"))
   
    if num.startswith('+972'):
        country_name = "Palestine"
        region_name = f"{Gr}Occupied Palestine{Wh}"
    tz=timezone.time_zones_for_number(p)
    ntype = phonenumbers.number_type(p)
    line_type = "Unknown"
    if ntype == 1: line_type = "Mobile"
    elif ntype == 0: line_type = "Fixed Line"
    result=[
        ("Country", country_name),
        ("Region/City", region_name),
        ("Carrier", carrier_name),
        ("Line Type", line_type),
        ("Timezone", list(tz)),
        ("Valid Number", phonenumbers.is_valid_number(p)),
        ("Possible", phonenumbers.is_possible_number(p)),
        ("E164 Format", phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.E164)),
        ("International", phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.INTERNATIONAL)),
        ("National", phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.NATIONAL)),
        ("RFC3966", phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.RFC3966))
    ]
    print(f"\n{Wh}====== ADVANCED PHONE ANALYSIS ======\n")
    for i,(k,v) in enumerate(result,1):
        print(f"{Wh}{i:02}. {k:<18}:{Gr} {v}")

async def check_username(session, name, url_template, var, semaphore):
    async with semaphore:
        try:
            url = url_template.format(var)
            async with session.get(url, headers=HEADERS, timeout=5) as r:
                if r.status in [200, 301, 302]:
                    content = await r.text()
                    content_lower = content.lower()
                    not_found_keywords = ["not found", "page not found", "404", "doesn't exist", "user not found", "profile not found"]
                    if not any(keyword in content_lower for keyword in not_found_keywords):
                        return (name, var, url, True)
                return (name, var, url, False)
        except:
            return (name, var, url, False)

async def username_osint_async(user, platforms, variations):
    semaphore = asyncio.Semaphore(20)
    async with aiohttp.ClientSession() as session:
        tasks = [check_username(session, name, url, var, semaphore) for name, url in platforms for var in variations]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        found = [res for res in results if isinstance(res, tuple) and res[3]]
        return found

def username_osint():
    sub_banner("USERNAME OSINT")
    user=input(f"{Wh}[+] Username : {Gr}").strip()
   
    platforms=[
        ("Facebook","https://facebook.com/{}"),
        ("Instagram","https://instagram.com/{}"),
        ("Twitter","https://twitter.com/{}"),
        ("TikTok","https://tiktok.com/@{}"),
        ("GitHub","https://github.com/{}"),
        ("Telegram","https://t.me/{}"),
        ("Snapchat","https://snapchat.com/add/{}"),
        ("Reddit","https://reddit.com/user/{}"),
        ("YouTube","https://youtube.com/@{}"),
        ("Pinterest","https://pinterest.com/{}"),
        ("LinkedIn","https://linkedin.com/in/{}"),
        ("Twitch","https://twitch.tv/{}"),
        ("Medium","https://medium.com/@{}"),
        ("Behance","https://behance.net/{}"),
        ("Dribbble","https://dribbble.com/{}"),
        ("Vimeo","https://vimeo.com/{}"),
        ("SoundCloud","https://soundcloud.com/{}"),
        ("DeviantArt","https://deviantart.com/{}"),
        ("VK","https://vk.com/{}"),
        ("About.me","https://about.me/{}"),
        ("Steam","https://steamcommunity.com/id/{}"),
        ("Spotify","https://open.spotify.com/user/{}"),
        ("Pinterest","https://www.pinterest.com/{}")
    ]
    variations = [user, user.capitalize(), user.lower(), user.upper()]
    for i in ['1']:
        variations += [i + var for var in variations] + [var + i for var in variations]
    variations = list(set(variations))
    print(f"\n{Wh}[*] Searching for {Ye}{user} on {len(platforms)} platforms...\n")
    found = asyncio.run(username_osint_async(user, platforms, variations))
    if found:
        print(f"{Gr}======= FOUND PROFILES =======\n")
        for name, var, url, _ in found:
            print(f"{Gr}[FOUND]{Wh} {name:<15} ({var}) -> {url}")
    else:
        print(f"{Re}[!] No profiles found")


def insecam_cams():
    sub_banner(" Camera ")
    
    try:
        import colorama
        colorama.init()
    except ImportError:
        print(f"{Re}[!] colorama not installed. Run: pip install colorama")
        return

    url = "http://www.insecam.org/en/jsoncountries/"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        countries = data.get('countries', {})
    except Exception as e:
        print(f"{Re}Error fetching countries: {e}{Wh}")
        return

    ordered = {}
    if "IL" in countries:
        ordered["PS"] = {
            "country": "Palestine",
            "count": countries["IL"]["count"]
        }
        del countries["IL"]

    for k, v in countries.items():
        ordered[k] = v

    print(f"{Wh}Available Countries / Cameras count:\n")
    for key, value in ordered.items():
        print(f"{Gr}Code: ({key}) - {value['country']} / ({value['count']} cameras){Wh}")

    try:
        country = input(f"\n{Ye}Enter Country Code (##): {Gr}").upper().strip()
        if not country:
            print(f"{Re}No code entered.{Wh}")
            return

        print(f"{Gr}Fetching cameras from {country} ...{Wh}\n")

        res = requests.get(
            f"http://www.insecam.org/en/bycountry/{country}",
            headers=headers,
            timeout=10
        )

        pages = re.findall(r'pagenavigator\("\?page=",\s*(\d+)', res.text)
        last_page = int(pages[0]) if pages else 1

        filename = f"{country}_cams.txt"
        with open(filename, 'a', encoding='utf-8') as f:
            count = 0
            for page in range(last_page):
                res = requests.get(
                    f"http://www.insecam.org/en/bycountry/{country}/?page={page}",
                    headers=headers,
                    timeout=10
                )

                find_ip = re.findall(
                    r"http://\d{1,3}(?:\.\d{1,3}){3}:\d+",
                    res.text
                )

                for ip in find_ip:
                    print(f"{Gr}{ip}{Wh}")
                    f.write(ip + '\n')
                    count += 1

        print(f"\n{Gr}Done! Saved {count} cameras to: {filename}{Wh}")

    except Exception as e:
        print(f"{Re}Error: {e}{Wh}")

def main():
    while True:
        banner()
        print(f"{Wh}[1]{Gr} IP Tracker")
        print(f"{Wh}[2]{Gr} Device Information")
        print(f"{Wh}[3]{Gr} Phone Number OSINT")
        print(f"{Wh}[4]{Gr} Username OSINT")
        print(f"{Wh}[5]{Gr} Cam-hacker")
        print(f"{Wh}[0]{Gr} Exit")
        ch = input(f"\n{Wh}[+] Select : ").strip()

        if ch == "1":
            IP_Track()
        elif ch == "2":
            device_info()
        elif ch == "3":
            phone_osint()
        elif ch == "4":
            username_osint()
        elif ch == "5":
            insecam_cams()
        elif ch == "0":
            print(f"{Gr}Goodbye! Free Palestine 🇵🇸")
            sys.exit(0)
        else:
            print(f"{Re}[!] Invalid choice")

        input(f"{Wh}\nPress Enter to return...")

if __name__ == "__main__":
    main()

