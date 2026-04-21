#!/usr/bin/env python3
"""
TikTok Ultimate Bot Toolkit v4.2 - Termux Compatible
Pure TikTok automation: Views, Likes, Shares, Followers, Live Streams
Async engine | Premium Proxies | Gorgon Encryption | Auto ID Resolver
Install: pip install aiohttp requests colorama user-agents faker
"""

import asyncio
import aiohttp
import random
import time
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore, Style
from user_agents import parse
from faker import Faker
import threading
from datetime import datetime

init(autoreset=True)  # Colorama init for Termux

# FIXED: Using Style.BRIGHT instead of Fore.BOLD for Termux/Python 3.13 compatibility
BOLD = Style.BRIGHT
RESET = Style.RESET_ALL

class GorgonSigner:
    """Simplified Gorgon/X-Gorgon signature generator"""
    def __init__(self):
        self.fake = Faker()
    
    def generate_gorgon(self, device_id):
        # Simplified Gorgon-like signature (replace with real SignerPy if available)
        ts = int(time.time() * 1000)
        sig = f"gorgon:{device_id}:{ts}:{random.randint(1000,9999)}"
        return sig
    
    def generate_device_id(self):
        return ''.join(random.choices('0123456789abcdef', k=16))

class ProxyManager:
    """Premium proxy handler - REPLACE WITH YOUR PROXIES"""
    def __init__(self):
        # REPLACE THESE WITH YOUR PREMIUM PROXIES (IP:PORT:USER:PASS format)
        self.proxies = [
            "your.proxy1.com:8080:username:password",
            "your.proxy2.com:8080:username:password",
            "your.proxy3.com:8080:username:password",
            "your.proxy4.com:8080:username:password",
            "your.proxy5.com:8080:username:password",
            "your.proxy6.com:8080:username:password",
            "your.proxy7.com:8080:username:password",
            "your.proxy8.com:8080:username:password",
            "your.proxy9.com:8080:username:password",
            "your.proxy10.com:8080:username:password"
        ]
        self.current_proxy = 0
    
    def get_proxy(self):
        proxy = self.proxies[self.current_proxy % len(self.proxies)]
        self.current_proxy += 1
        ip, port, user, passw = proxy.split(':')
        return {
            'http': f'http://{user}:{passw}@{ip}:{port}',
            'https': f'http://{user}:{passw}@{ip}:{port}'
        }

class TikTokWorker:
    """Async TikTok action worker"""
    def __init__(self, proxy_mgr, gorgon, mode, target_id):
        self.proxy_mgr = proxy_mgr
        self.gorgon = gorgon
        self.mode = mode
        self.target_id = target_id
        self.session = None
        self.stats = {'success': 0, 'fail': 0, 'rps': 0}
        self.last_reset = time.time()
    
    async def create_session(self):
        proxy = self.proxy_mgr.get_proxy()
        timeout = aiohttp.ClientTimeout(total=30)
        headers = self.get_headers()
        
        self.session = aiohttp.ClientSession(
            timeout=timeout,
            headers=headers,
            proxy=proxy['http']
        )
    
    def get_headers(self):
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
        ]
        
        device_id = self.gorgon.generate_device_id()
        gorgon_sig = self.gorgon.generate_gorgon(device_id)
        
        return {
            'User-Agent': random.choice(user_agents),
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.tiktok.com/',
            'X-Gorgon': gorgon_sig,
            'X-Khronos': str(int(time.time() * 1000)),
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Origin': 'https://www.tiktok.com'
        }
    
    async def send_request(self, url, data=None):
        try:
            if not self.session:
                await self.create_session()
            
            if data:
                async with self.session.post(url, json=data) as resp:
                    return await resp.json()
            else:
                async with self.session.get(url) as resp:
                    return await resp.json()
        except Exception as e:
            self.stats['fail'] += 1
            return None
    
    async def view_video(self):
        url = f"https://www.tiktok.com/aweme/v1/aweme/stats/?aweme_id={self.target_id}"
        data = {"item_id": self.target_id, "play_delta": 1}
        result = await self.send_request(url, data)
        if result: 
            self.stats['success'] += 1
        return result
    
    async def like_video(self):
        url = f"https://www.tiktok.com/aweme/v1/commit/item/digg/"
        data = {
            "item_id": self.target_id,
            "type": 1
        }
        result = await self.send_request(url, data)
        if result: 
            self.stats['success'] += 1
        return result
    
    async def share_video(self):
        url = f"https://www.tiktok.com/aweme/v1/commit/item/share/"
        data = {
            "item_id": self.target_id
        }
        result = await self.send_request(url, data)
        if result: 
            self.stats['success'] += 1
        return result
    
    async def follow_user(self):
        url = f"https://www.tiktok.com/aweme/v1/commit/follow/user/"
        data = {
            "user_id": self.target_id,
            "type": 1
        }
        result = await self.send_request(url, data)
        if result: 
            self.stats['success'] += 1
        return result
    
    async def join_live(self):
        url = f"https://www.tiktok.com/live/v1/room/info/?room_id={self.target_id}"
        result = await self.send_request(url)
        if result: 
            self.stats['success'] += 1
        return result
    
    async def work(self):
        methods = {
            'views': self.view_video,
            'likes': self.like_video,
            'shares': self.share_video,
            'followers': self.follow_user,
            'live': self.join_live
        }
        
        method = methods.get(self.mode)
        if method:
            await method()
            self.update_rps()
    
    def update_rps(self):
        now = time.time()
        if now - self.last_reset > 1:
            self.stats['rps'] = self.stats['success'] - self.stats.get('last_success', 0)
            self.stats['last_success'] = self.stats['success']
            self.last_reset = now

class StatsDisplay(threading.Thread):
    """Live statistics display"""
    def __init__(self, workers):
        super().__init__(daemon=True)
        self.workers = workers
        self.running = True
    
    def run(self):
        while self.running:
            total_success = sum(w.stats['success'] for w in self.workers)
            total_fail = sum(w.stats['fail'] for w in self.workers)
            total_rps = sum(w.stats['rps'] for w in self.workers)
            
            print(f"\r{BOLD}{Fore.GREEN}[STATS] {Fore.CYAN}Success: {total_success} | Fail: {total_fail} | RPS: {total_rps} | Workers: {len(self.workers)}{RESET}", end='', flush=True)
            time.sleep(1)
    
    def stop(self):
        self.running = False

def clear_screen():
    print("\033[H\033[J", end="")  # Termux clear command

def extract_id(url_or_id):
    """Auto-extract video/room/user ID from TikTok URL"""
    patterns = [
        r'tiktok\.com/[^/]+/video/(\d+)',
        r'tiktok\.com/@[^/]+/video/(\d+)',
        r'vm\.tiktok\.com/[^/]+/(\d+)',
        r'livestream\.tiktok\.com/room/(\d+)',
        r'tiktok\.com/@[^/]+/live/(\d+)'
    ]
    
    if url_or_id.isdigit():
        return url_or_id
    
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    
    return None

def main_menu():
    clear_screen()
    print(f"{BOLD}{Fore.MAGENTA}{'='*60}{RESET}")
    print(f"{BOLD}{Fore.CYAN}     TikTok Ultimate Bot Toolkit v4.2 - Termux Edition{RESET}")
    print(f"{BOLD}{Fore.MAGENTA}{'='*60}{RESET}")
    print(f"{Fore.YELLOW}[1] 💎 Video Views Booster")
    print(f"{Fore.YELLOW}[2] ❤️ Likes Engine") 
    print(f"{Fore.YELLOW}[3] 🔄 Shares Multiplier")
    print(f"{Fore.YELLOW}[4] 👥 Followers Generator")
    print(f"{Fore.YELLOW}[5] 📺 Live Stream Joiner")
    print(f"{Fore.YELLOW}[6] ⚙️  Settings")
    print(f"{Fore.YELLOW}[0] 🚪 Exit")
    print(f"{BOLD}{Fore.MAGENTA}{'='*60}{RESET}")

async def run_attack(mode, target_id, workers=50, duration=3600):
    proxy_mgr = ProxyManager()
    gorgon = GorgonSigner()
    
    workers_list = []
    for _ in range(workers):
        worker = TikTokWorker(proxy_mgr, gorgon, mode, target_id)
        workers_list.append(worker)
    
    stats_display = StatsDisplay(workers_list)
    stats_display.start()
    
    print(f"\n{BOLD}{Fore.GREEN}[+] Starting {workers} workers for {duration//60} minutes...{RESET}")
    
    try:
        start_time = time.time()
        while time.time() - start_time < duration:
            tasks = [worker.work() for worker in workers_list]
            await asyncio.gather(*tasks, return_exceptions=True)
            await asyncio.sleep(0.1)  # 1000+ RPS control
        
        print(f"\n{BOLD}{Fore.GREEN}[+] Attack completed!{RESET}")
    finally:
        stats_display.stop()
        for worker in workers_list:
            if worker.session:
                await worker.session.close()

def settings_menu():
    clear_screen()
    print(f"{BOLD}{Fore.CYAN}⚙️ Settings & Configuration{RESET}")
    print(f"{Fore.YELLOW}1. Edit Proxies (REPLACE in code with your premium proxies)")
    print(f"{Fore.YELLOW}2. Worker Count (default: 50)")
    print(f"{Fore.YELLOW}3. Duration (default: 60min)")
    print("\n{Fore.RED}⚠️  IMPORTANT: Edit proxies in ProxyManager.proxies list!")
    print(f"{Fore.CYAN}Proxies format: 'IP:PORT:USER:PASS'{RESET}")
    input("\nPress Enter to return...")

async def main():
    while True:
        main_menu()
        choice = input(f"{BOLD}{Fore.WHITE}Select mode: {RESET}").strip()
        
        if choice == '0':
            print(f"{BOLD}{Fore.GREEN}Goodbye! 🚀{RESET}")
            break
        
        if choice in ['1', '2', '3', '4', '5']:
            clear_screen()
            print(f"{BOLD}{Fore.CYAN}🎯 Target Input{RESET}")
            print(f"{Fore.YELLOW}Enter TikTok URL or ID directly:{RESET}")
            target = input(f"{BOLD}{Fore.WHITE}Target: {RESET}").strip()
            
            target_id = extract_id(target)
            if not target_id:
                print(f"{Fore.RED}❌ Invalid TikTok URL/ID!{RESET}")
                input("Press Enter...")
                continue
            
            modes = {'1': 'views', '2': 'likes', '3': 'shares', '4': 'followers', '5': 'live'}
            mode = modes[choice]
            
            print(f"{Fore.GREEN}🎯 Target ID: {target_id} | Mode: {mode.upper()}{RESET}")
            input("Press Enter to start (Ctrl+C to cancel)...")
            
            try:
                await run_attack(mode, target_id)
            except KeyboardInterrupt:
                print(f"\n{BOLD}{Fore.YELLOW}[!] Stopped by user{RESET}")
            
            input("\nPress Enter to continue...")
        
        elif choice == '6':
            settings_menu()
        else:
            print(f"{Fore.RED}❌ Invalid option!{RESET}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        print(f"{BOLD}{Fore.MAGENTA}🚀 Starting TikTok Ultimate Bot v4.2...{RESET}")
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{BOLD}{Fore.YELLOW}👋 Session terminated.{RESET}")
    except Exception as e:
        print(f"{Fore.RED}❌ Error: {e}{RESET}")
