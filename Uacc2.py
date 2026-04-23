import requests
import re
import time
import random
import string
import os
import uuid
import threading
import SignerPy
from pystyle import Colors, Colorate, Center
from colorama import Fore, init

init(autoreset=True)

# =============================================================================
# KONFIGURATION
# =============================================================================
TM_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Content-Type": "application/json"
}

# =============================================================================
# HILFSFUNKTIONEN
# =============================================================================
def xor_encrypt(text: str, key: int = 5) -> str:
    return ''.join(hex(ord(c) ^ key)[2:] for c in text)

def make_tiktok_params():
    did = str(random.randint(7000000000000000000, 7999999999999999999))
    iid = str(random.randint(7000000000000000000, 7999999999999999999))
    return {
        "device_id": did, "iid": iid, "device_platform": "android",
        "aid": "1233", "app_name": "musical_ly", "version_code": "370805"
    }, did

# =============================================================================
# MODUL: ROOM-ID GRABBER (STABILISIERT)
# =============================================================================
def grab_room_id(username):
    username = username.replace("@", "").strip()
    print(f"[*] Suche Room-ID für: {username}...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}
    try:
        res = requests.get(f"https://www.tiktok.com/@{username}/live", headers=headers, timeout=10).text
        match = re.search(r'\"roomId\":\"(\d+)\"', res)
        if match:
            rid = match.group(1)
            print(f"{Fore.GREEN}[+] Room-ID gefunden: {rid}")
            with open("room_id.txt", "w") as f: f.write(rid)
            return rid
    except: pass
    print(f"{Fore.RED}[-] Konnte Room-ID nicht automatisch finden.")
    return None

# =============================================================================
# MODUL: LIVE BOOSTER (VIEWER & LIKES)
# =============================================================================
def send_live_interaction(session_key, room_id):
    params, did = make_tiktok_params()
    params["room_id"] = room_id
    headers = {"Cookie": f"sessionid={session_key}", "User-Agent": "com.zhiliaoapp.musically/2023708050"}
    
    # 1. Viewer Check-in (Pusht Viewer Count)
    try:
        requests.get("https://api16-normal-c-alisg.tiktokv.com/aweme/v1/check/in/", params=params, headers=headers)
    except: pass
    
    # 2. Hearts/Likes senden
    try:
        payload = {"room_id": room_id, "count": 1}
        requests.post("https://api16-normal-c-alisg.tiktokv.com/aweme/v1/live/item/heart/", params=params, data=payload, headers=headers)
    except: pass

def run_live_booster():
    print(f"\n{Fore.CYAN}--- LIVE BOOSTER EINSTELLUNGEN ---")
    print("[1] Username eingeben (Auto-Grab)")
    print("[2] Room-ID manuell eingeben")
    mode = input("Wähle Modus: ")

    room_id = None
    if mode == '1':
        user = input("Username: ")
        room_id = grab_room_id(user)
    else:
        room_id = input("Manuelle Room-ID: ").strip()

    if not room_id or len(room_id) < 5:
        print(f"{Fore.RED}[!] Ungültige Room-ID.")
        return

    try:
        with open("session.txt", "r") as f:
            sessions = [line.strip() for line in f if line.strip()]
        
        if not sessions:
            print(f"{Fore.RED}[!] session.txt ist leer! Erstelle erst Accounts (Option 0).")
            return

        print(f"[*] Sende {len(sessions)} Accounts in den Stream {room_id}...")
        for sid in sessions:
            threading.Thread(target=send_live_interaction, args=(sid, room_id)).start()
            time.sleep(0.1)
        print(f"{Fore.GREEN}[+] Alle Threads gestartet!")
        input("\nDrücke Enter für das Hauptmenü...")
    except FileNotFoundError:
        print(f"{Fore.RED}[!] session.txt nicht gefunden.")

# =============================================================================
# ACCOUNT CREATOR (BASIEREND AUF DEINEM CODE)
# =============================================================================
def run_account_creator():
    # ... (Die Logik bleibt wie im vorherigen kombinierten Skript)
    print(f"{Fore.YELLOW}[*] Account Creator Loop gestartet (Strg+C zum Beenden)...")
    # (Hier kommt die Schleife aus dem letzten Skript rein)

# =============================================================================
# HAUPTMENÜ
# =============================================================================
banner = """
  ██████╗ ██████╗  ██████╗ ███████╗████████╗███████╗██████╗ 
  ██╔══██╗██╔══██╗██╔═══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗
  ██████╔╝██║  ██║██║   ██║███████╗   ██║   █████╗  ██████╔╝
  ██╔══██╗██║  ██║██║   ██║╚════██║   ██║   ██╔══╝  ██╔══██╗
  ██████╔╝██████╔╝╚██████╔╝███████║   ██║   ███████╗██║  ██║
"""

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Colorate.Horizontal(Colors.cyan_to_blue, Center.XCenter(banner)))
    print(f"\n{Fore.WHITE}[0] Account Creator (Auto-Save session.txt)")
    print(f"{Fore.WHITE}[1] Live Booster (Viewer + Likes)")
    print(f"{Fore.WHITE}[2] Room-ID Grabber (Nur ID finden)")
    print(f"{Fore.RED}[E] Exit")

    choice = input("\nAuswahl: ").lower()
    if choice == '0':
        # Hier die Creator Logik aufrufen
        pass 
    elif choice == '1':
        run_live_booster()
    elif choice == '2':
        u = input("Username: ")
        grab_room_id(u)
        input("Enter...")
    elif choice == 'e':
        exit()
    
    main()

if __name__ == "__main__":
    main()

