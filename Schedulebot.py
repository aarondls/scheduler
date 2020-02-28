import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datefinder
import csv_reader

# to grant read/write access to Calendars
scopes = ['https://www.googleapis.com/auth/calendar']

credentials = None

possibleSchedTypes = ["A", "B", "C", "D", "E", "F", "G"]

extractedSched = csv_reader.extractedData

defaultTimeZone = "America/New_York"

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

def createEvent(summary, location, description, startTime, endTime, timezone):
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

    service.events().insert(calendarId='primary', body=event,sendNotifications=True).execute()

if __name__ == '__main__':
    print("Attempting to create")
    try: 
        startDate = datetime.datetime.strptime(input("What is the starting date in m/d/yyyy?"), '%m/%d/%Y').date()
        startSchedType = int(input("What is the starting schedule type (as a number, ie 2)?"))
        duration = int(input("How long will this schedule last in days (as a number, ie 5)?")) 
    except:
        print("Cannot understand format")

    dateOnLoop = startDate
    schedKeyOnLoop = startSchedType
    
    for _ in range(duration):
        schedOnLoop = possibleSchedTypes[schedKeyOnLoop]

        for period in extractedSched[schedOnLoop]:
            print(period)
            # For each period in each schedule type
            timeStart = extractedSched[schedOnLoop][period]["Start Time"]
            timeEnd = extractedSched[schedOnLoop][period]["End Time"]
            summary = extractedSched[schedOnLoop][period]["Summary"]
            location = extractedSched[schedOnLoop][period]["Location"]
            description = extractedSched[schedOnLoop][period]["Description"]

            strStartDate = str(dateOnLoop) + timeStart
            strEndDate = str(dateOnLoop) + timeEnd
            startDate = datetime.datetime.strptime(strStartDate, '%Y-%m-%d%I:%M %p').isoformat()
            endDate = datetime.datetime.strptime(strEndDate, '%Y-%m-%d%I:%M %p').isoformat()
            print(summary)
            print(location)
            print(startDate)
            print(endDate)
            createEvent(summary, location, description, startDate, endDate, defaultTimeZone)

        dateOnLoop = dateOnLoop + datetime.timedelta(days=1)

        if schedKeyOnLoop < 6:
            schedKeyOnLoop = schedKeyOnLoop + 1
        else:
            schedKeyOnLoop = 0
    print("Created events")