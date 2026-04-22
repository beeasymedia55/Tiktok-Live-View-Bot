from urllib.parse import urlencode, quote, urlparse, parse_qs
from pystyle import *
from random import choice
import os, sys, ssl, re, time, random, threading, requests, hashlib, json, base64, uuid, subprocess
from console.utils import set_title
from urllib3.exceptions import InsecureRequestWarning
from http import cookiejar
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from html5lib import *

# --- INITIALISIERUNG ---
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context
_lock = threading.Lock()
success = 0
errors = 0

# --- PROXY SERVER LISTE ---
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
    return choice(list(proxy_servers.values()))

# --- PYSIGNER (Ultitikbot) ---
class PySigner:
    @staticmethod
    def get_signature(params, payload="", cookies="", ticket=""):
        ts = int(time.time())
        str_to_hash = f"{params}{payload}{cookies}{ts}"
        gorgon_hash = hashlib.md5(str_to_hash.encode()).hexdigest()
        return {"X-Gorgon": f"0404b0d30000{gorgon_hash}", "X-Khronos": str(ts)}

# --- DEVICE GENERATOR (tool.py) ---
class AdvancedDeviceGenerator:
    @staticmethod
    def generate_v2():
        device_id = str(random.randint(7000000000000000000, 7999999999999999999))
        iid = str(random.randint(7000000000000000000, 7999999999999999999))
        cdid = str(uuid.uuid4())
        openudid = hashlib.md5(str(time.time()).encode()).hexdigest()[:16]
        return f"{device_id}:{iid}:{cdid}:{openudid}"

# --- ORIGINAL BANNER ---
def Banner():
    os.system("cls" if os.name == "nt" else "clear")
    banner_text = r"""
████████╗██╗██╗  ██╗████████╗ ██████╗ ██╗  ██╗    ██████╗  ██████╗ ████████╗
╚══██╔══╝██║██║ ██╔╝╚══██╔══╝██╔═══██╗██║ ██╔╝    ██╔══██╗██╔═══██╗╚══██╔══╝
   ██║   ██║█████╔╝    ██║   ██║   ██║█████╔╝     ██████╔╝██║   ██║   ██║   
   ██║   ██║██╔═██╗    ██║   ██║   ██║██╔═██╗     ██╔══██╗██║   ██║   ██║   
   ██║   ██║██║  ██╗   ██║   ╚██████╔╝██║  ██╗    ██████╔╝╚██████╔╝   ██║   
   ╚═╝   ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝    ╚═════╝  ╚═════╝    ╚═╝
    """
    print(Center.XCenter(Colorate.Vertical(Colors.yellow_to_green, banner_text, 2)))

# --- FIX: ROBUSTER UNPACKER ---
def safe_split_device(device_str):
    parts = device_str.split(':')
    if len(parts) >= 4:
        return parts[0], parts[1], parts[2], parts[3]
    else:
        # Falls das Format falsch ist, generiere on-the-fly ein neues
        new_dev = AdvancedDeviceGenerator.generate_v2().split(':')
        return new_dev[0], new_dev[1], new_dev[2], new_dev[3]

# --- PLATZHALTER FÜR DEINE ORIGINALEN SEND-FUNKTIONEN ---
# (Stelle sicher, dass diese Funktionen did, iid, cdid, openudid akzeptieren)
def sendLiveViews(did, iid, cdid, openudid):
    global success, errors
    # Beispielhafter Request mit Proxy-Rotation
    proxy = get_rotated_proxy()
    try:
        # Hier dein originaler Request-Code...
        # Wenn erfolgreich:
        with _lock:
            success += 1
            print(f"{Colors.green}[+] Success: {success} | Proxy: {proxy}")
    except:
        with _lock:
            errors += 1

def main():
    Banner()
    print(f"{Colors.cyan}[1] Video Views       [2] Video Shares")
    print(f"{Colors.cyan}[3] Video Favorites   [4] Video Hearts")
    print(f"{Colors.cyan}[5] Followers         [6] Live Views")
    print(f"{Colors.purple}[8] Generate New Devices")
    
    try:
        sendType = int(input(f"\n{Colors.white}Option >> "))
        
        if sendType == 8:
            num = int(input("How many? "))
            with open("devices.txt", "a") as f:
                for _ in range(num): f.write(AdvancedDeviceGenerator.generate_v2() + "\n")
            return main()

        amountTosend = int(input("Amount >> "))
        threads_count = int(input("Threads >> "))

        if not os.path.exists("devices.txt"):
            print("Creating devices.txt...")
            with open("devices.txt", "w") as f: f.write(AdvancedDeviceGenerator.generate_v2() + "\n")

        with open("devices.txt", "r") as f:
            devices = f.read().splitlines()

        def thread_starter():
            while success < amountTosend:
                device_str = choice(devices)
                # NUTZE DEN SAFE SPLIT HIER:
                did, iid, cdid, openudid = safe_split_device(device_str)
                
                if sendType == 6:
                    sendLiveViews(did, iid, cdid, openudid)
                # Füge hier die anderen Typen (1-5) analog hinzu

        for _ in range(threads_count):
            threading.Thread(target=thread_starter, daemon=True).start()

        while success < amountTosend:
            time.sleep(1)

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(3)
        main()

if __name__ == "__main__":
    main()
