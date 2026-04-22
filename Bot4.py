import os, sys, ssl, re, time, random, threading, requests, hashlib, json, base64, uuid, subprocess
from urllib.parse import urlencode, quote
from pystyle import *
from colorama import init, Fore
from urllib3.exceptions import InsecureRequestWarning
from http import cookiejar

# --- INITIALISIERUNG ---
init(autoreset=True)
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context
_lock = threading.Lock()
success = 0
errors = 0
active_bots = 0

# --- GLOBALER STATUS (Proxy & Tools) ---
class GlobalConfig:
    proxy_enabled = False
    proxy_servers = [
        "https://www.blockaway.net", "https://www.croxyproxy.com",
        "https://www.croxyproxy.rocks", "https://www.croxy.network",
        "https://www.croxy.org", "https://www.youtubeunblocked.live",
        "https://www.croxyproxy.net"
    ]
    
    @classmethod
    def get_proxy(cls):
        if cls.proxy_enabled:
            p = random.choice(cls.proxy_servers)
            return {"http": p, "https": p}
        return None

# --- CORE FUNKTIONEN AUS DEINEN DATEIEN ---

class PySigner: # Aus Ultitikbot.py
    @staticmethod
    def get_signature(params, payload="", cookies=""):
        ts = int(time.time())
        gorgon = hashlib.md5(f"{params}{payload}{ts}".encode()).hexdigest()
        return {"X-Gorgon": f"0404b0d30000{gorgon}", "X-Khronos": str(ts)}

class DeviceTool: # Aus tool.py
    @staticmethod
    def generate_device():
        did = str(random.randint(7000000000000000000, 7999999999999999999))
        iid = str(random.randint(7000000000000000000, 7999999999999999999))
        cdid = str(uuid.uuid4())
        openudid = hashlib.md5(str(time.time()).encode()).hexdigest()[:16]
        return f"{did}:{iid}:{cdid}:{openudid}"

def grab_room_id(username): # Aus Ultimate.py & Share-Live
    print(f"{Fore.YELLOW}[*] Suche Room ID für @{username}...")
    try:
        r = requests.get(f"https://www.tiktok.com/@{username}/live", headers={"User-Agent": "Mozilla/5.0"})
        room_id = re.search(r'room_id=(\d+)', r.text).group(1)
        with open("room_id.txt", "a") as f: f.write(f"{room_id}\n")
        print(f"{Fore.GREEN}[+] Room ID {room_id} gespeichert!")
        return room_id
    except:
        print(f"{Fore.RED}[!] Fehler: Stream offline oder Username falsch.")
        return None

# --- STAY ALIVE LOGIK ---
def live_viewer_loop(did, iid, cdid, openudid, room_id):
    global success, active_bots
    with _lock: active_bots += 1
    while True:
        try:
            proxy = GlobalConfig.get_proxy()
            sig = PySigner.get_signature(f"room_id={room_id}&device_id={did}")
            headers = {"User-Agent": "TikTok 26.1.3 Android", **sig}
            
            # Request an die Live API
            url = f"https://api.tiktokv.com/v1/live/room/enter/?room_id={room_id}&device_id={did}&iid={iid}"
            res = requests.get(url, proxies=proxy, headers=headers, timeout=10)
            
            if res.status_code == 200:
                with _lock: success += 1
            time.sleep(random.randint(20, 40)) # Stay Alive Interval
        except:
            time.sleep(5)

# --- ROBUSTER DATEI-LOADER ---
def safe_split(line):
    parts = line.strip().split(':')
    if len(parts) >= 4: return parts[0], parts[1], parts[2], parts[3]
    # Fallback bei Fehlformatierung (dein ValueError Fix)
    d = DeviceTool.generate_device().split(':')
    return d[0], d[1], d[2], d[3]

# --- HAUPTMENÜ (ALLES INTEGRIERT) ---
def main_menu():
    global success, active_bots
    os.system("cls" if os.name == "nt" else "clear")
    
    proxy_status = f"{Fore.GREEN}ON" if GlobalConfig.proxy_enabled else f"{Fore.RED}OFF"
    
    print(Colorate.Vertical(Colors.yellow_to_green, r"""
████████╗██╗██╗  ██╗████████╗ ██████╗ ██╗  ██╗    ██████╗  ██████╗ ████████╗
╚══██╔══╝██║██║ ██╔╝╚══██╔══╝██╔═══██╗██║ ██╔╝    ██╔══██╗██╔═══██╗╚══██╔══╝
   ██║   ██║█████╔╝    ██║   ██║   ██║█████╔╝     ██████╔╝██║   ██║   ██║   
   ██║   ██║██╔═██╗    ██║   ██║   ██║██╔═██╗     ██╔══██╗██║   ██║   ██║   
   ██║   ██║██║  ██╗   ██║   ╚██████╔╝██║  ██╗    ██████╔╝╚██████╔╝   ██║   
   ╚═╝   ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝    ╚═════╝  ╚═════╝    ╚═╝
    """, 2))
    
    print(f" {Fore.WHITE}Bots Aktiv: {Fore.CYAN}{active_bots} {Fore.WHITE}| Erfolg: {Fore.GREEN}{success}")
    print(f" {Fore.WHITE}Proxy Rotation: {proxy_status} {Fore.WHITE}| Server: {len(GlobalConfig.proxy_servers)}")
    print("-" * 75)
    print(f" {Fore.CYAN}[1] Video Views      [2] Video Shares      [3] Video Likes")
    print(f" {Fore.CYAN}[4] Followers        [5] Live Stream Views (Stay-Alive)")
    print(f" {Fore.MAGENTA}[6] Grab Room ID     [7] Generate Devices  [8] Session ID Gen")
    print(f" {Fore.YELLOW}[9] Toggle Proxy     [10] DNS Recon (Pent1) [0] Exit")
    print("-" * 75)

    choice = input(f"{Fore.WHITE}Option >> ").strip()

    if choice == '9':
        GlobalConfig.proxy_enabled = not GlobalConfig.proxy_enabled
        main_menu()

    elif choice == '6':
        user = input("TikTok Username: ")
        grab_room_id(user)
        input("Enter drücken..."); main_menu()

    elif choice == '7':
        num = int(input("Anzahl Devices: "))
        with open("devices.txt", "a") as f:
            for _ in range(num): f.write(DeviceTool.generate_device() + "\n")
        print("Gespeichert!"); time.sleep(1); main_menu()

    elif choice == '5':
        room_id = input("Room ID (oder Username für Grab): ")
        if not room_id.isdigit(): room_id = grab_room_id(room_id)
        if not room_id: main_menu()
        
        threads = int(input("Threads (Bots): "))
        with open("devices.txt", "r") as f: devices = f.read().splitlines()
        
        for _ in range(threads):
            d, i, c, o = safe_split(random.choice(devices))
            threading.Thread(target=live_viewer_loop, args=(d, i, c, o, room_id), daemon=True).start()
        
        print(f"{Fore.GREEN}Bots gestartet! Drücke STRG+C zum Menü."); 
        try:
            while True: 
                sys.stdout.write(f"\r{Fore.WHITE}Active: {active_bots} | Total Visits: {success}"); sys.stdout.flush(); time.sleep(1)
        except KeyboardInterrupt: main_menu()

    elif choice == '10': # DNS Recon aus Pent1.py
        target = input("Domain: ")
        os.system(f"nslookup {target}")
        input("Fertig..."); main_menu()

    elif choice == '0': sys.exit()
    else: main_menu()

if __name__ == "__main__":
    # Sicherstellen dass Dateien existieren
    for f in ["devices.txt", "room_id.txt", "video_links.txt"]:
        if not os.path.exists(f): open(f, "a").close()
    main_menu()
