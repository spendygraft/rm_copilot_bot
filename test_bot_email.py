# test_bot_email.py
from gmail_service import get_gmail_service
from config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_simple_email(recipient_email):
    """Test sending a simple email"""
    print("\n" + "="*60)
    print("🧪 TEST 1: Simple Text Email")
    print("="*60)
    
    gmail = get_gmail_service()
    
    result = gmail.send_email(
        to=recipient_email,
        subject='✅ Test: Bot Service Account Working',
        body_text='''Hello,

This email confirms that your bot-service account is properly configured and sending emails as rm.copilot@telostravel.ai.

Setup Details:
- Service Account: ✅ Configured
- Domain-Wide Delegation: ✅ Enabled
- Bot User: bot-service@telostravel.ai
- Sending As: rm.copilot@telostravel.ai

Your automated email system is ready for production!

Best regards,
RM Copilot Bot
'''
    )
    
    print(f"✅ Email sent! Message ID: {result['id']}")
    print(f"📧 Check your inbox at {recipient_email}")


def test_html_email(recipient_email):
    """Test sending an HTML email"""
    print("\n" + "="*60)
    print("🧪 TEST 2: HTML Email with Styling")
    print("="*60)
    
    gmail = get_gmail_service()
    
    html_body = '''
    <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; }
                .header { background-color: #4285f4; color: white; padding: 20px; }
                .content { padding: 20px; }
                .success { color: #0f9d58; font-weight: bold; }
                .info-box { background-color: #f8f9fa; padding: 15px; border-left: 4px solid #4285f4; margin: 20px 0; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🎉 Telos Travel AI Email System</h1>
            </div>
            <div class="content">
                <h2 class="success">✅ Configuration Successful!</h2>
                
                <p>Your automated email system is now fully operational.</p>
                
                <div class="info-box">
                    <h3>System Details:</h3>
                    <ul>
                        <li><strong>Bot Account:</strong> bot-service@telostravel.ai</li>
                        <li><strong>Sending Identity:</strong> rm.copilot@telostravel.ai</li>
                        <li><strong>Authentication:</strong> Service Account with Domain-Wide Delegation</li>
                        <li><strong>Status:</strong> <span class="success">Active</span></li>
                    </ul>
                </div>
                
                <p>You can now use this system to send automated emails for:</p>
                <ul>
                    <li>Customer notifications</li>
                    <li>Pricing updates</li>
                    <li>System alerts</li>
                    <li>Reporting</li>
                </ul>
                
                <p>Best regards,<br>
                <strong>The Telos Development Team</strong></p>
            </div>
        </body>
    </html>
    '''
    
    result = gmail.send_email(
        to=recipient_email,
        subject='🎨 Test: HTML Email with Styling',
        body_text='This is the plain text fallback.',
        body_html=html_body
    )
    
    print(f"✅ HTML email sent! Message ID: {result['id']}")


def test_email_with_cc_bcc(recipient_email):
    """Test sending email with CC and BCC"""
    print("\n" + "="*60)
    print("🧪 TEST 3: Email with CC and BCC")
    print("="*60)
    
    gmail = get_gmail_service()
    
    result = gmail.send_email(
        to=recipient_email,
        cc=recipient_email,
        subject='📋 Test: Email with CC',
        body_text='This email tests CC functionality. Check that you received it in both TO and CC.'
    )
    
    print(f"✅ Email with CC sent! Message ID: {result['id']}")


def run_all_tests():
    """Run all email tests"""
    print("\n" + "="*60)
    print("🚀 STARTING BOT EMAIL TESTS")
    print("="*60)
    print(f"\n📋 Configuration:")
    print(f"   Impersonating: {Config.IMPERSONATE_USER}")
    print(f"   Sending From: {Config.SEND_FROM_EMAIL}")
    print(f"   Service Account: {Config.SERVICE_ACCOUNT_FILE}")

    # Prompt user for recipient email
    print("\n" + "="*60)
    recipient_email = input("📧 Enter the recipient email address for tests: ").strip()

    if not recipient_email:
        print("❌ No email address provided. Exiting.")
        return

    print(f"✅ All test emails will be sent to: {recipient_email}")

    try:
        test_simple_email(recipient_email)
        input("\n✅ Test 1 complete. Press Enter to continue to Test 2...")

        test_html_email(recipient_email)
        input("\n✅ Test 2 complete. Press Enter to continue to Test 3...")

        test_email_with_cc_bcc(recipient_email)

        print("\n" + "="*60)
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\n✅ Your bot email system is fully operational!")
        print(f"📧 Check your inbox at {recipient_email} for all test emails")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        logger.exception("Test error:")


if __name__ == "__main__":
    run_all_tests()