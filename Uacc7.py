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
# TEIL 1: ACCOUNT CREATOR LOGIK (AUS ACC3MAIN.PY)
# =============================================================================

TM_HEADERS = {
    "Application-Name": "web", "Application-Version": "4.0.0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "X-Cors-Header": "iaWg3pchvFx48fY", "Content-Type": "application/json"
}

def xor_encrypt(text: str, key: int = 5) -> str:
    return ''.join(hex(ord(c) ^ key)[2:] for c in text)

def make_tiktok_params():
    dd = str(random.randint(1, 10**19))
    return {
        "passport-sdk-version": "6031990", "device_platform": "android",
        "os": "android", "ssmix": "a", "aid": "1233", "app_name": "musical_ly",
        "version_code": "370805", "version_name": "37.8.5", "device_brand": "OnePlus",
        "device_type": "NE2211", "os_api": "28", "os_version": "9"
    }, dd

def run_account_creator():
    print(f"{Fore.YELLOW}[*] Starte Account Creator (Acc3main-Engine)...")
    while True:
        try:
            # Email erstellen
            email_data = requests.post("https://api.internal.temp-mail.io/api/v3/email/new", headers=TM_HEADERS, json={"min_name_length": 10, "max_name_length": 10}).json()
            email, tm_token = email_data['email'], email_data['token']
            password = "".join(random.choices(string.ascii_letters + string.digits, k=12))
            
            session = requests.Session()
            params, did = make_tiktok_params()
            
            # Code senden
            payload = {'password': xor_encrypt(password), 'email': xor_encrypt(email), 'type': "34"}
            sig = SignerPy.sign(params=params, payload=payload)
            session.post("https://api16-normal-c-alisg.tiktokv.com/passport/email/send_code/", params=params, data=payload, headers={'User-Agent': "com.zhiliaoapp.musically/2023708050", 'X-Gorgon': sig.get('x-gorgon')})
            
            print(f"[*] Warte auf Code für {email}...")
            code = None
            for _ in range(20):
                msgs = requests.get(f"https://api.internal.temp-mail.io/api/v3/email/{email}/messages", headers=TM_HEADERS).json()
                for m in msgs:
                    match = re.search(r"\b\d{6}\b", m.get("subject", "") + m.get("body_text", ""))
                    if match: code = match.group(); break
                if code: break
                time.sleep(3)
            
            if code:
                # Verifizieren
                v_payload = {'birthday': "1999-01-01", 'code': xor_encrypt(code), 'email': xor_encrypt(email), 'type': "34"}
                v_sig = SignerPy.sign(params=params, payload=v_payload)
                resp = session.post("https://api16-normal-c-alisg.tiktokv.com/passport/email/register_verify_login/", params=params, data=v_payload, headers={'X-Gorgon': v_sig.get('x-gorgon')}).json()
                
                sid = resp.get("data", {}).get("session_key")
                if sid:
                    with open("session.txt", "a") as f: f.write(f"{sid}\n")
                    print(f"{Fore.GREEN}[+] Account erstellt & Session gespeichert!")
        except Exception as e:
            print(f"{Fore.RED}[!] Fehler: {e}")
        time.sleep(2)

# =============================================================================
# TEIL 2: ROOM-ID GRABBER (AUS UACC2.PY)
# =============================================================================

def grab_room_id(username):
    username = username.replace("@", "").strip()
    print(f"[*] Suche Room-ID für @{username} (Uacc2-Regex-Methode)...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        res = requests.get(f"https://www.tiktok.com/@{username}/live", headers=headers, timeout=10).text
        # Das erfolgreiche Pattern aus Uacc2
        match = re.search(r'\"roomId\":\"(\d+)\"', res)
        if match:
            rid = match.group(1)
            print(f"{Fore.GREEN}[+] Room-ID gefunden: {rid}")
            with open("room_id.txt", "w") as f: f.write(rid)
            return rid
    except: pass
    print(f"{Fore.RED}[-] Grabber fehlgeschlagen.")
    return None

# =============================================================================
# TEIL 3: LIVE BOOSTER DASHBOARD
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

def live_worker(sid, room_id, do_like, do_share):
    global stats
    params, _ = make_tiktok_params()
    params["room_id"] = room_id
    headers = {"Cookie": f"sessionid={sid}", "User-Agent": "com.zhiliaoapp.musically/2023708050"}
    
    while True:
        try:
            # Viewer Keep-Alive (Check-in)
            requests.get("https://api16-normal-c-alisg.tiktokv.com/aweme/v1/check/in/", params=params, headers=headers, timeout=10)
            with stats_lock: stats["joined"] += 1
            update_dashboard(f"ID {sid[:4]} Active")

            if do_like:
                requests.post("https://api16-normal-c-alisg.tiktokv.com/aweme/v1/live/item/heart/", params=params, data={"room_id": room_id, "count": 1}, headers=headers)
                with stats_lock: stats["likes"] += 1
                update_dashboard(f"ID {sid[:4]} Liked")

            if do_share:
                requests.get("https://api16-normal-c-alisg.tiktokv.com/aweme/v1/live/share/", params=params, headers=headers)
                with stats_lock: stats["shares"] += 1
                update_dashboard(f"ID {sid[:4]} Shared")

            time.sleep(25) # Wichtig für Viewer-Stabilität
        except:
            with stats_lock: stats["errors"] += 1
            break

def run_live_booster():
    user = input("\nUsername oder Room-ID: ")
    room_id = grab_room_id(user) if not user.isdigit() else user
    if not room_id: return

    do_like = input("Liken? (y/n): ").lower() == 'y'
    do_share = input("Sharen? (y/n): ").lower() == 'y'

    with open("session.txt", "r") as f:
        sessions = [line.strip() for line in f if line.strip()]
    
    print(f"\n{Fore.GREEN}[!] Dashboard gestartet. Beenden mit STRG+C.")
    for sid in sessions:
        threading.Thread(target=live_worker, args=(sid, room_id, do_like, do_share), daemon=True).start()
        time.sleep(0.2)
    
    while True: time.sleep(1)

# =============================================================================
# HAUPTMENÜ
# =============================================================================

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Colorate.Horizontal(Colors.blue_to_purple, Center.XCenter("ULTIMATE TIKTOK BOT SYSTEM\n(Engine: Acc3main + Uacc2)")))
    print(f"\n[0] Account Creator (Acc3main Logic)")
    print(f"[1] Live Booster & Dashboard")
    print(f"[2] Room-ID Finder (Uacc2 Logic)")
    print(f"[E] Exit")
    
    choice = input("\nAuswahl: ").lower()
    if choice == '0': run_account_creator()
    elif choice == '1': run_live_booster()
    elif choice == '2': 
        u = input("User: "); grab_room_id(u); input("Enter..."); main()
    elif choice == 'e': exit()
    else: main()

if __name__ == "__main__":
    main()
