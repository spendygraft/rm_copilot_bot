#!/usr/bin/env python3
"""Simple non-interactive test of the email service"""
import sys
from gmail_service import get_gmail_service
from config import Config

def main():
    print("="*60, flush=True)
    print("Testing Gmail Service Bot", flush=True)
    print("="*60, flush=True)

    try:
        print(f"\nConfiguration:", flush=True)
        print(f"  Service Account: {Config.SERVICE_ACCOUNT_FILE}", flush=True)
        print(f"  Impersonate User: {Config.IMPERSONATE_USER}", flush=True)
        print(f"  Send From: {Config.SEND_FROM_EMAIL}", flush=True)

        print("\nInitializing Gmail service...", flush=True)
        gmail = get_gmail_service()
        print("✅ Gmail service initialized successfully!", flush=True)

        print("\nSending test email...", flush=True)
        result = gmail.send_email(
            to='scott.pendygraft@telostravel.ai',
            subject='Test Email from Bot',
            body_text='This is a test email sent from the automated bot service.'
        )

        print(f"✅ Email sent successfully!", flush=True)
        print(f"   Message ID: {result.get('id', 'N/A')}", flush=True)
        print(f"   Thread ID: {result.get('threadId', 'N/A')}", flush=True)

        return 0

    except FileNotFoundError as e:
        print(f"\n❌ Configuration Error: {e}", flush=True)
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}", flush=True)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
