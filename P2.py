#!/usr/bin/env python3
# =====================================================
# ULTIMATIVES TIKTOK BOT TOOLKIT v4.0 - NUR TIKTOK FEATURES
# Asyncio + Premium Proxies + SignerPy + 1000+ RPS
# =====================================================

import asyncio
import aiohttp
import os
import random
import re
import sys
import time
import threading
import binascii
import uuid
import requests
from urllib.parse import urlencode
from colorama import init, Fore, Back, Style
from user_agent import generate_user_agent

# Mock SignerPy (ersetze mit echtem Import falls verfügbar)
class MockSignerPy:
    @staticmethod
    def XG(query, payload, ticket):
        return {"X-Gorgon": "0404b0d30000" + "0"*40, "X-Khronos": str(int(time.time()))}

try:
    import SignerPy
except ImportError:
    SignerPy = MockSignerPy

# Initialize colorama
init(autoreset=True)

# =====================================================
# STATE & PREMIUM PROXIES
# =====================================================

class State:
    success = 0
    fails = 0
    start_time = time.time()
    is_running = False
    target_id = ""
    
    # PREMIUM AUTHENTICATED PROXIES (ersetze mit deinen)
    PROXIES = [
        "31.59.20.176:6754:hxidjrjw:nylyfhelpvdx", "198.23.239.134:6540:hxidjrjw:nylyfhelpvdx",
        "45.38.107.97:6014:hxidjrjw:nylyfhelpvdx", "107.172.163.27:6543:hxidjrjw:nylyfhelpvdx",
        "198.105.121.200:6462:hxidjrjw:nylyfhelpvdx", "216.10.27.159:6837:hxidjrjw:nylyfhelpvdx",
        "142.111.67.146:5611:hxidjrjw:nylyfhelpvdx", "191.96.254.138:6185:hxidjrjw:nylyfhelpvdx",
        "31.58.9.4:6077:hxidjrjw:nylyfhelpvdx", "23.26.71.145:5628:hxidjrjw:nylyfhelpvdx"
    ]

# =====================================================
# ROOM ID RESOLVER
# =====================================================

def get_room_id(username):
    """TikTok Live Room ID Resolver"""
    headers = {
        "User-Agent": generate_user_agent(),
        "Accept": "*/*",
        "Referer": "https://www.tiktok.com/"
    }
    url = f"https://www.tiktok.com/api-live/user/room/?aid=1988&app_name=tiktok_web&uniqueId={username}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        if data.get("status_code") == 0:
            return data["data"]["user"]["roomId"]
        return None
    except:
        return None

# =====================================================
# ASYNC TIKTOK ENGINE (1000+ RPS)
# =====================================================

class TikTokEngine:
    def get_proxy(self):
        """Random Premium Proxy Selector"""
        p = random.choice(State.PROXIES).split(':')
        return f"http://{p[2]}:{p[3]}@{p[0]}:{p[1]}"

    async def worker(self, session, sem, mode):
        """Async Worker für alle TikTok Features"""
        endpoints = {
            "1": "https://api16-core-c-alisg.tiktokv.com/aweme/v1/aweme/stats/",      # Views
            "2": "https://api16-core-c-alisg.tiktokv.com/aweme/v1/commit/item/share/", # Shares
            "3": "https://api16-core-c-alisg.tiktokv.com/aweme/v1/aweme/collect/",     # Favorites
            "4": "https://api16-core-c-alisg.tiktokv.com/aweme/v1/commit/item/digg/",  # Likes/Hearts
            "5": "https://api16-core-c-alisg.tiktokv.com/aweme/v1/commit/follow/user/",# Followers
            "6": "https://webcast16-normal-useastred.tiktokv.eu/webcast/room/enter/"   # Live Entry
        }
        
        mode_names = {
            "1": "VIEWS", "2": "SHARES", "3": "FAVORITES", 
            "4": "LIKES", "5": "FOLLOWERS", "6": "LIVE"
        }
        
        while State.is_running:
            async with sem:
                try:
                    # Random Device IDs
                    did = str(random.randint(10**18, 10**19))
                    iid = str(random.randint(10**18, 10**19))
                    
                    # Base Parameters
                    params = {
                        "device_id": did,
                        "iid": iid,
                        "version_code": "400304",
                        "device_platform": "android",
                        "aid": "1233",
                        "cdid": str(uuid.uuid4()),
                        "openudid": binascii.hexlify(os.urandom(8)).decode()
                    }

                    # Mode-specific Payloads
                    payload = ""
                    if mode == "1":  # Views
                        payload = f"item_id={State.target_id}&play_delta=1"
                    elif mode == "2":  # Shares
                        payload = f"item_id={State.target_id}&share_delta=1"
                    elif mode == "3":  # Favorites
                        params["aweme_id"] = State.target_id
                    elif mode == "4":  # Likes
                        params["aweme_id"] = State.target_id
                    elif mode == "5":  # Followers
                        params["user_id"] = State.target_id
                    elif mode == "6":  # Live
                        params.update({
                            "room_id": State.target_id,
                            "store-idc": "no1a",
                            "tt-target-idc": "eu-ttp2",
                            "d_ticket": "27"
                        })
                        payload = f"room_id={State.target_id}&hold_living_room=1&enter_source=live_cell"

                    # SignerPy Signature
                    query = urlencode(params)
                    sig = SignerPy.XG(query, payload, "d_ticket=27" if mode == "6" else "")
                    xg = sig.get("X-Gorgon", "")
                    xk = sig.get("X-Khronos", str(int(time.time())))

                    # Headers
                    headers = {
                        "User-Agent": "com.ss.android.ugc.trill/400304 (Linux; U; Android 12; Pixel 6)",
                        "X-Gorgon": xg,
                        "X-Khronos": xk,
                        "Content-Type": "application/x-www-form-urlencoded",
                        "Accept": "*/*"
                    }
                    if mode == "6":
                        headers["Cookie"] = "d_ticket=27"

                    # Async Request
                    proxy = self.get_proxy()
                    async with session.post(
                        endpoints[mode],
                        params=params,
                        data=payload,
                        headers=headers,
                        proxy=proxy,
                        timeout=aiohttp.ClientTimeout(total=10),
                        ssl=False
                    ) as response:
                        
                        if response.status == 200:
                            try:
                                resp_json = await response.json()
                                if resp_json.get("status_code") == 0:
                                    State.success += 1
                                    print(f"{Fore.GREEN}[{mode_names[mode]}] SUCCESS #{State.success} | ID: {State.target_id[:12]}...{Style.RESET_ALL}", end='\r')
                                else:
                                    State.fails += 1
                            except:
                                State.fails += 1
                        else:
                            State.fails += 1

                except Exception:
                    State.fails += 1
                
                await asyncio.sleep(0.0005)  # 2000+ RPS möglich

# =====================================================
# LIVE STATISTICS
# =====================================================

def live_stats():
    """Live RPS & Stats Display"""
    while True:
        if State.is_running:
            elapsed = time.time() - State.start_time
            rps = State.success / elapsed if elapsed > 0 else 0
            rpm = rps * 60
            
            stats = (f"{Fore.CYAN}[STATS] "
                    f"SUCCESS: {Fore.GREEN}{State.success}{Style.RESET_ALL} | "
                    f"FAILS: {Fore.RED}{State.fails}{Style.RESET_ALL} | "
                    f"RPS: {Fore.YELLOW}{rps:.1f}{Style.RESET_ALL} | "
                    f"RPM: {rpm:.0f}{Style.RESET_ALL}")
            
            print(f"\r{stats:<80}", end="")
        time.sleep(0.5)

# =====================================================
# BANNER & UI
# =====================================================

def banner():
    """Epic TikTok Bot Banner"""
    os.system('cls' if os.name == 'nt' else 'clear')
    b = f"""
{Fore.RED}
    ╔══════════════════════════════════════════════════════╗
    ║  {Fore.YELLOW}TIKTOK ULTIMATE BOT v4.0 - 1000+ RPS{Style.RESET_ALL} {Fore.RED}║
    ║  {Fore.CYAN}Async • Premium Proxies • SignerPy • Multi-Feature{Style.RESET_ALL} {Fore.RED}║
    ╚══════════════════════════════════════════════════════╝
{Fore.WHITE}
    {Fore.GREEN}1.{Style.RESET_ALL} Video VIEWS     {Fore.RED}4.{Style.RESET_ALL} LIKES/Hearts
    {Fore.GREEN}2.{Style.RESET_ALL} SHARES          {Fore.RED}5.{Style.RESET_ALL} FOLLOWERS  
    {Fore.GREEN}3.{Style.RESET_ALL} FAVORITES      {Fore.RED}6.{Style.RESET_ALL} LIVE Stream
    {Fore.YELLOW}7.{Style.RESET_ALL} Room ID Resolver   {Fore.RED}0.{Style.RESET_ALL} EXIT
{Style.RESET_ALL}
    """
    print(b)

# =====================================================
# MAIN ASYNC LOOP
# =====================================================

async def main_loop():
    """Haupt Asyncio Loop"""
    threading.Thread(target=live_stats, daemon=True).start()
    
    while True:
        banner()
        choice = input(f"{Fore.BOLD}{Fore.RED}Wähle Funktion [0-7]: {Style.RESET_ALL}").strip()
        
        if choice == "0":
            print(f"{Fore.GREEN}Tschüss!{Style.RESET_ALL}")
            sys.exit(0)
        
        if choice == "7":  # Room ID Resolver
            username = input(f"{Fore.YELLOW}Username (z.B. @user): {Style.RESET_ALL}").strip()
            if username.startswith('@'):
                username = username[1:]
            
            print(f"{Fore.CYAN}[RESOLVER] Suche Room ID für {username}...{Style.RESET_ALL}")
            room_id = get_room_id(username)
            
            if room_id:
                print(f"{Fore.GREEN}✅ ROOM ID: {room_id}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Verwende diese ID für Live Views (Option 6)!{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ User ist OFFLINE oder Fehler{Style.RESET_ALL}")
            
            input(f"{Fore.YELLOW}Enter drücken...{Style.RESET_ALL}")
            continue
        
        if choice not in ["1", "2", "3", "4", "5", "6"]:
            print(f"{Fore.RED}Ungültige Option!{Style.RESET_ALL}")
            time.sleep(2)
            continue
        
        # Target ID Input + Auto-Extractor
        target_input = input(f"{Fore.YELLOW}Video/Live ID oder URL: {Style.RESET_ALL}").strip()
        
        # Auto-Extract ID from URL
        id_match = re.search(r'(\d{15,20})', target_input)
        if id_match:
            State.target_id = id_match.group(1)
            print(f"{Fore.GREEN}Auto-extrahiert: {State.target_id[:12]}...{Style.RESET_ALL}")
        else:
            State.target_id = target_input
        
        # Threads Input
        threads = input(f"{Fore.YELLOW}Threads (500-2000): {Style.RESET_ALL}").strip()
        try:
            threads = int(threads)
            if threads > 3000: threads = 2000
            if threads < 50: threads = 50
        except:
            threads = 500
        
        # Start Async Bot
        print(f"{Fore.GREEN}🚀 Starte {threads} Threads auf {State.target_id[:12]}...{Style.RESET_ALL}")
        State.is_running = True
        State.success = 0
        State.fails = 0
        State.start_time = time.time()
        
        sem = asyncio.Semaphore(threads)
        connector = aiohttp.TCPConnector(limit=threads * 2, limit_per_host=100)
        
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = [TikTokEngine().worker(session, sem, choice) for _ in range(threads)]
            try:
                await asyncio.gather(*tasks)
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}⏹️ GESTOPPT! Erfolg: {State.success} | Fehlschläge: {State.fails}{Style.RESET_ALL}")
                State.is_running = False
                time.sleep(2)

# =====================================================
# ENTRY POINT
# =====================================================

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProctorEventLoopPolicy())
    
    print(f"{Fore.GREEN}TikTok Ultimate Bot v4.0 geladen!{Style.RESET_ALL}")
    asyncio.run(main_loop())
