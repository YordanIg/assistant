from openai import OpenAI
client = OpenAI()

def read_email_for_singletask(email_text):
    """
    Parse the new email for a single task, deciding how long it will take to 
    achieve. Return the task and its duration in the format 
    {"duration": "HH:MM", "title": "Example task"}.
    """
    # Read in the system instructions.
    with open("system_instructions.txt", "r") as file:
        system_instructions = file.read()

    # Search the email for a task that must be completed and its duration.
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system", 
                "content": system_instructions
            },
            {
                "role": "user",
                "content": email_text
            }
        ]
    )
    print(completion.choices[0].message)
    return completion.choices[0].message.content

if __name__=="__main__":
    # Read in the new email.
    with open("new_email.txt", "r") as file:
        email_text = file.read()
    task = read_email_for_singletask(email_text)
    print(task)