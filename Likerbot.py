# main.py - TIKTOK LIKE BOT PRO v3.1 (Dựa trên code của bạn)
import aiohttp
import asyncio
import random
import requests
import re
import time
import secrets
import os
import signal
import sys
from hashlib import md5
from time import time as T
from typing import Dict, Tuple, Optional, List
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class DeviceInfo:
    model: str
    version: str
    api_level: int

class DeviceGenerator:
    DEVICES = [
        DeviceInfo("Pixel 6", "12", 31),
        DeviceInfo("Pixel 5", "11", 30),
        DeviceInfo("Samsung Galaxy S21", "13", 33),
        DeviceInfo("Oppo Reno 8", "12", 31),
        DeviceInfo("Xiaomi Mi 11", "12", 31),
        DeviceInfo("OnePlus 9", "13", 33),
    ]
    
    @classmethod
    def random_device(cls) -> DeviceInfo:
        return random.choice(cls.DEVICES)

class Signature:
    KEY = [0xDF, 0x77, 0xB9, 0x40, 0xB9, 0x9B, 0x84, 0x83, 0xD1, 0xB9, 
           0xCB, 0xD1, 0xF7, 0xC2, 0xB9, 0xEA, 0xC3, 0xD0, 0xFB, 0xC3]
    def __init__(self, params: str, data: str, cookies: str):
        self.params = params
        self.data = data
        self.cookies = cookies
    
    def _md5_hash(self, data: str) -> str:
        return md5(data.encode()).hexdigest()
    
    def _reverse_byte(self, n: int) -> int:
        return int(f"{n:02x}"[1:] + f"{n:02x}"[0], 16)
    
    def generate(self) -> Dict[str, str]:
        g = self._md5_hash(self.params)
        g += self._md5_hash(self.data) if self.data else "0" * 32
        g += self._md5_hash(self.cookies) if self.cookies else "0" * 32
        g += "0" * 32
        
        unix_timestamp = int(T())
        payload = []
        
        for i in range(0, 12, 4):
            chunk = g[8 * i:8 * (i + 1)]
            for j in range(4):
                payload.append(int(chunk[j * 2:(j + 1) * 2], 16))
        
        payload.extend([0x0, 0x6, 0xB, 0x1C])
        payload.extend([
            (unix_timestamp & 0xFF000000) >> 24,
            (unix_timestamp & 0x00FF0000) >> 16,
            (unix_timestamp & 0x0000FF00) >> 8,
            (unix_timestamp & 0x000000FF)
        ])
        
        encrypted = [a ^ b for a, b in zip(payload, self.KEY)]
        
        for i in range(0x14):
            C = self._reverse_byte(encrypted[i])
            D = encrypted[(i + 1) % 0x14]
            F = int(bin(C ^ D)[2:].zfill(8)[::-1], 2)
            H = ((F ^ 0xFFFFFFFF) ^ 0x14) & 0xFF
            encrypted[i] = H
        
        signature = "".join(f"{x:02x}" for x in encrypted)
        
        return {
            "X-Gorgon": "040280416000" + signature,
            "X-Khronos": str(unix_timestamp)
        }

class OptimizedTikTokLikeBot:
    def __init__(self):
        self.count = 0
        self.start_time = 0
        self.is_running = False
        self.session = None
        self.successful_requests = 0
        self.failed_requests = 0
        self.peak_speed = 0
        
    async def init_session(self):
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        connector = aiohttp.TCPConnector(limit=0, limit_per_host=0, keepalive_timeout=30, enable_cleanup_closed=True)
        
        self.session = aiohttp.ClientSession(
            timeout=timeout,
            connector=connector,
            headers={'User-Agent': 'com.ss.android.ugc.trill/400304'},
            cookie_jar=aiohttp.DummyCookieJar()
        )
    
    async def close_session(self):
        if self.session:
            await self.session.close()
    
    def get_video_id(self, url: str) -> Optional[str]:
        try:
            patterns_url = [
                r'/video/(\d+)',
                r'tiktok\.com/@[^/]+/video/(\d+)',
                r'(\d{18,19})'
            ]
            for pattern in patterns_url:
                match = re.search(pattern, url)
                if match:
                    video_id = match.group(1)
                    logger.info(f"Found Video ID from URL: {video_id}")
                    return video_id
            
            response = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }, timeout=15)
            response.raise_for_status()
            
            patterns_page = [
                r'"id":"(\d+)"',
                r'"aweme_id":"(\d+)"',
                r'video/(\d+)'
            ]
            for pattern in patterns_page:
                match = re.search(pattern, response.text)
                if match:
                    video_id = match.group(1)
                    logger.info(f"Found Video ID from page: {video_id}")
                    return video_id
                    
            logger.error("No video ID found")
            return None
                
        except Exception as e:
            logger.error(f"Error getting video ID: {e}")
            return None
    
    def generate_request_data(self, video_id: str) -> Tuple[str, Dict, Dict, Dict]:
        device = DeviceGenerator.random_device()
        
        # THAY ĐỔI: Endpoint LIKE
        base_url = random.choice([
            "api16-core-c-alisg.tiktokv.com",
            "api22-core-c-alisg.tiktokv.com",
            "api19-core-c-alisg.tiktokv.com"
        ])
        
        params = (
            f"aid=1340&app_name=tiktok&version_code=400304"
            f"&device_platform=android&device_type={device.model.replace(' ', '+')}"
            f"&os_version={device.version}&device_id={random.randint(7000000000000000000, 7999999999999999999)}"
            f"&os_api={device.api_level}&app_language=vi&tz_name=Asia%2FHo_Chi_Minh"
        )
        
        url = f"https://{base_url}/aweme/v1/commit/item/digg/?{params}"
        
        # THAY ĐỔI: Data cho LIKE
        data = {
            "item_id": video_id,
            "digg_type": 1,  # 1 = like, 0 = unlike
            "action_time": int(time.time())
        }
        
        cookies = {"sessionid": secrets.token_hex(16)}
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "com.ss.android.ugc.trill/400304",
            "Accept-Encoding": "gzip",
            "Connection": "keep-alive"
        }
        
        return url, data, cookies, headers
    
    async def send_like_request(self, video_id: str, semaphore: asyncio.Semaphore) -> bool:
        async with semaphore:
            for attempt in range(2):
                try:
                    url, data, cookies, base_headers = self.generate_request_data(video_id)
                    
                    sig = Signature(url.split('?')[1], '&'.join([f"{k}={v}" for k, v in data.items()]), str(cookies)).generate()
                    headers = {**base_headers, **sig}
                    
                    async with self.session.post(
                        url, 
                        data=data, 
                        headers=headers, 
                        cookies=cookies,
                        ssl=False
                    ) as response:
                        
                        if response.status == 200:
                            text = await response.text()
                            if "status_code\":0" in text or "success" in text.lower():
                                self.count += 1
                                self.successful_requests += 1
                                return True
                            else:
                                self.failed_requests += 1
                                return False
                        else:
                            if attempt == 0:
                                await asyncio.sleep(0.01)
                                continue
                            self.failed_requests += 1
                            return False
                            
                except Exception as e:
                    if attempt == 0:
                        await asyncio.sleep(0.01)
                        continue
                    self.failed_requests += 1
                    return False
    
    async def like_sender(self, video_id: str, task_id: int, semaphore: asyncio.Semaphore):
        consecutive_success = 0
        base_delay = 0.001
        
        while self.is_running:
            success = await self.send_like_request(video_id, semaphore)
            
            if success:
                consecutive_success += 1
                delay = base_delay * (0.5 if consecutive_success > 100 else 0.7 if consecutive_success > 50 else 1.0)
            else:
                consecutive_success = 0
                delay = base_delay * 2
            
            current_speed = self.calculate_stats()["likes_per_second"]
            if current_speed > 500:
                delay *= 1.5
            elif current_speed > 1000:
                delay *= 2
            
            await asyncio.sleep(delay + random.uniform(0, 0.002))
    
    def calculate_stats(self) -> Dict[str, float]:
        elapsed = time.time() - self.start_time
        likes_per_second = self.count / elapsed if elapsed > 0 else 0
        
        if likes_per_second > self.peak_speed:
            self.peak_speed = likes_per_second
        
        return {
            "total_likes": self.count,
            "elapsed_time": elapsed,
            "likes_per_second": likes_per_second,
            "likes_per_minute": likes_per_second * 60,
            "likes_per_hour": likes_per_second * 3600,
            "success_rate": (self.successful_requests / (self.successful_requests + self.failed_requests)) * 100 if (self.successful_requests + self.failed_requests) > 0 else 0,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "peak_speed": self.peak_speed
        }
    
    def display_stats(self):
        stats = self.calculate_stats()
        print(f"\n{'='*60}")
        print(f"THỐNG KÊ - TIKTOK LIKE BOT PRO v3.1")
        print(f"{'='*60}")
        print(f"Tổng tim: {stats['total_likes']:,}")
        print(f"Thời gian: {stats['elapsed_time']:.1f}s")
        print(f"Tốc độ hiện tại: {stats['likes_per_second']:.1f} tim/s")
        print(f"Tốc độ cao nhất: {stats['peak_speed']:.1f} tim/s")
        print(f"Dự kiến: {stats['likes_per_minute']:,.0f} tim/phút")
        print(f"Dự kiến: {stats['likes_per_hour']:,.0f} tim/giờ")
        print(f"Thành công: {stats['success_rate']:.1f}%")
        print(f"{'='*60}")
    
    async def run(self, video_url: str):
        print("Đang lấy Video ID...")
        video_id = self.get_video_id(video_url)
        if not video_id:
            print("Không thể lấy Video ID!")
            return
        
        cpu_count = os.cpu_count() or 1
        optimal_workers = 8000 if cpu_count > 4 else 5000 if cpu_count > 2 else 2000
        
        print(f"Video ID: {video_id}")
        print(f"CPU: {cpu_count} cores → {optimal_workers:,} tasks")
        print("Bắt đầu buff tim... (Ctrl+C để dừng)")
        await asyncio.sleep(2)
        
        await self.init_session()
        self.is_running = True
        self.start_time = time.time()
        semaphore = asyncio.Semaphore(min(3000, optimal_workers // 3))
        
        try:
            tasks = [asyncio.create_task(self.like_sender(video_id, i, semaphore)) for i in range(optimal_workers)]
            logger.info(f"Khởi tạo {len(tasks):,} tasks")
            
            last_display = 0
            while self.is_running:
                await asyncio.sleep(0.5)
                if time.time() - last_display >= 2:
                    stats = self.calculate_stats()
                    print(f"\rĐã buff: {stats['total_likes']:,} | "
                          f"{stats['likes_per_second']:.1f} tim/s | "
                          f"Peak: {stats['peak_speed']:.1f} | "
                          f"{stats['success_rate']:.1f}% thành công", end="", flush=True)
                    last_display = time.time()
                    
        except KeyboardInterrupt:
            print("\n\nDừng bot...")
        finally:
            self.is_running = False
            for task in tasks: task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
            await self.close_session()
            self.display_stats()

# === UI & MAIN ===
def display_banner():
    os.system("cls" if os.name == "nt" else "clear")
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║               TIKTOK LIKE BOT PRO v3.1                 ║
    ║                     BUFF TIM SIÊU TỐC                   ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(banner)

def get_user_input():
    print("\n" + "═" * 60)
    video_url = input("Nhập link video TikTok: ").strip()
    if not video_url.startswith("http"):
        print("URL không hợp lệ!")
        return None
    return video_url

async def main():
    display_banner()
    signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))
    
    url = get_user_input()
    if not url: return
    
    bot = OptimizedTikTokLikeBot()
    await bot.run(url)
    
    print("\nHoàn thành! Cảm ơn bạn đã dùng tool!")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())
