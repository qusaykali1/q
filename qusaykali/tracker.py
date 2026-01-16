#!/usr/bin/python3
# -*- coding: utf-8 -*-
# OSINT TOOL – FINAL COMPLETE BUILD
# Author : Qusay_kali
# FREE PALESTINE 🇵🇸

import os, sys, requests
import phonenumbers
from phonenumbers import carrier, geocoder, timezone

# ================= COLORS =================
Re = '\033[1;31m'
Gr = '\033[1;32m'
Ye = '\033[1;33m'
Cy = '\033[1;36m'
Wh = '\033[1;37m'

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# ================= UI =================
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    clear()
    print(f"""{Cy}
 ██████╗ ███████╗██╗███╗   ██╗████████╗
██╔════╝ ██╔════╝██║████╗  ██║╚══██╔══╝
██║  ███╗█████╗  ██║██╔██╗ ██║   ██║   
██║   ██║██╔══╝  ██║██║╚██╗██║   ██║   
╚██████╔╝███████╗██║██║ ╚████║   ██║   
 ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   

{Gr}FREE PALESTINE 🇵🇸
{Wh}OSINT MULTI TOOL – FINAL
""")

def sub_banner(title):
    print(f"\n{Cy}========== {Gr}{title} {Cy}=========={Wh}\n")

# =====================================================
# (1) USERNAME OSINT – 40 PLATFORMS – REAL CHECK
# =====================================================
def TrackLu():
    sub_banner("USERNAME OSINT (40 PLATFORMS)")
    user = input(f"{Wh}[+] Username : {Gr}").strip()

    variations = set()
    variations.update([
        user, user.lower(), user.upper(), user.capitalize()
    ])

    for i in range(10):
        variations.add(f"{i}{user}")
        variations.add(f"{user}{i}")
        variations.add(f"{i}{user.lower()}")
        variations.add(f"{user.lower()}{i}")

    platforms = [
        ("Facebook", "https://www.facebook.com/{}"),
        ("Instagram", "https://www.instagram.com/{}"),
        ("Twitter/X", "https://twitter.com/{}"),
        ("TikTok", "https://www.tiktok.com/@{}"),
        ("GitHub", "https://github.com/{}"),
        ("Telegram", "https://t.me/{}"),
        ("Snapchat", "https://www.snapchat.com/add/{}"),
        ("Reddit", "https://www.reddit.com/user/{}"),
        ("LinkedIn", "https://www.linkedin.com/in/{}"),
        ("YouTube", "https://www.youtube.com/@{}"),
        ("Pinterest", "https://www.pinterest.com/{}"),
        ("Twitch", "https://www.twitch.tv/{}"),
        ("Spotify", "https://open.spotify.com/user/{}"),
        ("Medium", "https://medium.com/@{}"),
        ("Behance", "https://www.behance.net/{}"),
        ("Dribbble", "https://dribbble.com/{}"),
        ("VK", "https://vk.com/{}"),
        ("OK", "https://ok.ru/{}"),
        ("Flickr", "https://www.flickr.com/people/{}"),
        ("SoundCloud", "https://soundcloud.com/{}"),
        ("DeviantArt", "https://www.deviantart.com/{}"),
        ("Quora", "https://www.quora.com/profile/{}"),
        ("Patreon", "https://www.patreon.com/{}"),
        ("Imgur", "https://imgur.com/user/{}"),
        ("Steam", "https://steamcommunity.com/id/{}"),
        ("Roblox", "https://www.roblox.com/user.aspx?username={}"),
        ("Bitbucket", "https://bitbucket.org/{}"),
        ("About.me", "https://about.me/{}"),
        ("Vimeo", "https://vimeo.com/{}"),
        ("Dailymotion", "https://www.dailymotion.com/{}"),
        ("Last.fm", "https://www.last.fm/user/{}"),
        ("Mixcloud", "https://www.mixcloud.com/{}"),
        ("Issuu", "https://issuu.com/{}"),
        ("Keybase", "https://keybase.io/{}"),
        ("Wattpad", "https://www.wattpad.com/user/{}"),
        ("ReverbNation", "https://www.reverbnation.com/{}"),
        ("Etsy", "https://www.etsy.com/shop/{}"),
        ("Xbox", "https://xboxgamertag.com/search/{}")
    ]

    for name, url_tpl in platforms:
        found = False
        for v in variations:
            url = url_tpl.format(v)
            try:
                r = requests.get(url, headers=HEADERS, timeout=5)
                if r.status_code == 200 and v.lower() in r.text.lower():
                    print(f"{Gr}[FOUND]{Wh} {name:<15} -> {url}")
                    found = True
                    break
            except:
                pass
        if not found:
            print(f"{Re}[NONE ]{Wh} {name}")

# =====================================================
# (2) PHONE OSINT – 30 DATA POINTS
# =====================================================
def phone30():
    sub_banner("PHONE OSINT (30 DATA POINTS)")
    num = input(f"{Wh}[+] Phone (+CountryCode) : {Gr}")

    try:
        p = phonenumbers.parse(num, None)

        data = [
            ("Valid Number", phonenumbers.is_valid_number(p)),
            ("Possible Number", phonenumbers.is_possible_number(p)),
            ("Country Code", p.country_code),
            ("National Number", p.national_number),
            ("Region Code", phonenumbers.region_code_for_number(p)),
            ("Country (EN)", geocoder.description_for_number(p, "en")),
            ("Country (AR)", geocoder.description_for_number(p, "ar")),
            ("Carrier (EN)", carrier.name_for_number(p, "en")),
            ("Carrier (AR)", carrier.name_for_number(p, "ar")),
            ("Timezone", timezone.time_zones_for_number(p)),
            ("E164 Format", phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.E164)),
            ("International Format", phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.INTERNATIONAL)),
            ("National Format", phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.NATIONAL)),
            ("Number Type", phonenumbers.number_type(p)),
            ("Mobile?", phonenumbers.number_type(p) == 1),
            ("Fixed Line?", phonenumbers.number_type(p) == 0),
            ("Geographical?", phonenumbers.is_number_geographical(p)),
            ("Italian Leading Zero", p.italian_leading_zero),
            ("Country Prefix", f"+{p.country_code}"),
            ("Raw Input", p.raw_input),
            ("Extension", p.extension),
            ("Preferred Domestic Carrier", p.preferred_domestic_carrier_code),
            ("National Destination Code", p.national_destination_code),
            ("Leading Zeros", p.number_of_leading_zeros),
            ("Source", "Google libphonenumber"),
            ("Standard", "ITU-T E.164"),
            ("OSINT Level", "Public"),
            ("Owner Name", "Not Available"),
            ("Exact Location", "Not Available"),
            ("Privacy Status", "Respected")
        ]

        for i, (k, v) in enumerate(data, 1):
            print(f"{Wh}{i:02}. {k:<25}:{Gr} {v}")

    except:
        print(f"{Re}[!] Invalid phone number")

# ================= MAIN =================
def main():
    while True:
        banner()
        print(f"{Wh}[1]{Gr} Username OSINT")
        print(f"{Wh}[2]{Gr} Phone OSINT")
        print(f"{Wh}[0]{Gr} Exit")

        c = input(f"\n{Wh}[+] Select : ")
        if c == '1': TrackLu()
        elif c == '2': phone30()
        elif c == '0': sys.exit()

        input(f"\n{Wh}Press Enter...")

if __name__ == "__main__":
    main()
