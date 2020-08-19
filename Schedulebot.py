from sys import exit
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import csv_reader
from itertools import cycle, islice
from pprint import pprint

# to grant read/write access to Calendars
scopes = ['https://www.googleapis.com/auth/calendar']

credentials = None

# A to Z type of schedule
# possibleSchedTypes = ["A", "B", "C", "D", "E", "F", "G"]

# M to F type of schedule
possibleSchedTypes = ["M", "T", "W", "R", "F"]

extractedSched = csv_reader.extractedData

defaultTimeZone = "America/Chicago"

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
    print("Attempting to create events.")
    try: 
        dateOnLoop = datetime.datetime.strptime(input("What is the starting date in m/d/yyyy?\n"), '%m/%d/%Y').date()
        strSchedStart = input("What is the starting schedule type (as defined in csv file, ie A)?\n")
        if strSchedStart not in possibleSchedTypes:
            raise Exception("Schedule type not recognized")
        duration = int(input("How long will this schedule last in days (as a number, ie 5)?\n")) 
        if input("Does the schedule skip weekends?\ny/n ") in ["Y", "y", "Yes", "yes"]:
            skipWeekends = True
        else:
            skipWeekends = False
    except:
        print("Cannot understand format")
        raise
    
    schedKey = possibleSchedTypes.index(strSchedStart)
    desiredSched = list(islice(cycle(possibleSchedTypes), schedKey, schedKey+duration))
    eventsCreated = []

    for schedOnLoop in desiredSched:
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
            eventsCreated.append(summary)
            createEvent(summary, location, description, startDate, endDate, defaultTimeZone)
        if skipWeekends and dateOnLoop.weekday() == 4:
            dateOnLoop = dateOnLoop + datetime.timedelta(days=3)
        else:
            dateOnLoop = dateOnLoop + datetime.timedelta(days=1)
    
    print("In total, I created", len(eventsCreated), "events over", duration, "days.")
    if input("Do you want to see a complete list of the events?\ny/n ") in ["Y", "y", "Yes", "yes"]:
        print("Here is a list of the events I created:")
        pprint(eventsCreated)