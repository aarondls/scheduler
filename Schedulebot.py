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

possibleSchedTypes = ["A", "B", "C", "D", "E", "F", "G"]

extractedSched = csv_reader.extractedData

if __name__ == '__main__':
    print("attempt to create")
    startDate = datetime.datetime.strptime("3/2/2020", '%m/%d/%Y').date()
    startSchedType = 2
    duration = 5 
    # endDate = startDate + datetime.timedelta(days=duration)
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
            createEvent(summary, location, description, startDate, endDate, "America/New_York")

        dateOnLoop = dateOnLoop + datetime.timedelta(days=1)

        if schedKeyOnLoop < 6:
            schedKeyOnLoop = schedKeyOnLoop + 1
        else:
            schedKeyOnLoop = 0
    print("Created events")