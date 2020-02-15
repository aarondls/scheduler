# Run Load.py only once for the first time to generate pickle file with the given scope

import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# to grant read/write access to Calendars
scopes = ['https://www.googleapis.com/auth/calendar']
credentialFile = "/Users/aarondelossantos/documents/schedulerkey/client_secret.json"

if __name__ == '__main__':
    # no pickle file exists yet
    if not os.path.exists('token.pickle'):
        flow = InstalledAppFlow.from_client_secrets_file(
        credentialFile, scopes)
        creds = flow.run_console()
        # Save the credentials by creating pickle file
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)