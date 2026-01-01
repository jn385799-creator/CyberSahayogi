import sqlite3
import datetime

def init_recovery_db():
    conn = sqlite3.connect("shield_secure.db")
    cursor = conn.cursor()
    # रिकभरी केसहरूको लागि नयाँ टेबल
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS RecoveryCases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            victim_name TEXT,
            platform TEXT,
            lost_access_reason TEXT,
            status TEXT DEFAULT 'Pending',
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_case(name, platform, reason):
    conn = sqlite3.connect("shield_secure.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO RecoveryCases (victim_name, platform, lost_access_reason, created_at) VALUES (?, ?, ?, ?)",
                   (name, platform, reason, str(datetime.datetime.now())))
    conn.commit()
    conn.close()
    print(f"✅ {name} को लागि {platform} रिकभरी केस दर्ता भयो।")

init_recovery_db()
add_case("Ram Kumar", "Facebook", "Hacked - Email changed")
