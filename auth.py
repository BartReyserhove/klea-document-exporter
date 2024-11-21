import os
from dotenv import load_dotenv
import requests
from typing import Optional

# Load environment variables from .env file
load_dotenv()

def get_access_token() -> Optional[str]:
    """
    Get access token from the API using credentials stored in environment variables.
    
    Returns:
        str: Access token if successful, None if failed
    """
    auth_url = os.getenv('API_AUTH_URL')
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    audience = os.getenv('AUDIENCE')
    
    # Verify all required environment variables are present
    if not all([auth_url, client_id, client_secret, audience]): 
        raise ValueError("Missing required environment variables. Please check your .env file.")
    
    # Prepare the authentication payload
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials',
        'audience': audience
    }
    
    try:              
        response = requests.post(auth_url, data=payload)        
        
        response.raise_for_status()  # Raise an exception for bad status codes
        
        token_data = response.json()
        return token_data.get('access_token')
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to get access token: {str(e)}")
        return None

if __name__ == "__main__":
    # Test the authentication
    token = get_access_token()
    if token:
        print("Successfully obtained access token")
        print(f"Token: {token}")
    else:
        print("Failed to obtain access token") 