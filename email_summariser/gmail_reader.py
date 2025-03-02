from gmail_auth import get_gmail_service

def list_messages():
    """Fetch and display the latest emails"""
    service = get_gmail_service()  # Authenticate with OAuth

    # Ask the Gmail facility for a list of emails
    results = service.users().messages().list(userId='me', maxResults=10).execute()
    messages = results.get('messages', [])
    for msg in messages:
        print(f"Email ID: {msg['id']}")
        if not messages:
            print("No messages found.")
            return
    

if __name__ == '__main__':
    list_messages()
