import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datefinder

# to grant read/write access to Calendars
scopes = ['https://www.googleapis.com/auth/calendar']

def main():
    credentials = None

    try:
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    except:
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
        else:
            print("""Something wrong with token. Run the load.py file first
         and verify pickle file exists and credentials are valid.""")
            raise

    service = build('calendar', 'v3', credentials=credentials)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
    
    result = service.calendarList().list().execute()
    calendar_id = result['items'][0]['id']
    print(calendar_id)

    return service

def createEvent(summary, location, description, startStr, endStr, timezone):
    matchesStart = list(datefinder.find_dates(startStr))
    for match in matchesStart:
        startTime = matchesStart[0]
    matchesEnd = list(datefinder.find_dates(endStr))
    for match in matchesEnd:
        endTime = matchesEnd[0]   
    event = {         
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': startTime,
            'timeZone': timezone,
        },
        'end': {
            'dateTime': endTime,
            'timeZone': timezone,
        },
        'reminders': {
            'useDefault': True,
        },
    }

    return service.events().insert(calendarId='primary', body=event, 
    sendNotifications=True).execute()

if __name__ == '__main__':
    service = main()
    createEvent("Test using CreateFunction Method", "", "", "15 Feb 07.00PM", "15 Feb 08.00PM", "America/New_York")