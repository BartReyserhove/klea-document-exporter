from typing import Optional, List
import requests
from companies import get_companies
from auth import get_access_token
import os
import zipfile
from datetime import datetime
import logging
from dotenv import load_dotenv

def setup_logging():
    """Setup logging to both file and console"""
    # Create logs directory if it doesn't exist
    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(logs_dir, f"document_export_{timestamp}.log")
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # Setup file handler
    file_handler = logging.FileHandler(log_filename)
    file_handler.setFormatter(formatter)
    
    # Setup console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Setup logger
    logger = logging.getLogger('document_exporter')
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def get_company_documents(company_id: int, token: str) -> Optional[dict]:
    """
    Get list of documents for a specific company
    """
    api_url = f"https://app.legalstudio.be/api/v1/companies/{company_id}/documents"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        documents = response.json()
        
        if not documents:  # Empty list is a valid response
            return []
        return documents
    except requests.exceptions.RequestException as e:
        print(f"Failed to get documents for company {company_id}: {str(e)}")
        return None

def get_document_content(company_id: int, document_id: int, token: str) -> Optional[tuple[bytes, str]]:
    """
    Download the content of a specific document
    Returns:
        tuple: (file_content, filename) if successful, None if failed
    """
    api_url = f"https://app.legalstudio.be/api/v1/companies/{company_id}/documents/{document_id}"
    headers = {
        'Authorization': f'Bearer {token}',
    }
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        if 'Content' in data and 'Filename' in data:
            import base64
            content = base64.b64decode(data['Content'])
            return (content, data['Filename'])
        else:
            print(f"Missing content or filename in document {document_id}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Failed to download document {document_id}: {str(e)}")
        return None

def export_documents():
    # Load environment variables
    load_dotenv()
    client = os.getenv('CLIENT', 'unknown')
    
    logger = setup_logging()
    logger.info(f"Starting document export for client: {client}")
    
    # Get access token
    token = get_access_token()
    if not token:
        logger.error("Failed to obtain access token")
        return
        
    # Get companies
    companies = get_companies()
    if not companies:
        logger.error("Failed to get companies")
        return
    
    # Create exports directory
    exports_dir = "exports"
    os.makedirs(exports_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = os.path.join(exports_dir, f"{client}_documents_{timestamp}.zip")
    
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        for company in companies:
            company_id = company['CompanyId']
            company_name = company['CompanyName']
            logger.info(f"Processing company: {company_name}")
            
            documents = get_company_documents(company_id, token)
            if documents is None:  # Error case
                logger.warning(f"Skipping company {company_name} - couldn't fetch documents")
                continue
            
            if not documents:  # Empty list case
                logger.info(f"Company {company_name} has no documents")
                continue
                
            logger.info(f"Found {len(documents)} documents for {company_name}")
            
            # Only create company folder in zip if we have documents
            safe_company_name = "".join(c for c in company_name if c.isalnum() or c in (' ', '-', '_')).strip()
            
            for doc in documents:
                doc_id = doc['Id']
                logger.info(f"Downloading document {doc_id}")
                
                result = get_document_content(company_id, doc_id, token)
                if result:
                    content, filename = result
                    name, ext = os.path.splitext(filename)
                    filename_with_id = f"{name}_{doc_id}{ext}"
                    zip_path = f"{safe_company_name}/{filename_with_id}"
                    
                    zip_file.writestr(zip_path, content)
                    logger.info(f"Saved: {zip_path}")
                else:
                    logger.error(f"Failed to download document {doc_id}")

if __name__ == "__main__":
    export_documents() 