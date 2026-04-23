import requests
import re
import time
import random
import string
import os
import threading
import sys
import SignerPy
from pystyle import Colors, Colorate, Center
from colorama import Fore, init

init(autoreset=True)

# Globaler Status für das Dashboard
stats = {"joined": 0, "likes": 0, "shares": 0, "errors": 0, "active_threads": 0}
stats_lock = threading.Lock()

# =============================================================================
# HILFSFUNKTIONEN
# =============================================================================

def make_tiktok_params():
    did = str(random.randint(7000000000000000000, 7999999999999999999))
    iid = str(random.randint(7000000000000000000, 7999999999999999999))
    return {
        "device_id": did, "iid": iid, "device_platform": "android",
        "aid": "1233", "app_name": "musical_ly", "version_code": "370805"
    }, did

def update_dashboard(last_msg="Warte auf Bots..."):
    with stats_lock:
        sys.stdout.write(f"\r{Fore.CYAN}[DASHBOARD] "
                         f"{Fore.GREEN}Joined: {stats['joined']} | "
                         f"{Fore.MAGENTA}Likes: {stats['likes']} | "
                         f"{Fore.BLUE}Shares: {stats['shares']} | "
                         f"{Fore.RED}Errors: {stats['errors']} "
                         f"{Fore.WHITE}[Last: {last_msg[:25]}]")
        sys.stdout.flush()

# =============================================================================
# INTERAKTIONS-LOGIK
# =============================================================================

def live_worker(sid, room_id, mode_config):
    """
    Ein Thread pro Account. Hält die Verbindung zum Stream und führt Aktionen aus.
    """
    global stats
    params, did = make_tiktok_params()
    params["room_id"] = room_id
    headers = {
        "Cookie": f"sessionid={sid}",
        "User-Agent": "com.zhiliaoapp.musically/2023708050 (Linux; U; Android 10; en_US;)",
        "Connection": "keep-alive"
    }

    first_join = True
    
    while True: # Keep-Alive Loop
        try:
            # 1. Join / Heartbeat (Viewer Count halten)
            # Wir checken alle 30 Sekunden ein, damit der Viewer-Count nicht sinkt
            requests.get("https://api16-normal-c-alisg.tiktokv.com/aweme/v1/check/in/", 
                         params=params, headers=headers, timeout=10)
            
            if first_join:
                with stats_lock: stats["joined"] += 1
                update_dashboard(f"ID {sid[:5]} joined")
                first_join = False

            # 2. Liken (wenn ausgewählt)
            if mode_config['like']:
                # Sendet ein Paket von 1-3 Likes pro Intervall
                for _ in range(random.randint(1, 3)):
                    requests.post("https://api16-normal-c-alisg.tiktokv.com/aweme/v1/live/item/heart/", 
                                 params=params, data={"room_id": room_id, "count": 1}, headers=headers)
                    with stats_lock: stats["likes"] += 1
                    update_dashboard(f"ID {sid[:5]} liked")
                    time.sleep(1)

            # 3. Sharen (wenn ausgewählt)
            if mode_config['share'] and random.random() > 0.7: # Nicht jeder Account shared jedes Mal (unauffälliger)
                requests.get("https://api16-normal-c-alisg.tiktokv.com/aweme/v1/live/share/", 
                             params=params, headers=headers)
                with stats_lock: stats["shares"] += 1
                update_dashboard(f"ID {sid[:5]} shared")

            # Wartezeit bis zum nächsten Heartbeat (wichtig für Viewer Count)
            time.sleep(25) 

        except Exception:
            with stats_lock: stats["errors"] += 1
            break # Thread beenden bei schwerem Fehler

# =============================================================================
# HAUPTFUNKTIONEN
# =============================================================================

def run_live_booster():
    print(f"\n{Fore.YELLOW}--- LIVE BOOSTER DASHBOARD SETUP ---")
    user_input = input("Username oder Room-ID eingeben: ")
    
    # Room-ID bestimmen
    if user_input.isdigit():
        room_id = user_input
    else:
        # Hier die Grabber-Logik von vorher nutzen
        room_id = input("Konnte Room-ID nicht finden. Bitte manuell eingeben: ")

    # Modus wählen
    print(f"\n{Fore.WHITE}Optionen wählen (y/n):")
    do_like = input("Sollen Bots Liken? ").lower() == 'y'
    do_share = input("Sollen Bots Sharen? ").lower() == 'y'
    
    mode_config = {'like': do_like, 'share': do_share}

    try:
        with open("session.txt", "r") as f:
            sessions = [line.strip() for line in f if line.strip()]
        
        if not sessions:
            print(Fore.RED + "session.txt ist leer!")
            return

        print(f"\n{Fore.GREEN}[!] Dashboard gestartet. {len(sessions)} Bots verbinden sich...")
        print(f"{Fore.WHITE}Beenden mit STRG+C\n")

        for sid in sessions:
            t = threading.Thread(target=live_worker, args=(sid, room_id, mode_config))
            t.daemon = True
            t.start()
            time.sleep(0.2) # Sanfter Start gegen Ratelimit

        # Haupt-Thread am Leben halten
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Booster gestoppt.")
    except FileNotFoundError:
        print(Fore.RED + "session.txt fehlt!")

# =============================================================================
# MENÜ
# =============================================================================

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = Center.XCenter("TIKTOK ULTIMATE DASHBOARD\n[Viewer | Likes | Shares]")
    print(Colorate.Horizontal(Colors.blue_to_purple, banner))
    
    print(f"\n{Fore.CYAN}[1] Live Booster & Dashboard")
    print(f"{Fore.CYAN}[2] Room-ID Finder")
    print(f"{Fore.RED}[E] Exit")
    
    choice = input("\nAuswahl: ").lower()
    if choice == '1': run_live_booster()
    elif choice == 'e': exit()
    else: main()

if __name__ == "__main__":
    main()
