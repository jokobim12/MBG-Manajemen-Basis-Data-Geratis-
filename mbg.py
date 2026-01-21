#!/usr/bin/env python3
"""
MBG (Manajemen Basis Geratis) - Database Management System
Sistem database mandiri dengan bahasa Indonesia
Menggunakan SQLite sebagai backend (tidak perlu MySQL)
"""

import sys
import readline
from translator import translate
from db import MBGDatabase
from bantuan import tampilkan_bantuan, tampilkan_selamat_datang

# Warna ANSI
class Warna:
    HIJAU = '\033[92m'
    KUNING = '\033[93m'
    MERAH = '\033[91m'
    BIRU = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_sukses(pesan):
    print(f"{Warna.HIJAU}✅ {pesan}{Warna.RESET}")

def print_error(pesan):
    print(f"{Warna.MERAH}❌ {pesan}{Warna.RESET}")

def print_info(pesan):
    print(f"{Warna.CYAN}ℹ️  {pesan}{Warna.RESET}")

def main():
    # Parse arguments
    show_help = False
    
    for arg in sys.argv[1:]:
        if arg in ["-h", "--help", "--bantuan"]:
            show_help = True
    
    if show_help:
        print(f"""
{Warna.BOLD}MBG (Manajemen Basis Geratis){Warna.RESET}
Sistem Manajemen Database dengan Bahasa Indonesia
Menggunakan SQLite - Tidak perlu MySQL/MariaDB!

{Warna.KUNING}Penggunaan:{Warna.RESET}
  ./mbg                 Jalankan MBG shell
  ./mbg --bantuan       Tampilkan bantuan ini

{Warna.KUNING}Di dalam shell:{Warna.RESET}
  BANTUAN;              Lihat daftar perintah
  KELUAR;               Keluar dari MBG

{Warna.KUNING}Contoh:{Warna.RESET}
  mbg> SEDIAKAN DAPUR sekolah;
  mbg> GUNAKAN DAPUR sekolah;
  mbg> SEDIAKAN BAHAN siswa (id ANGKA UTAMA OTOMATIS, nama TEKS);
  mbg> MASAK siswa PAKAI nama='Budi';
  mbg> SAJIKAN siswa;
""")
        return
    
    # Inisialisasi database
    db = MBGDatabase()
    db.connect()
    
    # Tampilkan pesan selamat datang
    tampilkan_selamat_datang()
    
    # Setup readline untuk history
    try:
        readline.read_history_file(".mbg_history")
    except FileNotFoundError:
        pass
    
    # Buffer untuk query multi-line
    query_buffer = ""
    
    def get_prompt():
        if db.current_db:
            return f"{Warna.BOLD}{Warna.HIJAU}mbg [{db.current_db}]>{Warna.RESET} "
        return f"{Warna.BOLD}{Warna.HIJAU}mbg>{Warna.RESET} "
    
    prompt_lanjut = f"{Warna.BOLD}{Warna.HIJAU}  ->{Warna.RESET} "
    
    while True:
        try:
            # Pilih prompt
            if query_buffer:
                prompt = prompt_lanjut
            else:
                prompt = get_prompt()
            
            # Baca input
            line = input(prompt)
            
            # Tambahkan ke buffer
            query_buffer += " " + line if query_buffer else line
            
            # Cek apakah query lengkap (diakhiri titik koma)
            if not query_buffer.strip():
                query_buffer = ""
                continue
                
            if not query_buffer.strip().endswith(";"):
                continue
            
            # Query lengkap, proses
            query = query_buffer.strip()
            query_buffer = ""
            
            # Cek command khusus
            query_upper = query.upper().replace(";", "").strip()
            
            if query_upper in ["KELUAR", "EXIT", "QUIT"]:
                print(f"\n{Warna.CYAN}Sampai jumpa! 👋{Warna.RESET}\n")
                break
            
            if query_upper in ["BANTUAN", "HELP", "?"]:
                tampilkan_bantuan()
                continue
            
            if query_upper == "BERSIHKAN" or query_upper == "CLEAR":
                print("\033[2J\033[H")  # Clear screen
                continue
            
            # Translate dan eksekusi
            try:
                sql = translate(query)
                db.execute(sql, query)
            except Exception as e:
                print_error(str(e))
        
        except KeyboardInterrupt:
            print(f"\n{Warna.KUNING}Ketik KELUAR; untuk keluar{Warna.RESET}")
            query_buffer = ""
            continue
        
        except EOFError:
            print(f"\n{Warna.CYAN}Sampai jumpa! 👋{Warna.RESET}\n")
            break
    
    # Simpan history
    try:
        readline.write_history_file(".mbg_history")
    except:
        pass
    
    db.close()

if __name__ == "__main__":
    main()
