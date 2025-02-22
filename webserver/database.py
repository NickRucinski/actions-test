import os
from supabase import create_client, Client
from dotenv import load_dotenv
import bcrypt

load_dotenv()

SUPABASE_URL: str = os.getenv('SUPABASE_URL')
SUPABASE_KEY: str = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY. Check your .env file.")

client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def log_event(event):
    """
    Creates a logs and inserts it into the database
    """
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
    """
    Get all logs ever created
    """
    try:
        response = client.table("Logs").select("*").execute()
        
        if response.error:
            raise Exception(f"Error fetching logs: {response.error}")
        
        return response.data
    
    except Exception as e:
        print(f"Exception occurred while fetching logs: {e}")
        raise e
    
def get_logs_by_user(user_id):
    """
    Get all logs for a specific user
    """
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
    """
    Fetch a single user by ID.
    """
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
    
def create_user(first_name, last_name, email, password):
    """
    Create a user in the database
    """
    try:
        existing_user = client.table("Users").select("id").eq("email", email).execute()
        if existing_user.data:
            return {"error": "Email already exists"}, 400
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        response = client.table("Users").insert({
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": hashed_password
        }).execute()

        if response.error:
            raise Exception(f"Error creating user: {response.error}")

        return response.data[0], 201
    
    except Exception as e:
        print(f"Exception while creating user: {e}")
        return {"error": "Internal server error"}, 500