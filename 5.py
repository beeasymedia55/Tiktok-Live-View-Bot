import os, sys, threading, time, random, re, json, uuid, string, binascii, asyncio, aiohttp
import requests
from urllib.parse import urlencode
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore, Style
from pystyle import Colorate, Colors, Center

init(autoreset=True)

# =============================================================================
# GLOBAL STATE & CONFIG
# =============================================================================
class State:
    success, fails, views, shares, likes, favs, live_joined, live_hearts = 0,0,0,0,0,0,0,0
    proxies = []
    valid_proxies = []
    active = True
    use_proxies = False

# =============================================================================
# CORE: DEVICE & SIGNATURE ENGINE
# =============================================================================
class TikTokCore:
    @staticmethod
    def get_device():
        return {
            "did": str(random.randint(10**18, 10**19)),
            "iid": str(random.randint(10**18, 10**19)),
            "cdid": str(uuid.uuid4()),
            "openudid": binascii.hexlify(os.urandom(8)).decode()
        }

    @staticmethod
    def sign(params, payload=None, cookie=None):
        try:
            import SignerPy
            return SignerPy.sign(params=params, payload=payload, cookie=cookie)
        except:
            ts = int(time.time())
            return {"x-gorgon": f"0404b0d30000{hashlib.md5(str(ts).encode()).hexdigest()}", "x-khronos": str(ts)}

class Scraper:
    @staticmethod
    def get_room_id(username):
        username = username.replace("@", "")
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}
        try:
            html = requests.get(f"https://www.tiktok.com/@{username}/live", headers=headers, timeout=10).text
            rid = re.search(r'\"roomId\":\"(\d+)\"', html) or re.search(r'\"room_id\":\"(\d+)\"', html)
            return rid.group(1) if rid else None
        except: return None

# =============================================================================
# PROXY ENGINE
# =============================================================================
class ProxyEngine:
    @staticmethod
    def scrape():
        print(f"{Fore.YELLOW}[*] Scrape öffentliche Proxys...")
        sources = [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"
        ]
        for url in sources:
            try: State.proxies += requests.get(url, timeout=5).text.splitlines()
            except: pass
        State.proxies = list(set(State.proxies))
        print(f"{Fore.GREEN}[+] {len(State.proxies)} Proxys geladen.")

    @staticmethod
    def test_worker(proxy):
        try:
            px = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
            r = requests.get("https://api-va.tiktokv.com/aweme/v1/feed/", proxies=px, timeout=3)
            if r.status_code in [200, 400, 403]: State.valid_proxies.append(proxy)
        except: pass

    @staticmethod
    def run_tester():
        print(f"{Fore.YELLOW}[*] Validiere Proxys (Threaded)...")
        with ThreadPoolExecutor(max_workers=100) as executor:
            executor.map(ProxyEngine.test_worker, State.proxies[:1000]) # Max 1000 for speed
        print(f"{Fore.GREEN}[+] {len(State.valid_proxies)} schnelle Proxys bereit.")

# =============================================================================
# ACCOUNT CREATOR & SESSION MANAGER
# =============================================================================
class AccountManager:
    TM_HEADERS = {"Application-Name": "web", "Application-Version": "4.0.0", "User-Agent": "Mozilla/5.0", "Accept": "*/*", "Origin": "https://temp-mail.io"}
    
    @staticmethod
    def create_guest_sid():
        dev = TikTokCore.get_device()
        params = urlencode({"app_name": "musically_go", "aid": 1340, "device_id": dev['did'], "device_platform": "android"})
        try:
            r = requests.post(f"https://api.tiktokv.com/passport/guest/startup/?{params}", timeout=10)
            sid = re.search(r"sessionid=([^;]+)", r.headers.get("Set-Cookie", ""))
            if sid:
                with open("ssid.txt", "a") as f: f.write(sid.group(1) + "\n")
                return True
        except: return False

    @staticmethod
    def validate_sessions(file_name):
        if not os.path.exists(file_name): return
        print(f"{Fore.YELLOW}[*] Prüfe {file_name}...")
        valid = []
        with open(file_name, "r") as f: sids = [l.strip().split(":")[0] for l in f if l.strip()]
        for s in sids:
            try:
                r = requests.get("https://api-va.tiktokv.com/passport/auth/status/", headers={"Cookie": f"sessionid={s}"}, timeout=5).json()
                if r.get("data", {}).get("is_login"): valid.append(s)
            except: pass
        with open(file_name, "w") as f:
            for v in valid: f.write(v + "\n")
        print(f"{Fore.GREEN}[+] {len(valid)} Sessions aktiv.")

    @staticmethod
    def worker_register():
        session = requests.Session()
        # 1. Email holen
        try:
            resp = session.post("https://api.internal.temp-mail.io/api/v3/email/new", headers=AccountManager.TM_HEADERS, json={"min_name_length": 10})
            email, tm_token = resp.json()["email"], resp.json()["token"]
        except: return

        pw = "".join(random.choices(string.ascii_letters + string.digits, k=12))
        dev = TikTokCore.get_device()
        params = {"device_id": dev['did'], "iid": dev['iid'], "aid": "1233", "device_platform": "android", "os": "android"}
        
        # 2. Send Code
        url_send = "https://api16-normal-c-alisg.tiktokv.com/passport/email/send_code/?" + urlencode(params)
        payload_send = {"email": email, "type": "34", "mix_mode": "1"}
        headers = {"User-Agent": "com.zhiliaoapp.musically/2023708050", **TikTokCore.sign(params, payload_send)}
        session.post(url_send, headers=headers, data=payload_send)

        # 3. Wait for Code
        code = None
        for _ in range(12):
            time.sleep(5)
            try:
                r = session.get(f"https://api.internal.temp-mail.io/api/v3/email/{email}/messages", headers=AccountManager.TM_HEADERS).json()
                for msg in r:
                    m = re.search(r'(\d{6})', msg.get("body_text", ""))
                    if m: code = m.group(1); break
                if code: break
            except: pass
        
        if not code: return

        # 4. Verify & Register
        url_reg = "https://api16-normal-c-alisg.tiktokv.com/passport/email/register_verify_login/?" + urlencode(params)
        payload_reg = {"email": email, "code": code, "password": pw, "mix_mode": "1"}
        headers = {"User-Agent": "com.zhiliaoapp.musically/2023708050", **TikTokCore.sign(params, payload_reg)}
        
        r = session.post(url_reg, headers=headers, data=payload_reg).json()
        if r.get("data", {}).get("session_key"):
            s_key = r["data"]["session_key"]
            with open("session.txt", "a") as f: f.write(f"{s_key}\n")
            with open("accounts.txt", "a") as f: f.write(f"{email}:{pw}\n")
            State.success += 1
        else: State.fails += 1

# =============================================================================
# ENGAGEMENT ENGINES (10 ENDPOINTS)
# =============================================================================
class EngagementSuite:
    @staticmethod
    async def video_engine(target, mode, sids):
        async with aiohttp.ClientSession() as session:
            while State.active:
                try:
                    dev = TikTokCore.get_device()
                    params = {"device_id": dev['did'], "iid": dev['iid'], "aid": "1233", "device_platform": "android"}
                    payload = None
                    url = "https://api-va.tiktokv.com"
                    
                    # Video 5 Endpoints
                    if mode == "1": # Views
                        params.update({"aweme_id": target, "play_delta": "1"})
                        url += "/aweme/v1/aweme/stats/"
                    elif mode == "2": # Shares
                        params.update({"item_id": target, "share_delta": "1"})
                        url += "/aweme/v1/aweme/stats/"
                    elif mode == "3": # Likes (Needs SID)
                        params.update({"aweme_id": target, "type": "1"})
                        url += "/aweme/v1/commit/item/digg/"
                    elif mode == "4": # Favs (Needs SID)
                        params.update({"aweme_id": target, "action": "1"})
                        url += "/aweme/v1/aweme/collect/"
                    elif mode == "5": # Comment Like (Needs SID)
                        params.update({"comment_id": target, "type": "1"})
                        url += "/aweme/v1/comment/digg/"

                    sid = random.choice(sids) if sids else ""
                    headers = {"User-Agent": "com.zhiliaoapp.musically/2023708050", "Cookie": f"sessionid={sid}", **TikTokCore.sign(params)}
                    proxy = f"http://{random.choice(State.valid_proxies)}" if State.use_proxies and State.valid_proxies else None

                    async with session.post(url, params=params, headers=headers, proxy=proxy, timeout=5) as r:
                        if r.status == 200:
                            if mode=="1": State.views+=1
                            elif mode=="2": State.shares+=1
                            elif mode=="3": State.likes+=1
                            elif mode=="4": State.favs+=1
                            else: State.success+=1
                        else: State.fails+=1
                except: State.fails+=1
                await asyncio.sleep(0.01)

    @staticmethod
    def live_engine(target, mode, sid):
        dev = TikTokCore.get_device()
        params = {"room_id": target, "aid": "1988", "device_id": dev['did'], "iid": dev['iid']}
        headers = {"Cookie": f"sessionid={sid}", "User-Agent": "com.zhiliaoapp.musically/2023708050"}
        proxy = {"http": f"http://{random.choice(State.valid_proxies)}"} if State.use_proxies and State.valid_proxies else None
        
        url = "https://webcast16-normal-c-alisg.tiktokv.com"
        
        try:
            # Entry is always needed
            headers.update(TikTokCore.sign(params))
            requests.post(f"{url}/webcast/room/enter/", params=params, headers=headers, proxies=proxy)
            State.live_joined += 1
            
            while State.active:
                if mode == "7": # Hearts
                    headers.update(TikTokCore.sign(params))
                    requests.post(f"{url}/webcast/stats/heart/", params=params, headers=headers, proxies=proxy)
                    State.live_hearts += 1
                elif mode == "8": # Share Live
                    headers.update(TikTokCore.sign(params))
                    requests.post(f"{url}/webcast/room/share/", params=params, headers=headers, proxies=proxy)
                    State.shares += 1
                elif mode == "9": # Chat
                    payload = {"content": random.choice(["Great stream!", "Wow", "Hello", "Nice!"])}
                    headers.update(TikTokCore.sign(params, payload))
                    requests.post(f"{url}/webcast/room/chat/", params=params, data=payload, headers=headers, proxies=proxy)
                    State.success += 1
                elif mode == "10": # Follow
                    headers.update(TikTokCore.sign(params))
                    requests.post(f"{url}/webcast/room/follow/", params=params, headers=headers, proxies=proxy)
                    State.success += 1
                    break # Follow ist ein One-Time Event
                
                time.sleep(random.randint(5, 12))
                
            # Leave gracefully
            if mode in ["6", "7", "8", "9"]:
                headers.update(TikTokCore.sign(params))
                requests.post(f"{url}/webcast/room/leave/", params=params, headers=headers, proxies=proxy)
                State.live_joined -= 1
        except: State.fails += 1

# =============================================================================
# DASHBOARD & MAIN MENU
# =============================================================================
def dashboard():
    while State.active:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Colorate.Horizontal(Colors.red_to_blue, Center.XCenter("TIKTOK ULTIMATE OMEGA SUITE v10")))
        print(f"\n {Fore.CYAN}--- VIDEO STATS ---")
        print(f" Views: {State.views} | Shares: {State.shares} | Likes: {State.likes} | Favs: {State.favs}")
        print(f"\n {Fore.MAGENTA}--- LIVE STATS ---")
        print(f" Viewer: {State.live_joined} | Hearts: {State.live_hearts} | Misc Success: {State.success}")
        print(f"\n {Fore.WHITE}--- SYSTEM ---")
        print(f" Errors: {Fore.RED}{State.fails}{Fore.WHITE} | Proxys: {len(State.valid_proxies)} | Threads: {threading.active_count()}")
        time.sleep(1.5)

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = """
    [ ULTIMATE SUITE MENU ]
    =======================
    [ SETUP & TOOLS ]
    1. Proxy Scraper & Validator
    2. Account Creator (Temp-Mail)
    3. Guest SID Generator
    4. Session Validator (Health Check)
    5. RoomID Resolver (@User -> ID)
    
    [ ENGAGEMENT BOT ]
    6. Video Suite (Views/Shares/Likes/Favs/Comments)
    7. Live Suite (Enter/Hearts/Share/Chat/Follow)
    
    0. Exit
    """
    print(Colorate.Horizontal(Colors.green_to_blue, banner))
    choice = input("\nAuswahl > ")

    if choice == "0": sys.exit()
    elif choice == "1": ProxyEngine.scrape(); ProxyEngine.run_tester(); input("Enter..."); main()
    elif choice == "2":
        amt = int(input("Wieviele Accounts erstellen? "))
        with ThreadPoolExecutor(max_workers=10) as ex:
            for _ in range(amt): ex.submit(AccountManager.worker_register)
        print(f"Erstellt: {State.success}"); input("Enter..."); main()
    elif choice == "3":
        amt = int(input("Wieviele Guest-SIDs? "))
        for _ in range(amt): AccountManager.create_guest_sid()
        input("Enter..."); main()
    elif choice == "4":
        AccountManager.validate_sessions("session.txt")
        AccountManager.validate_sessions("ssid.txt")
        input("Enter..."); main()
    elif choice == "5":
        user = input("TikTok Username (@): ")
        print(f"RoomID: {Scraper.get_room_id(user)}")
        input("Enter..."); main()
    elif choice in ["6", "7"]:
        target = input("Target ID (Video/Comment/Room): ")
        if choice == "7" and not target.isdigit():
            print("[*] Suche RoomID..."); target = Scraper.get_room_id(target)
            if not target: print("User Offline!"); time.sleep(2); main()
            print(f"[+] Found: {target}")

        if choice == "6":
            print("\n[1] Views [2] Shares [3] Likes [4] Favs [5] Comment Likes")
            mode = input("Video Mode > ")
        else:
            print("\n[6] Enter Only [7] Hearts [8] Share Live [9] Chat Spammer [10] Follow Host")
            mode = input("Live Mode > ")

        State.use_proxies = input("Proxies nutzen? (y/n): ").lower() == 'y'
        if State.use_proxies and not State.valid_proxies: ProxyEngine.scrape(); ProxyEngine.run_tester()

        # Load sessions if needed
        sids = []
        if mode in ["3", "4", "5", "6", "7", "8", "9", "10"]:
            f_name = input("Session File (session.txt / ssid.txt): ")
            if os.path.exists(f_name):
                with open(f_name, "r") as f: sids = [l.strip().split(":")[0] for l in f if l.strip()]
            if not sids and mode != "1" and mode != "2":
                print("Keine Sessions gefunden! Für diese Aktion nötig."); time.sleep(2); main()

        threads = int(input("Threads / Menge: "))
        threading.Thread(target=dashboard, daemon=True).start()

        if choice == "6":
            loop = asyncio.new_event_loop()
            for _ in range(threads):
                threading.Thread(target=lambda: loop.run_until_complete(EngagementSuite.video_engine(target, mode, sids)), daemon=True).start()
        else:
            for s in sids[:threads]:
                threading.Thread(target=EngagementSuite.live_engine, args=(target, mode, s), daemon=True).start()

        while True: time.sleep(1)

if __name__ == "__main__":
    main()
