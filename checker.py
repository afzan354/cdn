import os
import requests
import websocket
from colorama import init, Fore

# Inisialisasi colorama
init(autoreset=True)

def is_domain_active(domain):
    """Memeriksa apakah domain aktif dan dapat diakses."""
    protocols = ["http", "https"]
    for protocol in protocols:
        try:
            print(f"Mencoba {protocol}://{domain}...")
            response = requests.head(f"{protocol}://{domain}", timeout=5)
            if response.status_code < 400:
                print(Fore.GREEN + f"✅ {protocol}://{domain} aktif.")
                return True
        except Exception as e:
            print(Fore.RED + f"❌ Gagal mengakses {protocol}://{domain}: {e}")
    return False

def supports_cdn_cgi_trace(domain):
    """Memeriksa apakah domain mendukung endpoint /cdn-cgi/trace."""
    protocols = ["http", "https"]
    for protocol in protocols:
        try:
            print(f"Mencoba {protocol}://{domain}/cdn-cgi/trace...")
            response = requests.get(f"{protocol}://{domain}/cdn-cgi/trace", timeout=5)
            if response.status_code == 200:
                print(Fore.GREEN + f"✅ {protocol}://{domain}/cdn-cgi/trace tersedia.")
                return True
        except Exception as e:
            print(Fore.RED + f"❌ Gagal mengakses {protocol}://{domain}/cdn-cgi/trace: {e}")
    return False

def has_no_unwanted_redirect(domain):
    """Memeriksa apakah domain tidak melakukan redirect yang tidak diinginkan."""
    try:
        # Coba akses domain menggunakan HTTP
        response = requests.get(f"http://{domain}", allow_redirects=False, timeout=5)
        if response.status_code in [301, 302]:
            # Jika redirect ke HTTPS, anggap valid
            redirect_location = response.headers.get("Location", "")
            if redirect_location.startswith("https://"):
                print(Fore.GREEN + f"✅ Redirect ke HTTPS ditemukan: {redirect_location}")
                return True
            else:
                print(Fore.RED + f"❌ Redirect ke lokasi tidak valid: {redirect_location}")
                return False
        elif response.status_code < 400:
            print(Fore.GREEN + "✅ Tidak ada redirect.")
            return True
        else:
            print(Fore.RED + f"❌ Status code tidak valid: {response.status_code}")
            return False
    except Exception as e:
        print(Fore.RED + f"❌ Gagal memeriksa redirect: {e}")
        return False

def supports_websocket(domain):
    """Memeriksa apakah domain mendukung WebSocket."""
    try:
        ws_url = f"ws://{domain}"
        ws = websocket.create_connection(ws_url, timeout=5)
        ws.close()
        print(Fore.GREEN + "✅ Domain mendukung WebSocket.")
        return True
    except Exception as e:
        print(Fore.RED + f"❌ Gagal mengakses WebSocket: {e}")
        return False

def main():
    while True:
        # Meminta input nama file dari pengguna
        file_name = input("Masukkan nama file yang berisi daftar domain (contoh: file.txt): ").strip()

        # Memeriksa apakah file ada
        if not os.path.isfile(file_name):
            print(Fore.RED + f"❌ File '{file_name}' tidak ditemukan. Silakan coba lagi.")
            continue

        # Membaca daftar domain dari file
        with open(file_name, "r") as file:
            domains = file.read().splitlines()

        # Jika file kosong
        if not domains:
            print(Fore.RED + "❌ File kosong. Tidak ada domain untuk diperiksa.")
            break

        # Menjalankan tes untuk setiap domain
        print("\nMulai pengecekan domain...\n")
        for domain in domains:
            domain = domain.strip()
            if not domain:
                continue  # Lewati baris kosong

            print(Fore.CYAN + f"\nTesting domain: {domain}")
            if not is_domain_active(domain):
                print(Fore.RED + "❌ Domain tidak aktif atau tidak dapat diakses.")
                continue

            if not supports_cdn_cgi_trace(domain):
                print(Fore.RED + "❌ Domain tidak mendukung endpoint /cdn-cgi/trace.")
                continue

            if not has_no_unwanted_redirect(domain):
                print(Fore.RED + "❌ Domain melakukan redirect yang tidak diinginkan.")
                continue

            if not supports_websocket(domain):
                print(Fore.RED + "❌ Domain tidak mendukung WebSocket.")
                continue

            print(Fore.GREEN + "✅ Domain lulus semua tes!")

        # Keluar dari loop setelah selesai
        break

if __name__ == "__main__":
    main()