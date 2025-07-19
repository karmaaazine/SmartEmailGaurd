"""
Gmail Integration for Smart Email Guardian
Reads emails from Gmail inbox and analyzes them for threats.
"""

import os
import base64
import email
from typing import List, Dict, Optional
from pathlib import Path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Add the ai directory to the path
import sys
sys.path.append(str(Path(__file__).parent.parent / "ai"))

from ai.email_guard import analyze_email

# Gmail API configuration
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'

class GmailReader:
    """Gmail API integration for reading and analyzing emails."""
    
    def __init__(self):
        """Initialize Gmail reader."""
        self.service = None
        self.credentials = None
        
    def authenticate(self) -> bool:
        """
        Authenticate with Gmail API using OAuth2.
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        try:
            # Check if we have valid credentials
            if os.path.exists(TOKEN_FILE):
                self.credentials = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
            
            # If no valid credentials available, let the user log in
            if not self.credentials or not self.credentials.valid:
                if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                    self.credentials.refresh(Request())
                else:
                    if not os.path.exists(CREDENTIALS_FILE):
                        print(f"Error: {CREDENTIALS_FILE} not found.")
                        print("Please download your OAuth2 credentials from Google Cloud Console.")
                        return False
                    
                    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                    self.credentials = flow.run_local_server(port=0)
                
                # Save the credentials for the next run
                with open(TOKEN_FILE, 'w') as token:
                    token.write(self.credentials.to_json())
            
            # Build the Gmail service
            self.service = build('gmail', 'v1', credentials=self.credentials)
            return True
            
        except Exception as e:
            print(f"Authentication error: {e}")
            return False
    
    def get_email_content(self, message_id: str) -> Optional[Dict]:
        """
        Get email content by message ID.
        
        Args:
            message_id: Gmail message ID
            
        Returns:
            Dict: Email content with subject, sender, body, etc.
        """
        try:
            # Get the full message
            message = self.service.users().messages().get(
                userId='me', 
                id=message_id, 
                format='full'
            ).execute()
            
            # Extract headers
            headers = message['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown Date')
            
            # Extract body
            body = self._extract_body(message['payload'])
            
            return {
                'id': message_id,
                'subject': subject,
                'sender': sender,
                'date': date,
                'body': body,
                'snippet': message.get('snippet', '')
            }
            
        except Exception as e:
            print(f"Error getting email content: {e}")
            return None
    
    def _extract_body(self, payload: Dict) -> str:
        """
        Extract email body from payload.
        
        Args:
            payload: Gmail message payload
            
        Returns:
            str: Email body text
        """
        body = ""
        
        if 'parts' in payload:
            # Multipart message
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        body += base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                elif part['mimeType'] == 'text/html':
                    if 'data' in part['body']:
                        # For HTML, we'll just extract text (simplified)
                        html_content = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                        # Simple HTML tag removal (in production, use BeautifulSoup)
                        import re
                        body += re.sub(r'<[^>]+>', '', html_content)
        else:
            # Simple message
            if 'data' in payload['body']:
                body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
        
        return body
    
    def get_recent_emails(self, max_results: int = 5) -> List[Dict]:
        """
        Get recent emails from inbox.
        
        Args:
            max_results: Maximum number of emails to retrieve
            
        Returns:
            List[Dict]: List of email content dictionaries
        """
        try:
            # Get recent messages
            results = self.service.users().messages().list(
                userId='me',
                labelIds=['INBOX'],
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            emails = []
            
            for message in messages:
                email_content = self.get_email_content(message['id'])
                if email_content:
                    emails.append(email_content)
            
            return emails
            
        except Exception as e:
            print(f"Error getting recent emails: {e}")
            return []
    
    def analyze_emails(self, emails: List[Dict]) -> List[Dict]:
        """
        Analyze a list of emails using the AI module.
        
        Args:
            emails: List of email content dictionaries
            
        Returns:
            List[Dict]: List of analysis results
        """
        results = []
        
        for email_data in emails:
            # Analyze the email body
            analysis = analyze_email(email_data['body'])
            
            # Combine email data with analysis
            result = {
                'email': email_data,
                'analysis': analysis,
                'timestamp': email_data['date']
            }
            
            results.append(result)
        
        return results
    
    def scan_inbox(self, max_emails: int = 5) -> List[Dict]:
        """
        Scan recent emails in inbox for threats.
        
        Args:
            max_emails: Maximum number of emails to scan
            
        Returns:
            List[Dict]: List of scan results
        """
        print(f"🔍 Scanning {max_emails} recent emails...")
        
        # Get recent emails
        emails = self.get_recent_emails(max_emails)
        
        if not emails:
            print("No emails found in inbox.")
            return []
        
        # Analyze emails
        results = self.analyze_emails(emails)
        
        return results
    
    def print_scan_summary(self, results: List[Dict]):
        """
        Print a summary of scan results.
        
        Args:
            results: List of scan results
        """
        if not results:
            print("No scan results to display.")
            return
        
        print(f"\n📊 Scan Summary ({len(results)} emails analyzed)")
        print("=" * 60)
        
        # Count classifications
        classifications = {}
        for result in results:
            classification = result['analysis']['classification']
            classifications[classification] = classifications.get(classification, 0) + 1
        
        # Print summary
        for classification, count in classifications.items():
            print(f"{classification.title()}: {count}")
        
        print("\n📧 Detailed Results:")
        print("-" * 60)
        
        for i, result in enumerate(results, 1):
            email_data = result['email']
            analysis = result['analysis']
            
            print(f"\n{i}. {email_data['subject']}")
            print(f"   From: {email_data['sender']}")
            print(f"   Date: {email_data['date']}")
            print(f"   Classification: {analysis['classification'].upper()}")
            print(f"   Confidence: {analysis['confidence']:.1%}")
            print(f"   Explanation: {analysis['explanation']}")
            
            if analysis['indicators']:
                print(f"   Indicators: {', '.join(analysis['indicators'])}")

def main():
    """Main function for Gmail scanning."""
    print("🛡️ Smart Email Guardian - Gmail Scanner")
    print("=" * 50)
    
    # Initialize Gmail reader
    gmail_reader = GmailReader()
    
    # Authenticate
    print("🔐 Authenticating with Gmail...")
    if not gmail_reader.authenticate():
        print("❌ Authentication failed. Please check your credentials.")
        return
    
    print("✅ Authentication successful!")
    
    # Get number of emails to scan
    try:
        max_emails = int(input("Enter number of recent emails to scan (default: 5): ") or "5")
    except ValueError:
        max_emails = 5
    
    # Scan inbox
    results = gmail_reader.scan_inbox(max_emails)
    
    # Print results
    gmail_reader.print_scan_summary(results)
    
    # Save results to file
    output_file = f"gmail_scan_{len(results)}_emails.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Results saved to {output_file}")

if __name__ == "__main__":
    main() 