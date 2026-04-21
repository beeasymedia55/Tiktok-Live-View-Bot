#!/usr/bin/env python3
# =====================================================
# ULTIMATIVES TIKTOK BOT TOOLKIT v4.1 - FIX für Termux/Python 3.13
# Asyncio + Premium Proxies + SignerPy + 1000+ RPS - TERMUX KOMPATIBEL
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

# Colorama initialisieren
init(autoreset=True)

# Mock SignerPy (ersetze mit echtem Import)
class MockSignerPy:
    @staticmethod
    def XG(query, payload, ticket):
        return {"X-Gorgon": "0404b0d30000" + "0"*40, "X-Khronos": str(int(time.time()))}

try:
    import SignerPy
except ImportError:
    SignerPy = MockSignerPy

# =====================================================
# STATE & PREMIUM PROXIES
# =====================================================

class State:
    success = 0
    fails = 0
    start_time = time.time()
    is_running = False
    target_id = ""
    
    # PREMIUM PROXIES (ersetze mit deinen)
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
# ASYNC TIKTOK ENGINE
# =====================================================

class TikTokEngine:
    def get_proxy(self):
        p = random.choice(State.PROXIES).split(':')
        return f"http://{p[2]}:{p[3]}@{p[0]}:{p[1]}"

    async def worker(self, session, sem, mode):
        endpoints = {
            "1": "https://api16-core-c-alisg.tiktokv.com/aweme/v1/aweme/stats/",
            "2": "https://api16-core-c-alisg.tiktokv.com/aweme/v1/commit/item/share/",
            "3": "https://api16-core-c-alisg.tiktokv.com/aweme/v1/aweme/collect/",
            "4": "https://api16-core-c-alisg.tiktokv.com/aweme/v1/commit/item/digg/",
            "5": "https://api16-core-c-alisg.tiktokv.com/aweme/v1/commit/follow/user/",
            "6": "https://webcast16-normal-useastred.tiktokv.eu/webcast/room/enter/"
        }
        
        mode_names = ["", "VIEWS", "SHARES", "FAVORITES", "LIKES", "FOLLOWERS", "LIVE"]
        
        while State.is_running:
            async with sem:
                try:
                    did = str(random.randint(10**18, 10**19))
                    iid = str(random.randint(10**18, 10**19))
                    
                    params = {
                        "device_id": did, "iid": iid, "version_code": "400304",
                        "device_platform": "android", "aid": "1233",
                        "cdid": str(uuid.uuid4()),
                        "openudid": binascii.hexlify(os.urandom(8)).decode()
                    }

                    payload = ""
                    if mode == "1": payload = f"item_id={State.target_id}&play_delta=1"
                    elif mode == "2": payload = f"item_id={State.target_id}&share_delta=1"
                    elif mode in ["3", "4"]: params["aweme_id"] = State.target_id
                    elif mode == "5": params["user_id"] = State.target_id
                    elif mode == "6":
                        params.update({"room_id": State.target_id, "store-idc": "no1a", "d_ticket": "27"})
                        payload = f"room_id={State.target_id}&hold_living_room=1"

                    query = urlencode(params)
                    sig = SignerPy.XG(query, payload, "d_ticket=27" if mode == "6" else "")
                    xg, xk = sig.get("X-Gorgon", ""), sig.get("X-Khronos", str(int(time.time())))

                    headers = {
                        "User-Agent": "com.ss.android.ugc.trill/400304 (Linux; U; Android 12; Pixel 6)",
                        "X-Gorgon": xg, "X-Khronos": xk,
                        "Content-Type": "application/x-www-form-urlencoded"
                    }
                    if mode == "6": headers["Cookie"] = "d_ticket=27"

                    proxy = self.get_proxy()
                    async with session.post(endpoints[mode], params=params, data=payload, 
                                          headers=headers, proxy=proxy, 
                                          timeout=aiohttp.ClientTimeout(total=10), ssl=False) as r:
                        
                        if r.status == 200:
                            try:
                                resp = await r.json()
                                if resp.get("status_code") == 0:
                                    State.success += 1
                                else:
                                    State.fails += 1
                            except:
                                State.fails += 1
                        else:
                            State.fails += 1

                except:
                    State.fails += 1
                
                await asyncio.sleep(0.0005)

# =====================================================
# LIVE STATS
# =====================================================

def live_stats():
    while True:
        if State.is_running:
            elapsed = time.time() - State.start_time
            rps = State.success / elapsed if elapsed > 0 else 0
            print(f"\r{Fore.CYAN}[LIVE] Erfolg: {Fore.GREEN}{State.success} {Fore.CYAN}| Fehlschläge: {Fore.RED}{State.fails} {Fore.CYAN}| RPS: {Fore.YELLOW}{rps:.1f}{Style.RESET_ALL}", end="")
        time.sleep(0.5)

# =====================================================
# BANNER
# =====================================================

def banner():
    os.system('clear' if os.name != 'nt' else 'cls')
    print(f"""
{Fore.RED}
    ╔══════════════════════════════════════════════════════╗
    ║  {Fore.YELLOW}TIKTOK ULTIMATE BOT v4.1 - TERMUX FIX{Style.RESET_ALL} {Fore.RED}║
    ║  {Fore.CYAN}Asyncio • 10x Proxies • 1000+ RPS{Style.RESET_ALL} {Fore.RED}║
    ╚══════════════════════════════════════════════════════╝
{Fore.WHITE}
    {Fore.GREEN}1.{Style.RESET_ALL} Video VIEWS      {Fore.RED}4.{Style.RESET_ALL} LIKES/Hearts
    {Fore.GREEN}2.{Style.RESET_ALL} SHARES         {Fore.RED}5.{Style.RESET_ALL} FOLLOWERS
    {Fore.GREEN}3.{Style.RESET_ALL} FAVORITES     {Fore.RED}6.{Style.RESET_ALL} LIVE Entry
    {Fore.YELLOW}7.{Style.RESET_ALL} Room ID       {Fore.RED}0.{Style.RESET_ALL} EXIT
{Style.RESET_ALL}
    """)

# =====================================================
# MAIN LOOP
# =====================================================

async def main_loop():
    threading.Thread(target=live_stats, daemon=True).start()
    
    while True:
        banner()
        print(f"{Fore.BOLD}{Fore.RED}Wähle Funktion [0-7]:{Style.RESET_ALL}", end="")
        choice = input("").strip()
        
        if choice == "0":
            print(f"{Fore.GREEN}Tschüss!{Style.RESET_ALL}")
            sys.exit(0)
        
        if choice == "7":
            print(f"{Fore.YELLOW}Username (ohne @):{Style.RESET_ALL}", end="")
            username = input("").strip()
            
            print(f"{Fore.CYAN}[RESOLVER] Suche Room ID...{Style.RESET_ALL}")
            room_id = get_room_id(username)
            
            if room_id:
                print(f"{Fore.GREEN}✅ ROOM ID: {room_id}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ User OFFLINE{Style.RESET_ALL}")
            
            input(f"\n{Fore.YELLOW}Enter...{Style.RESET_ALL}")
            continue
        
        if choice not in ["1", "2", "3", "4", "5", "6"]:
            print(f"{Fore.RED}❌ Ungültig!{Style.RESET_ALL}")
            time.sleep(2)
            continue
        
        print(f"{Fore.YELLOW}Video/Live ID oder URL:{Style.RESET_ALL}", end="")
        target_input = input("").strip()
        
        # Auto-Extract
        id_match = re.search(r'(\d{15,20})', target_input)
        if id_match:
            State.target_id = id_match.group(1)
        else:
            State.target_id = target_input
        
        print(f"{Fore.YELLOW}Threads (500-2000):{Style.RESET_ALL}", end="")
        try:
            threads = int(input())
            threads = max(50, min(threads, 2000))
        except:
            threads = 500
        
        print(f"{Fore.GREEN}🚀 Starte {threads} Threads...{Style.RESET_ALL}")
        State.is_running = True
        State.success = State.fails = 0
        State.start_time = time.time()
        
        sem = asyncio.Semaphore(threads)
        connector = aiohttp.TCPConnector(limit=threads * 2)
        
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = [TikTokEngine().worker(session, sem, choice) for _ in range(threads)]
            try:
                await asyncio.gather(*tasks)
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}⏹️ GESTOPPT! Erfolg: {State.success}{Style.RESET_ALL}")
                State.is_running = False
                time.sleep(3)

# =====================================================
# START
# =====================================================

if __name__ == "__main__":
    print(f"{Fore.GREEN}TikTok Bot v4.1 - Termux Ready!{Style.RESET_ALL}")
    asyncio.run(main_loop())
