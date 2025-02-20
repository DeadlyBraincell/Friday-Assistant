from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
SERVICE_ACCOUNT_FILE = "credentials.json"

def get_calendar_events():
    """Fetches upcoming calendar events."""
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build("calendar", "v3", credentials=creds)
    
    events_result = service.events().list(calendarId="primary", maxResults=5).execute()
    events = events_result.get("items", [])

    event_list = []
    for event in events:
        event_list.append(f"{event['summary']} at {event['start']['dateTime']}")

    return event_list if event_list else ["No upcoming events found."]

print(get_calendar_events())
