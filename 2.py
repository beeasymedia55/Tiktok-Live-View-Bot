import requests, re, time, random, os, threading, uuid, asyncio, aiohttp, sys, hashlib, json, binascii
from urllib.parse import urlencode, quote
from pystyle import Colors, Colorate, Center, Write
from colorama import Fore, init

init(autoreset=True)

# Statistiken & State
class State:
    joined, likes, views, shares, favs, errors = 0, 0, 0, 0, 0, 0
    valid_proxies = []
    use_proxies = False
    lock = threading.Lock()

# Device & Header Konfiguration aus allen Modulen
DEVICES = ["SM-G9900", "SM-A528B", "SM-F711B", "SM-N976N", "Pixel 6", "Samsung S21"]

def make_tiktok_params(aid="1233", extra_params=None):
    ts = str(int(time.time() * 1000))
    params = {
        "aid": aid, "device_platform": "android", "os_version": "12",
        "version_code": "370805", "version_name": "37.8.5", "device_brand": "samsung",
        "device_type": random.choice(DEVICES), "language": "en", "region": "US",
        "app_name": "musical_ly", "ad_set_id": "0", "_rticket": ts, "cdid": str(uuid.uuid4())
    }
    if extra_params: params.update(extra_params)
    return params

# =============================================================================
# PROXY & SESSION MANAGEMENT
# =============================================================================

def scrape_and_test_proxies():
    print(f"{Fore.YELLOW}[*] Scrape & Test Proxies...")
    sources = [
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"
    ]
    raw = []
    for s in sources:
        try: raw.extend(requests.get(s, timeout=5).text.splitlines())
        except: pass
    
    def test(p_str):
        try:
            r = requests.get("https://api-va.tiktokv.com/aweme/v1/feed/", 
                             proxies={"http": f"http://{p_str}", "https": f"http://{p_str}"}, timeout=3)
            if r.status_code == 200: State.valid_proxies.append(p_str)
        except: pass

    threads = []
    for p in list(set(raw))[:1000]:
        t = threading.Thread(target=test, args=(p,))
        t.start(); threads.append(t)
        if len(threads) > 100:
            for t in threads: t.join()
            threads = []
    print(f"{Fore.GREEN}[+] {len(State.valid_proxies)} Proxies bereit.")

def check_sessions(filename):
    if not os.path.exists(filename): return
    print(f"{Fore.YELLOW}[*] Validierung läuft...")
    valid = []
    with open(filename, "r") as f:
        sids = [l.strip().split(":")[0] for l in f if l.strip()]
    for s in sids:
        try:
            r = requests.get("https://api-va.tiktokv.com/passport/auth/status/", 
                             headers={"Cookie": f"sessionid={s}"}, timeout=5).json()
            if r.get("data", {}).get("is_login"):
                valid.append(s); print(f"{Fore.GREEN}[LIVE] {s[:12]}...")
        except: pass
    with open(filename, "w") as f:
        for v in valid: f.write(v + "\n")

def generate_guest_ids(amount):
    print(f"{Fore.YELLOW}[*] Generiere {amount} Guest-IDs...")
    count = 0
    with open("ssid.txt", "a") as f:
        for _ in range(amount):
            try:
                url = "https://api.tiktokv.com/passport/guest/startup/?" + urlencode({"app_name": "musically_go", "aid": 1340, "device_id": str(random.randint(10**18, 10**19))})
                r = requests.post(url, timeout=10)
                sid = re.search(r"sessionid=([^;]+)", r.headers.get("Set-Cookie", ""))
                if sid: 
                    f.write(sid.group(1) + "\n"); count += 1
            except: pass
    print(f"{Fore.CYAN}[!] {count} IDs gespeichert.")

# =============================================================================
# WORKER ENGINES (LIVE & VIDEO)
# =============================================================================

def grab_room_id(user):
    try:
        r = requests.get(f"https://www.tiktok.com/@{user.replace('@','')}/live", timeout=10).text
        return re.search(r'\"roomId\":\"(\d+)\"', r).group(1)
    except: return None

def live_worker(sid, room_id):
    proxy = {"http": f"http://{random.choice(State.valid_proxies)}"} if State.use_proxies and State.valid_proxies else None
    params = make_tiktok_params(aid="1988", extra_params={"room_id": room_id, "scene": "live_room"})
    headers = {"Cookie": f"sessionid={sid}", "User-Agent": "com.zhiliaoapp.musically/2023708050"}
    
    try:
        # Signatur-Prozess für Room Entry
        import SignerPy
        sig = SignerPy.sign(params=params, payload={"room_id": str(room_id)})
        headers.update({"X-Gorgon": sig.get("x-gorgon"), "X-Khronos": sig.get("x-khronos")})
        
        requests.post("https://webcast16-normal-c-alisg.tiktokv.com/webcast/room/enter/", 
                      params=params, headers=headers, proxies=proxy, timeout=10)
        with State.lock: State.joined += 1
        
        while True:
            requests.get("https://webcast16-normal-c-alisg.tiktokv.com/webcast/room/ping/", 
                         params=params, headers=headers, proxies=proxy, timeout=7)
            if random.random() > 0.7:
                requests.post("https://webcast16-normal-c-alisg.tiktokv.com/webcast/stats/heart/", 
                              params=params, headers=headers, proxies=proxy)
                with State.lock: State.likes += 1
            time.sleep(20)
    except:
        with State.lock: State.errors += 1

def video_worker(target_id, mode):
    while True:
        try:
            proxy = {"http": f"http://{random.choice(State.valid_proxies)}"} if State.use_proxies and State.valid_proxies else None
            params = make_tiktok_params()
            endpoint = "/aweme/v1/aweme/stats/"
            payload = f"item_id={target_id}&share_delta=1" if mode == "shares" else f"aweme_id={target_id}&play_delta=1"
            
            import SignerPy
            sig = SignerPy.sign(params=params, payload=payload)
            headers = {"X-Gorgon": sig.get("x-gorgon"), "X-Khronos": sig.get("x-khronos"), "Content-Type": "application/x-www-form-urlencoded"}
            
            r = requests.post(f"https://api-va.tiktokv.com{endpoint}", params=params, data=payload, headers=headers, proxies=proxy, timeout=5)
            if r.status_code == 200:
                with State.lock:
                    if mode == "shares": State.shares += 1
                    else: State.views += 1
            time.sleep(0.2)
        except: 
            with State.lock: State.errors += 1

# =============================================================================
# DASHBOARD & MENU
# =============================================================================

def dashboard():
    while True:
        os.system('clear' if os.name != 'nt' else 'cls')
        print(Colorate.Horizontal(Colors.blue_to_purple, Center.XCenter("TIKTOK OVERLORD v19 - OMEGA")))
        print(f"\n {Fore.GREEN}LIVE: {State.joined} | LIKES: {State.likes} | VIEWS: {State.views} | SHARES: {State.shares}")
        print(f" {Fore.RED}ERRORS: {State.errors} | PROXIES: {len(State.valid_proxies)}")
        print(f"\n {Fore.WHITE}Threads: {threading.active_count()} | Mode: Active")
        time.sleep(2)

def main():
    os.system('clear' if os.name != 'nt' else 'cls')
    print(Colorate.Horizontal(Colors.red_to_yellow, Center.XCenter("TIKTOK OMEGA TOOLSET")))
    print(f"\n[1] Live Booster (Guest/Accs)  [5] Check session.txt")
    print(f"[2] Video Viewbot (Ultra)      [6] Check ssid.txt")
    print(f"[3] Video Sharebot (Ranking)   [7] Guest-SID Generator")
    print(f"[4] Room-ID Grabber            [8] Proxy Scraper & Tester")
    
    choice = input("\nAuswahl > ")
    
    if choice == '8': scrape_and_test_proxies(); input(); main()
    if choice == '7': generate_guest_ids(int(input("Menge: "))); main()
    if choice in ['5','6']: check_sessions("session.txt" if choice=='5' else "ssid.txt"); main()
    
    if choice in ['1','2','3']:
        target = input("Target (ID/@User): ")
        if choice == '1' and not target.isdigit(): target = grab_room_id(target)
        State.use_proxies = input("Proxies nutzen? (y/n): ").lower() == 'y'
        
        threading.Thread(target=dashboard, daemon=True).start()
        
        if choice == '1':
            f_name = input("File (ssid.txt / session.txt): ")
            with open(f_name, "r") as f: sids = [l.strip() for l in f]
            for s in sids: threading.Thread(target=live_worker, args=(s, target), daemon=True).start()
        else:
            threads = int(input("Threads: "))
            mode = "views" if choice == '2' else "shares"
            for _ in range(threads): threading.Thread(target=video_worker, args=(target, mode), daemon=True).start()
        
        while True: time.sleep(1)

if __name__ == "__main__":
    main()
