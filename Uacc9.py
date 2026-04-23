import requests
import re
import time
import random
import string
import os
import threading
import sys
import uuid  # Das Standard-Modul für IDs
import SignerPy
from pystyle import Colors, Colorate, Center
from colorama import Fore, init

init(autoreset=True)

# Globaler Status für das Dashboard
stats = {"joined": 0, "likes": 0, "shares": 0, "errors": 0}
stats_lock = threading.Lock()

# =============================================================================
# REPARIERTE PARAMETER-FUNKTION (FIX FÜR UUID FEHLER)
# =============================================================================

def make_tiktok_params():
    # Hier war der Fehler: requests.utils.uuid -> uuid.uuid4()
    return {
        "passport-sdk-version": "6031990",
        "device_platform": "android",
        "os": "android",
        "ssmix": "a",
        "_rticket": str(int(time.time() * 1000)),
        "cdid": str(uuid.uuid4()),  # KORREKT
        "aid": "1233",
        "app_name": "musical_ly",
        "version_code": "370805",
        "version_name": "37.8.5",
        "device_brand": "OnePlus",
        "device_type": "NE2211",
        "device_id": str(random.randint(7000000000000000000, 7999999999999999999)),
        "iid": str(random.randint(7000000000000000000, 7999999999999999999))
    }

# =============================================================================
# ACCOUNT CREATOR LOGIK (ACC3MAIN ENGINE)
# =============================================================================

def xor_encrypt(text: str, key: int = 5) -> str:
    return ''.join(hex(ord(c) ^ key)[2:] for c in text)

def run_account_creator():
    print(f"{Fore.YELLOW}[*] Account Creator läuft...")
    tm_headers = {"Application-Name": "web", "Content-Type": "application/json", "X-Cors-Header": "iaWg3pchvFx48fY"}
    while True:
        try:
            # Email holen
            email_resp = requests.post("https://api.internal.temp-mail.io/api/v3/email/new", headers=tm_headers, json={"min_name_length": 10, "max_name_length": 10}).json()
            email = email_resp['email']
            password = "".join(random.choices(string.ascii_letters + string.digits, k=12))
            
            params = make_tiktok_params()
            payload = {'password': xor_encrypt(password), 'email': xor_encrypt(email), 'type': "34"}
            sig = SignerPy.sign(params=params, payload=payload)
            
            headers = {'User-Agent': "com.zhiliaoapp.musically/2023708050", 'X-Gorgon': sig.get('x-gorgon'), 'X-Khronos': sig.get('x-khronos')}
            requests.post("https://api16-normal-c-alisg.tiktokv.com/passport/email/send_code/", params=params, data=payload, headers=headers)
            print(f"[*] Code gesendet an: {email}")

            code = None
            for _ in range(15):
                time.sleep(4)
                msgs = requests.get(f"https://api.internal.temp-mail.io/api/v3/email/{email}/messages", headers=tm_headers).json()
                for m in msgs:
                    found = re.search(r"\b\d{6}\b", m.get("subject", "") + m.get("body_text", ""))
                    if found: code = found.group(); break
                if code: break

            if code:
                v_payload = {'birthday': "1998-05-05", 'code': xor_encrypt(code), 'email': xor_encrypt(email), 'type': "34"}
                v_sig = SignerPy.sign(params=params, payload=v_payload)
                v_headers = {'User-Agent': "com.zhiliaoapp.musically/2023708050", 'X-Gorgon': v_sig.get('x-gorgon'), 'X-Khronos': v_sig.get('x-khronos')}
                resp = requests.post("https://api16-normal-c-alisg.tiktokv.com/passport/email/register_verify_login/", params=params, data=v_payload, headers=v_headers).json()
                
                sid = resp.get("data", {}).get("session_key")
                if sid:
                    with open("session.txt", "a") as f: f.write(f"{sid}\n")
                    print(f"{Fore.GREEN}[+] Erfolg! Session gespeichert.")
        except Exception as e:
            print(f"{Fore.RED}[!] Fehler: {e}")
        time.sleep(5)

# =============================================================================
# BOOSTER LOGIK (LIVE DASHBOARD)
# =============================================================================

def update_dashboard(last_action):
    with stats_lock:
        sys.stdout.write(f"\r{Fore.CYAN}[DASHBOARD] {Fore.GREEN}Join: {stats['joined']} | {Fore.MAGENTA}Likes: {stats['likes']} | {Fore.RED}Errors: {stats['errors']} {Fore.WHITE}[{last_action[:15]}]")
        sys.stdout.flush()

def live_worker(sid, room_id):
    global stats
    # WICHTIG: Hier rufen wir jetzt die korrigierte Funktion auf
    params = make_tiktok_params()
    params["room_id"] = room_id
    headers = {"Cookie": f"sessionid={sid}", "User-Agent": "com.zhiliaoapp.musically/2023708050"}
    
    while True:
        try:
            # Join / Keep-Alive
            r = requests.get("https://api16-normal-c-alisg.tiktokv.com/aweme/v1/check/in/", params=params, headers=headers, timeout=10)
            if r.status_code == 200:
                with stats_lock: stats["joined"] += 1
                update_dashboard(f"SID {sid[:3]} OK")
            
            # Auto-Like
            requests.post("https://api16-normal-c-alisg.tiktokv.com/aweme/v1/live/item/heart/", params=params, data={"room_id": room_id, "count": 1}, headers=headers)
            with stats_lock: stats["likes"] += 1
            
            time.sleep(25)
        except:
            with stats_lock: stats["errors"] += 1
            break

def run_live_booster():
    room_id = input("\nRoom-ID eingeben: ")
    if not room_id: return
    
    try:
        with open("session.txt", "r") as f:
            sessions = [line.strip() for line in f if line.strip()]
        
        print(f"\n{Fore.GREEN}[!] Starte Booster für {room_id}...")
        for s in sessions:
            threading.Thread(target=live_worker, args=(s, room_id), daemon=True).start()
            time.sleep(0.1)
        
        while True: time.sleep(1)
    except FileNotFoundError:
        print("session.txt fehlt!")

# =============================================================================
# MENÜ
# =============================================================================

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Colorate.Horizontal(Colors.blue_to_purple, Center.XCenter("TIKTOK FIX v10\nKeine uuid-Fehler mehr")))
    print(f"\n[0] Creator | [1] Booster | [E] Exit")
    
    c = input("\nAuswahl: ")
    if c == '0': run_account_creator()
    elif c == '1': run_live_booster()
    elif c == 'e': exit()

if __name__ == "__main__":
    main()
