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
stats = {"joined": 0, "likes": 0, "shares": 0, "errors": 0}
stats_lock = threading.Lock()

# =============================================================================
# TEIL 1: ACCOUNT CREATOR (BASIERT 1:1 AUF ACC3MAIN.PY)
# =============================================================================

TM_HEADERS = {
    "Application-Name": "web", "Application-Version": "4.0.0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Origin": "https://temp-mail.io", "Referer": "https://temp-mail.io/",
    "X-Cors-Header": "iaWg3pchvFx48fY", "Content-Type": "application/json"
}

def xor_encrypt(text: str, key: int = 5) -> str:
    return ''.join(hex(ord(c) ^ key)[2:] for c in text)

def make_tiktok_params():
    # Exakt die Parameter aus deiner Acc3main.py
    return {
        "passport-sdk-version": "6031990",
        "device_platform": "android",
        "os": "android",
        "ssmix": "a",
        "_rticket": str(int(time.time() * 1000)),
        "cdid": str(requests.utils.uuid.uuid4()),
        "aid": "1233",
        "app_name": "musical_ly",
        "version_code": "370805",
        "version_name": "37.8.5",
        "device_brand": "OnePlus",
        "device_type": "NE2211",
        "device_id": str(random.randint(7000000000000000000, 7999999999999999999)),
        "iid": str(random.randint(7000000000000000000, 7999999999999999999))
    }

def run_account_creator():
    print(f"{Fore.YELLOW}[*] Starte Account Creator (Acc3main-Engine)...")
    while True:
        try:
            # 1. Temp-Mail Email generieren
            email_resp = requests.post("https://api.internal.temp-mail.io/api/v3/email/new", headers=TM_HEADERS, json={"min_name_length": 10, "max_name_length": 10}).json()
            email = email_resp['email']
            tm_token = email_resp['token']
            password = "".join(random.choices(string.ascii_letters + string.digits, k=12))
            
            session = requests.Session()
            params = make_tiktok_params()
            
            # 2. Code senden
            payload = {'password': xor_encrypt(password), 'email': xor_encrypt(email), 'type': "34"}
            sig = SignerPy.sign(params=params, payload=payload)
            headers = {'User-Agent': "com.zhiliaoapp.musically/2023708050", 'X-Gorgon': sig.get('x-gorgon'), 'X-Khronos': sig.get('x-khronos')}
            
            session.post("https://api16-normal-c-alisg.tiktokv.com/passport/email/send_code/", params=params, data=payload, headers=headers)
            print(f"{Fore.CYAN}[*] Code gesendet an {email}...")

            # 3. Code abrufen
            code = None
            for _ in range(25):
                time.sleep(3)
                msgs = requests.get(f"https://api.internal.temp-mail.io/api/v3/email/{email}/messages", headers=TM_HEADERS).json()
                for m in msgs:
                    found = re.search(r"\b\d{6}\b", m.get("subject", "") + m.get("body_text", ""))
                    if found: code = found.group(); break
                if code: break

            if code:
                # 4. Verifizieren & Registrieren
                v_payload = {'birthday': "1998-05-05", 'code': xor_encrypt(code), 'email': xor_encrypt(email), 'type': "34"}
                v_sig = SignerPy.sign(params=params, payload=v_payload)
                v_headers = {'User-Agent': "com.zhiliaoapp.musically/2023708050", 'X-Gorgon': v_sig.get('x-gorgon'), 'X-Khronos': v_sig.get('x-khronos')}
                
                resp = session.post("https://api16-normal-c-alisg.tiktokv.com/passport/email/register_verify_login/", params=params, data=v_payload, headers=v_headers).json()
                
                sid = resp.get("data", {}).get("session_key")
                if sid:
                    with open("session.txt", "a") as f: f.write(f"{sid}\n")
                    print(f"{Fore.GREEN}[+] Account erfolgreich erstellt: {email}")
                else:
                    print(f"{Fore.RED}[-] Registrierung fehlgeschlagen: {resp.get('message')}")

        except Exception as e:
            print(f"{Fore.RED}[!] Creator Fehler: {e}")
        time.sleep(5)

# =============================================================================
# TEIL 2: ROOM-ID GRABBER (UACC2) & DASHBOARD
# =============================================================================

def grab_room_id(username):
    username = username.replace("@", "").strip()
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        res = requests.get(f"https://www.tiktok.com/@{username}/live", headers=headers, timeout=10).text
        match = re.search(r'\"roomId\":\"(\d+)\"', res)
        if match:
            rid = match.group(1)
            print(f"{Fore.GREEN}[+] Room-ID: {rid}")
            return rid
    except: pass
    return None

def live_worker(sid, room_id, do_like, do_share):
    params = make_tiktok_params()
    params["room_id"] = room_id
    headers = {"Cookie": f"sessionid={sid}", "User-Agent": "com.zhiliaoapp.musically/2023708050"}
    while True:
        try:
            requests.get("https://api16-normal-c-alisg.tiktokv.com/aweme/v1/check/in/", params=params, headers=headers, timeout=10)
            with stats_lock: stats["joined"] += 1
            if do_like:
                requests.post("https://api16-normal-c-alisg.tiktokv.com/aweme/v1/live/item/heart/", params=params, data={"room_id": room_id, "count": 1}, headers=headers)
                with stats_lock: stats["likes"] += 1
            time.sleep(25)
        except: break

# =============================================================================
# MENÜ
# =============================================================================

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Colorate.Horizontal(Colors.blue_to_purple, Center.XCenter("TIKTOK MULTI-BOT FIX\nEngine: Acc3main & Uacc2")))
    print(f"\n[0] Account Creator")
    print(f"[1] Live Booster")
    print(f"[2] Room-ID Finder")
    
    choice = input("\nAuswahl: ")
    if choice == '0': run_account_creator()
    elif choice == '1':
        user = input("User oder Room-ID: ")
        rid = grab_room_id(user) if not user.isdigit() else user
        if rid:
            with open("session.txt", "r") as f:
                sids = [line.strip() for line in f if line.strip()]
            for s in sids: threading.Thread(target=live_worker, args=(s, rid, True, True), daemon=True).start()
            print("Booster läuft. Dashboard aktiv (simuliert)...")
            while True: time.sleep(1)
    elif choice == '2':
        u = input("Username: "); grab_room_id(u); input("Enter..."); main()

if __name__ == "__main__":
    main()
