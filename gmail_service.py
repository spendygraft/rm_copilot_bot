# gmail_service.py
import base64
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional, List
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.utils import formataddr

from config import Config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GmailService:
    """
    Gmail service for sending emails using service account with domain-wide delegation.
    """
    
    def __init__(self):
        """Initialize the Gmail service"""
        Config.validate()
        self.service = self._create_service()
        self.default_sender = Config.SEND_FROM_EMAIL
        self.default_sender_name = "Telos RM CoPilot"  # Add this line
        logger.info(f"Gmail service initialized. Impersonating: {Config.IMPERSONATE_USER}")
    
    def _create_service(self):
        """Create authenticated Gmail API service"""
        try:
            # Load service account credentials
            credentials = service_account.Credentials.from_service_account_file(
                Config.SERVICE_ACCOUNT_FILE,
                scopes=Config.SCOPES
            )
            
            # Create delegated credentials (impersonate the bot user)
            delegated_credentials = credentials.with_subject(Config.IMPERSONATE_USER)
            
            # Build the Gmail service
            service = build('gmail', 'v1', credentials=delegated_credentials)
            
            logger.info("Gmail service created successfully")
            return service
            
        except Exception as e:
            logger.error(f"Failed to create Gmail service: {e}")
            raise
    
    def _create_message(
        self,
        sender: str,
        to: str,
        subject: str,
        body_text: str,
        body_html: Optional[str] = None,
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
        attachments: Optional[List[str]] = None,
        sender_name: Optional[str] = None
    ) -> dict:
        """
        Create an email message.
        
        Args:
            sender: Email address to send from
            to: Recipient email address(es) - comma-separated for multiple
            subject: Email subject
            body_text: Plain text body
            body_html: Optional HTML body
            cc: Optional CC recipients - comma-separated
            bcc: Optional BCC recipients - comma-separated
            attachments: Optional list of file paths to attach
        `   sender_name: Optional friendly name for sender (e.g., "Telos RM CoPilot")
        Returns:
            Dict containing the encoded message
        """
        # Create message container
        if body_html or attachments:
            message = MIMEMultipart('mixed')
            
            # Create the body part
            if body_html:
                body_part = MIMEMultipart('alternative')
                body_part.attach(MIMEText(body_text, 'plain'))
                body_part.attach(MIMEText(body_html, 'html'))
                message.attach(body_part)
            else:
                message.attach(MIMEText(body_text, 'plain'))
        else:
            message = MIMEText(body_text)
        
        # Set headers
        message['to'] = to
        # Format the From header with friendly name
        if sender_name:
            # Use formataddr to properly format "Display Name <email@domain.com>"
            message['from'] = formataddr((sender_name, sender))
        else:
            message['from'] = sender
        message['subject'] = subject
        
        if cc:
            message['cc'] = cc
        if bcc:
            message['bcc'] = bcc
        
        # Add attachments if any
        if attachments:
            for file_path in attachments:
                self._attach_file(message, file_path)
        
        # Encode the message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        
        return {'raw': raw_message}
    
    def _attach_file(self, message: MIMEMultipart, file_path: str):
        """Attach a file to the message"""
        try:
            path = Path(file_path)
            if not path.exists():
                logger.warning(f"Attachment not found: {file_path}")
                return
            
            with open(file_path, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
            
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename={path.name}'
            )
            message.attach(part)
            logger.debug(f"Attached file: {path.name}")
            
        except Exception as e:
            logger.error(f"Failed to attach file {file_path}: {e}")
            raise
    
    def send_email(
        self,
        to: str,
        subject: str,
        body_text: str,
        body_html: Optional[str] = None,
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
        sender: Optional[str] = None,
        sender_name: Optional[str] = None,
        attachments: Optional[List[str]] = None
    ) -> dict:
        """
        Send an email.
        
        Args:
            to: Recipient email(s) - comma-separated for multiple
            subject: Email subject
            body_text: Plain text body
            body_html: Optional HTML body
            cc: Optional CC recipients
            bcc: Optional BCC recipients
            sender: Optional custom sender (defaults to rm.copilot@telostravel.ai)
            sender_name: Optional friendly name (defaults to "Telos RM CoPilot")
            attachments: Optional list of file paths to attach
        
        Returns:
            Dict with message ID and other info
        
        Raises:
            HttpError: If the API request fails
        """
        sender = sender or self.default_sender
        sender_name = sender_name or self.default_sender_name
        
        try:
            logger.info(f"Sending email to: {to}, subject: {subject}")
            
            # Create the message
            message = self._create_message(
                sender=sender,
                to=to,
                subject=subject,
                body_text=body_text,
                body_html=body_html,
                cc=cc,
                bcc=bcc,
                attachments=attachments,
                sender_name=sender_name  # Pass the friendly name
            )
            
            # Send the message
            sent_message = self.service.users().messages().send(
                userId='me',
                body=message
            ).execute()
            
            logger.info(f"✅ Email sent successfully! Message ID: {sent_message['id']}")
            return sent_message
            
        except HttpError as error:
            logger.error(f"❌ Failed to send email: {error}")
            raise
        except Exception as e:
            logger.error(f"❌ Unexpected error sending email: {e}")
            raise


# Convenience singleton instance
_gmail_service_instance = None

def get_gmail_service() -> GmailService:
    """Get or create the Gmail service singleton"""
    global _gmail_service_instance
    if _gmail_service_instance is None:
        _gmail_service_instance = GmailService()
    return _gmail_service_instance