import os
import sys
import re
import time
import random
import threading
import requests
from urllib.parse import urlencode
from colorama import init, Fore, Style

# --- Initialization ---
init(autoreset=True)
_lock = threading.Lock()
success = 0
errors = 0

class TikTokSigner:
    @staticmethod
    def get_headers(did, iid, session=None):
        headers = {
            "User-Agent": "com.ss.android.ugc.trill/2613 (Linux; U; Android 12; en_US; Pixel 6 Pro)",
            "Accept-Encoding": "gzip",
            "Connection": "keep-alive",
            "x-common-params-v2": "version_code=26.1.3&app_name=musically_go&device_platform=android",
            "x-did": str(did),
            "x-iid": str(iid)
        }
        if session:
            headers["Cookie"] = f"sessionid={session}"
        return headers

def load_list(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

def grab_and_save_room_id(username):
    print(f"{Fore.YELLOW}[*] Fetching Room ID for @{username}...")
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(f"https://www.tiktok.com/@{username}/live", headers=headers, timeout=15)
        room_id = re.search(r'room_id=(\d+)', response.text) or re.search(r'"roomId":"(\d+)"', response.text)
        if room_id:
            final_id = room_id.group(1)
            with open("room_id.txt", "w") as f: f.write(final_id)
            print(f"{Fore.GREEN}[+] Saved Room ID: {final_id}")
            return final_id
    except: pass
    print(f"{Fore.RED}[!] Failed to find Room ID.")
    return None

# --- Live Stream Action Modules ---

def sendLiveViews(did, iid, room_id):
    global success, errors
    try:
        params = {"room_id": room_id, "device_id": did, "iid": iid, "version_code": "26.1.3"}
        url = "https://webcast16-normal-c-useast1a.tiktokv.com/webcast/ranklist/audience/?" + urlencode(params)
        resp = requests.get(url, headers=TikTokSigner.get_headers(did, iid), timeout=10)
        if resp.status_code == 200:
            with _lock:
                success += 1
                print(f"{Fore.YELLOW}[LIVE VIEW] Total: {success}")
    except: errors += 1

def sendLiveLikes(did, iid, room_id, session):
    global success, errors
    try:
        params = {
            "room_id": room_id,
            "device_id": did,
            "iid": iid,
            "count": random.randint(1, 5) # Number of taps per request
        }
        url = "https://webcast16-normal-c-useast1a.tiktokv.com/webcast/stats/like/?" + urlencode(params)
        # Likes usually require a session to stick
        resp = requests.post(url, headers=TikTokSigner.get_headers(did, iid, session), timeout=10)
        if resp.status_code == 200:
            with _lock:
                success += 1
                print(f"{Fore.RED}[LIVE LIKE] Total: {success}")
    except: errors += 1

def sendLiveShare(did, iid, room_id):
    global success, errors
    try:
        params = {
            "room_id": room_id,
            "device_id": did,
            "iid": iid,
            "share_type": "1" # Internal share logic
        }
        url = "https://webcast16-normal-c-useast1a.tiktokv.com/webcast/stats/share/?" + urlencode(params)
        resp = requests.post(url, headers=TikTokSigner.get_headers(did, iid), timeout=10)
        if resp.status_code == 200:
            with _lock:
                success += 1
                print(f"{Fore.BLUE}[LIVE SHARE] Total: {success}")
    except: errors += 1

# --- Interface ---

def Main():
    global success
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Fore.MAGENTA}TikTok Live Suite - All-In-One")
    print("---------------------------------------")
    print("0. GRAB Room ID from Username")
    print("1. Live Stream Views")
    print("2. Live Stream Likes (Requires sessions.txt)")
    print("3. Live Stream Shares")
    print("---------------------------------------")
    
    choice = input("Choice: ")
    if choice == "0":
        user = input("Username: ")
        grab_and_save_room_id(user)
        return Main()

    threads_count = int(input("Threads: "))
    amount_target = int(input("Target Amount: "))
    
    devices = load_list("devices.txt")
    room_ids = load_list("room_id.txt")
    sessions = load_list("sessions.txt")
    
    if not devices or not room_ids:
        print(f"{Fore.RED}Error: devices.txt or room_id.txt is missing!")
        return

    room_id = room_ids[0]
    print(f"\n{Fore.WHITE}Botting Room: {room_id}...\n")

    while success < amount_target:
        if threading.active_count() <= threads_count:
            device = random.choice(devices)
            try:
                did, iid, cdid, openudid = device.split(':')
                
                if choice == "1":
                    threading.Thread(target=sendLiveViews, args=(did, iid, room_id)).start()
                elif choice == "2":
                    sess = random.choice(sessions) if sessions else None
                    threading.Thread(target=sendLiveLikes, args=(did, iid, room_id, sess)).start()
                elif choice == "3":
                    threading.Thread(target=sendLiveShare, args=(did, iid, room_id)).start()
                
            except: continue
            time.sleep(0.01)

if __name__ == "__main__":
    Main()
