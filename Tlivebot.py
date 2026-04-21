import asyncio, aiohttp, os, random, re, sys, time, threading, binascii, uuid, requests
from urllib.parse import urlencode
from pystyle import Center, Colorate, Colors, Write, System
from user_agent import generate_user_agent

# --- Initialization & Signer Check ---
try:
    import SignerPy
except ImportError:
    pass

class State:
    success = 0
    fails = 0
    start_time = time.time()
    is_running = False
    target_id = ""
    # Hardcoded authenticated proxies from your setup
    PROXIES = [
        "31.59.20.176:6754:hxidjrjw:nylyfhelpvdx", "198.23.239.134:6540:hxidjrjw:nylyfhelpvdx",
        "45.38.107.97:6014:hxidjrjw:nylyfhelpvdx", "107.172.163.27:6543:hxidjrjw:nylyfhelpvdx",
        "198.105.121.200:6462:hxidjrjw:nylyfhelpvdx", "216.10.27.159:6837:hxidjrjw:nylyfhelpvdx",
        "142.111.67.146:5611:hxidjrjw:nylyfhelpvdx", "191.96.254.138:6185:hxidjrjw:nylyfhelpvdx",
        "31.58.9.4:6077:hxidjrjw:nylyfhelpvdx", "23.26.71.145:5628:hxidjrjw:nylyfhelpvdx"
    ]

# --- Core Logic Functions ---
def get_room_id(username):
    """Integrated from Ultimate.py & Share-Live.py"""
    headers = {"User-Agent": generate_user_agent(), "Accept": "*/*"}
    url = f"https://www.tiktok.com/api-live/user/room/?aid=1988&uniqueId={username}"
    try:
        res = requests.get(url, headers=headers, timeout=10).json()
        return res["data"]["user"]["roomId"]
    except: return None

class TikTokEngine:
    def get_proxy(self):
        p = random.choice(State.PROXIES).split(':')
        return f"http://{p[2]}:{p[3]}@{p[0]}:{p[1]}"

    async def worker(self, session, sem, mode):
        # Endpoints mapped to menu options
        endpoints = {
            "1": "https://api16-core-c-alisg.tiktokv.com/aweme/v1/aweme/stats/",
            "2": "https://api16-core-c-alisg.tiktokv.com/aweme/v1/commit/item/share/",
            "3": "https://api16-core-c-alisg.tiktokv.com/aweme/v1/aweme/collect/",
            "4": "https://api16-core-c-alisg.tiktokv.com/aweme/v1/commit/item/digg/",
            "5": "https://api16-core-c-alisg.tiktokv.com/aweme/v1/commit/follow/user/",
            "6": "https://webcast16-normal-useastred.tiktokv.eu/webcast/room/enter/"
        }
        
        while State.is_running:
            async with sem:
                try:
                    proxy = self.get_proxy()
                    did, iid = str(random.randint(10**18, 10**19)), str(random.randint(10**18, 10**19))
                    
                    params = {
                        "device_id": did, "iid": iid, "version_code": "400304",
                        "device_platform": "android", "aid": "1233",
                        "cdid": str(uuid.uuid4()), "openudid": binascii.hexlify(os.urandom(8)).decode()
                    }

                    # Mode-specific payload/params
                    payload = ""
                    if mode == "1": payload = f"item_id={State.target_id}&play_delta=1"
                    elif mode == "2": payload = f"item_id={State.target_id}&share_delta=1"
                    elif mode in ["3", "4"]: params["aweme_id"] = State.target_id
                    elif mode == "5": params["user_id"] = State.target_id
                    elif mode == "6":
                        params.update({"room_id": State.target_id, "store-idc": "no1a", "tt-target-idc": "eu-ttp2", "d_ticket": "27"})
                        payload = f"room_id={State.target_id}&hold_living_room=1&enter_source=live_cell"

                    query = urlencode(params)
                    try:
                        sig = SignerPy.XG(query, payload, "d_ticket=27" if mode == "6" else "")
                        xg, xk = sig.get("X-Gorgon"), sig.get("X-Khronos")
                    except: xg, xk = "", str(int(time.time()))

                    headers = {
                        "User-Agent": "com.ss.android.ugc.trill/400304 (Linux; U; Android 12; Pixel 6)",
                        "X-Gorgon": xg, "X-Khronos": xk, "Content-Type": "application/x-www-form-urlencoded"
                    }
                    if mode == "6": headers["Cookie"] = "d_ticket=27"

                    async with session.post(endpoints[mode], params=params, data=payload, headers=headers, proxy=proxy, timeout=10, ssl=False) as r:
                        resp = await r.json()
                        if r.status == 200 and resp.get("status_code") == 0: State.success += 1
                        else: State.fails += 1
                except: State.fails += 1
                await asyncio.sleep(0.001)

# --- UI & Threading ---
def live_stats():
    while True:
        if State.is_running:
            elapsed = time.time() - State.start_time
            rps = State.success / elapsed if elapsed > 0 else 0
            System.Title(f"SUCCESS: {State.success} | FAIL: {State.fails} | {rps:.1f} r/s")
        time.sleep(0.5)

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    b = r"""
████████╗██╗██╗  ██╗████████╗ ██████╗ ██╗  ██╗
╚══██╔══╝██║██║ ██╔╝╚══██╔══╝██╔═══██╗██║ ██╔╝
   ██║   ██║█████╔╝    ██║   ██║   ██║█████╔╝ 
   ██║   ██║██╔═██╗    ██║   ██║   ██║██╔═██╗ 
   ██║   ██║██║  ██╗   ██║   ╚██████╔╝██║  ██╗
   ╚═╝   ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
    [ ULTIMATE INTEGRATED BOT - 2026 EDITION ]"""
    print(Colorate.Vertical(Colors.yellow_to_green, Center.XCenter(b)))

async def main():
    threading.Thread(target=live_stats, daemon=True).start()
    while True:
        banner()
        print(Colorate.Horizontal(Colors.green_to_yellow, "\n[1] Views [2] Shares [3] Favorites [4] Likes [5] Followers [6] Live Entry [7] RoomID Resolver [0] Exit"))
        choice = Write.Input("\nSelection > ", Colors.white_to_green, interval=0.001)

        if choice == "0": break
        if choice == "7":
            user = Write.Input("Username > ", Colors.white_to_green)
            rid = get_room_id(user)
            print(f"Room ID: {rid}" if rid else "User is Offline")
            time.sleep(3); continue

        State.target_id = Write.Input("Target ID/URL > ", Colors.white_to_green)
        if "/" in State.target_id: # Basic extractor
            match = re.search(r'(\d{15,20})', State.target_id)
            if match: State.target_id = match.group(1)
        
        threads = int(Write.Input("Threads > ", Colors.white_to_green))
        
        State.success, State.fails, State.is_running = 0, 0, True
        State.start_time = time.time()
        
        sem = asyncio.Semaphore(threads)
        async with aiohttp.ClientSession() as session:
            tasks = [TikTokEngine().worker(session, sem, choice) for _ in range(threads)]
            try:
                await asyncio.gather(*tasks)
            except KeyboardInterrupt:
                State.is_running = False

if __name__ == "__main__":
    if sys.platform == 'win32': asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())
