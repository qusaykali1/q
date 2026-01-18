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
    num = input(f"{Wh}[+] Phone number (press Enter to go back): {Gr}").strip()

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
            cam_hacker()
        elif ch == "0":
            print(f"{Gr}Goodbye! Free Palestine 🇵🇸")
            sys.exit(0)
        else:
            print(f"{Re}[!] Invalid choice")

        input(f"{Wh}\nPress Enter to continue...")

if __name__ == "__main__":
    main()


