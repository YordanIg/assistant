from email_reader import read_email_for_singletask
from cal_reader import find_available_slot
import json

# Load JSON file
with open("cal.json", "r") as file:
    calendar = json.load(file)

# Load the email
with open("new_email.txt", "r") as file:
    email_text = file.read()

def convert_duration_to_minutes(duration_str):
    """
    Convert a duration string in the format "HH:MM" to minutes.
    """
    hours, minutes = map(int, duration_str.split(":"))
    return hours * 60 + minutes

def read_email_and_schedule_task(email_text, calendar):
    """
    Read the email and schedule the task in the calendar. Assumes that the first
    date in the calendar is today's date.
    """
    # Read the email for a single task
    task_str = read_email_for_singletask(email_text)
    try:
        task = json.loads(task_str)
    except json.JSONDecodeError:
        print(f"Error: Could not parse taskstr {task_str} from email into JSON.")
        return
    print("new task:",task)

    # Find an available slot, beginning from today.
    possible_dates = []
    i = 0
    while True:
        try:
            date = calendar['calendar'][i]['date']
            possible_dates.append(date)
            i += 1
        except IndexError:
            break

    found_date = False
    for date in possible_dates:
        duration = convert_duration_to_minutes(task['duration'])
        best_slot = find_available_slot(date, duration, calendar)
        if best_slot:
            found_date = True
            break
    
    if found_date:
        print(f"Best available time for {task['title']} on {date}: {best_slot}")
    else:
        print(f"No available time found for {task['title']} in the next week.")

if __name__=="__main__":
    read_email_and_schedule_task(email_text, calendar)
