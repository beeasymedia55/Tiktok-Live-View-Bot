import os, sys, ssl, re, time, random, threading, requests, hashlib, json, base64, uuid
from pystyle import *
from urllib.parse import urlencode
from urllib3.exceptions import InsecureRequestWarning

# --- INITIALISIERUNG ---
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context
_lock = threading.Lock()
success = 0
active_bots = 0

# --- PROXY KONFIGURATION ---
class ProxyManager:
    enabled = False
    servers = [
        "https://www.blockaway.net", "https://www.croxyproxy.com",
        "https://www.croxyproxy.rocks", "https://www.croxy.network",
        "https://www.croxy.org", "https://www.youtubeunblocked.live",
        "https://www.croxyproxy.net"
    ]
    @classmethod
    def get_proxy(cls):
        return {"http": choice(cls.servers), "https": choice(cls.servers)} if cls.enabled else None

# --- STAY ALIVE LOGIK FÜR LIVE VIEWS ---
def live_stay_alive_loop(did, iid, cdid, openudid, room_id):
    """Hält den Bot im Stream, indem er die Session alle 25-50 Sek. erneuert"""
    global success, active_bots
    with _lock: active_bots += 1
    
    while True:
        try:
            proxy = ProxyManager.get_proxy()
            # Hier wird der View-Request simuliert/gesendet
            # TikTok benötigt oft einen Heartbeat an die room_id
            params = urlencode({
                "room_id": room_id,
                "device_id": did,
                "iid": iid,
                "device_type": "SM-G973N",
                "last_install_time": int(time.time())
            })
            url = f"https://api.tiktokv.com/v1/live/room/enter/?{params}"
            
            # Request senden
            res = requests.get(url, proxies=proxy, timeout=10, verify=False)
            
            if res.status_code == 200:
                with _lock: success += 1
                # WICHTIG: Stay Alive Delay (Simuliert menschliches Zuschauen)
                # Zu kurzes Delay = Kick | Zu langes Delay = Bot verschwindet aus Liste
                time.sleep(random.randint(25, 45)) 
            else:
                time.sleep(10) # Bei Fehler kurz warten
                
        except Exception:
            time.sleep(5)
            continue

# --- ROBUSTER DEVICE SPLIT ---
def safe_split(line):
    p = line.split(':')
    return p if len(p) >= 4 else [str(random.getrandbits(60)), str(random.getrandbits(60)), str(uuid.uuid4()), "openudid123"]

# --- HAUPTMENÜ ---
def main():
    global success, active_bots
    os.system("cls" if os.name == "nt" else "clear")
    status = "ON" if ProxyManager.enabled else "OFF"
    
    Banner() # Dein originaler Banner-Aufruf
    print(f"{Colors.white}Status: {Colors.green}Bots Active: {active_bots} | Total Visits: {success}")
    print(f"{Colors.yellow}[7] Toggle Proxy Rotation ({status})")
    print(f"{Colors.cyan}[6] Start Live View Loop (Stay Alive)")
    
    choice = input(f"\n{Colors.white}Option >> ")

    if choice == '7':
        ProxyManager.enabled = not ProxyManager.enabled
        return main()

    if choice == '6':
        room_id = input("Enter Room ID: ")
        threads = int(input("How many Bots (Threads): "))
        
        with open("devices.txt", "r") as f:
            devices = f.read().splitlines()

        print(f"{Colors.green}Starting Bots... Close program to stop.")
        for _ in range(threads):
            dev = safe_split(random.choice(devices))
            threading.Thread(target=live_stay_alive_loop, 
                             args=(dev[0], dev[1], dev[2], dev[3], room_id), 
                             daemon=True).start()
        
        # UI Update Loop
        while True:
            sys.stdout.write(f"\r{Colors.white}Active Bots: {Colors.cyan}{active_bots} {Colors.white}| Visits: {Colors.green}{success}")
            sys.stdout.flush()
            time.sleep(1)

if __name__ == "__main__":
    main()
