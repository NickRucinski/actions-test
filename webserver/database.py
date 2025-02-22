import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL: str = os.getenv('SUPABASE_URL')
SUPABASE_KEY: str = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY. Check your .env file.")

client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def log_event(event):
    log_data = {
        "event": event.get("event"),
        "text": event.get("text"),
        "data": event.get("data")
    }

    try:
        response = client.table("Logs").insert(log_data).execute()

        if response.error:
            raise Exception(f"Error logging event: {response.error}")
        else:
            print(f"LOGGED EVENT: {event}")
    
    except Exception as e:
        print(f"Exception occurred while logging event: {e}")
        raise e
    
def get_all_logs():
    try:
        response = client.table("Logs").select("*").execute()
        
        if response.error:
            raise Exception(f"Error fetching logs: {response.error}")
        
        return response.data
    
    except Exception as e:
        print(f"Exception occurred while fetching logs: {e}")
        raise e
    
def get_logs_by_user(user_id):
    try:
        # This will not work right now. Need to decide if we want to store user id in schema or data
        response = client.table("Logs").select("*").eq("data->>user_id", str(user_id)).execute()

        if response.error:
            raise Exception(f"Error fetching logs for user {user_id}: {response.error}")
        
        return response.data
    
    except Exception as e:
        print(f"Exception occurred while fetching logs for user {user_id}: {e}")
        raise e
    
def get_user_by_id(user_id):
    try:
        response = client.table("Users").select("*").eq("id", user_id).execute()

        if response.error:
            raise Exception(f"Error fetching user {user_id}: {response.error}")

        if not response.data:
            return None
        
        return response.data[0]
    
    except Exception as e:
        print(f"Exception occurred while fetching user {user_id}: {e}")
        raise e