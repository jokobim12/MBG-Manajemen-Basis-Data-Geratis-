# MBG - Manajemen Basis Geratis

Sistem database sederhana dengan bahasa Indonesia. Cocok untuk belajar konsep database.

## Apa itu MBG?

MBG adalah **translator/penerjemah** yang mengubah perintah berbahasa Indonesia menjadi query SQL, kemudian dieksekusi ke database **SQLite**.

**MBG bukan database engine baru**, melainkan:

- **Frontend/Interface** berbahasa Indonesia
- **Backend** menggunakan SQLite (database open-source dari [sqlite.org](https://sqlite.org))
- Ditulis dengan **Python 3**

### Teknologi yang Digunakan

| Komponen           | Teknologi | Lisensi       |
| ------------------ | --------- | ------------- |
| Database Engine    | SQLite 3  | Public Domain |
| Bahasa Pemrograman | Python 3  | PSF License   |
| MBG Translator     | Original  | MIT License   |

### Cara Kerja

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Perintah MBG   │ --> │   Translator    │ --> │     SQLite      │
│  (Bhs Indonesia)│     │  (MBG → SQL)    │     │   (Database)    │
└─────────────────┘     └─────────────────┘     └─────────────────┘

Contoh:
  SAJIKAN siswa;  -->  SELECT * FROM siswa;  -->  [hasil query]
```

### Mengapa Dibuat?

Dibuat untuk fun aja. Iseng-iseng sekalian menambah project dari yang sebelumnya saya pernah membuat BanjarScript

## Instalasi

### Linux / macOS (Satu Perintah)

```bash
curl -sSL https://raw.githubusercontent.com/jokobim12/MBG-Manajemen-Basis-data-geratis-/main/remote-install.sh | sudo bash
```

Setelah itu, jalankan `mbg` dari terminal manapun.

### Uninstall

```bash
sudo rm -rf /opt/mbg /usr/local/bin/mbg
```

### Windows

Untuk Windows, download file-file berikut dan jalankan dengan Python:

- `mbg.py`
- `translator.py`
- `db.py`
- `bantuan.py`

```powershell
python mbg.py
```

## Cara Pakai

```
mbg> SEDIAKAN DAPUR sekolah;
✅ Dapur "sekolah" berhasil disediakan!

mbg> GUNAKAN DAPUR sekolah;
✅ Dapur berubah ke: sekolah

mbg> SEDIAKAN BAHAN siswa (
  -> id ANGKA UTAMA OTOMATIS,
  -> nama TEKS WAJIB,
  -> umur ANGKA
  -> );
✅ Bahan "siswa" berhasil disediakan!

mbg> MASAK siswa PAKAI nama='Budi', umur=17;
✅ 1 resep berhasil dimasak!

mbg> SAJIKAN siswa;
+----+------+------+
| id | nama | umur |
+----+------+------+
| 1  | Budi | 17   |
+----+------+------+
```

## Daftar Perintah

| Perintah                          | Fungsi               |
| --------------------------------- | -------------------- |
| `LIHAT DAPUR;`                    | Daftar database      |
| `SEDIAKAN DAPUR nama;`            | Buat database        |
| `GUNAKAN DAPUR nama;`             | Pilih database       |
| `HAPUS DAPUR nama;`               | Hapus database       |
| `LIHAT BAHAN;`                    | Daftar tabel         |
| `SEDIAKAN BAHAN nama (...);`      | Buat tabel           |
| `JELASKAN BAHAN nama;`            | Lihat struktur       |
| `HAPUS BAHAN nama;`               | Hapus tabel          |
| `MASAK tabel PAKAI ...;`          | Insert data          |
| `SAJIKAN tabel;`                  | Select semua         |
| `SAJIKAN tabel YANG ...;`         | Select dengan filter |
| `BUMBUI tabel JADI ... YANG ...;` | Update data          |
| `BUANG tabel YANG ...;`           | Delete data          |
| `HITUNG tabel;`                   | Count data           |
| `BANTUAN;`                        | Tampilkan bantuan    |
| `KELUAR;`                         | Keluar               |

## Tipe Data

| MBG                    | Penjelasan              |
| ---------------------- | ----------------------- |
| `ANGKA`                | Bilangan bulat          |
| `ANGKA UTAMA`          | Primary key             |
| `ANGKA UTAMA OTOMATIS` | Auto increment          |
| `TEKS`                 | Teks (max 255 karakter) |
| `TEKS PANJANG`         | Teks panjang            |
| `TANGGAL`              | Tanggal                 |
| `WAKTU`                | Waktu                   |

## Modifier

| Modifier | Fungsi                        |
| -------- | ----------------------------- |
| `WAJIB`  | Tidak boleh kosong (NOT NULL) |
| `UNIK`   | Harus berbeda (UNIQUE)        |

## Struktur File

```
mbg/
├── mbg           # Launcher (Linux/macOS)
├── mbg.py        # Program utama
├── translator.py # Penerjemah MBG → SQL
├── db.py         # Handler database SQLite
├── bantuan.py    # Sistem bantuan
└── dapur/        # Folder penyimpanan database
    └── *.mbg     # File database
```

## Lisensi

MIT License - Bebas digunakan dan dimodifikasi.
