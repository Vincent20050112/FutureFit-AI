# build_ics.py

from icalendar import Calendar, Event
from datetime import datetime, timedelta, date
import pytz

def build_ics(final_selected_tasks: list, timezone_str: str) -> bytes:
    """
    Accepts the list of all individually checked tasks from the frontend UI
    and converts them into a raw .ics calendar byte stream.
    
    final_selected_tasks: Expected format is a list of flattened tuples:
                          [("07:30 AM", "EXERCISE", "Morning walk - 20 minutes"), ...]
    timezone_str:         The timezone string selected by the user (e.g., "US/Pacific")
    """
    cal = Calendar()
    cal.add("prodid", "-//FutureFit AI//EN")
    cal.add("version", "2.0")

    tz = pytz.timezone(timezone_str)
    today = date.today()

    for time_str, category, task in final_selected_tasks:
        # Clean up category tags by removing brackets and formatting as uppercase
        category_cleaned = str(category).replace("[", "").replace("]", "").upper()

        # Parse the standard 12-hour clock string (e.g., "07:30 AM") into today's datetime object
        try:
            parsed_time = datetime.strptime(time_str, "%I:%M %p").time()
            dt_start = datetime.combine(today, parsed_time)
        except Exception:
            # Fallback: use current execution time if string parsing encounters an anomaly
            dt_start = datetime.combine(today, datetime.now().time())

        # Construct the unique calendar event block
        event = Event()
        # Event Title: [EXERCISE] Morning walk - 20 minutes
        event.add("summary", f"[{category_cleaned}] {task}")
        # Apply the timezone localization mapping
        event.add("dtstart", tz.localize(dt_start))
        # Enforce a default duration of 30 minutes per habit window
        event.add("duration", timedelta(minutes=30))
        event.add("description", f"FutureFit AI Personalized Health Plan\nCategory: {category_cleaned}")
        
        # Configure the recurrence rule to repeat seamlessly every single day
        event.add("rrule", {"FREQ": ["DAILY"]})
        
        cal.add_component(event)

    return cal.to_ical()