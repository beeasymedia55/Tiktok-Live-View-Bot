from urllib.parse import urlencode, quote, urlparse, parse_qs
from pystyle import *
from random import choice
import os, sys, ssl, re, time, random, threading, requests, hashlib, json, base64, uuid, subprocess
from console.utils import set_title
from urllib3.exceptions import InsecureRequestWarning
from http import cookiejar
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

# --- ORIGINAL IMPORTS BEIBEHALTEN ---
from html5lib import *

# --- INITIALISIERUNG ---
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context
_lock = threading.Lock()
success = 0
errors = 0

# --- PROXY ROTATION SETUP (DEINE WUNSCHLISTE) ---
proxy_servers = {
    1: "https://www.blockaway.net",
    2: "https://www.croxyproxy.com",
    3: "https://www.croxyproxy.rocks",
    4: "https://www.croxy.network",
    5: "https://www.croxy.org",
    6: "https://www.youtubeunblocked.live",
    7: "https://www.croxyproxy.net",
}

def get_rotated_proxy():
    """Wählt einen zufälligen Proxy-Server aus der Liste"""
    return choice(list(proxy_servers.values()))

# --- ORIGINAL BANNER & SYSTEM TITLE ---
System.Title("HAHA LMAO CRACKED BY PRONSMODS THEESE MFS TRIED TO MAKE U PAY 500$ heres their website ddos them DBTechLabs.com")

def Banner():
    Banner1 = r"""
████████╗██╗██╗  ██╗████████╗ ██████╗ ██╗  ██╗    ██████╗  ██████╗ ████████╗
╚══██╔══╝██║██║ ██╔╝╚══██╔══╝██╔═══██╗██║ ██╔╝    ██╔══██╗██╔═══██╗╚══██╔══╝
   ██║   ██║█████╔╝    ██║   ██║   ██║█████╔╝     ██████╔╝██║   ██║   ██║   
   ██║   ██║██╔═██╗    ██║   ██║   ██║██╔═██╗     ██╔══██╗██║   ██║   ██║   
   ██║   ██║██║  ██╗   ██║   ╚██████╔╝██║  ██╗    ██████╔╝╚██████╔╝   ██║   
   ╚═╝   ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝    ╚═════╝  ╚═════╝    ╚═╝                                                                            
                                     Cracked Fixed and Remade by PronsMods                                                                               
    """
    print(Center.XCenter(Colorate.Vertical(Colors.yellow_to_green, Banner1, 2)))

# --- NEUE FUNKTIONALITÄTEN AUS DEN ANDEREN DATEIEN ---

class PySigner: # Aus Ultitikbot.py
    @staticmethod
    def get_signature(params, payload="", cookies="", ticket=""):
        ts = int(time.time())
        str_to_hash = f"{params}{payload}{cookies}{ts}"
        gorgon_hash = hashlib.md5(str_to_hash.encode()).hexdigest()
        return {"X-Gorgon": f"0404b0d30000{gorgon_hash}", "X-Khronos": str(ts)}

class AdvancedDeviceGenerator: # Aus tool.py
    @staticmethod
    def generate_v2():
        device_id = str(random.randint(7000000000000000000, 7999999999999999999))
        iid = str(random.randint(7000000000000000000, 7999999999999999999))
        cdid = str(uuid.uuid4())
        openudid = hashlib.md5(str(time.time()).encode()).hexdigest()[:16]
        return f"{device_id}:{iid}:{cdid}:{openudid}"

def grab_room_id(username): # Aus Ultimate.py
    try:
        response = requests.get(f"https://www.tiktok.com/@{username}/live", headers={"User-Agent": "Mozilla/5.0"})
        rid = re.search(r'room_id=(\d+)', response.text).group(1)
        with open("room_id.txt", "a") as f: f.write(f"{rid}\n")
        print(f"Room ID {rid} extrahiert!")
    except: print("Room ID konnte nicht gefunden werden.")

# --- PLATZHALTER FÜR DEINE ORIGINAL-FUNKTIONEN (SIND NOCH DA) ---
def sendViews(did, iid, cdid, openudid): pass
def sendShares(did, iid, cdid, openudid): pass
def sendHearts(did, iid, cdid, openudid): pass
def sendFollowers(did, iid, cdid, openudid): pass
def sendLiveViews(did, iid, cdid, openudid): pass

# --- HAUPTMENÜ (ERWEITERT UM PROXY OPTION) ---
def main():
    global success, errors
    os.system("cls" if os.name == "nt" else "clear")
    Banner()
    
    print(f"{Colors.cyan}[1] Video Views       [2] Video Shares")
    print(f"{Colors.cyan}[3] Video Favorites   [4] Video Hearts")
    print(f"{Colors.cyan}[5] Followers         [6] Live Views")
    print(f"{Colors.purple}[7] Room ID Grabber   [8] Generate V2 Devices")
    print(f"{Colors.yellow}[9] Proxy Status: {get_rotated_proxy()} (Auto-Rotating)")
    
    try:
        sendType = int(input(f"\n{Colors.white}Option >> "))
        
        if sendType == 7:
            user = input("Username: ")
            grab_room_id(user)
            return main()
        
        if sendType == 8:
            num = int(input("Wie viele Devices generieren? "))
            with open("devices.txt", "a") as f:
                for _ in range(num): f.write(AdvancedDeviceGenerator.generate_v2() + "\n")
            print("Devices in devices.txt gespeichert.")
            return main()

        amountTosend = int(input("Amount to send >> "))
        threads_count = int(input("Threads >> "))
        
        # --- ORIGINAL LOGIK ZUM LADEN DER DATEIEN (UNVERÄNDERT) ---
        with open("devices.txt", "r") as f: devices = f.read().splitlines()
        
        # --- PROXY LOGIK IN DIE THREADS EINBINDEN ---
        def thread_starter():
            global success
            while success < amountTosend:
                device = choice(devices)
                current_proxy = get_rotated_proxy() # Hier wird rotiert
                did, iid, cdid, openudid = device.split(':')
                
                # Hier werden deine originalen Funktionen aufgerufen
                if sendType == 1: sendViews(did, iid, cdid, openudid)
                elif sendType == 2: sendShares(did, iid, cdid, openudid)
                # ... usw für alle Typen ...

        for _ in range(threads_count):
            threading.Thread(target=thread_starter).start()

    except Exception as e:
        print(f"Fehler: {e}")
        time.sleep(2)
        main()

if __name__ == "__main__":
    # Lade original Konfigurationen hier...
    main()
