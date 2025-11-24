# config.py
import os
from pathlib import Path

class Config:
    # Path to your service account credentials
    SERVICE_ACCOUNT_FILE = os.getenv(
        'SERVICE_ACCOUNT_FILE',
        './config/telos-email-service-credentials.json'
    )
    
    # Bot user that the service account will impersonate
    IMPERSONATE_USER = 'bot-service@telostravel.ai'
    
    # Group email to send from
    IMPERSONATE_USER = 'bot-service@telostravel.ai'
    SEND_FROM_EMAIL = 'rm.copilot@telostravel.ai'
    SEND_FROM_NAME = 'Telos RM CoPilot'  

    # Gmail API scopes
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    
    @classmethod
    def validate(cls):
        """Validate that all required config is present"""
        if not Path(cls.SERVICE_ACCOUNT_FILE).exists():
            raise FileNotFoundError(
                f"Service account file not found: {cls.SERVICE_ACCOUNT_FILE}"
            )
        return True