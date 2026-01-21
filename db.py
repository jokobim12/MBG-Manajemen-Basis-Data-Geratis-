"""
MBG Database Handler - SQLite Backend
Database mandiri tanpa perlu MySQL/MariaDB
Setiap "DAPUR" disimpan sebagai file .mbg
"""

import sqlite3
import os

# Warna ANSI
class Warna:
    HIJAU = '\033[92m'
    KUNING = '\033[93m'
    MERAH = '\033[91m'
    BIRU = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'


class MBGDatabase:
    def __init__(self, data_dir=None):
        # Direktori untuk menyimpan database
        if data_dir is None:
            self.data_dir = os.path.join(os.path.dirname(__file__), "dapur")
        else:
            self.data_dir = data_dir
        
        # Buat direktori jika belum ada
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        self.conn = None
        self.current_db = None
    
    def connect(self) -> bool:
        """Inisialisasi MBG (tidak perlu koneksi khusus untuk SQLite)"""
        return True
    
    def close(self):
        """Tutup koneksi database aktif"""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def _get_db_path(self, db_name: str) -> str:
        """Dapatkan path file database"""
        return os.path.join(self.data_dir, f"{db_name}.mbg")
    
    def _db_exists(self, db_name: str) -> bool:
        """Cek apakah database ada"""
        return os.path.exists(self._get_db_path(db_name))
    
    def get_databases(self) -> list:
        """Dapatkan daftar semua database"""
        databases = []
        if os.path.exists(self.data_dir):
            for f in os.listdir(self.data_dir):
                if f.endswith(".mbg"):
                    databases.append(f[:-4])  # Hapus ekstensi .mbg
        return databases
    
    def execute(self, sql: str, original_query: str = ""):
        """Eksekusi query SQL dan tampilkan hasil"""
        sql = sql.strip()
        sql_upper = sql.upper()
        
        try:
            # === SHOW DATABASES ===
            if sql_upper.startswith("SHOW DATABASES"):
                databases = self.get_databases()
                if databases:
                    self._tampilkan_daftar("Dapur", databases)
                else:
                    print(f"{Warna.KUNING}(Belum ada dapur. Buat dengan: SEDIAKAN DAPUR nama;){Warna.RESET}")
                return
            
            # === CREATE DATABASE ===
            if sql_upper.startswith("CREATE DATABASE"):
                db_name = sql.replace("CREATE DATABASE", "").replace(";", "").strip()
                db_name = db_name.replace("IF NOT EXISTS", "").strip()
                
                if self._db_exists(db_name):
                    print(f"{Warna.MERAH}❌ Dapur \"{db_name}\" sudah ada!{Warna.RESET}")
                    return
                
                # Buat database baru (file kosong)
                conn = sqlite3.connect(self._get_db_path(db_name))
                conn.close()
                print(f"{Warna.HIJAU}✅ Dapur \"{db_name}\" berhasil disediakan!{Warna.RESET}")
                return
            
            # === DROP DATABASE ===
            if sql_upper.startswith("DROP DATABASE"):
                db_name = sql.replace("DROP DATABASE", "").replace("IF EXISTS", "").replace(";", "").strip()
                
                db_path = self._get_db_path(db_name)
                if os.path.exists(db_path):
                    # Tutup koneksi jika ini database aktif
                    if self.current_db == db_name:
                        self.close()
                        self.current_db = None
                    os.remove(db_path)
                    print(f"{Warna.HIJAU}✅ Dapur \"{db_name}\" berhasil dihapus!{Warna.RESET}")
                else:
                    print(f"{Warna.MERAH}❌ Dapur \"{db_name}\" tidak ditemukan!{Warna.RESET}")
                return
            
            # === USE database ===
            if sql_upper.startswith("USE "):
                db_name = sql.replace("USE", "").replace("use", "").replace(";", "").strip()
                
                if not self._db_exists(db_name):
                    print(f"{Warna.MERAH}❌ Dapur \"{db_name}\" tidak ditemukan!{Warna.RESET}")
                    return
                
                # Tutup koneksi lama
                self.close()
                
                # Buka koneksi baru
                self.conn = sqlite3.connect(self._get_db_path(db_name))
                self.current_db = db_name
                print(f"{Warna.HIJAU}✅ Dapur berubah ke: {db_name}{Warna.RESET}")
                return
            
            # === Commands yang memerlukan database aktif ===
            if self.conn is None:
                print(f"{Warna.MERAH}❌ Belum memilih dapur! Gunakan: GUNAKAN DAPUR nama_dapur;{Warna.RESET}")
                return
            
            cursor = self.conn.cursor()
            
            # === SHOW TABLES ===
            if sql_upper.startswith("SHOW TABLES"):
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
                tables = [row[0] for row in cursor.fetchall()]
                if tables:
                    self._tampilkan_daftar(f"Bahan di {self.current_db}", tables)
                else:
                    print(f"{Warna.KUNING}(Belum ada bahan. Buat dengan: SEDIAKAN BAHAN nama (...);){Warna.RESET}")
                return
            
            # === DESCRIBE table ===
            if sql_upper.startswith("DESCRIBE"):
                table_name = sql.replace("DESCRIBE", "").replace(";", "").strip()
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = cursor.fetchall()
                
                if not columns:
                    print(f"{Warna.MERAH}❌ Bahan \"{table_name}\" tidak ditemukan!{Warna.RESET}")
                    return
                
                # Format output
                print(f"\n{Warna.CYAN}Struktur bahan: {table_name}{Warna.RESET}")
                print("-" * 50)
                for col in columns:
                    # col = (cid, name, type, notnull, default, pk)
                    pk = " 🔑 UTAMA" if col[5] else ""
                    nn = " WAJIB" if col[3] else ""
                    print(f"  {col[1]}: {col[2]}{pk}{nn}")
                print()
                return
            
            # === CREATE TABLE - perlu konversi syntax ===
            if sql_upper.startswith("CREATE TABLE"):
                # SQLite tidak mendukung beberapa syntax MySQL
                # Konversi AUTO_INCREMENT ke AUTOINCREMENT
                sql_sqlite = sql.replace("AUTO_INCREMENT", "AUTOINCREMENT")
                cursor.execute(sql_sqlite)
                self.conn.commit()
                
                # Extract table name
                import re
                match = re.search(r"CREATE TABLE\s+(\w+)", sql, re.I)
                table_name = match.group(1) if match else "tabel"
                print(f"{Warna.HIJAU}✅ Bahan \"{table_name}\" berhasil disediakan!{Warna.RESET}")
                return
            
            # === DROP TABLE ===
            if sql_upper.startswith("DROP TABLE"):
                cursor.execute(sql)
                self.conn.commit()
                print(f"{Warna.HIJAU}✅ Bahan berhasil dihapus!{Warna.RESET}")
                return
            
            # === SELECT queries ===
            if sql_upper.startswith("SELECT"):
                cursor.execute(sql)
                self._tampilkan_hasil(cursor)
                return
            
            # === INSERT ===
            if sql_upper.startswith("INSERT"):
                cursor.execute(sql)
                self.conn.commit()
                print(f"{Warna.HIJAU}✅ {cursor.rowcount} resep berhasil dimasak!{Warna.RESET}")
                return
            
            # === UPDATE ===
            if sql_upper.startswith("UPDATE"):
                cursor.execute(sql)
                self.conn.commit()
                print(f"{Warna.HIJAU}✅ {cursor.rowcount} baris berhasil dibumbui!{Warna.RESET}")
                return
            
            # === DELETE ===
            if sql_upper.startswith("DELETE"):
                cursor.execute(sql)
                self.conn.commit()
                print(f"{Warna.HIJAU}✅ {cursor.rowcount} baris berhasil dibuang!{Warna.RESET}")
                return
            
            # === Query lainnya ===
            cursor.execute(sql)
            self.conn.commit()
            print(f"{Warna.HIJAU}✅ Query berhasil dijalankan!{Warna.RESET}")
            
        except sqlite3.Error as e:
            error_msg = str(e)
            if "no such table" in error_msg:
                print(f"{Warna.MERAH}❌ Bahan tidak ditemukan!{Warna.RESET}")
            elif "already exists" in error_msg:
                print(f"{Warna.MERAH}❌ Bahan sudah ada!{Warna.RESET}")
            elif "UNIQUE constraint failed" in error_msg:
                print(f"{Warna.MERAH}❌ Data sudah ada (duplikat)!{Warna.RESET}")
            elif "NOT NULL constraint failed" in error_msg:
                print(f"{Warna.MERAH}❌ Kolom WAJIB tidak boleh kosong!{Warna.RESET}")
            else:
                print(f"{Warna.MERAH}❌ Error: {error_msg}{Warna.RESET}")
        except Exception as e:
            print(f"{Warna.MERAH}❌ Error: {str(e)}{Warna.RESET}")
    
    def _tampilkan_daftar(self, judul: str, items: list):
        """Tampilkan daftar dalam format tabel sederhana"""
        max_width = max(len(judul), max(len(item) for item in items) if items else 0)
        
        separator = "+" + "-" * (max_width + 2) + "+"
        
        print(f"{Warna.CYAN}{separator}{Warna.RESET}")
        print(f"| {Warna.BOLD}{judul:<{max_width}}{Warna.RESET} |")
        print(f"{Warna.CYAN}{separator}{Warna.RESET}")
        
        for item in items:
            print(f"| {item:<{max_width}} |")
        
        print(f"{Warna.CYAN}{separator}{Warna.RESET}")
        print(f"{Warna.DIM}{len(items)} item{Warna.RESET}")
    
    def _tampilkan_hasil(self, cursor):
        """Tampilkan hasil query dalam format tabel yang rapi"""
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        
        if not rows:
            print(f"{Warna.KUNING}(Tidak ada hasil){Warna.RESET}")
            return
        
        # Hitung lebar maksimal setiap kolom
        widths = []
        for i, col in enumerate(columns):
            max_width = len(str(col))
            for row in rows:
                cell_width = len(str(row[i]) if row[i] is not None else "NULL")
                max_width = max(max_width, cell_width)
            widths.append(max_width)
        
        # Buat garis pemisah
        separator = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
        
        # Tampilkan header
        print(f"{Warna.CYAN}{separator}{Warna.RESET}")
        header = "|"
        for i, col in enumerate(columns):
            header += f" {Warna.BOLD}{col:<{widths[i]}}{Warna.RESET} |"
        print(header)
        print(f"{Warna.CYAN}{separator}{Warna.RESET}")
        
        # Tampilkan data
        for row in rows:
            row_str = "|"
            for i, cell in enumerate(row):
                cell_val = str(cell) if cell is not None else "NULL"
                row_str += f" {cell_val:<{widths[i]}} |"
            print(row_str)
        
        print(f"{Warna.CYAN}{separator}{Warna.RESET}")
        print(f"{Warna.DIM}{len(rows)} baris{Warna.RESET}")


# Backward compatibility
def execute_sql(sql: str):
    """Fungsi lama untuk backward compatibility"""
    db = MBGDatabase()
    db.execute(sql)
    db.close()
