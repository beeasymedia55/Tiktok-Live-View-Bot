import requests
from urllib.parse import urlencode
import re
import time
import random
import string
import os
import uuid
import threading
import SignerPy
from pystyle import Colors, Colorate, Write, Center, System
from colorama import Fore, init

# Initialisierung
init(autoreset=True)
success = 0
errors = 0

# =============================================================================
# KONFIGURATION & HEADERS
# =============================================================================

TM_HEADERS = {
    "Application-Name": "web",
    "Application-Version": "4.0.0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "*/*",
    "Origin": "https://temp-mail.io",
    "Referer": "https://temp-mail.io/",
    "X-Cors-Header": "iaWg3pchvFx48fY",
    "Content-Type": "application/json"
}

# =============================================================================
# HILFSFUNKTIONEN (SIGNING & GENERATION)
# =============================================================================

def xor_encrypt(text: str, key: int = 5) -> str:
    return ''.join(hex(ord(c) ^ key)[2:] for c in text)

def generate_password(length=12):
    all_chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(all_chars) for _ in range(length))

def make_tiktok_params():
    device_id = str(random.randint(7000000000000000000, 7999999999999999999))
    iid = str(random.randint(7000000000000000000, 7999999999999999999))
    return {
        "device_id": device_id,
        "iid": iid,
        "device_platform": "android",
        "os": "android",
        "aid": "1233",
        "app_name": "musical_ly",
        "version_code": "370805",
        "version_name": "37.8.5",
    }, device_id

# =============================================================================
# MODUL 0: ACCOUNT ERSTELLER (Acc3main logic)
# =============================================================================

def run_account_creator():
    print(Colorate.Horizontal(Colors.green_to_white, "\n[*] Account Creator Modus gestartet..."))
    while True:
        try:
            # Email erstellen
            email_resp = requests.post("https://api.internal.temp-mail.io/api/v3/email/new", headers=TM_HEADERS, json={"min_name_length": 10, "max_name_length": 10}).json()
            email = email_resp['email']
            tm_token = email_resp['token']
            
            password = generate_password()
            session = requests.Session()
            params, did = make_tiktok_params()
            
            # Code senden
            print(f"[*] Registriere: {email}")
            send_tiktok_code(session, email, params, did, password)
            
            # Code abfragen
            code = None
            for _ in range(30):
                msg_resp = requests.get(f"https://api.internal.temp-mail.io/api/v3/email/{email}/messages", headers=TM_HEADERS).json()
                for msg in msg_resp:
                    m = re.search(r"\b\d{6}\b", msg.get("subject", "") + msg.get("body_text", ""))
                    if m: code = m.group(); break
                if code: break
                time.sleep(2)
            
            if code:
                # Verifizieren
                resp = verify_tiktok_email(session, email, code, "1998-01-01")
                data = resp.json().get("data", {})
                sid = data.get("session_key")
                if sid:
                    with open("session.txt", "a") as f: f.write(f"{sid}\n")
                    with open("accounts.txt", "a") as f: f.write(f"{email}:{password}\n")
                    print(f"{Fore.GREEN}[+] Account erfolgreich erstellt & Session gespeichert!")
            
        except Exception as e:
            print(f"{Fore.RED}[!] Fehler im Creator: {e}")
        time.sleep(5)

def send_tiktok_code(session, email, params, did, password):
    url = "https://api16-normal-c-alisg.tiktokv.com/passport/email/send_code/"
    payload = {'password': xor_encrypt(password), 'email': xor_encrypt(email), 'type': "34"}
    m = SignerPy.sign(params=params, payload=payload)
    headers = {'User-Agent': "com.zhiliaoapp.musically/2023708050", 'X-Gorgon': m.get('x-gorgon')}
    return session.post(url, params=params, data=payload, headers=headers)

def verify_tiktok_email(session, email, code, birthdate):
    url = "https://api16-normal-c-alisg.tiktokv.com/passport/email/register_verify_login/"
    payload = {'birthday': birthdate, 'code': xor_encrypt(code), 'email': xor_encrypt(email), 'type': "34"}
    params, _ = make_tiktok_params()
    m = SignerPy.sign(params=params, payload=payload)
    headers = {'User-Agent': "com.zhiliaoapp.musically/2023708050", 'X-Gorgon': m.get('x-gorgon')}
    return session.post(url, params=params, data=payload, headers=headers)

# =============================================================================
# MODUL 3 & 4: LIVE STREAM LOGIK (Share-Live & stupid logic)
# =============================================================================

def grab_room_id(username):
    print(f"[*] Suche Room-ID für {username}...")
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(f"https://www.tiktok.com/@{username}/live", headers=headers).text
        room_id = re.search(r'\"roomId\":\"(\d+)\"', res).group(1)
        print(f"{Fore.GREEN}[+] Room-ID gefunden: {room_id}")
        return room_id
    except:
        print(f"{Fore.RED}[-] User ist nicht live oder Fehler beim Scrapen.")
        return None

def send_live_view(session_key, room_id):
    # Logik basierend auf stupid (1).py
    url = "https://api16-normal-c-alisg.tiktokv.com/aweme/v1/check/in/"
    params, did = make_tiktok_params()
    params["room_id"] = room_id
    headers = {"Cookie": f"sessionid={session_key}", "User-Agent": "com.zhiliaoapp.musically/2023708050"}
    try:
        requests.get(url, params=params, headers=headers)
        return True
    except: return False

def send_live_heart(session_key, room_id):
    url = "https://api16-normal-c-alisg.tiktokv.com/aweme/v1/live/item/heart/"
    params, _ = make_tiktok_params()
    payload = {"room_id": room_id, "count": 1}
    headers = {"Cookie": f"sessionid={session_key}"}
    try:
        requests.post(url, params=params, data=payload, headers=headers)
        return True
    except: return False

def run_live_booster():
    user = input("TikTok Username des Live-Streams: ")
    room_id = grab_room_id(user)
    if not room_id: return

    try:
        with open("session.txt", "r") as f:
            sessions = [line.strip() for line in f if line.strip()]
        
        print(f"[*] Starte Boost mit {len(sessions)} Accounts...")
        for sid in sessions:
            # Viewer senden
            threading.Thread(target=send_live_view, args=(sid, room_id)).start()
            # Likes senden
            threading.Thread(target=send_live_heart, args=(sid, room_id)).start()
            print(f"[+] Account {sid[:6]}... im Stream.")
            time.sleep(0.5)
    except FileNotFoundError:
        print(f"{Fore.RED}[-] Keine sessions.txt gefunden. Erstelle erst Accounts!")

# =============================================================================
# HAUPTMENÜ
# =============================================================================

banner = """
 ██╗   ██╗██╗     ████████╗██╗███╗   ███╗ █████╗ ████████╗███████╗
 ██║   ██║██║     ╚══██╔══╝██║████╗ ████║██╔══██╗╚══██╔══╝██╔════╝
 ██║   ██║██║        ██║   ██║██╔████╔██║███████║   ██║   █████╗  
 ██║   ██║██║        ██║   ██║██║╚██╔╝██║██╔══██║   ██║   ██╔══╝  
 ╚██████╔╝███████╗   ██║   ██║██║ ╚═╝ ██║██║  ██║   ██║   ███████╗
  ╚═════╝ ╚══════╝   ╚═╝   ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝
           --- MULTI-BOT SYSTEM - LIVE EDITION ---
"""

def main_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Colorate.Horizontal(Colors.purple_to_blue, Center.XCenter(banner)))
    
    print(f"{Fore.CYAN}[0] Account Creator (Auto-Register & Session Save)")
    print(f"{Fore.CYAN}[1] Video Liker/Commenter (Aus sessions.txt)")
    print(f"{Fore.GREEN}[2] Live Stream Booster (Viewer + Likes)")
    print(f"{Fore.YELLOW}[3] Room-ID Grabber")
    print(f"{Fore.RED}[E] Beenden")
    
    choice = input("\nAuswahl: ").strip().lower()
    
    if choice == '0': run_account_creator()
    elif choice == '2': run_live_booster()
    elif choice == '3': 
        u = input("Username: "); grab_room_id(u); input("Enter zum Zurückkehren...")
        main_menu()
    elif choice == 'e': exit()
    else: main_menu()

if __name__ == "__main__":
    main_menu()
