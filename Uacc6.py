import requests
import re
import time
import random
import string
import os
import uuid
import threading
import sys
import SignerPy
from pystyle import Colors, Colorate, Center
from colorama import Fore, init

init(autoreset=True)

# Globaler Status für das Dashboard
stats = {"joined": 0, "likes": 0, "shares": 0, "errors": 0}
stats_lock = threading.Lock()

# =============================================================================
# STABILE PARAMETER (AUS ACC3MAIN.PY ÜBERNOMMEN)
# =============================================================================

def get_stable_headers(session_id=None):
    headers = {
        'User-Agent': "com.zhiliaoapp.musically/2023708050 (Linux; U; Android 9; en_GB; NE2211; Build/SKQ1.220617.001;tt-ok/3.12.13.16)",
        'Accept-Encoding': "gzip",
        'Connection': "Keep-Alive",
        'passport-sdk-version': "6031990",
        'sdk-version': "2",
        'x-tt-bypass-dp': "1",
        'x-vc-bdturing-sdk-version': "2.3.8.i18n"
    }
    if session_id:
        headers["Cookie"] = f"sessionid={session_id}"
    return headers

def make_tiktok_params():
    # Exakt wie in deiner funktionierenden Acc3main.py
    dd = str(random.randint(1, 10**19))
    return {
        "passport-sdk-version": "6031990",
        "device_platform": "android",
        "os": "android",
        "ssmix": "a",
        "aid": "1233",
        "app_name": "musical_ly",
        "version_code": "370805",
        "version_name": "37.8.5",
        "device_brand": "OnePlus",
        "device_type": "NE2211",
        "os_api": "28",
        "os_version": "9",
        "channel": "googleplay",
        "device_id": str(random.randint(7000000000000000000, 7999999999999999999)),
        "iid": str(random.randint(7000000000000000000, 7999999999999999999))
    }, dd

# =============================================================================
# REPARIERTER ROOM-ID FINDER
# =============================================================================

def grab_room_id(username):
    username = username.replace("@", "").strip()
    print(f"[*] Suche Room-ID für @{username}...")
    
    headers = get_stable_headers()
    params = {
        "unique_id": username,
        "source": "share",
        "aid": "1233",
        "version_code": "370805"
    }

    try:
        # Versuch über den offiziellen API-Endpunkt
        res = requests.get("https://api16-normal-c-alisg.tiktokv.com/aweme/v1/live/room/base/info/", 
                          params=params, headers=headers, timeout=10).json()
        
        room_id = str(res.get("room_id", ""))
        
        if room_id and room_id != "0":
            print(f"{Fore.GREEN}[+] Room-ID gefunden: {room_id}")
            with open("room_id.txt", "w") as f: f.write(room_id)
            return room_id
        else:
            # Fallback auf Web-Parsing
            print(f"{Fore.YELLOW}[!] API blockiert, versuche Web-Parsing...")
            web_res = requests.get(f"https://www.tiktok.com/@{username}/live", headers=headers, timeout=10).text
            match = re.search(r'\"roomId\":\"(\d+)\"', web_res)
            if match:
                print(f"{Fore.GREEN}[+] Room-ID über Web gefunden: {match.group(1)}")
                return match.group(1)
                
        print(f"{Fore.RED}[-] User ist nicht live oder blockiert Anfragen.")
        return None
    except:
        return None

# =============================================================================
# DASHBOARD & LIVE WORKER
# =============================================================================

def update_dashboard(last_action):
    with stats_lock:
        sys.stdout.write(f"\r{Fore.CYAN}[DASHBOARD] "
                         f"{Fore.GREEN}Join: {stats['joined']} | "
                         f"{Fore.MAGENTA}Likes: {stats['likes']} | "
                         f"{Fore.BLUE}Shares: {stats['shares']} | "
                         f"{Fore.RED}Fail: {stats['errors']} "
                         f"{Fore.WHITE}[Log: {last_action[:20]}]")
        sys.stdout.flush()

def live_interaction_worker(sid, room_id, do_like, do_share):
    global stats
    params, _ = make_tiktok_params()
    params["room_id"] = room_id
    headers = get_stable_headers(sid)
    
    while True:
        try:
            # 1. Join / Heartbeat (alle 25 Sek für Viewer Count)
            resp = requests.get("https://api16-normal-c-alisg.tiktokv.com/aweme/v1/check/in/", 
                                params=params, headers=headers, timeout=10)
            
            if resp.status_code == 200:
                with stats_lock: stats["joined"] += 1
                update_dashboard(f"ID {sid[:4]} Active")

            if do_like:
                for _ in range(random.randint(1, 4)):
                    requests.post("https://api16-normal-c-alisg.tiktokv.com/aweme/v1/live/item/heart/", 
                                 params=params, data={"room_id": room_id, "count": 1}, headers=headers)
                    with stats_lock: stats["likes"] += 1
                    update_dashboard(f"ID {sid[:4]} Liked")
                    time.sleep(1)

            if do_share:
                requests.get("https://api16-normal-c-alisg.tiktokv.com/aweme/v1/live/share/", 
                             params=params, headers=headers)
                with stats_lock: stats["shares"] += 1
                update_dashboard(f"ID {sid[:4]} Shared")

            time.sleep(25) # Wartezeit bis zum nächsten Heartbeat
        except:
            with stats_lock: stats["errors"] += 1
            break

def run_live_booster():
    mode = input("\n[1] Auto-Grab ID | [2] Manuelle ID: ")
    if mode == '1':
        user = input("Username: ")
        room_id = grab_room_id(user)
    else:
        room_id = input("Room-ID: ")

    if not room_id: return

    do_like = input("Sollen Bots LIKEN? (y/n): ").lower() == 'y'
    do_share = input("Sollen Bots SHAREN? (y/n): ").lower() == 'y'

    try:
        with open("session.txt", "r") as f:
            sessions = [line.split(":")[0] for line in f if line.strip()]
        
        print(f"\n{Fore.GREEN}[!] Dashboard gestartet mit {len(sessions)} Bots...\n")
        for sid in sessions:
            threading.Thread(target=live_interaction_worker, args=(sid, room_id, do_like, do_share), daemon=True).start()
            time.sleep(0.3)
        
        while True: time.sleep(1)
    except KeyboardInterrupt: print("\nBooster gestoppt.")

# =============================================================================
# MAIN MENU
# =============================================================================

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = Center.XCenter(f"{Fore.MAGENTA}TIKTOK MULTI-TOOL (Acc3-Engine)\n{Fore.WHITE}Status: Verbunden")
    print(banner)
    print(f"\n[0] Account Creator (Startet Acc3main-Logik)")
    print(f"[1] Live Booster & Dashboard (Viewer + Likes + Shares)")
    print(f"[2] Room-ID Finder")
    print(f"[E] Beenden")
    
    choice = input("\nAuswahl: ").lower()
    if choice == '0':
        # Hier die Logik aus deiner funktionierenden Acc3main aufrufen
        print("Starte Account Erstellung...")
        # (Da du sagst sie geht, füge hier deinen Code-Block ein)
    elif choice == '1': run_live_booster()
    elif choice == '2': 
        u = input("User: "); grab_room_id(u); input("Enter...")
        main()
    elif choice == 'e': exit()
    else: main()

if __name__ == "__main__":
    main()
