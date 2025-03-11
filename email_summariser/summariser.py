"""
This file contains the code to summarise a new Gmail email, by looking both at
the email's content and the previous emails in the same thread. It uses the
Email class from gmail_reader.py to extract the email's details and the
list_messages_in_thread function to fetch the previous emails in the thread.
"""
from gmail_auth import get_gmail_service
import gmail_reader as gr
from openai import OpenAI
client = OpenAI()

def summarise_email_thread(service, email_id):
    """
    Read the email specified by its ID and summarise it by looking at the
    previous emails in the same thread.
    """
    messages = gr.list_messages_in_thread(service, email_id)
    emails = [gr.Email(message) for message in messages]
    email_details = [email.get_email_details(service) for email in emails]
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

def summarise_list_of_emails(service, email_list):
    """
    Summarise a list of emails object.
    """
    email_details = email_list.get_email_details(service)
    email_bodies  = [email["body"] for email in email_details]

    # Generate a summary of the email thread
    sys_instructions = "You are a helpful assistant. Summarise the following email thread."
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": sys_instructions
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
    
    # Fetch and summarise the latest 5 emails.
    latest_emails = gr.fetch_latest_emails(service, n=5)
    summarise_list_of_emails(service, latest_emails)
