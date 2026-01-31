from supabase import create_client
from datetime import datetime

# ---------------- CONFIG ----------------
# 🔴 PUT YOUR SUPABASE DETAILS HERE
SUPABASE_URL = "https://togvkxlblwsrvopvvcgt.supabase.co"
SUPABASE_KEY = "sb_publishable_iWx5opdybTCoT1bqP0RAxA_n_N2A-Yo"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

TABLE_NAME = "attendance"

# ---------------- FUNCTIONS ----------------
def already_marked_today(name, date):
    response = supabase.table(TABLE_NAME).select("*") \
        .eq("name", name).eq("date", date).execute()
    return len(response.data) > 0


def mark_attendance(name):
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    if already_marked_today(name, date):
        return False

    supabase.table(TABLE_NAME).insert({
        "name": name,
        "date": date,
        "time": time
    }).execute()

    return True
