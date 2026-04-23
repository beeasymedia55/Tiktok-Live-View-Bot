import requests, os, sys, threading, time, random, re, json, hashlib, uuid, asyncio, aiohttp
from urllib.parse import urlencode
from colorama import init, Fore
from pystyle import Colorate, Colors, Center

init(autoreset=True)

class GlobalState:
    success, fails, joined, likes, shares, views = 0, 0, 0, 0, 0, 0
    proxies = []
    use_proxies = False
    active = True

class TikTokCore:
    @staticmethod
    def get_device():
        return {"did": str(random.randint(10**18, 10**19)), "iid": str(random.randint(10**18, 10**19))}

    @staticmethod
    def sign(params):
        # 2026 Simulation der SignerPy Logik
        ts = int(time.time())
        return {"x-gorgon": f"0404b0d30000{hashlib.md5(str(ts).encode()).hexdigest()}", "x-khronos": str(ts)}

class Scraper:
    @staticmethod
    def get_room_id(username):
        """Verbesserter Scraper mit Fallback-Logik"""
        username = username.replace("@", "")
        url = f"https://www.tiktok.com/@{username}/live"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }
        try:
            response = requests.get(url, headers=headers, timeout=10)
            html = response.text
            
            # Pattern 1: Direktes roomId im JSON
            rid = re.search(r'\"roomId\":\"(\d+)\"', html)
            if rid: return rid.group(1)
            
            # Pattern 2: room_id im script tag
            rid = re.search(r'\"room_id\":\"(\d+)\"', html)
            if rid: return rid.group(1)

            # Pattern 3: Falls User offline oder Seite geblockt
            if "LIVE is finished" in html or "is currently offline" in html:
                return "OFFLINE"
            
            return None
        except:
            return None

# --- ENGINES ---
async def video_engine(target, mode):
    async with aiohttp.ClientSession() as session:
        while GlobalState.active:
            try:
                dev = TikTokCore.get_device()
                params = {"device_id": dev['did'], "iid": dev['iid'], "aid": "1233"}
                if mode == "views": params.update({"aweme_id": target, "play_delta": "1"})
                else: params.update({"item_id": target, "share_delta": "1"})
                
                sig = TikTokCore.sign(params)
                headers = {"User-Agent": "com.zhiliaoapp.musically/2023503040", **sig}
                
                async with session.post("https://api-va.tiktokv.com/aweme/v1/aweme/stats/", params=params, headers=headers) as r:
                    if r.status == 200:
                        if mode == "views": GlobalState.views += 1
                        else: GlobalState.shares += 1
                    else: GlobalState.fails += 1
            except: GlobalState.fails += 1
            await asyncio.sleep(0.01)

def live_worker(sid, room_id):
    dev = TikTokCore.get_device()
    params = {"room_id": room_id, "aid": "1988", "device_id": dev['did'], "iid": dev['iid']}
    headers = {"Cookie": f"sessionid={sid}", **TikTokCore.sign(params)}
    try:
        requests.post("https://webcast16-normal-c-alisg.tiktokv.com/webcast/room/enter/", params=params, headers=headers, timeout=5)
        GlobalState.joined += 1
        while GlobalState.active:
            requests.post("https://webcast16-normal-c-alisg.tiktokv.com/webcast/stats/heart/", params=params, headers=headers, timeout=5)
            GlobalState.likes += 1
            time.sleep(random.randint(5, 10))
    except: GlobalState.fails += 1

# --- DASHBOARD & UI ---
def dashboard():
    while GlobalState.active:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Colorate.Horizontal(Colors.blue_to_purple, Center.XCenter("STUPID OMEGA MANAGER - 2026 EDITION")))
        print(f"\n [V] Views: {GlobalState.views} | [S] Shares: {GlobalState.shares}")
        print(f" [L] Live-Zuschauer: {GlobalState.joined} | [H] Likes: {GlobalState.likes}")
        print(f" [E] Fehler: {GlobalState.fails} | Threads: {threading.active_count()}")
        time.sleep(1.5)

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Colorate.Horizontal(Colors.red_to_yellow, Center.XCenter("ULTRA BOT DASHBOARD")))
    print(f"\n[1] Video Views (Async)  [4] Room-ID Finder")
    print(f"[2] Video Shares         [5] Guest SID Gen")
    print(f"[3] Live Booster         [0] Exit")
    
    choice = input("\nAuswahl > ")
    if choice == '0': sys.exit()
    
    target = input("Target (@User oder ID): ")
    
    # Room-ID Check für Live
    if choice == '3':
        if not target.isdigit():
            print(f"{Fore.YELLOW}[*] Suche Room-ID für {target}...")
            rid = Scraper.get_room_id(target)
            if rid == "OFFLINE":
                print(f"{Fore.RED}[!] User scheint wirklich offline zu sein.")
            elif rid:
                print(f"{Fore.GREEN}[+] Room-ID gefunden: {rid}")
                target = rid
            else:
                print(f"{Fore.YELLOW}[!] Konnte ID nicht automatisch finden.")
                target = input(f"{Fore.CYAN}Bitte Room-ID manuell eingeben: ")
    
    threads = int(input("Threads/Anzahl: "))
    threading.Thread(target=dashboard, daemon=True).start()

    if choice in ['1', '2']:
        mode = "views" if choice == '1' else "shares"
        loop = asyncio.new_event_loop()
        for _ in range(threads):
            threading.Thread(target=lambda: loop.run_until_complete(video_engine(target, mode)), daemon=True).start()
    elif choice == '3':
        if os.path.exists("ssid.txt"):
            with open("ssid.txt", "r") as f: sids = [l.strip() for l in f if l.strip()]
            for s in sids[:threads]:
                threading.Thread(target=live_worker, args=(s, target), daemon=True).start()
        else:
            print(f"{Fore.RED}Keine ssid.txt gefunden! Bitte erst SIDs generieren.")

    while True: time.sleep(1)

if __name__ == "__main__":
    main()
