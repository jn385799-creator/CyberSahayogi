import os
import time
import shutil
from datetime import datetime, timedelta

VAULT_DIR = "encrypted_vault"
BACKUP_DIR = "backups"

if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

def run_maintenance():
    print(f"[{datetime.now()}] 🛠️ मर्मत कार्य सुरु भयो...")
    
    # १. ब्याकअप लिने
    backup_file = f"{BACKUP_DIR}/db_backup_{datetime.now().strftime('%Y%m%d')}.bak"
    shutil.copy2("shield_secure.db", backup_file)
    print("✅ डाटाबेस ब्याकअप सुरक्षित गरियो।")

    # २. पुराना डकुमेन्ट सफा गर्ने (३० दिन भन्दा पुराना)
    now = time.time()
    for f in os.listdir(VAULT_DIR):
        f_path = os.path.join(VAULT_DIR, f)
        # यदि फाइल ३० दिन (३० * २४ * ६० * ६० सेकेन्ड) भन्दा पुरानो छ भने
        if os.stat(f_path).st_mtime < now - (30 * 86400):
            os.remove(f_path)
            print(f"🗑️ पुरानो डकुमेन्ट डिलिट गरियो: {f}")

if __name__ == "__main__":
    run_maintenance()
