import datetime
import os.path
import datetime
import pytz
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# remplacer par os.path.join

def get_creds():
  creds = None
  if os.path.exists("../gcp_client_secret_v2.json"):
    creds = Credentials.from_authorized_user_file("../gcp_client_secret_v2.json", SCOPES)
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "../credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    with open("../gcp_client_secret_v2.json", "w") as token:
      token.write(creds.to_json())
  return creds

def get_calandar_events(service, creds):
  try:
    timezone_paris = pytz.timezone('Europe/Paris')
    now = datetime.datetime.now(timezone_paris).isoformat()
    print(now)
    print("Getting the upcoming 10 events")
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])
    if not events:
      print("No upcoming events found.")
      return
    return events
  except HttpError as error:
    print(f"An error occurred: {error}")


def create_calandar_event(service, event_object):
  start_datetime = datetime.datetime.strptime(event_object['datetime_debut'], '%Y-%m-%dT%H:%M:%S%z')
  end_datetime = start_datetime + datetime.timedelta(hours=event_object['duree'])
  event = {
  'summary': event_object['title'],
  'description': event_object['description'],
  'start': {
    'dateTime': event_object['datetime_debut'],
    'timeZone': 'Europe/Paris',
  },
  'end': {
    'dateTime': end_datetime.isoformat(),
    'timeZone': 'Europe/Paris',
  },
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'popup', 'minutes': 10},
    ],
  },
}
  event_resut = (
    service.events()
    .insert(
      calendarId='primary', 
      body=event
      )
      .execute()
  )
  return event_resut

if __name__ == "__main__":
  creds = get_creds()
  service = build("calendar", "v3", credentials=creds)
  
  event_object = {
    "title" : "Google I/O 2015",
    "description" : "A chance to hear more <strong>about</strong> Google\'s developer products.",
    "datetime_debut": "2024-05-02T12:00:00+02:00",
    "duree" : 1,
  }
  #print(json.dumps(get_calandar_events(service, creds), indent=2))
  #print ("Event created:create ", create_calandar_event(service, event_object).get('htmlLink'))
  
