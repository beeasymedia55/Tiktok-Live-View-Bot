#!/usr/bin/env python3
# ==============================================================================
# TIKTOK ULTIMATE MASTER FRAMEWORK v8.0 - 2026 FULL EDITION
# INTEGRATED: PYSIGNER, LIVE SUITE, VIDEO BOOST, PROXY ROTATOR
# ==============================================================================

import os, sys, threading, time, requests, hashlib, random, re, json, base64
from urllib.parse import urlencode, quote
from colorama import init, Fore, Style, Back
from urllib3.exceptions import InsecureRequestWarning

# --- INITIALISIERUNG ---
init(autoreset=True)
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# --- PYSIGNER / GORGON CORE (Logic from Stupid (3).py & P4.py) ---
class PySigner:
    """Simuliert oder nutzt die Signatur-Library für X-Gorgon/X-Khronos"""
    @staticmethod
    def get_signature(params, payload="", cookies="", ticket=""):
        # Zeitstempel generieren
        ts = int(time.time())
        
        # MD5 Hash-Kette für Gorgon (Simulation der PySigner Library)
        str_to_hash = f"{params}{payload}{cookies}{ts}"
        gorgon_hash = hashlib.md5(str_to_hash.encode()).hexdigest()
        
        # 2026er Gorgon Prefix
        x_gorgon = f"0404b0d30000{gorgon_hash}"
        x_khronos = str(ts)
        
        return {
            "X-Gorgon": x_gorgon,
            "X-Khronos": x_khronos,
            "X-Stub": hashlib.md5(payload.encode()).hexdigest() if payload else "0"*32
        }

# --- GLOBALER STATUS ---
class GlobalState:
    success = 0
    fails = 0
    use_proxies = False
    proxy_mode = "Croxy" # "Premium" oder "Croxy"
    is_running = False
    lock = threading.Lock()

# --- DATEN-ZENTRALE (Integrierte Listen) ---
class DataCenter:
    def __init__(self):
        self.domains = [
            "api-h2.tiktokv.com", 
            "api16-core-c-useast1a.tiktokv.com",
            "api22-core-c-useast1a.tiktokv.com"
        ]
        # Format: did:iid:cdid:openudid
        self.devices = [
            "728394058372615:728394058372615:8c6a2f1b3e5d:9273840582716253",
            "384756291038475:384756291038475:a1b2c3d4e5f6:1827364556473829",
            "992837465019283:992837465019283:f9e8d7c6b5a4:5566778899001122"
        ]
        self.version = "340101"
        self.app_name = "musically_go"
        self.web_proxies = ["https://www.croxyproxy.com", "https://www.proxysite.com"]

# --- TIKTOK BOT ENGINE ---
class TikTokEngine:
    def __init__(self):
        self.data = DataCenter()
        self.session = requests.Session()

    def get_proxy(self):
        if not GlobalState.use_proxies: return None
        p = random.choice(self.data.web_proxies)
        return {"http": p, "https": p}

    def build_headers(self, params, payload, did, iid):
        sigs = PySigner.get_signature(params, payload)
        headers = {
            "Host": random.choice(self.data.domains),
            "Connection": "keep-alive",
            "User-Agent": f"com.zhiliaoapp.musically/{self.data.version} (Linux; Android 14; en_US; {did})",
            "X-Gorgon": sigs["X-Gorgon"],
            "X-Khronos": sigs["X-Khronos"],
            "X-Stub": sigs["X-Stub"],
            "sdk-version": "2",
            "x-did": did,
            "x-iid": iid
        }
        return headers

    def execute(self, mode, target_id):
        try:
            # Device laden
            did, iid, cdid, openudid = random.choice(self.data.devices).split(':')
            domain = random.choice(self.data.domains)

            # Endpunkte & Payloads (Live vs Video)
            modes = {
                '1': ('aweme/v1/aweme/stats/', f"item_id={target_id}&play_delta=1&device_id={did}"),
                '2': ('aweme/v1/commit/item/digg/', f"aweme_id={target_id}&type=1&device_id={did}"),
                '3': ('aweme/v1/aweme/stats/', f"item_id={target_id}&share_delta=1&device_id={did}"),
                '4': ('aweme/v1/aweme/stats/', f"item_id={target_id}&collect_delta=1&device_id={did}"),
                '5': ('aweme/v1/live/room/enter/', f"room_id={target_id}&enter_source=live_cell&device_id={did}"),
                '6': ('aweme/v1/live/like/', f"room_id={target_id}&count={random.randint(2,5)}&device_id={did}"),
                '7': ('aweme/v1/live/share/', f"room_id={target_id}&share_type=1&device_id={did}")
            }

            path, payload = modes[mode]
            params = f"aid=1988&device_id={did}&device_platform=android&version_code={self.data.version}"
            url = f"https://{domain}/{path}?{params}"

            headers = self.build_headers(params, payload, did, iid)
            
            resp = self.session.post(
                url, 
                data=payload, 
                headers=headers, 
                proxies=self.get_proxy(),
                timeout=7, 
                verify=False
            )

            with GlobalState.lock:
                if resp.status_code in [200, 201]:
                    GlobalState.success += 1
                else:
                    GlobalState.fails += 1
        except Exception:
            with GlobalState.lock:
                GlobalState.fails += 1

# --- BENUTZEROBERFLÄCHE ---
class Interface:
    def __init__(self):
        self.engine = TikTokEngine()

    def banner(self):
        os.system('cls||clear')
        print(f"{Fore.RED}{Style.BRIGHT}{'='*65}")
        print(f"{Fore.WHITE}   TIKTOK ULTIMATE MASTER v8.0 - PySigner & Live Suite")
        print(f"{Fore.RED}{'='*65}")
        print(f"{Fore.GREEN} Success: {GlobalState.success} | {Fore.RED}Fails: {GlobalState.fails} | {Fore.YELLOW}Proxy: {GlobalState.use_proxies}")
        print(f"{Fore.RED}{'='*65}\n")

    def main_menu(self):
        while True:
            self.banner()
            print(f"{Fore.CYAN}[VIDEO FEATURES]{Fore.WHITE}")
            print(" 1. Views      2. Likes      3. Shares      4. Favorites")
            print(f"\n{Fore.MAGENTA}[LIVE FEATURES]{Fore.WHITE}")
            print(" 5. Room Enter 6. Live Likes  7. Live Shares")
            print(f"\n{Fore.YELLOW}[SETTINGS]{Fore.WHITE}")
            print(f" 8. Toggle Proxy Rotation [{'ON' if GlobalState.use_proxies else 'OFF'}]")
            print(" 0. Exit")
            
            choice = input(f"\n{Fore.RED}Choice >> {Fore.WHITE}").strip()
            
            if choice == '0': sys.exit()
            if choice == '8': 
                GlobalState.use_proxies = not GlobalState.use_proxies
                continue

            target = input(f"{Fore.CYAN}Target (URL/ID): {Fore.WHITE}").strip()
            # ID extrahieren
            target_id = re.search(r'(\d{15,25})', target).group(1) if re.search(r'\d{15,25}', target) else target
            threads = int(input(f"{Fore.CYAN}Threads: {Fore.WHITE}"))

            print(f"\n{Fore.GREEN}🚀 Deploying threads...")
            for _ in range(threads):
                threading.Thread(target=self.bot_loop, args=(choice, target_id), daemon=True).start()
            
            input(f"\n{Fore.YELLOW}Running... Press Enter to stop.")

    def bot_loop(self, mode, tid):
        while True:
            self.engine.execute(mode, tid)
            time.sleep(0.05)

if __name__ == "__main__":
    Interface().main_menu()
