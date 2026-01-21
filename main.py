import sys
from translator import translate
from db import execute_sql

def main():
    if len(sys.argv) < 2:
        print("❌ Pakai: python main.py <file.mbg>")
        return

    with open(sys.argv[1], "r") as f:
        mbg_query = f.read()

    sql = translate(mbg_query)

    print("🍽️ SQL hasil terjemahan:")
    print(sql)

    execute_sql(sql)

if __name__ == "__main__":
    main()
