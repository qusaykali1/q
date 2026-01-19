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
import webbrowser
import urllib3
import subprocess
import sys
from colorama import Fore, init
init(autoreset=True)

def install_requirements():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--break-system-packages"])
    except Exception as e:
        pass 
install_requirements()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

Bl = '\033[30m'
Re = '\033[1;31m'
Gr = '\033[1;32m'
Ye = '\033[1;33m'
Blu = '\033[1;34m'
Mage = '\033[1;35m'
Cy = '\033[1;36m'
Wh = '\033[1;37m'

PAL_EN = f"{Re}P{Gr}A{Wh}L{Bl}E{Re}S{Gr}T{Wh}I{Bl}N{Re}E{Wh}"
FREE_PAL = f"{Gr} {PAL_EN} 🇵🇸{Wh}"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

def setup_database():
    file_path = "data.json"
    url = "https://raw.githubusercontent.com/sherlock-project/sherlock/master/sherlock/resources/data.json"
    
    if not os.path.exists(file_path) or os.path.getsize(file_path) < 1000:
        print(f"{Ye}[*] Initializing Database... Please wait.{Wh}")
        try:
            r = requests.get(url, timeout=20, verify=False, headers=HEADERS) 
            if r.status_code == 200:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(r.text)
                print(f"{Gr}[+] Database downloaded successfully!{Wh}")
            else:
                print(f"{Re}[!] Failed to download database. Status: {r.status_code}{Wh}")
        except Exception as e:
            print(f"{Re}[!] Connection error during setup: {e}{Wh}")

setup_database()

async def sherlock_search(username):
    file_path = "data.json"
    if not os.path.exists(file_path):
        return []
        
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        return []

    semaphore = asyncio.Semaphore(50)
    found_accounts = []

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        tasks = []
        for site in data:
            site_url = data[site].get("url")
            if site_url:
                tasks.append(sherlock_check(session, site, site_url, username, semaphore))
        
        results = await asyncio.gather(*tasks)
        found_accounts = [r for r in results if r]
    
    return found_accounts


def clear():
    os.system("cls" if os.name == "nt" else "clear")

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
{Re}               //           🇵🇸🇵🇸             \\\\
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
{Wh}         | {Cy}  version {Wh}: {Re}1.1 {Wh}                    |
{Wh}         | {Wh}------------------------------------{Wh}|
{Wh}         | {Gr}  AUTHOR: {Wh}Qusay_kali                {Wh}|
{Wh}         | {Gr}  MODULE: {Wh}CYBER SECURITY            {Wh}|
{Wh}         |_____________________________________|
    """.format(title=title))

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

def get_country_info(country_name):
    """Fetch additional country info from REST Countries API and World Bank"""
    country_info = {}
    try:
        if country_name == FREE_PAL or "Palestine" in str(country_name):
            country_info = {
                "Official Name": "State of Palestine",
                "Capital": "Jerusalem",
                "Timezone GMT": "UTC+02:00 (Palestine Standard Time)",
                "Flag Description": "Three horizontal stripes (black, white, green) with a red triangle on the hoist side",
                "Flag URL": "https://flagcdn.com/ps.svg",
                "Location on Map": "Middle East, bordering the Mediterranean Sea, between Egypt and Israel (occupied territories)",
                "Favorite Food": "Maqluba (upside-down rice and vegetable dish)",
                "Currency": "Israeli New Shekel (ILS)",
                "GDP (Latest)": "N/A (Disputed)",
                "Main Industries": "Agriculture, tourism, small-scale manufacturing",
                "Population": "Approximately 5.4 million",
                "Area": "6,020 sq km",
                "Languages": "Arabic",
                "Calling Code": "+970",
                "Internet TLD": ".ps",
                "Driving Side": "Right",
                "Borders": "Egypt, Jordan, Israel (occupied)",
                "Continent": "Asia",
                "Subregion": "Western Asia",
                "Demonym": "Palestinian",
                "Independence Day": "November 15 (Declaration)",
                "Government Type": "Semi-presidential republic",
                "President": "Mahmoud Abbas",
                "Prime Minister": "Mohammad Shtayyeh",
                "Currency Symbol": "₪",
                "Life Expectancy": "73 years",
                "Literacy Rate": "97%",
                "Main Exports": "Stone, olives, fruit",
                "Main Imports": "Food, consumer goods, construction materials",
                "Climate": "Mediterranean",
                "Highest Point": "Mount Nabi Yunis (1,030 m)",
                "Lowest Point": "Dead Sea (-408 m)",
                "National Animal": "Palestinian mountain gazelle",
                "National Anthem": "Fida'i",
                "FIFA Code": "PLE",
                "IOC Code": "PLE",
                "ISO Code": "PS",
                "UN Member": "No (observer state)",
                "WHO Region": "Eastern Mediterranean",
            }
            return country_info

        url = f"https://restcountries.com/v3.1/name/{country_name}?fullText=true"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            data = resp.json()[0] if resp.json() else {}
            official_name = data.get("name", {}).get("official", country_name)
            capital = data.get("capital", ["N/A"])[0]
            timezones = ", ".join(data.get("timezones", ["N/A"]))
            flag_desc = data.get("flags", {}).get("alt", "N/A")
            flag_url = data.get("flags", {}).get("png", "N/A")
            region = data.get("region", "N/A")
            subregion = data.get("subregion", "N/A")
            location = f"{region}, {subregion}"
            currencies = data.get("currencies", {})
            currency_code = list(currencies.keys())[0] if currencies else "N/A"
            currency_name = currencies.get(currency_code, {}).get("name", "N/A") if currency_code else "N/A"
            currency_symbol = currencies.get(currency_code, {}).get("symbol", "N/A") if currency_code else "N/A"
            languages = ", ".join(data.get("languages", {}).values())
            population = f"{data.get('population', 'N/A'):,}"
            area = f"{data.get('area', 'N/A'):,} sq km"
            calling_code = data.get("idd", {}).get("root", "") + "".join(data.get("idd", {}).get("suffixes", ["N/A"]))
            tld = ", ".join(data.get("tld", ["N/A"]))
            driving_side = data.get("car", {}).get("side", "N/A")
            borders = ", ".join(data.get("borders", ["N/A"]))
            continent = data.get("continents", ["N/A"])[0]
            demonym = data.get("demonyms", {}).get("eng", {}).get("m", "N/A")
            un_member = "Yes" if data.get("unMember") else "No"
            independent = "Yes" if data.get("independent") else "No"
            start_of_week = data.get("startOfWeek", "N/A")
            latlng = data.get("latlng", ["N/A", "N/A"])
            highest_point = "N/A"   
            lowest_point = "N/A"   
            fifa = data.get("fifa", "N/A")
            ioc = "N/A"  

            favorite_foods = {
                "Jordan": "Mansaf (lamb cooked in fermented yogurt sauce)",
                "United States": "Hamburger",
                "France": "Croissant",
                "Italy": "Pizza",
                "India": "Biryani",
                "Japan": "Sushi",
                "Mexico": "Tacos",
                "China": "Dumplings",
                "Germany": "Sausage (Wurst)",
                "Brazil": "Feijoada",
            }
            favorite_food = favorite_foods.get(country_name, "Varies by region")

            gdp = "N/A"
            country_code = data.get("cca2", "")
            if country_code:
                wb_url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/NY.GDP.MKTP.CD?date=2022&format=json"
                wb_resp = requests.get(wb_url, headers=HEADERS, timeout=10)
                if wb_resp.status_code == 200:
                    wb_data = wb_resp.json()
                    if wb_data and len(wb_data) > 1 and wb_data[1]:
                        gdp_value = wb_data[1][0].get('value')
                        gdp = f"${gdp_value:,.0f} USD" if gdp_value else "N/A"

            pop_growth = "N/A"
            if country_code:
                pop_growth_url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/SP.POP.GROW?date=2022&format=json"
                pg_resp = requests.get(pop_growth_url, headers=HEADERS, timeout=10)
                if pg_resp.status_code == 200:
                    pg_data = pg_resp.json()
                    if pg_data and len(pg_data) > 1 and pg_data[1]:
                        pop_growth = f"{pg_data[1][0].get('value', 'N/A')}%"

            life_exp = "N/A"
            if country_code:
                life_url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/SP.DYN.LE00.IN?date=2022&format=json"
                life_resp = requests.get(life_url, headers=HEADERS, timeout=10)
                if life_resp.status_code == 200:
                    life_data = life_resp.json()
                    if life_data and len(life_data) > 1 and life_data[1]:
                        life_exp = f"{life_data[1][0].get('value', 'N/A')} years"

            literacy = "N/A"
            if country_code:
                lit_url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/SE.ADT.LITR.ZS?date=2022&format=json"
                lit_resp = requests.get(lit_url, headers=HEADERS, timeout=10)
                if lit_resp.status_code == 200:
                    lit_data = lit_resp.json()
                    if lit_data and len(lit_data) > 1 and lit_data[1]:
                        literacy = f"{lit_data[1][0].get('value', 'N/A')}%"

            country_info = {
                "Official Name": official_name,
                "Capital": capital,
                "Timezone GMT": timezones,
                "Flag Description": flag_desc,
                "Flag URL": flag_url,
                "Location on Map": location,
                "Favorite Food": favorite_food,
                "Currency": f"{currency_name} ({currency_code})",
                "Currency Symbol": currency_symbol,
                "GDP ": gdp,
                "Population": population,
                "Population Growth ": pop_growth,
                "Area": area,
                "Languages": languages,
                "Calling Code": calling_code,
                "Internet TLD": tld,
                "Driving Side": driving_side.capitalize(),
                "Borders": borders,
                "Continent": continent,
                "Subregion": subregion,
                "Demonym": demonym,
                "UN Member": un_member,
                "Independent": independent,
                "Start of Week": start_of_week.capitalize(),
                "Latitude (approx)": latlng[0],
                "Longitude (approx)": latlng[1],
                "Life Expectancy": life_exp,
                "Literacy Rate": literacy,
                "FIFA Code": fifa,
                "Highest Point": highest_point,
                "Lowest Point": lowest_point,
            }
    except Exception as e:
        print(f"{Re}Error fetching country info: {e}{Wh}")
    return country_info

def IP_Track():
    while True:
        sub_banner("IP TRACKER")
        print(f"{Wh}[+] Target IP (press Enter to go back): {Gr}", end="")
        ip = input().strip()

        if not ip:
            return

        apis = [
            f"http://ip-api.com/json/{ip}",
            f"https://ipapi.co/{ip}/json/",
            f"https://ipwho.is/{ip}",
            f"https://ipinfo.io/{ip}/json",
            f"https://freegeoip.app/json/{ip}",
            f"https://api.db-ip.com/v2/free/{ip}",
        ]

        all_data = {}
        for api in apis:
            try:
                r = requests.get(api, headers=HEADERS, timeout=9).json()
                if isinstance(r, dict) and r.get("status") != "fail" and r.get("message") != "reserved range":
                    all_data.update(r)
            except:
                pass

        if not all_data:
            print(f"{Re}[!] No information found for this IP")
            input(f"{Wh}Press Enter to try again...")
            continue

        print(f"\n{Wh}========== IP INFORMATION ==========\n")

        important = [
            ("ip", all_data.get("query") or all_data.get("ip") or all_data.get("addr") or "N/A"),
            ("network", all_data.get("network") or "N/A"),
            ("version", all_data.get("version") or "N/A"),
            ("city", all_data.get("city") or "N/A"),
            ("region", all_data.get("regionName") or all_data.get("region") or "N/A"),
            ("region_code", all_data.get("region_code") or "N/A"),
            ("country", filter_p(all_data.get("country") or all_data.get("country_name")) or "N/A"),
            ("country_name", filter_p(all_data.get("country_name") or all_data.get("country")) or "N/A"),
            ("country_code", all_data.get("countryCode") or all_data.get("country_code") or "N/A"),
            ("country_code_iso3", all_data.get("country_code_iso3") or "N/A"),
            ("country_capital", all_data.get("country_capital") or "N/A"),
            ("country_tld", all_data.get("country_tld") or "N/A"),
            ("continent_code", all_data.get("continentCode") or all_data.get("continent_code") or "N/A"),
            ("in_eu", all_data.get("in_eu") or "N/A"),
            ("postal", all_data.get("postal") or all_data.get("zip") or "N/A"),
            ("latitude", all_data.get("latitude") or all_data.get("lat") or "N/A"),
            ("longitude", all_data.get("longitude") or all_data.get("lon") or "N/A"),
            ("timezone", all_data.get("timezone") or "N/A"),
            ("utc_offset", all_data.get("utc_offset") or "N/A"),
            ("country_calling_code", all_data.get("country_calling_code") or all_data.get("calling_code") or "N/A"),
            ("currency", all_data.get("currency") or "N/A"),
            ("currency_name", all_data.get("currency_name") or "N/A"),
            ("languages", all_data.get("languages") or "N/A"),
            ("country_area", all_data.get("country_area") or "N/A"),
            ("country_population", all_data.get("country_population") or "N/A"),
            ("asn", all_data.get("asn") or all_data.get("as") or "N/A"),
            ("org", all_data.get("org") or all_data.get("organisation") or "N/A"),
            ("success", all_data.get("success") or "N/A"),
            ("type", all_data.get("type") or "N/A"),
            ("continent", filter_p(all_data.get("continent") or all_data.get("continent_name")) or "N/A"),
            ("is_eu", all_data.get("is_eu") or all_data.get("in_eu") or "N/A"),
            ("calling_code", all_data.get("calling_code") or all_data.get("country_calling_code") or "N/A"),
            ("capital", all_data.get("capital") or all_data.get("country_capital") or "N/A"),
            ("borders", all_data.get("borders") or "N/A"),
            ("flag", all_data.get("flag") or "N/A"),
            ("connection", all_data.get("connection") or "N/A"),
            ("hostname", all_data.get("hostname") or "N/A"),
            ("loc", all_data.get("loc") or "N/A"),
            ("readme", all_data.get("readme") or "N/A"),
            ("status", all_data.get("status") or "N/A"),
            ("district", all_data.get("district") or "N/A"),
            ("offset", all_data.get("offset") or "N/A"),
            ("isp", all_data.get("isp") or "N/A"),
            ("asname", all_data.get("asname") or "N/A"),
            ("reverse", all_data.get("reverse") or "N/A"),
            ("mobile", all_data.get("mobile") or "N/A"),
            ("proxy", all_data.get("proxy") or "N/A"),
            ("hosting", all_data.get("hosting") or "N/A"),
            ("connection_type", all_data.get("connection_type") or "N/A"),
            ("abuse_confidence_score", all_data.get("abuse_confidence_score") or "N/A"),
            ("usage_type", all_data.get("usage_type") or "N/A"),
            ("domain", all_data.get("domain") or "N/A"),
            ("metro_code", all_data.get("metro_code") or "N/A"),
            ("time_zone", all_data.get("time_zone") or all_data.get("timezone") or "N/A"),
        ]

        for i, (k, v) in enumerate(important, 1):
            if v is not None:
                print(f"{Wh}{i:02}. {k:<18}: {Gr}{v}")

        lat = all_data.get("latitude") or all_data.get("lat")
        lon = all_data.get("longitude") or all_data.get("lon")

        if lat is not None and lon is not None:
            print(f"\n{Wh}━━━━━━━━━━ MAP LINKS ━━━━━━━━━━")
            print(f"{Gr}Google Maps          : {Wh}https://www.google.com/maps?q={lat},{lon}")
            print(f"{Gr}Google Earth         : {Wh}https://earth.google.com/web/@{lat},{lon},1000a,500d,35y,0h,0t,0r")
            print(f"{Gr}Google Street View   : {Wh}https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={lat},{lon}")
            print(f"{Gr}OpenStreetMap        : {Wh}https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=15/{lat}/{lon}")
        else:
            print(f"\n{Re}No coordinates (lat/lon) available for this IP")

        country = filter_p(all_data.get("country") or all_data.get("country_name", "N/A"))
        print(f"\n{Wh}━━━━━━━━━━ COUNTRY DETAILS ━━━━━━━━━━")
        details = get_country_info(country)
        for k, v in details.items():
            print(f"{Wh}{k:<20}: {Gr}{v}")

        input(f"{Wh}\nPress Enter to continue...")

async def sherlock_check(session, site_name, site_url, username, semaphore):
    async with semaphore:
        try:
            url = site_url.replace("{}", username)
            async with session.get(url, allow_redirects=True, timeout=8) as resp:
                if resp.status == 200:
                    final_url = str(resp.url)
                    if any(x in final_url.lower() for x in ["login", "signup", "join", "register", "auth"]):
                        return None
                    return (site_name, url)
                return None
        except:
            return None
def EchoIntel():
    ()          # مسح الشاشة
    ()           
R  = Fore.RED
LR = Fore.LIGHTRED_EX
G  = Fore.GREEN
LG = Fore.LIGHTGREEN_EX
Y  = Fore.YELLOW
LY = Fore.LIGHTYELLOW_EX
B  = Fore.BLUE
LB = Fore.LIGHTBLUE_EX
C  = Fore.CYAN
LC = Fore.LIGHTCYAN_EX
W  = Fore.WHITE

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner(title=""):
    clear()
    
    print(f"""{C}
   ███████╗ ██████╗██╗  ██╗ ██████╗ ██████╗ ███████╗██╗███╗   ██╗████████╗███████╗██╗     
   ██╔════╝██╔════╝██║  ██║██╔═══██╗██╔══██╗██╔════╝██║████╗  ██║╚══██╔══╝██╔════╝██║     
   █████╗  ██║     ███████║██║   ██║██████╔╝█████╗  ██║██╔██╗ ██║   ██║   █████╗  ██║     
   ██╔══╝  ██║     ██╔══██║██║   ██║██╔══██╗██╔══╝  ██║██║╚██╗██║   ██║   ██╔══╝  ╚═╝     
   ███████╗╚██████╗██║  ██║╚██████╔╝██║  ██║███████╗██║██║ ╚████║   ██║   ███████╗██╗     
   ╚══════╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝{R}Qusay_kali{W}                                       
------------------------------------------------------------
 {Y}Instagram : @qusay_kali1   {C}🇵🇸 palestin   {Y}youtube : @Qusay_kali{W} 
------------------------------------------------------------
    """)

    if title:
        print(f"{LC}================ {title} ================")


if __name__ == "__main__":
    show_banner("EchoIntel v1.1")
    print("\nBanner test complete!")

SUBDOMAINS = [
    'ftp', 'cpanel', 'webmail', 'localhost', 'local', 'mysql', 'forum', 'direct-connect', 'blog', 'vb', 'forums', 'home', 'direct', 'mail', 'access', 'admin', 'administrator', 'email', 'downloads', 'ssh', 'owa', 'bbs', 'webmin', 'parallel', 'parallels', 'www0', 'www', 'www1', 'www2', 'www3', 'www4', 'www5', 'shop', 'api', 'blogs', 'test', 'mx1', 'cdn', 'mysql', 'mail1', 'secure', 'server', 'ns1', 'ns2', 'smtp', 'vpn', 'm', 'mail2', 'postal', 'support', 'web', 'dev'
]

ROBOTS_PATHS = [
    'robots.txt','search/','admin/','login/','sitemap.xml','sitemap2.xml','config.php','wp-login.php','log.txt','update.php','INSTALL.pgsql.txt','user/login/',
    'INSTALL.txt','profiles/','scripts/','LICENSE.txt','CHANGELOG.txt','themes/','includes/','misc/','user/logout/','user/register/','cron.php','filter/tips/',
    'comment/reply/','xmlrpc.php','modules/','install.php','MAINTAINERS.txt','user/password/','node/add/','INSTALL.sqlite.txt','UPGRADE.txt','INSTALL.mysql.txt'
]

ADMIN_PATHS = [
    'admin/','administrator/','login.php','administration/','admin1/','admin2/','admin3/','admin4/','admin5/','moderator/','webadmin/','adminarea/','bb-admin/','adminLogin/','admin_area/','panel-administracion/','instadmin/',
    'memberadmin/','administratorlogin/','adm/','account.asp','admin/account.asp','admin/index.asp','admin/login.asp','admin/admin.asp','/login.aspx',
    'admin_area/admin.asp','admin_area/login.asp','admin/account.html','admin/index.html','admin/login.html','admin/admin.html',
    'admin_area/admin.html','admin_area/login.html','admin_area/index.html','admin_area/index.asp','bb-admin/index.asp','bb-admin/login.asp','bb-admin/admin.asp',
    'bb-admin/index.html','bb-admin/login.html','bb-admin/admin.html','admin/home.html','admin/controlpanel.html','admin.html','admin/cp.html','cp.html',
    'administrator/index.html','administrator/login.html','administrator/account.html','administrator.html','login.html','modelsearch/login.html','moderator.html',
    'moderator/login.html','moderator/admin.html','account.html','controlpanel.html','admincontrol.html','admin_login.html','panel-administracion/login.html',
    'admin/home.asp','admin/controlpanel.asp','admin.asp','pages/admin/admin-login.asp','admin/admin-login.asp','admin-login.asp','admin/cp.asp','cp.asp',
    'administrator/account.asp','administrator.asp','acceso.asp','login.asp','modelsearch/login.asp','moderator.asp','moderator/login.asp','administrator/login.asp',
    'moderator/admin.asp','controlpanel.asp','admin/account.html','adminpanel.html','webadmin.html','administration','pages/admin/admin-login.html','admin/admin-login.html',
    'webadmin/index.html','webadmin/admin.html','webadmin/login.html','user.asp','user.html','admincp/index.asp','admincp/login.asp','admincp/index.html',
    'admin/adminLogin.html','adminLogin.html','admin/adminLogin.html','home.html','adminarea/index.html','adminarea/admin.html','adminarea/login.html',
    'panel-administracion/index.html','panel-administracion/admin.html','modelsearch/index.html','modelsearch/admin.html','admin/admin_login.html',
    'admincontrol/login.html','adm/index.html','adm.html','admincontrol.asp','admin/account.asp','adminpanel.asp','webadmin.asp','webadmin/index.asp',
    'webadmin/admin.asp','webadmin/login.asp','admin/admin_login.asp','admin_login.asp','panel-administracion/login.asp','adminLogin.asp',
    'admin/adminLogin.asp','home.asp','admin.asp','adminarea/index.asp','adminarea/admin.asp','adminarea/login.asp','admin-login.html',
    'panel-administracion/index.asp','panel-administracion/admin.asp','modelsearch/index.asp','modelsearch/admin.asp','administrator/index.asp',
    'admincontrol/login.asp','adm/admloginuser.asp','admloginuser.asp','admin2.asp','admin2/login.asp','admin2/index.asp','adm/index.asp',
    'adm.asp','affiliate.asp','adm_auth.asp','memberadmin.asp','administratorlogin.asp','siteadmin/login.asp','siteadmin/index.asp','siteadmin/login.html',
    'memberadmin/','administratorlogin/','adm/','admin/account.php','admin/index.php','admin/login.php','admin/admin.php','admin/account.php',
    'admin_area/admin.php','admin_area/login.php','siteadmin/login.php','siteadmin/index.php','siteadmin/login.html','admin/account.html','admin/index.html','admin/login.html','admin/admin.html',
    'admin_area/index.php','bb-admin/index.php','bb-admin/login.php','bb-admin/admin.php','admin/home.php','admin_area/login.html','admin_area/index.html',
    'admin/controlpanel.php','admin.php','admincp/index.asp','admincp/login.asp','admincp/index.html','admin/account.html','adminpanel.html','webadmin.html',
    'webadmin/index.html','webadmin/admin.html','webadmin/login.html','admin/admin_login.html','admin_login.html','panel-administracion/login.html',
    'admin/cp.php','cp.php','administrator/index.php','administrator/login.php','nsw/admin/login.php','webadmin/login.php','admin/admin_login.php','admin_login.php',
    'administrator/account.php','administrator.php','admin_area/admin.html','pages/admin/admin-login.php','admin/admin-login.php','admin-login.php',
    'bb-admin/index.html','bb-admin/login.html','acceso.php','bb-admin/admin.html','admin/home.html','login.php','modelsearch/login.php','moderator.php','moderator/login.php',
    'moderator/admin.php','account.php','pages/admin/admin-login.html','admin/admin-login.html','admin-login.html','controlpanel.php','admincontrol.php',
    'admin/adminLogin.html','adminLogin.html','admin/adminLogin.html','home.html','rcjakar/admin/login.php','adminarea/index.html','adminarea/admin.html',
    'webadmin.php','webadmin/index.php','webadmin/admin.php','admin/controlpanel.html','admin.html','admin/cp.html','cp.html','adminpanel.php','moderator.html',
    'administrator/index.html','administrator/login.html','user.html','administrator/account.html','administrator.html','login.html','modelsearch/login.html',
    'moderator/login.html','adminarea/login.html','panel-administracion/index.html','panel-administracion/admin.html','modelsearch/index.html','modelsearch/admin.html',
    'admincontrol/login.html','adm/index.html','adm.html','moderator/admin.html','user.php','account.html','controlpanel.html','admincontrol.html',
    'panel-administracion/login.php','wp-login.php','adminLogin.php','admin/adminLogin.php','home.php','admin.php','adminarea/index.php',
    'adminarea/admin.php','adminarea/login.php','panel-administracion/index.php','panel-administracion/admin.php','modelsearch/index.php',
    'modelsearch/admin.php','admincontrol/login.php','adm/admloginuser.php','admloginuser.php','admin2.php','admin2/login.php','admin2/index.php','usuarios/login.php',
    'adm/index.php','adm.php','affiliate.php','adm_auth.php','memberadmin.php','administratorlogin.php','adm/','admin/account.cfm','admin/index.cfm','admin/login.cfm','admin/admin.cfm','admin/account.cfm',
    'admin_area/admin.cfm','admin_area/login.cfm','siteadmin/login.cfm','siteadmin/index.cfm','siteadmin/login.html','admin/account.html','admin/index.html','admin/login.html','admin/admin.html',
    'admin_area/index.cfm','bb-admin/index.cfm','bb-admin/login.cfm','bb-admin/admin.cfm','admin/home.cfm','admin_area/login.html','admin_area/index.html',
    'admin/controlpanel.cfm','admin.cfm','admincp/index.asp','admincp/login.asp','admincp/index.html','admin/account.html','adminpanel.html','webadmin.html',
    'webadmin/index.html','webadmin/admin.html','webadmin/login.html','admin/admin_login.html','admin_login.html','panel-administracion/login.html',
    'admin/cp.cfm','cp.cfm','administrator/index.cfm','administrator/login.cfm','nsw/admin/login.cfm','webadmin/login.cfm','admin/admin_login.cfm','admin_login.cfm',
    'administrator/account.cfm','administrator.cfm','admin_area/admin.html','pages/admin/admin-login.cfm','admin/admin-login.cfm','admin-login.cfm',
    'bb-admin/index.html','bb-admin/login.html','bb-admin/admin.html','admin/home.html','login.cfm','modelsearch/login.cfm','moderator.cfm','moderator/login.cfm',
    'moderator/admin.cfm','account.cfm','pages/admin/admin-login.html','admin/admin-login.html','admin-login.html','controlpanel.cfm','admincontrol.cfm',
    'admin/adminLogin.html','acceso.cfm','adminLogin.html','admin/adminLogin.html','home.html','rcjakar/admin/login.cfm','adminarea/index.html','adminarea/admin.html',
    'webadmin.cfm','webadmin/index.cfm','webadmin/admin.cfm','admin/controlpanel.html','admin.html','admin/cp.html','cp.html','adminpanel.cfm','moderator.html',
    'administrator/index.html','administrator/login.html','user.html','administrator/account.html','administrator.html','login.html','modelsearch/login.html',
    'moderator/login.html','adminarea/login.html','panel-administracion/index.html','panel-administracion/admin.html','modelsearch/index.html','modelsearch/admin.html',
    'admincontrol/login.html','adm/index.html','adm.html','moderator/admin.html','user.cfm','account.html','controlpanel.html','admincontrol.html',
    'panel-administracion/login.cfm','wp-login.cfm','adminLogin.cfm','admin/adminLogin.cfm','home.cfm','admin.cfm','adminarea/index.cfm',
    'adminarea/admin.cfm','adminarea/login.cfm','panel-administracion/index.cfm','panel-administracion/admin.cfm','modelsearch/index.cfm',
    'modelsearch/admin.cfm','admincontrol/login.cfm','adm/admloginuser.cfm','admloginuser.cfm','admin2.cfm','admin2/login.cfm','admin2/index.cfm','usuarios/login.cfm',
    'adm/index.cfm','adm.cfm','affiliate.cfm','adm_auth.cfm','memberadmin.cfm','administratorlogin.cfm','adminLogin/','admin_area/','panel-administracion/','instadmin/','login.aspx',
    'memberadmin/','administratorlogin/','adm/','admin/account.aspx','admin/index.aspx','admin/login.aspx','admin/admin.aspx','admin/account.aspx',
    'admin_area/admin.aspx','admin_area/login.aspx','siteadmin/login.aspx','siteadmin/index.aspx','siteadmin/login.html','admin/account.html','admin/index.html','admin/login.html','admin/admin.html',
    'admin_area/index.aspx','bb-admin/index.aspx','bb-admin/login.aspx','bb-admin/admin.aspx','admin/home.aspx','admin_area/login.html','admin_area/index.html',
    'admin/controlpanel.aspx','admin.aspx','admincp/index.asp','admincp/login.asp','admincp/index.html','admin/account.html','adminpanel.html','webadmin.html',
    'webadmin/index.html','webadmin/admin.html','webadmin/login.html','admin/admin_login.html','admin_login.html','panel-administracion/login.html',
    'admin/cp.aspx','cp.aspx','administrator/index.aspx','administrator/login.aspx','nsw/admin/login.aspx','webadmin/login.aspx','admin/admin_login.aspx','admin_login.aspx',
    'administrator/account.aspx','administrator.aspx','admin_area/admin.html','pages/admin/admin-login.aspx','admin/admin-login.aspx','admin-login.aspx',
    'bb-admin/index.html','bb-admin/login.html','bb-admin/admin.html','admin/home.html','login.aspx','modelsearch/login.aspx','moderator.aspx','moderator/login.aspx',
    'moderator/admin.aspx','acceso.aspx','account.aspx','pages/admin/admin-login.html','admin/admin-login.html','admin-login.html','controlpanel.aspx','admincontrol.aspx',
    'admin/adminLogin.html','adminLogin.html','admin/adminLogin.html','home.html','rcjakar/admin/login.aspx','adminarea/index.html','adminarea/admin.html',
    'webadmin.aspx','webadmin/index.aspx','webadmin/admin.aspx','admin/controlpanel.html','admin.html','admin/cp.html','cp.html','adminpanel.aspx','moderator.html',
    'administrator/index.html','administrator/login.html','user.html','administrator/account.html','administrator.html','login.html','modelsearch/login.html',
    'moderator/login.html','adminarea/login.html','panel-administracion/index.html','panel-administracion/admin.html','modelsearch/index.html','modelsearch/admin.html',
    'admincontrol/login.html','adm/index.html','adm.html','moderator/admin.html','user.aspx','account.html','controlpanel.html','admincontrol.html',
    'panel-administracion/login.aspx','wp-login.aspx','adminLogin.aspx','admin/adminLogin.aspx','home.aspx','admin.aspx','adminarea/index.aspx',
    'adminarea/admin.aspx','adminarea/login.aspx','panel-administracion/index.aspx','panel-administracion/admin.aspx','modelsearch/index.aspx',
    'modelsearch/admin.aspx','admincontrol/login.aspx','adm/admloginuser.aspx','admloginuser.aspx','admin2.aspx','admin2/login.aspx','admin2/index.aspx','usuarios/login.aspx',
    'adm/index.aspx','adm.aspx','affiliate.aspx','adm_auth.aspx','memberadmin.aspx','administratorlogin.aspx','memberadmin/','administratorlogin/','adm/','admin/account.js','admin/index.js','admin/login.js','admin/admin.js','admin/account.js',
    'admin_area/admin.js','admin_area/login.js','siteadmin/login.js','siteadmin/index.js','siteadmin/login.html','admin/account.html','admin/index.html','admin/login.html','admin/admin.html',
    'admin_area/index.js','bb-admin/index.js','bb-admin/login.js','bb-admin/admin.js','admin/home.js','admin_area/login.html','admin_area/index.html',
    'admin/controlpanel.js','admin.js','admincp/index.asp','admincp/login.asp','admincp/index.html','admin/account.html','adminpanel.html','webadmin.html',
    'webadmin/index.html','webadmin/admin.html','webadmin/login.html','admin/admin_login.html','admin_login.html','panel-administracion/login.html',
    'admin/cp.js','cp.js','administrator/index.js','administrator/login.js','nsw/admin/login.js','webadmin/login.js','admin/admin_login.js','admin_login.js',
    'administrator/account.js','administrator.js','admin_area/admin.html','pages/admin/admin-login.js','admin/admin-login.js','admin-login.js',
    'bb-admin/index.html','bb-admin/login.html','bb-admin/admin.html','admin/home.html','login.js','modelsearch/login.js','moderator.js','moderator/login.js',
    'moderator/admin.js','account.js','pages/admin/admin-login.html','admin/admin-login.html','admin-login.html','controlpanel.js','admincontrol.js',
    'admin/adminLogin.html','adminLogin.html','admin/adminLogin.html','home.html','rcjakar/admin/login.js','adminarea/index.html','adminarea/admin.html',
    'webadmin.js','webadmin/index.js','acceso.js','webadmin/admin.js','admin/controlpanel.html','admin.html','admin/cp.html','cp.html','adminpanel.js','moderator.html',
    'administrator/index.html','administrator/login.html','user.html','administrator/account.html','administrator.html','login.html','modelsearch/login.html',
    'moderator/login.html','adminarea/login.html','panel-administracion/index.html','panel-administracion/admin.html','modelsearch/index.html','modelsearch/admin.html',
    'admincontrol/login.html','adm/index.html','adm.html','moderator/admin.html','user.js','account.html','controlpanel.html','admincontrol.html',
    'panel-administracion/login.js','wp-login.js','adminLogin.js','admin/adminLogin.js','home.js','admin.js','adminarea/index.js',
    'adminarea/admin.js','adminarea/login.js','panel-administracion/index.js','panel-administracion/admin.js','modelsearch/index.js',
    'modelsearch/admin.js','admincontrol/login.js','adm/admloginuser.js','admloginuser.js','admin2.js','admin2/login.js','admin2/index.js','usuarios/login.js',
    'adm/index.js','adm.js','affiliate.js','adm_auth.js','memberadmin.js','administratorlogin.js','bb-admin/index.cgi','bb-admin/login.cgi','bb-admin/admin.cgi','admin/home.cgi','admin_area/login.html','admin_area/index.html',
    'admin/controlpanel.cgi','admin.cgi','admincp/index.asp','admincp/login.asp','admincp/index.html','admin/account.html','adminpanel.html','webadmin.html',
    'webadmin/index.html','webadmin/admin.html','webadmin/login.html','admin/admin_login.html','admin_login.html','panel-administracion/login.html',
    'admin/cp.cgi','cp.cgi','administrator/index.cgi','administrator/login.cgi','nsw/admin/login.cgi','webadmin/login.cgi','admin/admin_login.cgi','admin_login.cgi',
    'administrator/account.cgi','administrator.cgi','admin_area/admin.html','pages/admin/admin-login.cgi','admin/admin-login.cgi','admin-login.cgi',
    'bb-admin/index.html','bb-admin/login.html','bb-admin/admin.html','admin/home.html','login.cgi','modelsearch/login.cgi','moderator.cgi','moderator/login.cgi',
    'moderator/admin.cgi','account.cgi','pages/admin/admin-login.html','admin/admin-login.html','admin-login.html','controlpanel.cgi','admincontrol.cgi',
    'admin/adminLogin.html','adminLogin.html','admin/adminLogin.html','home.html','rcjakar/admin/login.cgi','adminarea/index.html','adminarea/admin.html',
    'webadmin.cgi','webadmin/index.cgi','acceso.cgi','webadmin/admin.cgi','admin/controlpanel.html','admin.html','admin/cp.html','cp.html','adminpanel.cgi','moderator.html',
    'administrator/index.html','administrator/login.html','user.html','administrator/account.html','administrator.html','login.html','modelsearch/login.html',
    'moderator/login.html','adminarea/login.html','panel-administracion/index.html','panel-administracion/admin.html','modelsearch/index.html','modelsearch/admin.html',
    'admincontrol/login.html','adm/index.html','adm.html','moderator/admin.html','user.cgi','account.html','controlpanel.html','admincontrol.html',
    'panel-administracion/login.cgi','wp-login.cgi','adminLogin.cgi','admin/adminLogin.cgi','home.cgi','admin.cgi','adminarea/index.cgi',
    'adminarea/admin.cgi','adminarea/login.cgi','panel-administracion/index.cgi','panel-administracion/admin.cgi','modelsearch/index.cgi',
    'modelsearch/admin.cgi','admincontrol/login.cgi','adm/admloginuser.cgi','admloginuser.cgi','admin2.cgi','admin2/login.cgi','admin2/index.cgi','usuarios/login.cgi',
    'adm/index.cgi','adm.cgi','affiliate.cgi','adm_auth.cgi','memberadmin.cgi','administratorlogin.cgi','admin_area/admin.brf','admin_area/login.brf','siteadmin/login.brf','siteadmin/index.brf','siteadmin/login.html','admin/account.html','admin/index.html','admin/login.html','admin/admin.html',
    'admin_area/index.brf','bb-admin/index.brf','bb-admin/login.brf','bb-admin/admin.brf','admin/home.brf','admin_area/login.html','admin_area/index.html',
    'admin/controlpanel.brf','admin.brf','admincp/index.asp','admincp/login.asp','admincp/index.html','admin/account.html','adminpanel.html','webadmin.html',
    'webadmin/index.html','webadmin/admin.html','webadmin/login.html','admin/admin_login.html','admin_login.html','panel-administracion/login.html',
    'admin/cp.brf','cp.brf','administrator/index.brf','administrator/login.brf','nsw/admin/login.brf','webadmin/login.brfbrf','admin/admin_login.brf','admin_login.brf',
    'administrator/account.brf','administrator.brf','acceso.brf','admin_area/admin.html','pages/admin/admin-login.brf','admin/admin-login.brf','admin-login.brf',
    'bb-admin/index.html','bb-admin/login.html','bb-admin/admin.html','admin/home.html','login.brf','modelsearch/login.brf','moderator.brf','moderator/login.brf',
    'moderator/admin.brf','account.brf','pages/admin/admin-login.html','admin/admin-login.html','admin-login.html','controlpanel.brf','admincontrol.brf',
    'admin/adminLogin.html','adminLogin.html','admin/adminLogin.html','home.html','rcjakar/admin/login.brf','adminarea/index.html','adminarea/admin.html',
    'webadmin.brf','webadmin/index.brf','webadmin/admin.brf','admin/controlpanel.html','admin.html','admin/cp.html','cp.html','adminpanel.brf','moderator.html',
    'administrator/index.html','administrator/login.html','user.html','administrator/account.html','administrator.html','login.html','modelsearch/login.html',
    'moderator/login.html','adminarea/login.html','panel-administracion/index.html','panel-administracion/admin.html','modelsearch/index.html','modelsearch/admin.html',
    'admincontrol/login.html','adm/index.html','adm.html','moderator/admin.html','user.brf','account.html','controlpanel.html','admincontrol.html',
    'panel-administracion/login.brf','wp-login.brf','adminLogin.brf','admin/adminLogin.brf','home.brf','admin.brf','adminarea/index.brf',
    'adminarea/admin.brf','adminarea/login.brf','panel-administracion/index.brf','panel-administracion/admin.brf','modelsearch/index.brf',
    'modelsearch/admin.brf','admincontrol/login.brf','adm/admloginuser.brf','admloginuser.brf','admin2.brf','admin2/login.brf','admin2/index.brf','usuarios/login.brf',
    'adm/index.brf','adm.brf','affiliate.brf','adm_auth.brf','memberadmin.brf','administratorlogin.brf','cpanel','cpanel.php','cpanel.html',
]

WP_PLUGINS = [
    "wordpress-importer","regenerate-thumbnails","wp-super-cache","jetpack","wordfence","wordpress-seo","tinymce-advanced","akismet","google-sitemap-generator",
    "google-analytics-for-wordpress","contact-form-7","duplicate-post","wp-pagenavi","advanced-custom-fields","hello-dolly","nextgen-gallery","woocommerce",
    "all-in-one-seo-pack","w3-total-cache","really-simple-captcha","siteorigin-panels","disable-comments","wp-multibyte-patch","google-analytics-dashboard-for-wp",
    "black-studio-tinymce-widget","updraftplus","better-wp-security","wpclef","duplicator","ml-slider","googleanalytics","so-widgets-bundle","shortcodes-ultimate",
    "redirection","ninja-forms","mailchimp-for-wp","breadcrumb-navxt","wp-mail-smtp","wp-optimize","wp-db-backup","backwpup","image-widget","broken-link-checker",
    "si-contact-form","wp-smushit","tablepress","contact-form-7-to-database-extension","the-events-calendar","google-analyticator","wp-maintenance-mode","iwp-client",
    "all-in-one-wp-security-and-firewall","post-types-order","wptouch","formidable","user-role-editor","captcha","wysija-newsletters","ewww-image-optimizer",
    "force-regenerate-thumbnails","bbpress","custom-post-type-ui","add-to-any","page-links-to","yet-another-related-posts-plugin","wp-google-maps","widget-logic",
    "yith-woocommerce-wishlist","si-captcha-for-wordpress","simple-page-ordering","contact-form-plugin","simple-custom-css","easy-google-fonts","types",
    "disqus-comment-system","wp-statistics","photo-gallery","quick-pagepost-redirect-plugin","easy-fancybox","maintenance","seo-ultimate","cookie-law-info",
    "sucuri-scanner","backupwordpress","redux-framework","antispam-bee","wp-clone-by-wp-academy","seo-image","instagram-feed","responsive-lightbox",
    "ps-auto-sitemap","display-widgets","wordpress-popular-posts","worker","woosidebars","newsletter","wp-postviews","login-lockdown","wp-user-avatar",
    "coming-soon","bwp-google-xml-sitemaps","recent-tweets-widget","addthis","social-media-widget","custom-sidebars","velvet-blues-update-urls","admin-menu-editor",
    "buddypress","simple-social-icons","loco-translate","pretty-link","enable-media-replace","custom-facebook-feed","genesis-simple-edits","sidekick",
    "php-code-widget","simple-301-redirects","taxonomy-terms-order","wp-retina-2x","mainwp-child","social-networks-auto-poster-facebook-twitter-g",
    "simple-share-buttons-adder","all-in-one-wp-migration","underconstruction","adminimize","widget-importer-exporter","google-publisher","cookie-notice",
    "polylang","wp-google-fonts","wp-dbmanager","wp-polls","simple-tags","official-statcounter-plugin-for-wordpress","social-media-feather","mailchimp",
    "meta-box","wp-spamshield","wp-migrate-db","wp-fastest-cache","anti-spam","ultimate-coming-soon-page","simple-lightbox","gotmls","autoptimize",
    "shareaholic","wp-edit","loginizer","share-this","youtube-embed-plus","slideshow-jquery-image-gallery","mappress-google-maps-for-wordpress",
    "ultimate-tinymce","wp-slimstat","insert-headers-and-footers","intuitive-custom-post-order","search-and-replace","wordpress-23-related-posts-plugin",
    "wp-lightbox-2","imsanity","options-framework","recent-posts-widget-extended","auto-post-thumbnail","contact-form-7-honeypot","members",
    "title-remover","theme-my-login","p3-profiler","easy-theme-and-plugin-upgrades","add-meta-tags","sumome","slider-image","comprehensive-google-map-plugin",
    "spacer","sg-cachepress","mce-table-buttons","amoforms","wp-social-bookmarking-light","all-in-one-event-calendar","iframe","wordpress-ping-optimizer",
    "wp-sitemap-page","google-sitemap-plugin","wp-security-scan","facebook-like-box-widget","pubsubhubbub","rename-wp-login","events-manager",
    "video-thumbnails","wp-instagram-widget","bulletproof-security","antivirus","facebook-comments-plugin","insert-php","pirate-forms","wp-editor",
    "column-shortcodes","visual-form-builder","white-label-cms","yith-woocommerce-ajax-search","easy-wp-smtp","better-search-replace","theme-check",
    "fancybox-for-wordpress","virtue-toolkit","xml-sitemap-feed","wordpress-backup-to-dropbox","cloudflare","password-protected","yith-woocommerce-compare",
    "list-category-posts","cornerstone","advanced-code-editor","wp-jquery-lightbox","seo-automatic-links","revision-control","addquicktag","qtranslate-x",
    "use-any-font","google-maps-widget","relevanssi","wp-postratings","cyr3lat","favicon-by-realfavicongenerator","simple-custom-post-order",
    "custom-field-template","subscribe2","easy-table","google-language-translator","use-google-libraries","wp-jalali","google-document-embedder",
    "easy-facebook-likebox","genesis-simple-hooks","simple-social-buttons","blogger-importer","disable-google-fonts","contact-form-7-datepicker",
    "responsive-add-ons","ckeditor-for-wordpress","post-duplicator","yith-woocommerce-zoom-magnifier","advanced-excerpt","soliloquy-lite","easing-slider",
    "genesis-enews-extended","custom-login","ps-disable-auto-formatting","cms-tree-page-view","search-everything","flamingo","gallery-plugin",
    "smart-youtube","meteor-slides","count-per-day","wp-tab-widget","contact-form-builder","reveal-ids-for-wp-admin-25","dynamic-widgets","wp-review",
    "automatic-updater","simple-image-widget","download-manager","master-slider","wp-recaptcha","wp-to-twitter","spam-free-wordpress","category-posts",
    "tweet-old-post","bwp-minify","pushpress","child-theme-configurator","oauth-twitter-feed-for-developers","responsive-menu","genesis-responsive-slider",
    "cyclone-slider-2","lightbox-gallery","siteguard","postman-smtp","add-from-server","peters-login-redirect","secure-wordpress","q2w3-fixed-widget",
    "wp-shortcode","auto-terms-of-service-and-privacy-policy","option-tree","yith-woocommerce-ajax-navigation","megamenu","ultimate-social-media-icons",
    "custom-permalinks","beaver-builder-lite-version","get-the-image","all-404-redirect-to-homepage","table-of-contents-plus","wp-paginate",
    "timthumb-vulnerability-scanner","one-click-child-theme","sitemap","xcloner-backup-and-restore","nav-menu-roles","uk-cookie-consent","form-maker",
    "hide-title","contextual-related-posts","csv-importer","stops-core-theme-and-plugin-updates","google-calendar-events","jquery-colorbox","header-footer",
    "display-posts-shortcode","404-to-start","login-customizer","widgets-on-pages","download-monitor","custom-contact-forms","feedwordpress",
    "zopim-live-chat","gallery-images","enhanced-media-library","subscribe-to-comments","facebook-pagelike-widget","wp-video-lightbox","newstatpress",
    "simple-image-sizes","better-delete-revision","wp-job-manager","wp-google-map-plugin","wp-members","maxbuttons","search-regex","widget-css-classes",
    "foobox-image-lightbox","nextend-facebook-connect","menu-icons","wpremote","amr-shortcode-any-widget","widget-settings-importexport",
    "easy-twitter-feed-widget","wp-piwik","enhanced-text-widget","bad-behavior","really-simple-csv-importer","block-bad-queries","testimonials-widget",
    "wp-smtp","printfriendly","email-address-encoder","exploit-scanner","portfolio-post-type","widget-context","sidebar-login","smk-sidebar-generator",
    "accesspress-social-icons","custom-post-type-permalinks","taxonomy-metadata","multiple-post-thumbnails","codepress-admin-columns","lazy-load",
    "baidu-sitemap-generator","sexybookmarks","404-to-301","floating-social-media-icon","categories-images","lockdown-wp-admin",
    "wpcat2tag-importer","asesor-cookies-para-la-ley-en-espana","wordpress-popup","404-redirection","twitter-widget-pro",
    "disable-xml-rpc-pingback","tiny-compress-images","rvg-optimize-database","movabletype-importer","jquery-collapse-o-matic","head-cleaner",
    "wp-clean-up","testimonials-by-woothemes","wassup","advanced-access-manager","user-switching","clean-and-simple-contact-form-by-meg-nicholas",
    "adrotate","verify-google-webmaster-tools","no-category-base-wpml","email-subscribers","login-with-ajax","editorial-calendar","amp",
    "google-analytics-dashboard","wp-e-commerce","eu-cookie-law","advanced-responsive-video-embedder","growmap-anti-spambot-plugin",
    "cryout-theme-settings","post-expirator","nk-google-analytics","wp-construction-mode","instagram-slider-widget","easy-digital-downloads",
    "hyper-cache","bulk-delete","envira-gallery-lite","easy-bootstrap-shortcodes","twitter","wp-database-backup","jquery-updater",
    "edit-author-slug","youtube-channel-gallery","wp-responsive-menu","powerpress","wpfront-user-role-editor","wp-copyprotect","wp-hide-post",
    "syntaxhighlighter","simple-page-sidebars","leaflet-maps-marker","contact-form-7-dynamic-text-extension","google-captcha",
    "remove-query-strings-from-static-resources","clone-posts","wp-product-review","crayon-syntax-highlighter","genesis-simple-sidebars",
    "wp-all-import","paid-memberships-pro","wordpress-simple-paypal-shopping-cart","page-list","disable-xml-rpc","wp-spamfree",
    "dynamic-featured-image","uber-login-logo","woocommerce-pdf-invoices-packing-slips","popup-maker","wp-author-date-and-meta-remover",
    "wp125","recent-posts-widget-with-thumbnails","portfolio-gallery","facebook-button-plugin","wp-customer-reviews","simple-sitemap",
    "accesspress-social-share","rss-importer","duracelltomi-google-tag-manager","wp-photo-album-plus","wp-subscribe",
    "hupso-share-buttons-for-twitter-facebook-google","social-media-builder","post-thumbnail-editor","adminer","contact-form-to-email",
    "feedburner-plugin","foogallery","contact-form-maker","wordpress-social-login","easy-adsense-lite","raw-html","zencache",
    "wps-hide-login","mailchimp-forms-by-mailmunch","slideshow-gallery","post-type-archive-links","related-posts","wp-gallery-custom-links",
    "user-photo","like-box","no-comments","coming-soon-maintenance-mode-from-acurax","tubepress","pdf-embedder","easy-social-icons",
    "woocommerce-multilingual","eps-301-redirects","cleantalk-spam-protect","wp-google-analytics","user-access-manager",
    "accesspress-social-counter","font","really-simple-facebook-twitter-share-buttons","backup","facebook-conversion-pixel",
    "dynamic-to-top","wp-total-hacks","profile-builder","scroll-back-to-top","yikes-inc-easy-mailchimp-extender","wp-add-custom-css",
    "paypal-donations","resize-image-after-upload","ad-injection","flash-album-gallery","post-type-switcher","favicon-rotator",
    "feed-them-social","slider-wd","wp-pagenavi-style","visitor-maps","flickr-rss","wysiwyg-widgets","wp-print","multi-plugin-installer",
    "bruteprotect","coming-soon-page","so-css","woocommerce-delivery-notes","wp-mail-bank","search-meter","wp-filebase","lightbox",
    "widget-shortcode","html-sitemap","all-in-one-schemaorg-rich-snippets","s2member","compact-wp-audio-player","bj-lazy-load",
    "wp-content-copy-protector","alpine-photo-tile-for-instagram","pods","site-is-offline-plugin","capability-manager-enhanced",
    "multi-device-switcher","remove-category-url","call-now-button","gzip-ninja-speed-compression","gtranslate","menu-image",
    "wordpress-database-reset","bootstrap-3-shortcodes","wp-rss-aggregator","ssh-sftp-updater-support","my-calendar",
    "wonderm00ns-simple-facebook-open-graph-tags","event-organiser","youtube-embed","wp-simple-firewall","woocommerce-customizer",
    "wpmandrill","easy-testimonials","gallery-video","woocommerce-grid-list-toggle","calendar","formget-contact-form",
    "content-views-query-and-display-post-page","baw-login-logout-menu","wufoo-shortcode","any-mobile-theme-switcher",
    "wp-content-copy-protection","oa-social-login","twitter-facebook-google-plusone-share","php-text-widget","spider-event-calendar",
    "top-10","wp-crontrol","json-api","features-by-woothemes","dropdown-menu-widget","simple-map","theme-junkie-custom-css",
    "pixtypes","social-sharing-toolkit","pinterest-pin-it-button","advanced-wp-columns","mashsharer","weaver-ii-theme-extras",
    "cmb2","wp-updates-notifier","ultimate-posts-widget","wp-security-audit-log","advanced-iframe","no-page-comment",
    "newsletter-sign-up","ag-custom-admin","varnish-http-purge","wp-useronline","easy-smooth-scroll-links","theme-test-drive",
    "video-embed-thumbnail-generator","gallery-bank","stop-spammer-registrations-plugin","awesome-weather","simple-history",
    "baw-post-views-count","wpide","posts-in-page","styles","custom-post-widget","crazy-bone","php-code-for-posts",
    "audit-trail","magee-shortcodes","related-posts-thumbnails","flexi-pages-widget","font-awesome-4-menus",
    "acurax-social-media-widget","smart-slider-3","tabby-responsive-tabs","woocommerce-checkout-manager","delete-all-comments",
    "page-scroll-to-id","woocommerce-menu-bar-cart","contact-widgets","templatesnext-toolkit","debug-bar","genesis-title-toggle",
    "ditty-news-ticker","ozh-admin-drop-down-menu","wowslider","mw-wp-form","rotatingtweets","better-analytics",
    "woocommerce-colors","ultimate-member","advanced-image-styles","ultimate-maintenance-mode","aqua-page-builder","fourteen-colors",
    "bwp-recaptcha","booking","video-sidebar-widgets","dropbox-backup","wp-admin-ui-customize","disable-emojis",
    "custom-field-suite","rocket-maintenance-mode","admin-menu-tree-page-view","lightweight-social-icons","nginx-helper",
    "wc-shortcodes","content-aware-sidebars","all-in-one-webmaster","insert-html-snippet","kk-star-ratings",
    "add-link-to-facebook","contact-bank","accesspress-twitter-feed","really-simple-ssl","only-tweet-like-share-and-google-1",
    "rss-includes-pages","ultimate-social-media-plus","woocommerce-google-analytics-integration","pixcodes","wunderground",
    "ultimate-form-builder-lite","facebook-auto-publish","ultimate-responsive-image-slider","social-count-plus","statify",
    "new-google-plus-badge-widget","remove-google-fonts-references","easy-pie-maintenance-mode","wp-flexible-map",
    "my-custom-css","commentluv","codepeople-post-map","responsive-select-menu","mp3-jplayer","safe-redirect-manager",
    "ad-inserter","svg-vector-icon-plugin","advanced-random-posts-widget","flexible-posts-widget",
    "transposh-translation-filter-for-wordpress","google-maps","wp-insert","italy-cookie-choices",
    "subscribe-to-comments-reloaded","popups","nextcellent-gallery-nextgen-legacy","ultimate-category-excluder",
    "dirtysuds-embed-pdf","heartbeat-control","easy-pricing-tables","bm-custom-login","woocommerce-all-in-one-seo-pack",
    "easy-watermark","speed-booster-pack","aryo-activity-log","pc-robotstxt","clicky","kiwi-logo-carousel",
    "gallery-by-supsystic","disable-feeds","related-posts-by-zemanta","tiled-gallery-carousel-without-jetpack",
    "erident-custom-login-and-dashboard","one-click-close-comments","under-construction-wp","better-font-awesome",
    "easy-pie-coming-soon","nofollow","login-security-solution","add-logo-to-admin","attachments",
    "sendgrid-email-delivery-simplified","sem-external-links","fonts","ga-google-analytics",
    "carousel-without-jetpack","media-library-assistant","kimili-flash-embed","smooth-slider","custom-meta-widget",
    "rss-footer","facebook-members","acf-field-date-time-picker","floating-social-bar","vaultpress","iq-block-country",
    "ssl-insecure-content-fixer","fruitful-shortcodes","genesis-favicon-uploader","jquery-pin-it-button-for-images",
    "amazon-web-services","woocommerce-csvimport","show-hide-author","facebook-page-promoter-lightbox",
    "customizer-export-import","extended-categories-widget","unyson","simple-follow-me-social-buttons-widget",
    "simply-exclude","svg-support","tracking-code-manager","menu-social-icons","homepage-control","wp-sendgrid",
    "wp-noexternallinks","wp-sticky","recent-facebook-posts","wp-super-cache-clear-cache-menu","saphali-woocommerce-lite",
    "wordpress-mobile-pack","wp-twitter-feeds","manual-image-crop","youtube-widget-responsive","yuzo-related-post",
    "image-watermark","wp-better-emails","simple-google-map","easy-coming-soon","easy-social-share-buttons",
    "intergeo-maps","duplicate-page-and-post","wp-external-links","testimonial-rotator","simply-instagram",
    "jquery-t-countdown-widget","wpgform","landing-pages","wp-share-buttons-analytics-by-getsocial","woocommerce-exporter",
    "footer-putter","favicon-xt-manager","itro-popup","buddypress-media","comet-cache","wordpress-access-control",
    "remove-dashboard-access-for-non-admins","gantry","super-socializer","bulk-page-creator","gwolle-gb","drafts-scheduler",
    "open-external-links-in-a-new-window","meta-manager","facebook-by-weblizar","hide-admin-bar-from-non-admins",
    "fv-top-level-cats","smart-slider-2","kebo-twitter-feed","yop-poll","persian-woocommerce","schema-creator",
    "optinmonster","code-snippets","embedplus-for-wordpress","calculated-fields-form","contact-form-7-mailchimp-extension",
    "quotes-collection","wp-performance-score-booster","wp-fail2ban","google","tawkto-live-chat","stealth-login-page",
    "metronet-reorder-posts","admin-management-xtended","newpost-catch","showcase-visual-composer-addon",
    "jquery-smooth-scroll","post-snippets","child-themify","global-content-blocks","bootstrap-for-contact-form-7",
    "custom-menu-wizard","wpfront-scroll-top","caldera-forms","simple-full-screen-background-image","fv-wordpress-flowplayer",
    "wp-pro-quiz","link-library","custom-favicon","wp-facebook-open-graph-protocol","wp-site-migrate","featured-video-plus",
    "mail-subscribe-list","woocommerce-product-archive-customiser","ad-widget","woocommerce-pagseguro",
    "orbisius-child-theme-creator","wordpress-reset","custom-share-buttons-with-floating-sidebar","woocommerce-jetpack",
    "email-encoder-bundle","addon-so-widgets-bundle","logo-slider","google-universal-analytics","rest-api","wp-ban",
    "strictly-autotags","contact-form-email","simple-twitter-tweets","ifeature-slider","restricted-site-access",
    "image-slider-widget","user-submitted-posts","easy-modal","rus-to-lat-advanced","wp-live-chat-support",
    "stats-counter","backup-with-restore","projects-by-woothemes","wp-htaccess-control","lj-maintenance-mode",
    "advanced-post-slider","gregs-high-performance-seo","wp-sweep","qtranslate-slug","google-maps-easy","grand-media",
    "widgetize-pages-light","visitors-traffic-real-time-statistics","what-the-file","taxonomy-images","cpt-bootstrap-carousel",
    "amazon-s3-and-cloudfront","polldaddy","wp-seo-qtranslate-x","cachify","robo-gallery","shortpixel-image-optimiser",
    "posts-to-posts","rich-text-tags","co-authors-plus","easy-video-player","soundcloud-is-gold","go-live-update-urls",
    "squirrly-seo","ecwid-shopping-cart","shortcoder","wp-math-captcha","genesis-translations","hide-my-site",
    "paypal-for-woocommerce","advanced-sidebar-menu","yith-maintenance-mode","duplicate-menu","wp-email-login",
    "simple-facebook-plugin","admin-custom-login","cimy-user-extra-fields","contact-form-manager",
    "wordpress-easy-paypal-payment-or-donation-accept-plugin","wp-backitup","yith-woocommerce-quick-view",
    "brute-force-login-protection","super-simple-google-analytics","wp-limit-login-attempts","header-and-footer-scripts",
    "wordpress-language","i-recommend-this","wc-gallery","business-directory-plugin","js-composer-qtranslate-x","customify",
    "advanced-ads","woocommerce-sequential-order-numbers","zero-spam","website-monetization-by-magenet","sydney-toolbox",
    "groups","pagerestrict","bootstrap-shortcodes","css-javascript-toolbox","easy-image-gallery","analytics-counter",
    "admin-post-navigation","horizontal-scrolling-announcement","woocommerce-shortcodes","mailgun","wordpress-social-ring",
    "embed-any-document","magic-fields-2","wangguard","disable-wordpress-updates","vanilla-pdf-embed","postie",
    "email-before-download","juiz-social-post-sharer","simple-maintenance-mode","yandex-metrika","breadcrumb-trail",
    "wp-job-manager-contact-listing","social-share-buttons-by-supsystic","wp-maintenance","trust-form","sqlite-integration",
    "social-media-icons-widget","captcha-on-login","post-views-counter","typekit-fonts-for-wordpress","alo-easymail",
    "udinra-all-image-sitemap","youtube-channel","gigpress","rating-widget","wp-media-library-categories","wp-nested-pages",
    "simple-ads-manager","genesis-simple-share","gravity-forms-custom-post-types","faster-pagination","advanced-text-widget",
    "wplegalpages","player","json-rest-api","google-authenticator","genesis-connect-woocommerce",
    "pinterest-pin-it-button-on-image-hover-and-post","cms-commander-client","contact-form-7-add-confirm","store-locator-le",
    "ajax-load-more","facebook-thumb-fixer","instagram-for-wordpress","easy-media-gallery","wordpress-move",
    "click-to-tweet-by-todaymade","improved-include-page","woocommerce-xml-csv-product-import","wp-hide-dashboard",
    "https-redirection","formbuilder","tumblr-importer","wordpress-post-tabs","wp-job-manager-locations",
    "welcome-email-editor","columns","wp-mobile-detect","acf-qtranslate","rss-post-importer","crazyegg-heatmap-tracking",
    "our-team-enhanced","social-locker","accordion-shortcodes","seamless-donations","media-file-renamer","thesis-openhook",
    "email-newsletter","wp-stats","flickr-badges-widget","uji-countdown","check-email","wp-editor-widget","alexa-internet",
    "basic-google-maps-placemarks","wp-social-likes","synved-shortcodes","xml-sitemaps","nav-menu-images","email-users",
    "mobble","woocommerce-correios","starbox","wp-recaptcha-integration","google-maps-builder","wp-page-widget",
    "wp-social-sharing","ricg-responsive-images","new-user-approve","rss-import","nospamnx","public-post-preview",
    "shortcode-widget","popup-by-supsystic","webriti-smtp-mail","magic-action-box","multiple-content-blocks",
    "genesis-layout-extras","animate-it","simple-wp-sitemap","aweber-web-form-widget"
]



def bypass_cloudflare():
    show_banner("Bypass CloudFlare")
    print(f"{LY}[!] Enter domain (example.com - no http/https)")
    domain = input(f"{W} → ").strip()

    if not domain:
        print(f"{LR}[!] Domain required")
        input("Press Enter...")
        return

    print(f"{LG}\nScanning {len(SUBDOMAINS)} subdomains...\n")
    found = False
    for sub in SUBDOMAINS:
        try:
            host = f"{sub}.{domain}"
            ip = socket.gethostbyname(host)
            print(f"{G}[+] {ip:16} → {host}")
            found = True
        except:
            pass

    if not found:
        print(f"{Y}[!] No subdomains resolved (possibly protected)")
    input(f"{LG}\nPress Enter to return...")


def cms_detection():
    show_banner("CMS Detection")
    print(f"{LY}[!] Enter target URL (with http:// or https://)")
    url = input(f"{W} → ").strip()

    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=12, allow_redirects=True)
        content = r.text.lower()
        headers_lower = {k.lower(): v.lower() for k, v in r.headers.items()}

        if any(x in content for x in ['wp-content', 'wp-includes', 'wp-json', 'wp-']):
            print(f"{G}[+] Detected: WordPress")
        elif 'shopify' in content or 'shopify' in headers_lower.get('server', '') or 'cdn.shopify' in content:
            print(f"{G}[+] Detected: Shopify")
        elif 'drupal' in content or 'sites/default' in content:
            print(f"{G}[+] Detected: Drupal")
        elif 'joomla' in content:
            print(f"{G}[+] Detected: Joomla")
        elif 'magento' in content:
            print(f"{G}[+] Detected: Magento")
        else:
            print(f"{Y}[!] No obvious CMS detected")
            print(f"    Server: {r.headers.get('Server', 'Unknown')}")
            print(f"    X-Powered-By: {r.headers.get('X-Powered-By', 'None')}")

    except Exception as e:
        print(f"{LR}[!] Error: {str(e)}")

    input(f"{LG}\nPress Enter to return...")


def whois_lookup():
    show_banner("Whois Lookup")
    print(f"{LY}[!] Enter domain or IP")
    target = input(f"{W} → ").strip()

    try:
        r = requests.get(f'http://api.hackertarget.com/whois/?q={target}', timeout=15)
        result = r.text.strip()
        if result and len(result) > 20:
            print(f"{W}\n{result}")
        else:
            print(f"{Y}[!] No useful whois data returned")
    except Exception as e:
        print(f"{LR}[!] Failed: {str(e)}")

    input(f"{LG}\nPress Enter to return...")


def dns_lookup():
    show_banner("DNS Lookup")
    print(f"{LY}[!] Enter domain")
    target = input(f"{W} → ").strip()

    try:
        r = requests.get(f'http://api.hackertarget.com/dnslookup/?q={target}', timeout=15)
        result = r.text.strip()
        if result and len(result) > 20:
            print(f"{W}\n{result}")
        else:
            print(f"{Y}[!] No useful DNS data returned")
    except Exception as e:
        print(f"{LR}[!] Failed: {str(e)}")

    input(f"{LG}\nPress Enter to return...")


def robots_admin_scanner():
    show_banner("Robots & Admin Scanner")
    print(f"{LY}[!] Enter website (with http or https)")
    url = input(f"{W} → ").strip()

    if not url.startswith(('http://','https://')):
        url = 'http://' + url
    if not url.endswith('/'):
        url += '/'

    print(f"{LG}\nScanning common sensitive files ({len(ROBOTS_PATHS)} paths)...\n")

    for path in ROBOTS_PATHS:
        try:
            r = requests.get(url + path, timeout=7)
            if r.status_code in (200, 403, 405):
                print(f"{G}[+] {r.status_code} → {url + path}")
            elif r.status_code in (301, 302):
                print(f"{Y}[~] Redirect {r.status_code} → {url + path}")
        except:
            pass

    print(f"\n{LG}Scanning admin/login paths ({len(ADMIN_PATHS)} paths)...\nThis may take a few minutes...\n")

    for path in ADMIN_PATHS:
        try:
            r = requests.get(url + path, timeout=6, allow_redirects=True)
            if r.status_code in (200, 301, 302, 403):
                print(f"{G}[+] {r.status_code} → {url + path}")
        except:
            pass

    input(f"{LG}\nPress Enter to return...")


def main():
    show_banner()

    while True:
        show_banner("Main Menu")
        print(f"{LG}\nChoose an option:")
        print(f"{B}  1 {W}- Information Gathering")
        print(f"{B}  2 {W}- Exit\n")

        choice = input(f"{W} → ").strip()

        if choice == '2':
            print(f"{G}Goodbye!")
            sys.exit(0)

        elif choice == '1':
            while True:
                show_banner("Information Gathering")
                print(f"{LG}\nAvailable tools:")
                print(f"{B}  1 {W}- Bypass CloudFlare ")
                print(f"{B}  2 {W}- CMS Detection")
                print(f"{B}  3 {W}- Whois Lookup")
                print(f"{B}  4 {W}- DNS Lookup")
                print(f"{B}  5 {W}- Robots r")
                print(f"{B}  0 {W}- Back to Main Menu\n")

                sub = input(f"{W} → ").strip()

                if sub == '0':
                    break
                elif sub == '1':
                    bypass_cloudflare()
                elif sub == '2':
                    cms_detection()
                elif sub == '3':
                    whois_lookup()
                elif sub == '4':
                    dns_lookup()
                elif sub == '5':
                    robots_admin_scanner()
                else:
                    print(f"{LY}[!] Please select 0-5")

        else:
            print(f"{LY}[!] Please select 1 or 2")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{G}Program terminated.")


def username_osint():
    sub_banner("USERNAME OSINT")
    user = input(f"{Wh}[+] Username (press Enter to go back): {Gr}").strip()
    if not user:
        print(f"{Ye}[!] Going back...{Wh}")
        return
    print(f"\n{Gr}[*] Searching for {Ye}{user}{Gr}...{Wh}\n")

    import json
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            data_json = json.load(f)
    except Exception as e:
        print(f"{Re}[!] Failed to load data.json: {e}{Wh}")
        return

    import asyncio
    import aiohttp

    async def check_username(session, site, url_template, variation, semaphore, data_json):
        async with semaphore:
            try:
                url = url_template.format(variation)
                async with session.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5) as r:

                    error_type = data_json.get(site, {}).get("errorType", "content")

                    if error_type == "status_code":
                        if r.status in (200, 301, 302):
                            final_url = str(r.url).lower()

                            if any(word in final_url for word in ("login", "signup", "register", "auth")):
                                return None

                            return site, url
                        return None

                    text = await r.text()
                    not_found = [
                        "not found",
                        "does not exist",
                        "page unavailable",
                        "404",
                        "user not found",
                        "profile not found",
                        "doesn't exist"
                    ]

                    if not any(x in text.lower() for x in not_found):
                        return site, url

                    return None
            except:
                return None

    

    async def username_osint_async(user, data_json):
     semaphore = asyncio.Semaphore(20)
     async with aiohttp.ClientSession() as session:
        tasks = []

        base = user
        chars = ["", "_", ".", "-", "1", "2", "3", "x", "z", "official", "real"]

        variations = set()
        for c in chars:
            variations.add(f"{base}{c}")
            variations.add(f"{c}{base}")
            variations.add(f"{base}_{c}")
            variations.add(f"{c}_{base}")
            variations.add(f"{base}.{c}")
            variations.add(f"{c}.{base}")

        variations.add(base.lower())
        variations.add(base.upper())
        variations.add(base.capitalize())
        variations = list(variations)

        for site, info in data_json.items():
            url_template = info.get("url") if isinstance(info, dict) else info
            for var in variations:
                tasks.append(check_username(session, site, url_template, var, semaphore, data_json))

        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [res for res in results if isinstance(res, tuple) and res]



    found = asyncio.run(username_osint_async(user, data_json))

    if found:
        print(f"{Gr}======= FOUND ({len(found)}) =======\n")
        for name, url in found:
            print(f"{Gr}[FOUND]{Wh} {name:<25} → {url}")
    else:
        print(f"{Re}[!] No accounts found.{Wh}")

    input(f"{Wh}\nPress Enter to continue...")


def phone_osint():
    sub_banner("Phone Number OSINT")
    num = input(f"{Wh}[+] +962xxx (press Enter to go back): {Gr}").strip()

    if not num:
        return

    if not num.startswith('+'):
        num = '+' + num

    try:
        p = phonenumbers.parse(num, None)
        if not phonenumbers.is_possible_number(p):
            print(f"{Re}[!] Invalid phone number format")
            return
    except:
        print(f"{Re}[!] Phone number parsing error")
        return

    carrier_name = carrier.name_for_number(p, "en") or "Unknown"
    region_name = filter_p(geocoder.description_for_number(p, "en"))
    country_name = filter_p(geocoder.country_name_for_number(p, "en"))

    if num.startswith('+972'):
        country_name = "Palestine"
        region_name = f"{Gr}Occupied Palestine{Wh}"

    tz = timezone.time_zones_for_number(p)
    ntype = phonenumbers.number_type(p)
    line_type = "Unknown"
    if ntype == phonenumbers.PhoneNumberType.MOBILE:
        line_type = "Mobile"
    elif ntype == phonenumbers.PhoneNumberType.FIXED_LINE:
        line_type = "Fixed Line"
    elif ntype == phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE:
        line_type = "Fixed Line or Mobile"
    elif ntype == phonenumbers.PhoneNumberType.TOLL_FREE:
        line_type = "Toll Free"
    elif ntype == phonenumbers.PhoneNumberType.PREMIUM_RATE:
        line_type = "Premium Rate"
    elif ntype == phonenumbers.PhoneNumberType.SHARED_COST:
        line_type = "Shared Cost"
    elif ntype == phonenumbers.PhoneNumberType.VOIP:
        line_type = "VoIP"
    elif ntype == phonenumbers.PhoneNumberType.PERSONAL_NUMBER:
        line_type = "Personal Number"
    elif ntype == phonenumbers.PhoneNumberType.PAGER:
        line_type = "Pager"
    elif ntype == phonenumbers.PhoneNumberType.UAN:
        line_type = "UAN"
    elif ntype == phonenumbers.PhoneNumberType.VOICEMAIL:
        line_type = "Voicemail"
    elif ntype == phonenumbers.PhoneNumberType.UNKNOWN:
        line_type = "Unknown"

    result = [
        ("Country", country_name),
        ("Region/City", region_name),
        ("Carrier", carrier_name),
        ("Line Type", line_type),
        ("Timezone", list(tz)),
        ("Valid", phonenumbers.is_valid_number(p)),
        ("Possible", phonenumbers.is_possible_number(p)),
        ("E164", phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.E164)),
        ("International", phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.INTERNATIONAL)),
        ("National", phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.NATIONAL)),
        ("RFC3966", phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.RFC3966)),
        ("Number Type Code", ntype),
    ]

    print(f"\n{Wh}====== PHONE NUMBER ANALYSIS ======\n")
    for i, (k, v) in enumerate(result, 1):
        print(f"{Wh}{i:02}. {k:<20}: {Gr}{v}")

    print(f"\n{Wh}━━━━━━━━━━ COUNTRY DETAILS ━━━━━━━━━━")
    details = get_country_info(country_name)
    for k, v in details.items():
        print(f"{Wh}{k:<20}: {Gr}{v}")

    input(f"{Wh}\nPress Enter to continue...")

def device_info():
    sub_banner("Device Information")
    host = socket.gethostname()
    address_full = "N/A"

    try:
        geo_r = requests.get("https://ipwho.is/", timeout=10).json()
        if geo_r.get("success", False):
            pub_ip = geo_r.get("ip")
            lat = geo_r.get("latitude")
            lon = geo_r.get("longitude")
            city = geo_r.get("city")
            country = filter_p(geo_r.get("country"))
            maps_link = f"https://www.google.com/maps?q={lat},{lon}" if lat and lon else "N/A"

            if Nominatim:
                try:
                    geolocator = Nominatim(user_agent="Qusay_kali_tool")
                    location = geolocator.reverse(f"{lat}, {lon}", timeout=10)
                    address_full = filter_p(location.address) if location else "Not available"
                except:
                    address_full = "Geocoding timeout"
        else:
            pub_ip = "N/A"
            lat = lon = city = country = maps_link = "N/A"
    except:
        pub_ip = "Offline / Error"
        lat = lon = city = country = maps_link = "N/A"

    mem = psutil.virtual_memory() if psutil else None
    disk = psutil.disk_usage("/") if psutil else None
    mac_addr = get_mac()

    info = [
        ("Hostname", host),
        ("MAC Address", mac_addr),
        ("Public IP", pub_ip),
        ("Local IP", socket.gethostbyname(host)),
        ("Country", country),
        ("City", city),
        ("Latitude", lat),
        ("Longitude", lon),
        ("Maps Link", maps_link),
        ("Full Address", address_full),
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
    ]

    print(f"\n{Wh}========== DEVICE & LOCATION INFO ==========\n")
    for i, (k, v) in enumerate(info, 1):
        print(f"{Wh}{i:02}. {k:<18}: {Gr}{v}")

    input(f"{Wh}\nPress Enter to continue...")

def fetch_from_source(name, base_url, regex_pat, filename):
    print(f"{Ye}[+] Fetching from {name} ...{Wh}")
    links = []
    try:
        res = requests.get(base_url, headers=HEADERS, timeout=12)
        found = re.findall(regex_pat, res.text)
        cleaned = [link for link in found if len(link) > 20 and any(kw in link.lower() for kw in ["cam", "live", "webcam", "stream"])]
        links.extend(cleaned)
        if links:
            with open(filename, 'w', encoding='utf-8') as f:
                for link in links:
                    print(f"{Gr}{link}{Wh}")
                    f.write(link + '\n')
            print(f"{Gr}Saved {len(links)} links to {filename}{Wh}")
        else:
            print(f"{Re}No useful links found from {name}{Wh}")
    except Exception as e:
        print(f"{Re}Error from {name}: {e}{Wh}")
    return links

def additional_cams_menu():
    while True:
        sub_banner("Public Webcams")
        print(f"{Wh}[1]{Gr} EarthCam")
        print(f"{Wh}[2]{Gr} SkylineWebcams")
        print(f"{Wh}[3]{Gr} Opentopia")
        print(f"{Wh}[0]{Gr} Back / Exit")
        choice = input(f"\n{Wh}[+] Select source (1-3 or 0): {Gr}").strip()

        if choice == "0":
            break

        sources = {
            "1": ("EarthCam", "https://www.earthcam.com/", r'(https?://(?:www\.)?earthcam\.com[^"\s\'<>\)]+)'),
            "2": ("SkylineWebcams", "https://www.skylinewebcams.com/", r'(https?://[^"\s\'<>\)]+skylinewebcams\.com[^"\s\'<>\)]*)'),
            "3": ("Opentopia", "https://www.opentopia.com/", r'(https?://[^"\s\'<>\)]+opentopia\.com[^"\s\'<>\)]*)'),
        }

        if choice in sources:
            name, url, regex = sources[choice]
            filename = f"{name.lower()}_cams.txt"
            fetch_from_source(name, url, regex, filename)
            input(f"{Wh}Press Enter to continue...")
        else:
            print(f"{Re}[!] Invalid choice")

def cam_hacker():
    sub_banner("Cam Hacker")
    try:
        import colorama
        colorama.init()
    except ImportError:
        print(f"{Re}[!] colorama not installed. Run: pip install colorama")
        return

    url = "http://www.insecam.org/en/jsoncountries/"
    countries = {}
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        data = resp.json()
        countries = data.get('countries', {})
    except Exception as e:
        print(f"{Re}Failed to load Insecam countries: {e}")

    if countries:
        ordered = {}
        if "IL" in countries:
            ordered["PS"] = {"country": "Palestine", "count": countries["IL"]["count"]}
            del countries["IL"]
        ordered.update(countries)

        print(f"\n{Wh}Available countries / camera count:\n")
        for code, info in ordered.items():
            print(f"{Gr}{code:<4} {info['country']:<25} ({info['count']} cams)")

        country = input(f"\n{Ye}Enter country code (or 'n' to skip Insecam): {Gr}").upper().strip()
        if country.lower() == 'n':
            additional_cams_menu()
            return
    else:
        country = input(f"\n{Ye}Enter country code (or 'n' to skip Insecam): {Gr}").upper().strip()
        if country.lower() == 'n':
            additional_cams_menu()
            return

    if not country:
        print(f"{Re}No code entered.")
        return

    print(f"{Gr}Fetching Insecam cameras for {country} ...{Wh}\n")
    filename = f"{country}_insecam_cams.txt"
    count = 0
    all_links = []

    try:
        res = requests.get(f"http://www.insecam.org/en/bycountry/{country}", headers=HEADERS, timeout=10)
        pages = re.findall(r'pagenavigator\("\?page=",\s*(\d+)', res.text)
        last_page = int(pages[0]) if pages else 1

        with open(filename, 'w', encoding='utf-8') as f:
            for page in range(last_page):
                try:
                    url = f"http://www.insecam.org/en/bycountry/{country}/?page={page}"
                    res = requests.get(url, headers=HEADERS, timeout=10)
                    ips = re.findall(r'http://\d{1,3}(?:\.\d{1,3}){3}:\d+', res.text)
                    for ip in ips:
                        print(f"{Gr}{ip}{Wh}")
                        f.write(ip + '\n')
                        all_links.append(ip)
                        count += 1
                except:
                    continue
        print(f"\n{Gr}Done! Saved {count} cameras to: {filename}{Wh}")
    except Exception as e:
        print(f"{Re}Insecam fetch error: {e}{Wh}")

    more = input(f"\n{Ye}Check other public webcam sites? (y/n): {Gr}").lower()
    if more in ['y', 'yes', '1']:
        additional_cams_menu()

def main():
    while True:
        clear()
        banner()
        
        print(f"{Wh}Available Tools:{Gr}")
        print("  [1]  IP Tracker")
        print("  [2]  Device Information")
        print("  [3]  Phone Number OSINT")
        print("  [4]  Username OSINT")
        print("  [5]  Cam-hacker")
        print("  [6]  EchoIntel")
        print(f"  [0]  Exit{Wh}\n")
        
        ch = input(f"{Wh}Select an option → {Gr}").strip()

        if ch == "0":
            print(f"\n{Gr}Thank you! Free Palestine 🇵🇸{Wh}")
            sys.exit(0)

        action = {
            "1": IP_Track,
            "2": device_info,
            "3": phone_osint,
            "4": username_osint,
            "5": cam_hacker,
            "6": EchoIntel
        }.get(ch)

        if action:
            action()
        else:
            print(f"{Re}Invalid selection. Please try again.{Wh}")
            # No need for extra input() — returns to menu immediately
