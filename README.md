# CDN and Domain Checker Tools

Repositori ini berisi serangkaian skrip Python yang digunakan untuk memeriksa status, dukungan CDN (Content Delivery Network), dan fungsionalitas terkait dari sekumpulan domain. Skrip ini sangat berguna untuk memastikan domain dikonfigurasi dengan benar, terutama terkait dengan Cloudflare atau layanan CDN serupa.

## Deskripsi File

### 1. `cdn.py`
Skrip ini melakukan pengecekan secara berurutan (synchronous) pada daftar domain.
- **Fungsi Utama:** Memeriksa apakah setiap domain mendukung endpoint `/cdn-cgi/trace` dan memvalidasi keberadaan parameter spesifik (seperti `fl=`, `h=`, `ip=`) yang biasanya dikembalikan oleh Cloudflare.
- **Pendekatan:** Menggunakan pustaka `requests` standar.
- **Output:** Menampilkan domain yang valid dengan warna hijau dan mendukung penghentian dengan `Ctrl+C`.

### 2. `cdn2.py`
Skrip ini merupakan versi asinkron (asynchronous) dari `cdn.py` untuk pengecekan yang lebih cepat.
- **Fungsi Utama:** Melakukan fungsi yang sama dengan `cdn.py` (memeriksa `/cdn-cgi/trace`), tetapi menggunakan `asyncio` dan `aiohttp` untuk memproses beberapa domain secara bersamaan (concurrently).
- **Pendekatan:** Menggunakan pendekatan asinkron, yang jauh lebih efisien untuk daftar domain yang besar.
- **Output:** Outputnya mirip dengan `cdn.py`.

### 3. `checker.py`
Skrip komprehensif ini melakukan serangkaian pemeriksaan yang lebih mendalam pada setiap domain.
- **Fungsi Utama:**
  - **Aksesibilitas (Akses HTTP/HTTPS):** Memeriksa apakah domain merespons terhadap permintaan HTTP/HTTPS.
  - **Dukungan `/cdn-cgi/trace`:** Memeriksa ketersediaan endpoint ini.
  - **Validasi Redirect:** Memeriksa apakah domain tidak melakukan redirect ke lokasi yang tidak diinginkan (hanya redirect dari HTTP ke HTTPS yang dianggap valid).
  - **Dukungan WebSocket:** Memeriksa apakah domain dapat diakses melalui protokol WebSocket (`ws://`).
- **Pendekatan:** Menggabungkan `requests` dan `websocket-client`.
- **Output:** Menampilkan hasil dari setiap tahap pengujian untuk setiap domain secara detail dan berwarna.

## Persyaratan (Requirements)

Sebelum menjalankan skrip-skrip ini, pastikan Anda telah menginstal dependensi yang diperlukan. Anda dapat menginstalnya menggunakan `pip`.

```bash
pip install requests colorama aiohttp websocket-client
```

## Cara Penggunaan

1. **Siapkan Daftar Domain:**
   Buat sebuah file teks (misalnya, `list_domain.txt`) dan isi dengan daftar domain yang ingin Anda periksa. Setiap domain harus berada pada baris baru (tanpa `http://` atau `https://`).
   *Contoh isi `list_domain.txt`:*
   ```text
   example.com
   test.net
   ```

2. **Jalankan Skrip:**
   Buka terminal atau command prompt dan jalankan skrip yang Anda inginkan.

   - **Untuk `cdn.py` (Pengecekan Sekuensial):**
     ```bash
     python cdn.py
     ```
   - **Untuk `cdn2.py` (Pengecekan Asinkron/Cepat):**
     ```bash
     python cdn2.py
     ```
   - **Untuk `checker.py` (Pengecekan Komprehensif):**
     ```bash
     python checker.py
     ```

3. **Masukkan Nama File:**
   Saat diminta, masukkan nama file teks yang berisi daftar domain Anda (misalnya, `list_domain.txt`). Skrip akan mulai memproses daftar dan menampilkan hasilnya.

## Catatan
- Semua skrip menggunakan antarmuka baris perintah (CLI) dan menampilkan pesan kesalahan jika file tidak ditemukan.
- Warna yang digunakan di terminal memerlukan pustaka `colorama` untuk berfungsi dengan benar pada berbagai platform.