from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scope gives read-only access to Gmail
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def search_interview_emails(service):
    query = 'subject:interview OR subject:screening OR subject:schedule'
    result = service.users().messages().list(userId='me', q=query).execute()
    messages = result.get('messages', [])
    return messages

def get_email_summary(service, msg_id):
    msg = service.users().messages().get(userId='me', id=msg_id, format='metadata', metadataHeaders=['Subject', 'From', 'Date']).execute()
    payload = msg.get('payload', {})
    headers = payload.get("headers", [])

    summary = {"From": "", "Subject": "", "Date": ""}
    for header in headers:
        name = header.get("name")
        if name in summary:
            summary[name] = header.get("value")

    return summary

def main():
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)

    print("\n📨 Searching for interview emails...\n")
    messages = search_interview_emails(service)

    if not messages:
        print("No interview emails found.")
        return

    for i, msg in enumerate(messages[:10], 1):  # Just show the 10 most recent
        info = get_email_summary(service, msg['id'])
        print(f"{i}. From: {info['From']}")
        print(f"   Subject: {info['Subject']}")
        print(f"   Date: {info['Date']}\n")

if __name__ == '__main__':
    main()
