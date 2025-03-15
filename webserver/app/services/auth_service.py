from flask import session
from app.controllers.database import client

def login():
    session.clear()  # Ensure fresh session
    res = client.auth.sign_in_with_oauth(
        {
            "provider": "github",
            "options": {
                "redirect_to": "https://ai.nickrucinski.com/auth/callback"
            },
        }
    )
    return res

def callback(code: str):
    """Handles OAuth callback and exchanges code for a session."""
    try:
        res = client.auth.exchange_code_for_session({"auth_code": code})
        print("Authentication successful:", res)
        return res
    except Exception as e:
        return {"error": f"Authentication failed: {str(e)}"}, 500
