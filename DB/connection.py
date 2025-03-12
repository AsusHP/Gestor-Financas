import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv(override=True)

def get_supabase_client():
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    return create_client(url, key)
