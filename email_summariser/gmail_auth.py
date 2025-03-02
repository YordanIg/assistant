from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

# Define the areas (scopes) our visitor pass grants access to
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    """Get a Gmail service instance using OAuth 2.0"""
    creds = None

    # Check if we already have a valid visitor pass (token.json)
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there's no valid pass, request a new one
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)  # Opens a browser for login

        # Save the new pass for future visits
        with open('token.json', 'w') as token_file:
            token_file.write(creds.to_json())

    # Return a Gmail service object
    return build('gmail', 'v1', credentials=creds)

if __name__ == '__main__':
    get_gmail_service()
