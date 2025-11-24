# Telos Email Service Bot

Automated email sending service for Telos Travel AI using Gmail API with service account authentication.

## Overview

This bot allows automated email sending through Gmail using a service account with domain-wide delegation. It sends emails as `rm.copilot@telostravel.ai` by impersonating `bot-service@telostravel.ai`.

## Prerequisites

- Python 3.7 or higher
- Google Workspace (formerly G Suite) account with admin access
- Service account with domain-wide delegation configured
- Service account credentials JSON file

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd c:\code\telos-email-service-bot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### 1. Service Account Setup

Ensure you have:
- A Google Cloud service account created
- Domain-wide delegation enabled for the service account
- The service account has the scope: `https://www.googleapis.com/auth/gmail.send`
- Service account credentials JSON file downloaded

### 2. Credentials File

Place your service account credentials file at:
```
./config/telos-email-service-credentials.json
```

Or set a custom path using the environment variable:
```bash
set SERVICE_ACCOUNT_FILE=path\to\your\credentials.json
```

### 3. Configuration Settings

Edit [config.py](config.py) if you need to change:
- `IMPERSONATE_USER`: The bot user account (default: `bot-service@telostravel.ai`)
- `SEND_FROM_EMAIL`: The email address to send from (default: `rm.copilot@telostravel.ai`)
- `SCOPES`: Gmail API scopes (default: send-only access)

## Usage

### Running Tests

Run all test scenarios:
```bash
python test_bot_email.py
```

This will run three tests:
1. Simple plain text email
2. HTML email with styling
3. Email with CC recipients

### Using in Your Code

```python
from gmail_service import get_gmail_service

# Get the Gmail service instance
gmail = get_gmail_service()

# Send a simple email
gmail.send_email(
    to='recipient@example.com',
    subject='Test Email',
    body_text='This is a test email.'
)

# Send an HTML email
gmail.send_email(
    to='recipient@example.com',
    subject='HTML Email',
    body_text='Plain text fallback',
    body_html='<h1>HTML Content</h1><p>Rich formatted email</p>'
)

# Send with CC, BCC, and attachments
gmail.send_email(
    to='recipient@example.com',
    subject='Email with Attachments',
    body_text='Please see attached files.',
    cc='cc@example.com',
    bcc='bcc@example.com',
    attachments=['path/to/file1.pdf', 'path/to/file2.xlsx']
)
```

## Project Structure

```
telos-email-service-bot/
├── config/
│   └── telos-email-service-credentials.json  # Service account credentials
├── config.py                                  # Configuration settings
├── gmail_service.py                           # Main Gmail service class
├── test_bot_email.py                          # Test suite
├── simple_test.py                             # Simple non-interactive test
├── requirements.txt                           # Python dependencies
└── README.md                                  # This file
```

## API Reference

### GmailService Class

#### `send_email()`

Send an email via Gmail API.

**Parameters:**
- `to` (str): Recipient email(s) - comma-separated for multiple
- `subject` (str): Email subject
- `body_text` (str): Plain text body
- `body_html` (str, optional): HTML body
- `cc` (str, optional): CC recipients - comma-separated
- `bcc` (str, optional): BCC recipients - comma-separated
- `sender` (str, optional): Custom sender (defaults to `rm.copilot@telostravel.ai`)
- `attachments` (List[str], optional): List of file paths to attach

**Returns:**
- `dict`: Response containing message ID and thread ID

**Raises:**
- `HttpError`: If the Gmail API request fails
- `FileNotFoundError`: If attachment file not found

## Use Cases

This email service is designed for:
- Customer notifications
- Pricing updates
- System alerts
- Automated reporting
- Workflow notifications

## Security Notes

- Service account credentials are sensitive - never commit to version control
- The service account uses domain-wide delegation (requires admin setup)
- Scoped to send-only access (no read or delete permissions)
- All emails are sent as the configured group email address

## Troubleshooting

### ModuleNotFoundError: No module named 'google.oauth2'

Install the required dependencies:
```bash
pip install -r requirements.txt
```

### FileNotFoundError: Service account file not found

Ensure the credentials file exists at the configured path:
```bash
# Check if file exists
dir config\telos-email-service-credentials.json

# Or set custom path
set SERVICE_ACCOUNT_FILE=path\to\credentials.json
```

### Authentication errors

Verify:
1. Service account has domain-wide delegation enabled
2. The scope `https://www.googleapis.com/auth/gmail.send` is authorized
3. The impersonated user (`bot-service@telostravel.ai`) exists in your domain
4. The service account has permission to impersonate the user

## License

Internal Telos Travel AI project.

## Support

For issues or questions, contact the Telos development team.
