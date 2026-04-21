from urllib.parse import urlencode
from pystyle import *
from random import choice
import os, sys, ssl, re, time, random, threading, requests, hashlib, json, base64
from console.utils import set_title
from urllib3.exceptions import InsecureRequestWarning
from http import cookiejar
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from html5lib import *
from user_agent import generate_user_agent

System.Title("[TikTok Ultimate Bot] DBTechLabs.com")
def Banner():
    Banner1 = r"""

████████╗██╗██╗  ██╗████████╗ ██████╗ ██╗  ██╗    ██████╗  ██████╗ ████████╗
╚══██╔══╝██║██║ ██╔╝╚══██╔══╝██╔═══██╗██║ ██╔╝    ██╔══██╗██╔═══██╗╚══██╔══╝
   ██║   ██║█████╔╝    ██║   ██║   ██║█████╔╝     ██████╔╝██║   ██║   ██║   
   ██║   ██║██╔═██╗    ██║   ██║   ██║██╔═██╗     ██╔══██╗██║   ██║   ██║   
   ██║   ██║██║  ██╗   ██║   ╚██████╔╝██║  ██╗    ██████╔╝╚██████╔╝   ██║   
   ╚═╝   ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝    ╚═════╝  ╚═════╝    ╚═╝                                                                            
                                                   made by DBTechLabs.com                                                                               
    """
    Banner2 = r"""
    """
    print(Center.XCenter(Colorate.Vertical(Colors.green_to_cyan, Add.Add(Banner2, Banner1, center=True), 2)))


class BlockCookies(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

r = requests.Session()
r.cookies.set_policy(BlockCookies())

with open(os.path.join("locale_lang.txt"), "r") as f:
        __localesLanguage = f.read().splitlines()
with open(os.path.join("region_lang.txt"), "r") as f:
        __regions = f.read().splitlines()
with open(os.path.join("region_timezone.txt"), "r") as f:
        __tzname = f.read().splitlines()
with open(os.path.join("video_links.txt"), "r") as f:
        __aweme_id = f.read().splitlines()
with open(os.path.join("room_id.txt"), "r") as f:
        __room_id = f.read().splitlines()
with open(os.path.join("live_channel_id.txt"), "r") as f:
        devices = f.read().splitlines()      
with open(os.path.join("sessions.txt"), "r") as f:
        __session_id = f.read().splitlines()
        
__domains = ["api-h2.tiktokv.com","api22-core-c-useast1a.tiktokv.com", "api19-core-c-useast1a.tiktokv.com","api16-core-c-useast1a.tiktokv.com", "api21-core-c-useast1a.tiktokv.com","api19-core-useast5.us.tiktokv.com"]
__offset = ["-28800", "-21600"]
__devices = ["SM-G9900","SM-A136U1", "SM-M225FV", "SM-E426B", "SM-M526BR", "SM-M326B","SM-A528B","SM-F711B","SM-F926B","SM-A037G","SM-A225F","SM-M325FV","SM-A226B","SM-M426B","SM-A525F","SM-N976N","SM-M526B","SM-G570MSM","SM-A520F","SM-G975F","SM-A215U1","SM-A125F","SM-J730F","SM-A207F","SM-G970F","SM-A236B","SM-J730F","SM-J730F","SM-G970F","SM-J730F","SM-J730F","SM-J327T1","SM-A205U","SM-A136B","SM-G991B","SM-G525F","SM-A528B","SM-A528B","SM-A528B","SM-A136B","SM-G900F","SM-A226B","SM-A528B","SM-A515F","SM-G935T","SM-A505F","SM-P619","SM-N976B","SM-A510M","SM-J530FM","SM-G998B","SM-A500FU", "SM-G935F"]

__versionCode = ["190303", "190205", "190204", "190103", "180904", "180804", "180803", "180802",  "270204"]
__versionUa =  [247, 312, 322, 357, 358, 415, 422, 444, 466]
__resolution = ["900*1600", "720*1280"]
__dpi = ["240", "300"]


class Gorgon:
	def __init__(self,params:str,data:str,cookies:str,unix:int)->None:self.unix=unix;self.params=params;self.data=data;self.cookies=cookies
	def hash(self,data:str)->str:
		try:_hash=str(hashlib.md5(data.encode()).hexdigest())
		except Exception:_hash=str(hashlib.md5(data).hexdigest())
		return _hash
	def get_base_string(self)->str:base_str=self.hash(self.params);base_str=base_str+self.hash(self.data)if self.data else base_str+str('0'*32);base_str=base_str+self.hash(self.cookies)if self.cookies else base_str+str('0'*32);return base_str
	def get_value(self)->json:base_str=self.get_base_string();return self.encrypt(base_str)
	def encrypt(self,data:str)->json:
		unix=self.unix;len=20;key=[223,119,185,64,185,155,132,131,209,185,203,209,247,194,185,133,195,208,251,195];param_list=[]
		for i in range(0,12,4):
			temp=data[8*i:8*(i+1)]
			for j in range(4):H=int(temp[j*2:(j+1)*2],16);param_list.append(H)
		param_list.extend([0,6,11,28]);H=int(hex(unix),16);param_list.append((H&4278190080)>>24);param_list.append((H&16711680)>>16);param_list.append((H&65280)>>8);param_list.append((H&255)>>0);eor_result_list=[]
		for (A,B) in zip(param_list,key):eor_result_list.append(A^B)
		for i in range(len):C=self.reverse(eor_result_list[i]);D=eor_result_list[(i+1)%len];E=C^D;F=self.rbit_algorithm(E);H=(F^4294967295^len)&255;eor_result_list[i]=H
		result=''
		for param in eor_result_list:result+=self.hex_string(param)
		return{'X-Gorgon':'0404b0d30000'+result,'X-Khronos':str(unix)}
	def rbit_algorithm(self,num):
		result='';tmp_string=bin(num)[2:]
		while len(tmp_string)<8:tmp_string='0'+tmp_string
		for i in range(0,8):result=result+tmp_string[7-i]
		return int(result,2)
	def hex_string(self,num):
		tmp_string=hex(num)[2:]
		if len(tmp_string)<2:tmp_string='0'+tmp_string
		return tmp_string
	def reverse(self,num):tmp_string=self.hex_string(num);return int(tmp_string[1:]+tmp_string[:1],16)

def sendViewsTest(__device_id, __install_id, cdid, openudid):
    global reqs, _lock, success, fails, rps, rpm
    for x in range(10):
        try:
            session_id = random.choice(__session_id)
            versionCode = random.choice(__versionCode)
            aweme_id = random.choice(__aweme_id)
            offset = random.choice(__offset)
            regions = random.choice(__regions)
            localesLanguage = random.choice(__localesLanguage)
            tzname = random.choice(__tzname)
            devices = random.choice(__devices)
            domains = random.choice(__domains)
            timestamp_ms = round(time.time() * 1000)
            _ts = unix=int(time.time())

            params = urlencode(
                                {
                                "IF you WANT the REST of the CODE please contact me on Telegram."
                                }
        )

            payload = f"item_id={aweme_id}&play_delta=1"
            sig     = Gorgon(params=params, cookies=None, data=None, unix=int(time.time())).get_value()
        
            response = r.post(
                url = ("https://" +  domains  + "/aweme/v1/aweme/stats/?" + params),
                data    = payload,
                headers = {"IF you WANT the REST of the CODE please contact me on Telegram."},
                verify  = False
            )
            reqs += 1
            try:
                if response.json()['status_code'] == 0:
                    _lock.acquire()
                    #print(f"Sent: {success}\nErrors: {fails}\nTotal: {success + fails}")
                    print(Colorate.Horizontal(Colors.yellow_to_green, f'Video ID : {__aweme_id} | Sent success: {success} '))
                    success += 1
                    _lock.release()
            except:
                if _lock.locked():_lock.release()
                fails += 1
                continue

        except Exception as e:
            pass

def sendViews(__device_id, __install_id, cdid, openudid):
    global reqs, _lock, success, fails, rps, rpm
    for x in range(10):
        try:
            session_id = random.choice(__session_id)
            versionCode = random.choice(__versionCode)
            aweme_id = random.choice(__aweme_id)
            offset = random.choice(__offset)
            regions = random.choice(__regions)
            localesLanguage = random.choice(__localesLanguage)
            tzname = random.choice(__tzname)
            devices = random.choice(__devices)
            domains = random.choice(__domains)

            params = urlencode(
                                {
                                   "IF you WANT the REST of the CODE please contact me on Telegram."
                                }
        )

            payload = f"item_id={aweme_id}&play_delta=1"
            sig     = Gorgon(params=params, cookies=None, data=None, unix=int(time.time())).get_value()
        
            response = r.post(
                url = (
                    "https://"
                    +  domains  +
                    "/aweme/v1/aweme/stats/?" + params
                ),
                data    = payload,
                headers = {"IF you WANT the REST of the CODE please contact me on Telegram."},
                verify  = False
            )
            reqs += 1
            try:
                if response.json()['status_code'] == 0:
                    _lock.acquire()
                    #print(f"Sent: {success}\nErrors: {fails}\nTotal: {success + fails}")
                    print(Colorate.Horizontal(Colors.yellow_to_green, f'Video ID : {__aweme_id} | Sent success: {success} '))
                    success += 1
                    _lock.release()
            except:
                if _lock.locked():_lock.release()
                fails += 1
                continue

        except Exception as e:
            pass
          
def getRoomID():
    headers = {
         "Cookie": f"_abck=05C80B079681C174EB755C5A9047B7E0~-1~YAAQ7e9hXrRFOaOCAQAA6Peiuwi+1m/wvh0Sd95YYjXPOZRpu/p1XsU/YbpX0u5ep+6SYGM5Axa2wVs4THSNdNxNS9zjxuxMBNN9DGQQENfIh57R0x4lSb8XWgA7GyB8TlOCzmbW8cOJkpFWAkwERVlwAX7hc88cuKRupEdZHZfx5InhX/un4CY3jVBVWEIgRKBNhfDBAfmc+UgcMmBbXFWg5IMiae8GMsDSPdeqyj8MLZle8EK6JpGqwiJ+PZ98UVHkDh3OzLBTRHlJpDKlpsoPGbgsYKrhLB2Z34BrMGlQojzLw8x6sOxHewEUhK5xanPH9lepQOKdg2eUBGqSxZSayNjMOpVCAFis133Fb4rXt5xOI9riszJFWgvTxZraYVVI1c6pM4GYpdM=~-1~-1~-1; ttwid=1%7C2qXf0NJ_8TEBHo0ciOwwkxVID_CxHCxfn2CJu3PaNG8%7C1661007783%7C4da417974c8fa5af103614e2f2e54eb64fe6e0c8446510311854b0c2a13e7443; _tt_covid_banner_closed=1; msToken=4tKkqrfVgaDb8DlU5F1WvJ8fBM4sejc9g2yMtVf_3BC59dwYANq2pTYSWPWMIOsz8kWO200qKaljJXMwwd-e-gQfQivz7OWjl8dJMSUZw3IHYLGEVbT4UvrHi-dNrSeMZF9w; tt_csrf_token=vyflaj82-Teur62dgDffmytMjXIxV_fO1B8Y; ak_bmsc=DF57974038A4C80578F35B8B2F7DD814~000000000000000000000000000000~YAAQxe9hXvfriqyCAQAAzlPHuxCZIUqtwnNk/PYipRpXb1wKBZ2ZfG/nDsDdIkBLysFF3V+cQkNPIEGqoXCxW7fUrb+IjgF859np2FZyGqLaEUhoR4aCmjw6ew7B2UODc3yh36kCpsaw7R7zC8qbwuOBlVHz9nVCxM36Hn2tRxWZv2F1SWnhd7+7nH3N1rfZM5WNdKA0aeIf3TfuRCwBVTmqOGq+N0Wu/GIGSwW09AZrfkZNyAXB5vYqi4RAp6R6xonYZlYbYWciF5kotJkd/KPPWhgc1sm/n+tYqVfjp6f+1EdNkPv/aRhJe7l+VUkINPn8wERFd0waIPyONckZtfTbEFZCXp5ylgpk0ZX1Ay7+wDRJCaMju1CRSHX+/mbP+fye6BOUuE+QS4jpCVJ+Wz8V2dN2V9rYE+7CmpbQrem7Bfnvp3zuliYBoHn1E2SB; bm_sz=AEBF4DA688161F9056A51B8D95790C42~YAAQ7e9hXrdFOaOCAQAA6PeiuxBHnHy28yMrfO0uHDpUAz+tpTr9qJhG+VW8JHcKqv10Yl3ed73Q4X9PToZPWFjdYVr3YjVSomcy9pgWDmqz3gNH5ssXabXuINuHIv7Vcj8mgFNLdlSzfXXgxW4jNWZ88QVF3PiV/D1AHwa3Pn+Wi9OIIqEAu9akYy/WjDsIXeJODYUSvYsTjR+M47d+veSK48Oqf3ggWA5sE7Y6jRej7HcGeN4im4GC0VO+y2+2CCPH3/CTI7kWJL20Ds8+V9PI4vOhTsS46Oh2LDZhjkLPhFo=~4534329~4469808; csrf_session_id=ff9a2e80a062531ee613a3c5035ab22d; bm_sv=D35DCD89570EBA72D0DE7ED8376EF748~YAAQ3e9hXkvgNaOCAQAALDzFuxAi1nMtjJBaMnVbDLA5g/6o8KBYCnm2AmQL3jw/nNDsfPHj+nocz3Wdmctg8tmmDOiUAu3zRhkYBG1UPDzlUF2cr3tYc6KMVq0+p/OG+Jgng780ohY5deyxgoXTFiMSR1eofkrfbwVZiS/5gNqEBW2qY5OWwjC+986AH7k3yGLRMrjfS8nsA3Gs9JLXG1jRMqHBMzf3cJpujbtj8mtq2dV/vD7jskE9rUjeY8bzlw==~1; passport_csrf_token=142ec4b7a7044cdbb6b59565f5b83ea8; passport_csrf_token_default=142ec4b7a7044cdbb6b59565f5b83ea8; s_v_web_id=verify_l71zqvs2_YCWVL2JM_1nvE_4oRk_8FnT_X2jkG5zAgQIK; bm_mi=827B8D45DCF4D9A9123D4222B8D1A780~YAAQ3e9hXibgNaOCAQAAmBvFuxB14MytETRuEOX80dRW7ZrhJoQ5k5HqNjG84KMQAXMPe8XLuT04QpERKaq7apAAdxzA5FqcwaXSVJ7wn8nKJedwyJ/SbJVA/rvQ9LS6S12DY5P/moBD3RZBvVjITm3rzqC1ujZmqB8xV/1Sd+hRVepvOfjf+0U+NpahDyWe6Gnj9lj2OpxW+6X5N+I9yaTyBzYPdVUb5Uxfc0MPasZ4DgNEuS3qupatPnKuIuUaMMoPxffUwhCl0jJyoyntmYeFnj9nrqpyOcBRj/w4NPFwsyZFAYifS2eOfEvJGLSMVMERrPXMN0jaTNg2~1; cookie-consent=%22ga%22:true%2C%22af%22:true%2C%22fbp%22:true%2C%22lip%22:true%2C%22bing%22:true%2C%22ttads%22:true%2C%22reddit%22:true%2C%22version%22:%22v8%22; odin_tt=4724e3abe4b96126f04d29e398cfbeed959da8118e140d6d302ae36653b80458143ac568cdb1b8365746f2ccdbe9d4195750ba0d80e48cdf5e8ed22369e99c87a37a55e202da924031990315d98caea8; cmpl_token=AgQQAPO_F-RO0rJxGTcZ6t04-JDRmasIf4A0YMXylQ; sid_guard={self.sess}%7C1661005518%7C5184000%7CWed%2C+19-Oct-2022+14%3A25%3A18+GMT; uid_tt=1ee9cd0d2fefcde0e55b49187afd72d2aef1b1030f0cd356bed6269bab701b5a; uid_tt_ss=1ee9cd0d2fefcde0e55b49187afd72d2aef1b1030f0cd356bed6269bab701b5a; sid_tt={self.sess}; sessionid={self.sess}; sessionid_ss={self.sess}; sid_ucp_v1=1.0.0-KGIxMmIxMzdkOGQ3ZDliYzNlYTg1ODVkNjU2MmYyNDYyN2NmNTE5OGEKIAiBiOCOifL9p2IQzt2DmAYYswsgDDC477-SBjgHQPQHEAMaBm1hbGl2YSIgYmRmNDIyNmRmYjgwMTIwYTQzMzA5MjllMzFjYWNhNzU; ssid_ucp_v1=1.0.0-KGIxMmIxMzdkOGQ3ZDliYzNlYTg1ODVkNjU2MmYyNDYyN2NmNTE5OGEKIAiBiOCOifL9p2IQzt2DmAYYswsgDDC477-SBjgHQPQHEAMaBm1hbGl2YSIgYmRmNDIyNmRmYjgwMTIwYTQzMzA5MjllMzFjYWNhNzU; store-idc=alisg; store-country-code=sa; store-country-code-src=uid; tt-target-idc=alisg; csrfToken=8cAqqxBZ_N6QnwsaxoO1sd4b",
         "User-Agent": generate_user_agent(),
         "Accept": "*/*",
         "Accept-Language": "ar,en-US;q=0.7,en;q=0.3",
         "Accept-Encoding": "gzip, deflate",
         "Referer": "https://www.tiktok.com/@kaito/live",
         "Sec-Fetch-Dest": "empty",
         "Sec-Fetch-Mode": "cors",
         "Sec-Fetch-Site": "same-origin",
         "Te": "trailers",}
        rez = requests.get(f"https://www.tiktok.com/api-live/user/room/?aid=1988&app_language=ar&app_name=tiktok_web&browser_language=ar&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20%28Windows%29&channel=tiktok_web&cookie_enabled=true&device_id=7129559580162868738&device_platform=web_pc&focus_state=true&from_page=user&history_len=7&is_fullscreen=false&is_page_visible=true&os=windows&priority_region=SA&referer=https%3A%2F%2Fwww.tiktok.com%2Fforyou%3Flang%3Dar&region=US&root_referer=https%3A%2F%2Fwww.tiktok.com%2F&screen_height=768&screen_width=1366&sourceType=54&tz_name=Asia%2FRiyadh&uniqueId={self.usersa}&verifyFp=verify_l71zqvs2_YCWVL2JM_1nvE_4oRk_8FnT_X2jkG5zAgQIK&webcast_language=ar",headers=headers).json()
        try:
            self.room = rez["data"]["user"]["roomId"]
        except:
            self.print_console("Something went wrong, contact the developer ...")
            exit(0)   

def sendLiveViews(__device_id, __install_id, cdid, openudid):
    global reqs, _lock, success, fails, rps, rpm
    for x in range(10):
        try:
            session_id = random.choice(__session_id)
            versionCode = random.choice(__versionCode)
            aweme_id = random.choice(__aweme_id)
            offset = random.choice(__offset)
            regions = random.choice(__regions)
            localesLanguage = random.choice(__localesLanguage)
            tzname = random.choice(__tzname)
            devices = random.choice(__devices)
            domains = random.choice(__domains)
            timestamp_ms = round(time.time() * 1000)
            ts = unix=int(time.time())
            room_id = random.choice(__room_id)

            params = urlencode(
                                {
                                "IF you WANT the REST of the CODE please contact me on Telegram."
                                }
        )
            payload = f"room_id={room_id}&hold_living_room=1&is_login=1&enter_source=general_search-general_search&request_id=xxxxxxxxx"
            sig     = Gorgon(params=params, cookies=None, data=None, unix=int(time.time())).get_value()
        
            response = r.post(
                url = (
                    "https://"
                    +  domains  +
                    "/webcast/room/enter/?" + params
                ),
                data    = payload,
                headers = {"IF you WANT the REST of the CODE please contact me on Telegram."},
                verify  = False
            )
            reqs += 1
            try:
                if response.json()['status_code'] == 0:
                    _lock.acquire()
                    #print(f"Sent: {success}\nErrors: {fails}\nTotal: {success + fails}")
                    print(Colorate.Horizontal(Colors.yellow_to_green, f'Video ID : {__aweme_id} | Sent success: {success} '))
                    success += 1
                    _lock.release()
            except:
                if _lock.locked():_lock.release()
                fails += 1
                continue

        except Exception as e:
            pass

def sendShares(__device_id, __install_id, cdid, openudid):
    global reqs, _lock, success, fails, rps, rpm
    for x in range(10):
        try:
            session_id = random.choice(__session_id)
            versionCode = random.choice(__versionCode)
            aweme_id = random.choice(__aweme_id)
            offset = random.choice(__offset)
            regions = random.choice(__regions)
            localesLanguage = random.choice(__localesLanguage)
            tzname = random.choice(__tzname)
            devices = random.choice(__devices)
            domains = random.choice(__domains)
            versionUa = random.choice(__versionUa)

            params = urlencode(
                                {
                                   "IF you WANT the REST of the CODE please contact me on Telegram."
                                }
            )
            payload = f"share_delta=1&item_id={aweme_id}"
            sig     = Gorgon(params=params, cookies=None, data=None, unix=int(time.time())).get_value()
        
            response = r.post(
                url = (
                    "https://"
                    +  domains  +
                    "/aweme/v1/aweme/stats/?" + params
                ),
                data    = payload,
                headers = {"IF you WANT the REST of the CODE please contact me on Telegram."},
                verify  = False
            )
            reqs += 1
            try:
                if response.json()['status_code'] == 0:
                    _lock.acquire()
                    #print(f"Sent: {success}\nErrors: {fails}\nTotal: {success + fails}")
                    print(Colorate.Horizontal(Colors.yellow_to_green, f'Video ID : {__aweme_id} | Sent success: {success} '))
                    success += 1
                    _lock.release()
            except:
                if _lock.locked():_lock.release()
                fails += 1
                continue

        except Exception as e:
            pass

def sendHearts(__device_id, __install_id, cdid, openudid):
    global reqs, _lock, success, fails, rps, rpm
    for x in range(10):
        try:
            session_id = random.choice(__session_id)
            versionCode = random.choice(__versionCode)
            aweme_id = random.choice(__aweme_id)
            offset = random.choice(__offset)
            regions = random.choice(__regions)
            localesLanguage = random.choice(__localesLanguage)
            tzname = random.choice(__tzname)
            devices = random.choice(__devices)
            domains = random.choice(__domains)
            resolution = random.choice(__resolution)
            dpi = random.choice(__dpi)
            timestamp_ms = round(time.time() * 1000)
            ts = unix=int(time.time())
            params = urlencode(
                                {
                                "IF you WANT the REST of the CODE please contact me on Telegram."
                                }
        )
        
            sig     = Gorgon(params=params, cookies=None, data=None, unix=int(time.time())).get_value()
            response = r.post(
                url = ("https://xxxxxxx.com/aweme/v1/commit/item/digg/?" + params),
                headers = {"IF you WANT the REST of the CODE please contact me on Telegram."},
                verify  = False
            )
            reqs += 1
            try:
                if response.json()['status_code'] == 0:
                    _lock.acquire()
                    print(Colorate.Horizontal(Colors.yellow_to_green, f'Video ID : {__aweme_id} | Sent success: {success} '))
                    success += 1
                    _lock.release()
            except:
                if _lock.locked():_lock.release()
                fails += 1
                continue

        except Exception as e:
            pass

def sendFavorites(__device_id, __install_id, cdid, openudid):
    global reqs, _lock, success, fails, rps, rpm
    for x in range(10):
        try:
            session_id = random.choice(__session_id)
            versionCode = random.choice(__versionCode)
            timestamp_ms = round(time.time() * 1000)
            _ts = unix=int(time.time())
            aweme_id = random.choice(__aweme_id)
            domains = random.choice(__domains)
            params = urlencode(
                                {
                                "IF you WANT the REST of the CODE please contact me on Telegram."
                                }
            )
            sig = Gorgon(params=params, cookies=None, data=None, unix=int(time.time())).get_value()
            response = r.post(
                url = ("https://" +  domains  + "/aweme/v1/aweme/collect/?aweme_id=" + aweme_id + params),
                headers = {"IF you WANT the REST of the CODE please contact me on Telegram."},
                verify  = False
            )
            reqs += 1
            try:
                if response.json()['status_code'] == 0:
                    _lock.acquire()
                    print(Colorate.Horizontal(Colors.yellow_to_green, f'Video ID : {__aweme_id} | Sent success: {success} '))
                    success += 1
                    _lock.release()
            except:
                if _lock.locked():_lock.release()
                fails += 1
                continue

        except Exception as e:
            pass

def rpsm_loop():
    global rps, rpm
    while True:
        initial = reqs
        time.sleep(1)
        rps = round((reqs - initial) / 60, 1)
        rpm = round(rps * 60, 1)

def clearConsole():
    if os.name == 'posix':
        os.system('clear')
    elif os.name in ('ce', 'nt', 'dos'):
        os.system('cls')
    else:
        pass
def sendFollowers():
    try:
         print("")

    except Exception as e:
        pass

def checkRegisterUser():
    try:
        response  = requests.get("license code url to check")
        if response.status_code == 200:
            print('Welcome back man, your license is valid!')
            time.sleep(3)
        else:
            print('License is NOT valid.')
            time.sleep(3)
            sys.exit()

    except Exception as e:
        pass

def stats():
    Banner()
    print(f"Sent: {success}\nErrors: {fails}\nTotal: {success + fails}")
    set_title(f"Sent: {success} Errors: {fails} Total:{success + fails}")
     
if __name__ == "__main__":
    clearConsole()
    Banner()
    threading.Thread(target=checkRegisterUser).start()
    time.sleep(3)
    with open(os.path.join("devices.txt"), "r") as f:
        devices = f.read().splitlines()

    sendType = int(Write.Input("[1] - TikTok Video Views\n[2] - TikTok Video Favorite\n[3] - TikTok Video Share\n[4] - TikTok Video Like (heart)\n[5] - TikTok Followers\n[6] - TikTok Live Stream\n\nType option number : ", Colors.green_to_yellow, interval=0.0001))
    threads = int(Write.Input("Number of Threads: ", Colors.green_to_yellow, interval=0.0001))
    amountTosend = int(Write.Input("Number of hits: ", Colors.green_to_yellow, interval=0.0001))
    
    _lock = threading.Lock()
    reqs = 0
    success = 0
    fails = 0
    rpm = 0
    rps = 0
    
    threading.Thread(target=rpsm_loop).start()
    while True:  
        device = random.choice(devices)
        for i in range(threads):
                if sendType == 1:
                    if success >= amountTosend:
                        print("All views sent!")
                        time.sleep(3)
                        exit()
                    else:    
                        did, iid, cdid, openudid = device.split(':')
                        t = threading.Thread(target=sendViews,args=[did,iid,cdid,openudid])
                        t.start()
                if sendType == 2:
                    if success >= amountTosend:
                        print("All views sent!")
                        time.sleep(1)
                        exit()
                    else:
                        did, iid, cdid, openudid = device.split(':')
                        t = threading.Thread(target=sendFavorites,args=[did,iid,cdid,openudid])
                        t.start()
                if sendType == 3:
                    if success >= amountTosend:
                        print("All views sent!")
                        time.sleep(1)
                        exit()
                    else:
                        did, iid, cdid, openudid = device.split(':')
                        t = threading.Thread(target=sendShares,args=[did,iid,cdid,openudid])
                        t.start() 
                if sendType == 4:
                    if success >= amountTosend:
                        print("All views sent!")
                        time.sleep(1)
                        exit()
                    else:
                        did, iid, cdid, openudid = device.split(':')
                        t = threading.Thread(target=sendHearts,args=[did,iid,cdid,openudid])
                        t.start() 
                if sendType == 5:
                    if success >= amountTosend:
                        print("All views sent!")
                        time.sleep(1)
                        exit()
                    else:
                        did, iid, cdid, openudid = device.split(':')
                        t = threading.Thread(target=sendFollowers,args=[did,iid,cdid,openudid])
                        t.start()  
                if sendType == 6:
                    if success >= amountTosend:
                        print("All views sent!")
                        time.sleep(1)
                        exit()
                    else:
                        did, iid, cdid, openudid = device.split(':')
                        t = threading.Thread(target=sendLiveViews,args=[did,iid,cdid,openudid])
                        t.start()              
