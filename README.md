# Klea Document Exporter

This script exports all documents from a given client companies into a structured ZIP file, organizing documents by company.

## Prerequisites

1. **Python Installation**
   - Download and install Python 3.11 or higher from [python.org](https://python.org)
   - During installation on Windows, make sure to check "Add Python to PATH"
   - On macOS, use `python3` instead of `python` in commands

2. **Verify Python Installation**
   ```bash
   python --version  # Windows
   python3 --version  # macOS/Linux
   ```

## Setup

1. **Clone the Repository**
   ```bash
   git clone [your-repository-url]
   cd klea-export-documents
   ```

2. **Create Virtual Environment** (recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   - Create a `.env` file in the project root
   - Add the following variables:
   ```env
   CLIENT=your_client_name
   DOMAIN=your_domain
   CLIENT_ID=your_client_id
   CLIENT_SECRET=your_client_secret
   AUDIENCE=api.legalstudio.be/api/v1
   ```

## Usage

1. **Activate Virtual Environment** (if not already activated)
   ```bash
   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

2. **Run the Script**
   ```bash
   # Windows
   python document_exporter.py

   # macOS/Linux
   python3 document_exporter.py
   ```

3. **Output**
   - The script creates two directories:
     - `exports/`: Contains the ZIP files with documents
     - `logs/`: Contains detailed logs of the export process
   - Files are named with timestamps: `{client}_documents_{timestamp}.zip`

## Output Structure 