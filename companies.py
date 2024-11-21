from typing import Optional
import requests
from auth import get_access_token

def get_companies() -> Optional[dict]:
    """
    Get list of companies from the Legal Studio API
    
    Returns:
        dict: JSON response with companies data if successful, None if failed
    """
    token = get_access_token()
    if not token:
        print("Failed to obtain access token")
        return None
        
    api_url = "https://app.legalstudio.be/api/v1/companies"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to get companies: {str(e)}")
        return None

if __name__ == "__main__":
    companies = get_companies()
    if companies:
        print("\nCompanies:")
        print(companies) 