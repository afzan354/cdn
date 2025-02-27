import asyncio
import aiohttp
import signal
import sys
from colorama import Fore, Style

# Variabel untuk menyimpan domain yang valid
valid_domains = []

def signal_handler(sig, frame):
    print("\nProgram dihentikan oleh pengguna.")
    if valid_domains:
        print("\nDomain dengan informasi CDN CGI:")
        for domain in valid_domains:
            print(f"{Fore.GREEN}centang {domain}/cdn-cgi/trace{Style.RESET_ALL}")
    print("cek dn selesai")
    sys.exit(0)

def normalize_url(domain):
    # Memastikan URL menggunakan protokol https
    if not domain.startswith(('http://', 'https://')):
        domain = f"https://{domain}"
    elif domain.startswith('http://'):
        domain = domain.replace('http://', 'https://')
    return domain

async def check_trace(session, domain):
    url = f"{normalize_url(domain)}/cdn-cgi/trace"
    try:
        async with session.get(url, timeout=5) as response:
            if response.status == 200:
                text = await response.text()
                # Memeriksa apakah respons mengandung informasi yang diinginkan
                if "fl=" in text and "h=" in text and "ip=" in text:
                    print(f"{Fore.GREEN}centang {domain}/cdn-cgi/trace{Style.RESET_ALL}")
                    valid_domains.append(domain)
    except (aiohttp.ClientError, asyncio.TimeoutError):
        pass  # Tidak menampilkan pesan error untuk domain yang gagal

async def main():
    global valid_domains
    filename = input("Masukkan nama file yang berisi list domain: ")

    try:
        with open(filename, 'r') as file:
            domains = file.read().splitlines()
        
        async with aiohttp.ClientSession() as session:
            tasks = [check_trace(session, domain) for domain in domains]
            await asyncio.gather(*tasks)
    
    except FileNotFoundError:
        print(f"File {filename} tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

    if valid_domains:
        print("\nDomain dengan informasi CDN CGI:")
        for domain in valid_domains:
            print(f"{Fore.GREEN}centang {domain}/cdn-cgi/trace{Style.RESET_ALL}")
    print("cek dn selesai")

if __name__ == "__main__":
    # Mengatur handler untuk Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    # Menginisialisasi Colorama
    from colorama import init
    init(autoreset=True)
    asyncio.run(main())