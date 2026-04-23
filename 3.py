import requests, os, sys, threading, time, random, re, json, hashlib, uuid, binascii, asyncio, aiohttp
from urllib.parse import urlencode, quote
from colorama import init, Fore, Style
from pystyle import Colorate, Colors, Center, Write

init(autoreset=True)

# --- GLOBALER STATUS ---
class GlobalState:
    success, fails, joined, likes, shares, views, favs = 0, 0, 0, 0, 0, 0, 0
    proxies = []
    use_proxies = False
    active = True

# --- TIKTOK CORE ENGINE (Kombiniert aus mobile_api & SignerPy) ---
class TikTokCore:
    @staticmethod
    def get_device():
        """Generiert komplexe Device-Daten für 2026er Protokolle"""
        did = str(random.randint(10**18, 10**19))
        iid = str(random.randint(10**18, 10**19))
        cdid = str(uuid.uuid4())
        openudid = binascii.hexlify(os.urandom(8)).decode()
        return {"did": did, "iid": iid, "cdid": cdid, "openudid": openudid}

    @staticmethod
    def sign(params, payload=None, cookie=None):
        """Signatur-Logik aus Tlivebot & Stupid(3)"""
        try:
            import SignerPy
            return SignerPy.sign(params=params, payload=payload, cookie=cookie)
        except:
            # Fallback Signatur-Simulation
            ts = int(time.time())
            return {"x-gorgon": f"0404b0d30000{hashlib.md5(str(ts).encode()).hexdigest()}", "x-khronos": str(ts)}

# --- MANAGEMENT TOOLS ---
class Manager:
    @staticmethod
    def scrape_proxies():
        print(f"{Fore.YELLOW}[*] Scrape frische Proxies...")
        urls = [
            "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"
        ]
        for url in urls:
            try:
                r = requests.get(url, timeout=5)
                GlobalState.proxies.extend(r.text.splitlines())
            except: pass
        GlobalState.proxies = list(set(GlobalState.proxies))
        print(f"{Fore.GREEN}[+] {len(GlobalState.proxies)} Proxies geladen.")

    @staticmethod
    def generate_guest_id():
        """Logik aus tiktok_sessionid_gen.py"""
        device = TikTokCore.get_device()
        params = urlencode({
            "app_name": "musically_go", "aid": 1340, "device_id": device['did'],
            "version_code": "260802", "device_platform": "android"
        })
        try:
            r = requests.post(f"https://api.tiktokv.com/passport/guest/startup/?{params}", timeout=10)
            sid = re.search(r"sessionid=([^;]+)", r.headers.get("Set-Cookie", ""))
            if sid:
                with open("ssid.txt", "a") as f: f.write(sid.group(1) + "\n")
                return True
        except: return False

    @staticmethod
    def get_room_id(user):
        """Room-ID Grabber aus Ultimate.py"""
        try:
            r = requests.get(f"https://www.tiktok.com/@{user.replace('@','')}/live", timeout=10).text
            return re.search(r'\"roomId\":\"(\d+)\"', r).group(1)
        except: return None

# --- WORKER ENGINES ---
class WorkerEngines:
    @staticmethod
    async def video_booster(target, mode):
        """Ultra-Fast Views/Shares/Favs (basierend auf coc.py & tool.py)"""
        async with aiohttp.ClientSession() as session:
            while GlobalState.active:
                try:
                    dev = TikTokCore.get_device()
                    params = {
                        "device_id": dev['did'], "iid": dev['iid'], "device_platform": "android",
                        "aid": "1233", "version_code": "370805"
                    }
                    if mode == "views": params["aweme_id"] = target; params["play_delta"] = "1"
                    elif mode == "shares": params["item_id"] = target; params["share_delta"] = "1"
                    elif mode == "favs": params["aweme_id"] = target; params["action"] = "1"

                    sig = TikTokCore.sign(params)
                    headers = {"User-Agent": "com.zhiliaoapp.musically/2023503040", **sig}
                    proxy = f"http://{random.choice(GlobalState.proxies)}" if GlobalState.use_proxies else None
                    
                    url = "https://api-va.tiktokv.com/aweme/v1/aweme/stats/"
                    if mode == "favs": url = "https://api-va.tiktokv.com/aweme/v1/aweme/collect/"

                    async with session.post(url, params=params, headers=headers, proxy=proxy, timeout=5) as r:
                        if r.status == 200:
                            if mode == "views": GlobalState.views += 1
                            elif mode == "shares": GlobalState.shares += 1
                            else: GlobalState.favs += 1
                        else: GlobalState.fails += 1
                except: GlobalState.fails += 1
                await asyncio.sleep(0.001)

    @staticmethod
    def live_booster(sid, room_id):
        """Live Entry & Like Spam (aus Tlivebot & Share-Live)"""
        dev = TikTokCore.get_device()
        params = {"room_id": room_id, "aid": "1988", "device_id": dev['did'], "iid": dev['iid']}
        headers = {"Cookie": f"sessionid={sid}", **TikTokCore.sign(params)}
        try:
            # Entry
            requests.post("https://webcast16-normal-c-alisg.tiktokv.com/webcast/room/enter/", params=params, headers=headers)
            GlobalState.joined += 1
            # Like/Ping Loop
            while GlobalState.active:
                requests.post("https://webcast16-normal-c-alisg.tiktokv.com/webcast/stats/heart/", params=params, headers=headers)
                GlobalState.likes += 1
                time.sleep(random.randint(8, 15))
        except: GlobalState.fails += 1

# --- UI & MAIN ---
def dashboard():
    while GlobalState.active:
        os.system('cls' if os.name == 'nt' else 'clear')
        banner = Center.XCenter("TIKTOK STUPID INFINITY - MASTER UI v19")
        print(Colorate.Horizontal(Colors.blue_to_purple, banner))
        print(f"\n{Fore.WHITE} [VIDEO] Views: {Fore.CYAN}{GlobalState.views} | Shares: {GlobalState.shares} | Favs: {GlobalState.favs}")
        print(f"{Fore.WHITE} [LIVE]  Viewer: {Fore.GREEN}{GlobalState.joined} | Likes: {Fore.RED}{GlobalState.likes}")
        print(f"{Fore.WHITE} [DATA]  Proxies: {len(GlobalState.proxies)} | Errors: {Fore.YELLOW}{GlobalState.fails}")
        print(f"\n{Fore.MAGENTA} Threads aktiv: {threading.active_count()}")
        time.sleep(2)

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Colorate.Horizontal(Colors.red_to_yellow, Center.XCenter("INFINITY BOT - ALL FEATURES INTEGRATED")))
    print(f"\n[1] Video Views (Ultra Fast)   [5] Guest-SID Generator")
    print(f"[2] Video Shares               [6] Proxy Scraper & Tester")
    print(f"[3] Video Favorites            [7] Room-ID Finder (@User)")
    print(f"[4] Live Stream Booster        [0] Exit")
    
    choice = input("\nAuswahl > ")
    if choice == '0': sys.exit()
    if choice == '6': Manager.scrape_proxies(); main()
    if choice == '5': 
        amt = int(input("Wieviele SIDs? ")); [Manager.generate_guest_id() for _ in range(amt)]; main()
    if choice == '7':
        print(f"Room ID: {Manager.get_room_id(input('Username: '))}"); input(); main()

    target = input("Target (ID oder @Username): ")
    if not target.isdigit(): 
        print("[*] Suche Room-ID..."); target = Manager.get_room_id(target)
        if not target: print("User Offline!"); time.sleep(2); main()

    GlobalState.use_proxies = input("Proxies nutzen? (y/n): ").lower() == 'y'
    if GlobalState.use_proxies and not GlobalState.proxies: Manager.scrape_proxies()

    threading.Thread(target=dashboard, daemon=True).start()

    if choice in ['1', '2', '3']:
        mode = "views" if choice=='1' else "shares" if choice=='2' else "favs"
        threads = int(input("Threads: "))
        loop = asyncio.new_event_loop()
        for _ in range(threads):
            threading.Thread(target=lambda: loop.run_until_complete(WorkerEngines.video_booster(target, mode)), daemon=True).start()
    elif choice == '4':
        file = input("Session File (ssid.txt): ")
        with open(file, "r") as f: sids = [l.strip() for l in f if l.strip()]
        for s in sids: threading.Thread(target=WorkerEngines.live_booster, args=(s, target), daemon=True).start()

    while True: time.sleep(1)

if __name__ == "__main__":
    main()
