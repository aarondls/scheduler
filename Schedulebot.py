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

def createEvent(summary, location, description, startStr, endStr, timezone):
    matchesStart = list(datefinder.find_dates(startStr))
    for match in matchesStart:
        startTime = matchesStart[0].strftime("%Y-%m-%dT%H:%M:%S")
    matchesEnd = list(datefinder.find_dates(endStr))
    for match in matchesEnd:
        endTime = matchesEnd[0].strftime("%Y-%m-%dT%H:%M:%S") 
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

def extractSchedDetails(schedType: str, period: int, value: str):
    print("test")
    return csv_reader.extractedData[schedType][period][value]

possibleSchedTypes = ["A", "B", "C", "D", "E", "F", "G"]

if __name__ == '__main__':
    print("attempt to create")
    startDate = datetime.date(2020,3,2)
    startSchedType = 2
    duration = 5 
    # endDate = startDate + datetime.timedelta(days=duration)
    dateOnLoop = startDate
    for _ in range(duration):
        scheduleOnLoop = possibleSchedTypes[startSchedType]
        fullDateInfo = str(dateOnLoop) + " 1:33 PM"
        startDate = datetime.datetime.strptime(fullDateInfo, '%Y-%d-%m %I:%M %p')
        print(startDate)
        dateOnLoop = dateOnLoop + datetime.timedelta(days=1)

        if startSchedType < 6:
            startSchedType = startSchedType + 1
        else:
            startSchedType = 0
    # createEvent("Test using CreateFunction Method", "S101", "A quick test", "28 Feb 07.00PM", "28 Feb 08.00PM", "America/New_York")
    print(extractSchedDetails("C",2,"End Time"))