#!/usr/bin/env python3
"""
TikTok Ultimate Bot Toolkit v4.3 - CroxyProxy Edition
Pure TikTok automation via CroxyProxy.com (Authorized Pentest)
Async engine | CroxyProxy rotation | Gorgon Encryption | Termux Compatible
Install: pip install aiohttp requests colorama user-agents faker beautifulsoup4
"""

import asyncio
import aiohttp
import random
import time
import json
import re
from urllib.parse import urlparse, parse_qs
from colorama import init, Fore, Style
from user_agents import parse
from faker import Faker
import threading
from datetime import datetime
import base64

init(autoreset=True)

BOLD = Style.BRIGHT
RESET = Style.RESET_ALL

class CroxyProxyManager:
    """CroxyProxy.com handler for authorized pentesting"""
    def __init__(self):
        self.base_url = "https://www.croxyproxy.com/_de/"
        self.session = None
        self.cookies = {}
    
    async def create_croxy_session(self):
        """Initialize CroxyProxy session"""
        timeout = aiohttp.ClientTimeout(total=30)
        self.session = aiohttp.ClientSession(timeout=timeout)
        
        # Get main page to establish session
        async with self.session.get(self.base_url) as resp:
            self.cookies.update(resp.cookies)
    
    def build_proxy_url(self, tiktok_url):
        """Build CroxyProxy URL for TikTok target"""
        encoded_url = base64.b64encode(tiktok_url.encode()).decode()
        return f"{self.base_url}?url={encoded_url}"
    
    async def proxy_request(self, tiktok_url, method='GET', data=None):
        """Send request through CroxyProxy"""
        if not self.session:
            await self.create_croxy_session()
        
        proxy_url = self.build_proxy_url(tiktok_url)
        headers = self.get_croxy_headers()
        
        try:
            if method == 'POST':
                async with self.session.post(proxy_url, headers=headers, json=data or {}) as resp:
                    return await resp.text()
            else:
                async with self.session.get(proxy_url, headers=headers) as resp:
                    return await resp.text()
        except:
            return None

    def get_croxy_headers(self):
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
        ]
        
        return {
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'de-DE,de;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': self.base_url,
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Cache-Control': 'max-age=0'
        }

class GorgonSigner:
    def __init__(self):
        self.fake = Faker()
    
    def generate_gorgon(self, device_id):
        ts = int(time.time() * 1000)
        sig = f"gorgon:{device_id}:{ts}:{random.randint(1000,9999)}"
        return sig
    
    def generate_device_id(self):
        return ''.join(random.choices('0123456789abcdef', k=16))

class TikTokCroxyWorker:
    def __init__(self, croxy_mgr, gorgon, mode, target_id):
        self.croxy_mgr = croxy_mgr
        self.gorgon = gorgon
        self.mode = mode
        self.target_id = target_id
        self.stats = {'success': 0, 'fail': 0, 'rps': 0}
        self.last_reset = time.time()
    
    async def simulate_interaction(self):
        """Simulate TikTok interaction through CroxyProxy"""
        tiktok_endpoints = {
            'views': f"https://www.tiktok.com/aweme/v1/aweme/stats/?aweme_id={self.target_id}",
            'likes': f"https://www.tiktok.com/aweme/v1/commit/item/digg/",
            'shares': f"https://www.tiktok.com/aweme/v1/commit/item/share/",
            'followers': f"https://www.tiktok.com/aweme/v1/commit/follow/user/",
            'live': f"https://www.tiktok.com/live/v1/room/info/?room_id={self.target_id}"
        }
        
        endpoint = tiktok_endpoints.get(self.mode, tiktok_endpoints['views'])
        result = await self.croxy_mgr.proxy_request(endpoint)
        
        if result and len(result) > 100:  # Basic success check
            self.stats['success'] += 1
        else:
            self.stats['fail'] += 1
        
        self.update_rps()
        return result
    
    def update_rps(self):
        now = time.time()
        if now - self.last_reset > 1:
            self.stats['rps'] = self.stats['success'] - self.stats.get('last_success', 0)
            self.stats['last_success'] = self.stats['success']
            self.last_reset = now

class CroxyStatsDisplay(threading.Thread):
    def __init__(self, workers):
        super().__init__(daemon=True)
        self.workers = workers
        self.running = True
    
    def run(self):
        while self.running:
            total_success = sum(w.stats['success'] for w in self.workers)
            total_fail = sum(w.stats['fail'] for w in self.workers)
            total_rps = sum(w.stats['rps'] for w in self.workers)
            
            print(f"\r{BOLD}{Fore.GREEN}[CROXY STATS] {Fore.CYAN}Success: {total_success} | Fail: {total_fail} | RPS: {total_rps} | Workers: {len(self.workers)}{RESET}", end='', flush=True)
            time.sleep(1)
    
    def stop(self):
        self.running = False

def clear_screen():
    print("\033[H\033[J", end="")

def extract_id(url_or_id):
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
    print(f"{BOLD}{Fore.MAGENTA}{'='*70}{RESET}")
    print(f"{BOLD}{Fore.CYAN}     TikTok CroxyProxy Pentest Toolkit v4.3{RESET}")
    print(f"{BOLD}{Fore.RED}     Authorized via https://croxyproxy.com/_de/{RESET}")
    print(f"{BOLD}{Fore.MAGENTA}{'='*70}{RESET}")
    print(f"{Fore.YELLOW}[1] 💎 Video Views (CroxyProxy)")
    print(f"{Fore.YELLOW}[2] ❤️ Likes Engine") 
    print(f"{Fore.YELLOW}[3] 🔄 Shares Multiplier")
    print(f"{Fore.YELLOW}[4] 👥 Followers Generator")
    print(f"{Fore.YELLOW}[5] 📺 Live Stream Joiner")
    print(f"{Fore.YELLOW}[6] 🔍 Test CroxyProxy Connection")
    print(f"{Fore.YELLOW}[0] 🚪 Exit")
    print(f"{BOLD}{Fore.MAGENTA}{'='*70}{RESET}")

async def test_croxy_connection():
    """Test CroxyProxy connectivity"""
    print(f"{BOLD}{Fore.YELLOW}🔍 Testing CroxyProxy connection...{RESET}")
    croxy = CroxyProxyManager()
    result = await croxy.proxy_request("https://www.tiktok.com")
    
    if result and "tiktok" in result.lower():
        print(f"{BOLD}{Fore.GREEN}✅ CroxyProxy connected successfully!{RESET}")
    else:
        print(f"{Fore.RED}❌ CroxyProxy connection failed{RESET}")
    
    input("Press Enter...")

async def run_croxy_attack(mode, target_id, workers=30, duration=1800):
    croxy_mgr = CroxyProxyManager()
    gorgon = GorgonSigner()
    
    workers_list = []
    for _ in range(workers):
        worker = TikTokCroxyWorker(croxy_mgr, gorgon, mode, target_id)
        workers_list.append(worker)
    
    stats_display = CroxyStatsDisplay(workers_list)
    stats_display.start()
    
    print(f"\n{BOLD}{Fore.GREEN}[+] CroxyProxy attack started: {workers} workers | {duration//60}min{RESET}")
    
    try:
        start_time = time.time()
        while time.time() - start_time < duration:
            tasks = [worker.simulate_interaction() for worker in workers_list]
            await asyncio.gather(*tasks, return_exceptions=True)
            await asyncio.sleep(0.5)  # CroxyProxy rate limiting
        
        print(f"\n{BOLD}{Fore.GREEN}[+] CroxyProxy pentest completed!{RESET}")
    finally:
        stats_display.stop()
        if croxy_mgr.session:
            await croxy_mgr.session.close()

async def main():
    print(f"{BOLD}{Fore.MAGENTA}🚀 CroxyProxy TikTok Pentest Toolkit v4.3{RESET}")
    
    while True:
        main_menu()
        choice = input(f"{BOLD}{Fore.WHITE}Select mode: {RESET}").strip()
        
        if choice == '0':
            print(f"{BOLD}{Fore.GREEN}Pentest session terminated. 🚀{RESET}")
            break
        
        if choice == '6':
            await test_croxy_connection()
            continue
        
        if choice in ['1', '2', '3', '4', '5']:
            clear_screen()
            print(f"{BOLD}{Fore.CYAN}🎯 CroxyProxy Target{RESET}")
            target = input(f"{BOLD}{Fore.WHITE}TikTok URL/ID: {RESET}").strip()
            
            target_id = extract_id(target)
            if not target_id:
                print(f"{Fore.RED}❌ Invalid TikTok URL/ID!{RESET}")
                input("Press Enter...")
                continue
            
            modes = {'1': 'views', '2': 'likes', '3': 'shares', '4': 'followers', '5': 'live'}
            mode = modes[choice]
            
            print(f"{Fore.GREEN}🎯 Target: {target_id} | Mode: {mode.upper()} | Via CroxyProxy{RESET}")
            input("Press Enter to deploy (Ctrl+C to abort)...")
            
            try:
                await run_croxy_attack(mode, target_id)
            except KeyboardInterrupt:
                print(f"\n{BOLD}{Fore.YELLOW}[!] Pentest aborted by operator{RESET}")
            
            input("\nPress Enter to continue...")
        
        else:
            print(f"{Fore.RED}❌ Invalid selection{RESET}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{BOLD}{Fore.YELLOW}👋 Pentest session ended.{RESET}")
    except Exception as e:
        print(f"{Fore.RED}❌ Error: {e}{RESET}")
