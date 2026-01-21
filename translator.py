"""
MBG Translator - Menerjemahkan bahasa MBG ke SQL
"""

import re

def translate(query: str) -> str:
    """Menerjemahkan query MBG ke SQL"""
    query = query.strip()
    query_upper = query.upper()
    
    # ======================
    # KELUAR / EXIT
    # ======================
    if query_upper.replace(";", "").strip() in ["KELUAR", "EXIT", "QUIT"]:
        return "__EXIT__"
    
    # ======================
    # BANTUAN / HELP
    # ======================
    if query_upper.replace(";", "").strip() in ["BANTUAN", "HELP", "?"]:
        return "__HELP__"
    
    # ======================
    # LIHAT DAPUR (SHOW DATABASES)
    # ======================
    if query_upper.startswith("LIHAT DAPUR"):
        return "SHOW DATABASES;"
    
    # ======================
    # LIHAT BAHAN (SHOW TABLES)
    # ======================
    if query_upper.startswith("LIHAT BAHAN"):
        return "SHOW TABLES;"
    
    # ======================
    # GUNAKAN DAPUR (USE database)
    # ======================
    if query_upper.startswith("GUNAKAN DAPUR"):
        nama_db = query.replace("GUNAKAN DAPUR", "").replace("gunakan dapur", "")
        nama_db = nama_db.replace(";", "").strip()
        return f"USE {nama_db};"
    
    # ======================
    # JELASKAN BAHAN (DESCRIBE table)
    # ======================
    if query_upper.startswith("JELASKAN BAHAN"):
        nama_tabel = query.replace("JELASKAN BAHAN", "").replace("jelaskan bahan", "")
        nama_tabel = nama_tabel.replace(";", "").strip()
        return f"DESCRIBE {nama_tabel};"
    
    # ======================
    # HAPUS DAPUR (DROP DATABASE)
    # ======================
    if query_upper.startswith("HAPUS DAPUR"):
        nama_db = query.replace("HAPUS DAPUR", "").replace("hapus dapur", "")
        nama_db = nama_db.replace(";", "").strip()
        return f"DROP DATABASE IF EXISTS {nama_db};"
    
    # ======================
    # HAPUS BAHAN (DROP TABLE)
    # ======================
    if query_upper.startswith("HAPUS BAHAN"):
        nama_tabel = query.replace("HAPUS BAHAN", "").replace("hapus bahan", "")
        nama_tabel = nama_tabel.replace(";", "").strip()
        return f"DROP TABLE IF EXISTS {nama_tabel};"
    
    # ======================
    # SEDIAKAN DAPUR (CREATE DATABASE)
    # ======================
    if query_upper.startswith("SEDIAKAN DAPUR"):
        nama_db = query.replace("SEDIAKAN DAPUR", "").replace("sediakan dapur", "")
        nama_db = nama_db.replace(";", "").strip()
        return f"CREATE DATABASE {nama_db};"
    
    # ======================
    # SEDIAKAN BAHAN (CREATE TABLE)
    # ======================
    if query_upper.startswith("SEDIAKAN BAHAN"):
        return translate_create_table(query)
    
    # ======================
    # MASAK (INSERT)
    # ======================
    if query_upper.startswith("MASAK"):
        return translate_insert(query)
    
    # ======================
    # SAJIKAN (SELECT)
    # ======================
    if query_upper.startswith("SAJIKAN"):
        return translate_select(query)
    
    # ======================
    # BUMBUI (UPDATE)
    # ======================
    if query_upper.startswith("BUMBUI"):
        return translate_update(query)
    
    # ======================
    # BUANG (DELETE)
    # ======================
    if query_upper.startswith("BUANG"):
        return translate_delete(query)
    
    # ======================
    # HITUNG (COUNT)
    # ======================
    if query_upper.startswith("HITUNG"):
        m = re.match(r"HITUNG\s+(\w+)\s*;", query, re.I)
        if m:
            table = m.group(1)
            return f"SELECT COUNT(*) AS jumlah FROM {table};"
        raise Exception("Syntax error pada HITUNG. Gunakan: HITUNG nama_tabel;")
    
    raise Exception(f"Query MBG tidak dikenali: {query[:50]}...")


def translate_create_table(query: str) -> str:
    """Translate SEDIAKAN BAHAN ke CREATE TABLE"""
    try:
        # Pisahkan header dan body
        match = re.match(r"SEDIAKAN BAHAN\s+(\w+)\s*\((.+)\)\s*;", query, re.I | re.DOTALL)
        if not match:
            raise Exception("Syntax error pada SEDIAKAN BAHAN")
        
        table_name = match.group(1)
        body = match.group(2)
        
        columns = []
        for line in body.split(","):
            line = line.strip()
            if not line:
                continue
                
            parts = line.split()
            if len(parts) < 2:
                continue
                
            nama = parts[0]
            tipe_mbg = " ".join(parts[1:]).upper()
            
            # Konversi tipe data MBG ke SQL (SQLite compatible)
            if "ANGKA" in tipe_mbg and "UTAMA" in tipe_mbg and "OTOMATIS" in tipe_mbg:
                sql_type = "INTEGER PRIMARY KEY AUTOINCREMENT"
            elif "ANGKA" in tipe_mbg and "UTAMA" in tipe_mbg:
                sql_type = "INTEGER PRIMARY KEY"
            elif "ANGKA" in tipe_mbg and "BESAR" in tipe_mbg:
                sql_type = "INTEGER"
            elif "ANGKA" in tipe_mbg and "KECIL" in tipe_mbg:
                sql_type = "INTEGER"
            elif "ANGKA" in tipe_mbg:
                sql_type = "INTEGER"
            elif "DESIMAL" in tipe_mbg:
                sql_type = "DECIMAL(10,2)"
            elif "TEKS" in tipe_mbg and "PANJANG" in tipe_mbg:
                sql_type = "TEXT"
            elif "TEKS" in tipe_mbg:
                # Cek apakah ada panjang yang ditentukan
                m = re.search(r"TEKS\s*\((\d+)\)", tipe_mbg)
                if m:
                    sql_type = f"VARCHAR({m.group(1)})"
                else:
                    sql_type = "VARCHAR(255)"
            elif "TANGGAL" in tipe_mbg and "WAKTU" in tipe_mbg:
                sql_type = "DATETIME"
            elif "TANGGAL" in tipe_mbg:
                sql_type = "DATE"
            elif "WAKTU" in tipe_mbg:
                sql_type = "TIME"
            elif "BOOLEAN" in tipe_mbg or "BENAR_SALAH" in tipe_mbg:
                sql_type = "BOOLEAN"
            else:
                sql_type = "VARCHAR(255)"
            
            # Cek constraint tambahan
            if "WAJIB" in tipe_mbg:
                sql_type += " NOT NULL"
            if "UNIK" in tipe_mbg:
                sql_type += " UNIQUE"
            
            columns.append(f"{nama} {sql_type}")
        
        kolom_sql = ", ".join(columns)
        return f"CREATE TABLE {table_name} ({kolom_sql});"
        
    except Exception as e:
        raise Exception(f"Error pada SEDIAKAN BAHAN: {str(e)}")


def translate_insert(query: str) -> str:
    """Translate MASAK ke INSERT"""
    try:
        m = re.match(r"MASAK\s+(\w+)\s+PAKAI\s+(.+);", query, re.I | re.DOTALL)
        if not m:
            raise Exception("Syntax error pada MASAK. Gunakan: MASAK tabel PAKAI kolom=nilai, ...;")
        
        table = m.group(1)
        pairs_str = m.group(2)
        
        columns = []
        values = []
        
        # Parse key=value pairs dengan memperhatikan string dalam quotes
        current_pair = ""
        in_quotes = False
        quote_char = None
        
        for char in pairs_str:
            if char in ["'", '"'] and not in_quotes:
                in_quotes = True
                quote_char = char
                current_pair += char
            elif char == quote_char and in_quotes:
                in_quotes = False
                quote_char = None
                current_pair += char
            elif char == "," and not in_quotes:
                if current_pair.strip():
                    k, v = current_pair.split("=", 1)
                    columns.append(k.strip())
                    values.append(v.strip())
                current_pair = ""
            else:
                current_pair += char
        
        # Jangan lupa pair terakhir
        if current_pair.strip():
            k, v = current_pair.split("=", 1)
            columns.append(k.strip())
            values.append(v.strip())
        
        col_sql = ", ".join(columns)
        val_sql = ", ".join(values)
        
        return f"INSERT INTO {table} ({col_sql}) VALUES ({val_sql});"
        
    except Exception as e:
        raise Exception(f"Error pada MASAK: {str(e)}")


def translate_select(query: str) -> str:
    """Translate SAJIKAN ke SELECT"""
    try:
        query_clean = query.replace(";", "").strip()
        query_upper = query_clean.upper()
        
        # SAJIKAN SEMUA tabel
        if "SAJIKAN SEMUA" in query_upper:
            parts = query_clean.split()
            table = parts[2] if len(parts) > 2 else ""
            
            if "YANG" in query_upper:
                idx = query_upper.index("YANG")
                table = query_clean[len("SAJIKAN SEMUA"):idx].strip()
                condition = query_clean[idx + 4:].strip()
                return f"SELECT * FROM {table} WHERE {condition};"
            else:
                return f"SELECT * FROM {table};"
        
        # SAJIKAN kolom1, kolom2 DARI tabel
        if "DARI" in query_upper:
            m = re.match(r"SAJIKAN\s+(.+?)\s+DARI\s+(\w+)(?:\s+YANG\s+(.+))?", query_clean, re.I)
            if m:
                columns = m.group(1).strip()
                table = m.group(2).strip()
                condition = m.group(3)
                
                if condition:
                    return f"SELECT {columns} FROM {table} WHERE {condition};"
                else:
                    return f"SELECT {columns} FROM {table};"
        
        # SAJIKAN tabel (simple)
        if "YANG" in query_upper:
            m = re.match(r"SAJIKAN\s+(\w+)\s+YANG\s+(.+)", query_clean, re.I)
            if m:
                table = m.group(1)
                condition = m.group(2)
                return f"SELECT * FROM {table} WHERE {condition};"
        
        # SAJIKAN tabel (paling simple)
        table = query_clean.replace("SAJIKAN", "").replace("sajikan", "").strip()
        return f"SELECT * FROM {table};"
        
    except Exception as e:
        raise Exception(f"Error pada SAJIKAN: {str(e)}")


def translate_update(query: str) -> str:
    """Translate BUMBUI ke UPDATE"""
    try:
        m = re.match(r"BUMBUI\s+(\w+)\s+JADI\s+(.+?)\s+YANG\s+(.+);", query, re.I | re.DOTALL)
        if not m:
            raise Exception("Syntax error pada BUMBUI. Gunakan: BUMBUI tabel JADI kolom=nilai YANG kondisi;")
        
        table = m.group(1)
        set_part = m.group(2).strip()
        condition = m.group(3).strip()
        
        return f"UPDATE {table} SET {set_part} WHERE {condition};"
        
    except Exception as e:
        raise Exception(f"Error pada BUMBUI: {str(e)}")


def translate_delete(query: str) -> str:
    """Translate BUANG ke DELETE"""
    try:
        # BUANG SEMUA tabel (DELETE all rows)
        if "BUANG SEMUA" in query.upper():
            m = re.match(r"BUANG SEMUA\s+(\w+)\s*;", query, re.I)
            if m:
                table = m.group(1)
                return f"DELETE FROM {table};"
            raise Exception("Syntax error pada BUANG SEMUA")
        
        # BUANG tabel YANG kondisi
        m = re.match(r"BUANG\s+(\w+)\s+YANG\s+(.+);", query, re.I | re.DOTALL)
        if m:
            table = m.group(1)
            condition = m.group(2).strip()
            return f"DELETE FROM {table} WHERE {condition};"
        
        raise Exception("Syntax error pada BUANG. Gunakan: BUANG tabel YANG kondisi;")
        
    except Exception as e:
        raise Exception(f"Error pada BUANG: {str(e)}")
