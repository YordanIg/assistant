from gmail_auth import get_gmail_service
import base64

def list_messages(service):
    """
    Fetch and display the latest emails, returning their IDs and thread IDs.
    """
    # Ask the Gmail facility for a list of emails
    results = service.users().messages().list(userId='me', maxResults=10).execute()
    messages = results.get('messages', [])
    return messages

def list_messages_in_thread(service, thread_id):
    """
    Fetch and display the emails in a thread, returning their IDs and thread IDs.
    """
    # Ask the Gmail facility for a list of emails in the thread
    results = service.users().threads().get(userId='me', id=thread_id).execute()
    messages = results.get('messages', [])
    return messages

def decode_base64(encoded_data):
    """Decodes base64 URL-safe encoded email content."""
    return base64.urlsafe_b64decode(encoded_data).decode("utf-8", errors="ignore")


class Email:
    """
    Represents an email message and provides methods to extract its details
    like headers, body, and attachments.
    """
    def __init__(self, email: dict):
        self.email = email
        self.id = email['id']
        self.snippet = email['snippet']

    def get_email_details(self):
        """Extracts email headers, best body content, and attachments."""
        
        # Extract headers
        headers = {h["name"]: h["value"] for h in self.email["payload"]["headers"]}
        from_email = headers.get("From", "Unknown Sender")
        to_email = headers.get("To", "Unknown Recipient")
        subject = headers.get("Subject", "No Subject")
        date = headers.get("Date", "No Date")

        # Extract body (HTML preferred, fallback to plain text)
        body = self.extract_email_body()

        return {
            "from": from_email,
            "to": to_email,
            "subject": subject,
            "date": date,
            "body": body
        }

    def extract_email_body(self):
        """Finds the best email body: HTML (preferred) or plain text."""
        payload = self.email['payload']
        if "body" in payload and "data" in payload["body"]:
            return decode_base64(payload["body"]["data"])  # Single-part email
        
        if "parts" in payload:
            for part in payload["parts"]:
                mime_type = part.get("mimeType", "")
                if mime_type == "text/html":  # Prefer HTML
                    return decode_base64(part["body"]["data"])
                elif mime_type == "text/plain":  # Fallback to plain text
                    plain_text = decode_base64(part["body"]["data"])
        
        return plain_text if 'plain_text' in locals() else "[No body found]"

class ListOfEmails:
    def __init__(self, *emails: Email):
        self.emails = emails

if __name__ == '__main__':
    # Authenticate with OAuth
    service = get_gmail_service()
    print("List of last email IDs:")
    messages = list_messages()
    print(messages)

    print("Example email:")
    msg_id      = messages[0]['id']
    email       = service.users().messages().get(userId='me', id=msg_id).execute()
    email_obj   = Email(email)
    print("ID:", email_obj.id)
    print("details:\n", email_obj.get_email_details(email))
