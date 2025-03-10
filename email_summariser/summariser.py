"""
This file contains the code to summarise a new Gmail email, by looking both at
the email's content and the previous emails in the same thread. It uses the
Email class from gmail_reader.py to extract the email's details and the
list_messages_in_thread function to fetch the previous emails in the thread.
"""
from gmail_auth import get_gmail_service
from gmail_reader import Email, list_messages, list_messages_in_thread
from openai import OpenAI
client = OpenAI()

def summarise_email_thread(service, email_id):
    """
    Read the email specified by its ID and summarise it by looking at the
    previous emails in the same thread.
    """
    messages = list_messages_in_thread(service, email_id)
    emails = [Email(message) for message in messages]
    email_details = [email.get_email_details() for email in emails]
    email_bodies = [email["body"] for email in email_details]

    # Generate a summary of the email thread
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Summarise the following email thread."
            },
            {
                "role": "user",
                "content": "\n".join(email_bodies)
            }
        ]
    )
    print(completion.choices[0].message)

if __name__ == "__main__":
    # Authenticate with OAuth
    service = get_gmail_service()
    print("List of last email IDs:")
    messages = list_messages(service)
    n = 0
    print(f"let's look at email {n} in the list with thread ID:", messages[n]["threadId"])
    email_id = messages[n]["id"]
    res = summarise_email_thread(service, email_id)
    print(res)
    