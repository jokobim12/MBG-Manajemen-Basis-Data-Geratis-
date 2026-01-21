"""
MBG Help System - Sistem Bantuan
"""

# Warna ANSI
class Warna:
    HIJAU = '\033[92m'
    KUNING = '\033[93m'
    MERAH = '\033[91m'
    BIRU = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'


def tampilkan_selamat_datang():
    """Menampilkan pesan selamat datang"""
    print(f"""
{Warna.CYAN}╔════════════════════════════════════════════════╗
║     MBG - Manajemen Basis Geratis v1.0         ║
╚════════════════════════════════════════════════╝{Warna.RESET}
Ketik {Warna.HIJAU}BANTUAN;{Warna.RESET} untuk panduan | {Warna.HIJAU}KELUAR;{Warna.RESET} untuk keluar
""")


def tampilkan_bantuan():
    """Menampilkan daftar perintah MBG"""
    print(f"""
{Warna.CYAN}PANDUAN PERINTAH MBG{Warna.RESET}
{Warna.DIM}────────────────────────────────────────────────{Warna.RESET}

{Warna.KUNING}DAPUR (Database){Warna.RESET}
  LIHAT DAPUR;              - Daftar semua database
  SEDIAKAN DAPUR nama;      - Buat database baru
  GUNAKAN DAPUR nama;       - Pilih database
  HAPUS DAPUR nama;         - Hapus database

{Warna.KUNING}BAHAN (Tabel){Warna.RESET}
  LIHAT BAHAN;              - Daftar semua tabel
  JELASKAN BAHAN nama;      - Lihat struktur tabel
  HAPUS BAHAN nama;         - Hapus tabel
  SEDIAKAN BAHAN nama (     - Buat tabel baru
    kolom TIPE,
    ...
  );

{Warna.KUNING}Tipe Data{Warna.RESET}
  ANGKA                     - Bilangan bulat
  ANGKA UTAMA               - Primary key
  ANGKA UTAMA OTOMATIS      - Auto increment
  TEKS                      - Teks pendek (255 karakter)
  TEKS PANJANG              - Teks panjang
  TANGGAL                   - Tanggal
  WAKTU                     - Waktu

{Warna.KUNING}Modifier{Warna.RESET}
  WAJIB                     - Tidak boleh kosong
  UNIK                      - Harus berbeda

{Warna.KUNING}Operasi Data{Warna.RESET}
  MASAK tabel PAKAI kol=nilai, ...;     - Tambah data
  SAJIKAN tabel;                        - Lihat semua data
  SAJIKAN tabel YANG kondisi;           - Lihat dengan filter
  BUMBUI tabel JADI kol=nilai YANG ...  - Ubah data
  BUANG tabel YANG kondisi;             - Hapus data
  HITUNG tabel;                         - Hitung jumlah

{Warna.KUNING}Lainnya{Warna.RESET}
  BANTUAN;      - Tampilkan panduan ini
  BERSIHKAN;    - Bersihkan layar
  KELUAR;       - Keluar

{Warna.DIM}────────────────────────────────────────────────{Warna.RESET}
{Warna.CYAN}Contoh:{Warna.RESET}
  SEDIAKAN DAPUR sekolah;
  GUNAKAN DAPUR sekolah;
  SEDIAKAN BAHAN siswa (id ANGKA UTAMA OTOMATIS, nama TEKS);
  MASAK siswa PAKAI nama='Budi';
  SAJIKAN siswa;
""")
