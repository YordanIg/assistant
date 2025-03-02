import json
from datetime import datetime, timedelta

# Load JSON file
with open("cal.json", "r") as file:
    calendar = json.load(file)

def find_available_slot(date, duration_minutes, calendar):
    """
    Finds the first available time slot on a given date, returning None if 
    no slot is available.
    """
    # Load preferences
    work_start = datetime.strptime(calendar["preferences"]["working_hours"]["start"], "%H:%M")
    work_end = datetime.strptime(calendar["preferences"]["working_hours"]["end"], "%H:%M")
    preferred_duration = timedelta(minutes=duration_minutes)

    # Get events for the given date
    events = next((day["events"] for day in calendar["calendar"] if day["date"] == date), [])

    # Convert events into datetime ranges
    busy_times = []
    for event in events:
        start = datetime.strptime(event["start_time"], "%H:%M")
        end = datetime.strptime(event["end_time"], "%H:%M")
        busy_times.append((start, end))

    # Sort events by start time
    busy_times.sort()

    # Find free slots
    current_time = work_start
    for start, end in busy_times:
        if current_time + preferred_duration <= start:  # Found a gap
            return current_time.strftime("%H:%M")
        current_time = max(current_time, end)  # Move past this event

    # Check if there's room at the end of the day
    if current_time + preferred_duration <= work_end:
        return current_time.strftime("%H:%M")

    return None

if __name__=="__main__":
    # Example usage
    date_to_check = "2025-02-22"
    duration = 45  # New event duration in minutes

    best_slot = find_available_slot(date_to_check, duration, calendar)
    print(f"Best available time on {date_to_check}: {best_slot}")
