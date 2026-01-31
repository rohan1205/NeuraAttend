from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client
from datetime import datetime

SUPABASE_URL = "https://togvkxlblwsrvopvvcgt.supabase.co"
SUPABASE_KEY = "sb_publishable_iWx5opdybTCoT1bqP0RAxA_n_N2A-Yo"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class FramePayload(BaseModel):
    frame: str
    timestamp: str

@app.get("/")
def root():
    return {"status": "Backend running"}

@app.post("/mark-attendance")
def mark_attendance(payload: FramePayload):
    name = "rohan"
    today = datetime.now().date().isoformat()

    existing = (
        supabase.table("attendance")
        .select("id")
        .eq("name", name)
        .eq("date", today)
        .execute()
    )

    if not existing.data:
        supabase.table("attendance").insert({
            "name": name,
            "date": today,
            "time": datetime.now().strftime("%H:%M:%S")
        }).execute()

    return {"success": True, "marked": [name]}

@app.get("/attendance")
def get_attendance():
    return supabase.table("attendance").select("*").execute().data
