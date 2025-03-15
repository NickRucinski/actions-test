import base64
import hashlib
import secrets

from supabase.client import Client, ClientOptions
from werkzeug.local import LocalProxy
from flask import g, session, current_app

def get_session_storage():
    from app import FlaskSessionStorage
    return FlaskSessionStorage()

def get_db() -> Client:
    if "db" not in g:
        g.db = Client(
            current_app.config["SUPABASE_URL"],
            current_app.config["SUPABASE_KEY"],
            options=ClientOptions(
                storage=get_session_storage(),
                flow_type="pkce"
            ),
        )
        return g.db

client: Client = LocalProxy(get_db)

def generate_code_verifier():
   """Generate a secure random code verifier (43-128 characters)."""
   return secrets.token_urlsafe(64)  # Secure random 64-character string

def generate_code_challenge(verifier):
   """Create a SHA256 challenge from the code verifier (RFC 7636)."""
   sha256_hash = hashlib.sha256(verifier.encode()).digest()
   challenge = base64.urlsafe_b64encode(sha256_hash).decode().rstrip("=")  # Remove '=' padding
   return challenge

def log_event(event):
    """
    Logs an event by inserting it into the 'Logs' table in the database.

    Args:
        event (dict): A dictionary containing event details. Expected keys are:
            - 'event': The name of the event.
            - 'time_lapse': A textual description of the event.
            - 'metadata': Additional data associated with the event.

    Raises:
        Exception: If there is an error inserting the log into the database.
    """

    try:
        response = client.table("logs").insert(event).execute()

        # if response.error:
        #     raise Exception(f"Error logging event: {response.error}")
        # else:
        print(f"LOGGED EVENT: {event}")
    
    except Exception as e:
        print(f"Exception occurred while logging event: {e}")
        raise e
    
def log_suggestion(suggestion):
    """
    Logs an event by inserting it into the 'Logs' table in the database.

    Args:
        event (dict): A dictionary containing event details. Expected keys are:
            - 'event': The name of the event.
            - 'time_lapse': A textual description of the event.
            - 'metadata': Additional data associated with the event.

    Raises:
        Exception: If there is an error inserting the log into the database.
    """

    try:
        response = client.table("suggestions").insert(suggestion).execute()

        if response.data:
            inserted_suggestion = response.data[0]
            suggestion['id'] = inserted_suggestion['id'] 

            print(f"LOGGED SUGGESTION: {suggestion}")
            return suggestion 
        else:
            raise Exception("No data returned from the insert operation")
    
    except Exception as e:
        print(f"Exception occurred while logging event: {e}")
        raise e


def get_all_logs():
    """
    Retrieves all logs stored in the 'Logs' table.

    Returns:
        list: A list of dictionaries containing all logs.

    Raises:
        Exception: If there is an error fetching the logs from the database.
    """
    try:
        response = client.table("logs").select("*").execute()
        
        # if response.error:
        #     raise Exception(f"Error fetching logs: {response.error}")
        
        return response.data
    
    except Exception as e:
        print(f"Exception occurred while fetching logs: {e}")
        raise e


def get_logs_by_user(user_id):
    """
    Retrieves all logs associated with a specific user.

    Args:
        user_id (str): The ID of the user whose logs are to be fetched.

    Returns:
        list: A list of dictionaries containing logs for the specified user.

    Raises:
        Exception: If there is an error fetching logs for the user.
    """
    try:
        # This will not work right now. Need to decide if we want to store user id in schema or data
        response = client.table("logs").select("*").eq("data->>user_id", str(user_id)).execute()

        # if response.error:
        #     raise Exception(f"Error fetching logs for user {user_id}: {response.error}")
        
        return response.data

    except Exception as e:
        print(f"Exception occurred while fetching logs for user {user_id}: {e}")
        raise e