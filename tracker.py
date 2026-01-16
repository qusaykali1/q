# CODE BY Qusay_kali
# Free Palestine 🇵🇸

import os, socket, platform, sys, time, requests, locale, datetime, json, re, uuid

try:
    import psutil
except:
    psutil = None

try:
    from geopy.geocoders import Nominatim
except:
    from geopy.geocoders import Nominatim
    Nominatim = None

import phonenumbers
from phonenumbers import carrier, geocoder, timezone

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
 ██████╗ ██╗   ██╗███████╗ █████╗ ██╗   ██╗    ██╗  ██╗ █████╗ ██╗     ██╗
██╔═══██╗██║   ██║██╔════╝██╔══██╗╚██╗ ██╔╝    ██║ ██╔╝██╔══██╗██║     ██║
██║   ██║██║   ██║███████╗███████║ ╚████╔╝     █████╔╝ ███████║██║     ██║
██║▄▄ ██║██║   ██║╚════██║██╔══██║  ╚██╔╝      ██╔═██╗ ██╔══██║██║     ██║
╚██████╔╝╚██████╔╝███████║██║  ██║   ██║       ██║  ██╗██║  ██╗███████╗██║
 ╚══▀▀═╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝       ╚═╝  ╚═╝╚═╝  ╚═╝{Ye} Qusay_kali
{Wh}-----------------------------------------------------------------------------
{Gr}  {Ye}Instagram : @qusay_kali | {Cy}palestin | {Ye}youtube  : @Qusay_kali
{Wh}-----------------------------------------------------------------------------""")

def sub_banner(title):
    clear()
    print(f"""
{Re}                .                         .
{Re}                //               ps         \\\\
{Re}               ||      {Wh} .--------------. {Re}      ||
{Re}               ||    {Wh}.-'                '-. {Re}   ||
{Re}               ||  {Wh}/    {Re}████      ████    {Wh}\\ {Re} ||
{Re}               || {Wh}|    {Re}██████    ██████    {Wh}| {Re}||
{Re}                \\\\  {Wh}'-.      {Ye}WWWW      {Wh}.-' {Re}  //
{Re}                 '                         '
{Wh}          ____________________________________
{Wh}         | {Cy}ACTION : {Gr}{title:<22}{Wh}   |
{Wh}         | {Cy}AUTHOR : {Wh}Qusay_kali        |  {Wh}|
{Wh}         |____________________________________|
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
    sub_banner("IP TRACKING")
    ip=input(f"{Wh}[+] Target IP : {Gr}").strip()

    apis=[
        f"https://ipwho.is/{ip}",
        f"https://ipapi.co/{ip}/json/",
        f"https://ipinfo.io/{ip}/json"
    ]

    for api in apis:
        try:
            r=requests.get(api,headers=HEADERS,timeout=8).json()
            if isinstance(r,dict) and r.get("success") is False:
                continue
            print(f"\n{Wh}========== IP INFORMATION ==========\n")
            for i,(k,v) in enumerate(r.items(),1):
                if i>30: break
                v = filter_p(v)
                print(f"{Wh}{i:02}. {k:<18}:{Gr} {v}")
            return
        except:
            pass

    print(f"{Re}[!] All IP services failed")

def device_info():
    sub_banner("DEVICE AUDIT (COMPLETE)")
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
    sub_banner("PHONE OSINT")
    num=input(f"{Wh}[+] Phone (+CountryCode): {Gr}").strip()
    
    if not num.startswith('+'): num = '+' + num
    
    try:
        p=phonenumbers.parse(num,None)
        if not phonenumbers.is_possible_number(p) and not num.startswith('+972'):
            print(f"{Re}[!] Invalid Phone Number")
            return
    except:
        print(f"{Re}[!] Parsing Error"); return

    carrier_name=carrier.name_for_number(p,"en")
    region_name=filter_p(geocoder.description_for_number(p,"en"))
    country_name=filter_p(geocoder.country_name_for_number(p, "en"))
    
    if num.startswith('+972'):
        country_name = FREE_PAL
        region_name = f"{Gr}Occupied {PAL_EN}{Wh}"

    tz=timezone.time_zones_for_number(p)
    ntype = phonenumbers.number_type(p)
    line_type = "Unknown"
    if ntype == 1: line_type = "Mobile"
    elif ntype == 0: line_type = "Fixed Line"

    result=[
        ("Country", country_name),
        ("Region/City", region_name),
        ("Carrier", carrier_name if carrier_name else "Unknown"),
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

    print(f"\n{Wh}[*] Searching for {Ye}{user} on {len(platforms)} platforms...\n")
    for name,url in platforms:
        try:
            r=requests.get(url.format(user),headers=HEADERS,timeout=5)
            if r.status_code==200:
                print(f"{Gr}[FOUND]{Wh} {name:<15} -> {url.format(user)}")
            else:
                print(f"{Re}[NONE ]{Wh} {name}")
        except: pass

def main():
    while True:
        banner()
        print(f"{Wh}[1]{Gr} IP Tracker")
        print(f"{Wh}[2]{Gr} Device Information ")
        print(f"{Wh}[3]{Gr} Phone Number ")
        print(f"{Wh}[4]{Gr} Username ")
        print(f"{Wh}[0]{Gr} Exit")
        ch=input(f"\n{Wh}[+] Select : ")
        if ch=="1": IP_Track()
        elif ch=="2": device_info()
        elif ch=="3": phone_osint()
        elif ch=="4": username_osint()
        elif ch=="0": sys.exit()
        input(f"{Wh}\nPress Enter to return...")

if __name__=="__main__":
    main()


