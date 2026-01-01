import shutil
import datetime
import os

def create_backup():
    source = "shield_secure.db"
    if os.path.exists(source):
        # समय अनुसार फाइलको नाम राख्ने (Backup_2026-01-01.bak)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_name = f"backup_shield_{timestamp}.bak"
        
        # फाइल कपि गर्ने
        shutil.copy2(source, backup_name)
        print(f"✅ ब्याकअप सफल! फाइलको नाम: {backup_name}")
    else:
        print("❌ ब्याकअप असफल: डाटाबेस फाइल भेटिएन।")

def restore_backup(backup_file):
    if os.path.exists(backup_file):
        shutil.copy2(backup_file, "shield_secure.db")
        print(f"🔄 डाटा रिस्टोर सफल! {backup_file} अहिले प्रयोगमा छ।")
    else:
        print("❌ फाइल भेटिएन!")

# रन गरौँ
print("--- SHIELD BACKUP SYSTEM ---")
create_backup()
