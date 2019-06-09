
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sys

from dateutil.parser import parse

SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']

def formatTimeDelta(tdelta):
    days = tdelta.days
    hours, rem = divmod(tdelta.seconds, 3600)
    minutes, seconds = divmod(rem, 60)

    if days == 0:
        if hours == 0:
            if minutes == 0:
                return f"{seconds} seconds"

            return f"{minutes} minutes, {seconds} seconds"

        return f"{hours} hours, {minutes} minutes, {seconds} seconds"

    return f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"

def quickAdd(text):
    service = getService()
    created_event = service.events().quickAdd(
        calendarId='primary',
        text=text).execute()
    startInfo = created_event['start']
    if 'dateTime' in startInfo:
        startTime = parse(startInfo['dateTime'])
    else:
        startTime = parse(startInfo['date'])
    delta = startTime - datetime.datetime.now(startTime.tzinfo)
    print(f"Event occurs in {formatTimeDelta(delta)}")

def getService():
    scriptDir = os.path.dirname(sys.argv[0])
    credentialsPath = os.path.join(scriptDir, 'credentials.json')

    if not os.path.isfile(credentialsPath):
        print("Could not find credentials.json!  You need to generate this yourself from the google api developer page")
        exit()

    tokensPickle = os.path.join(scriptDir, 'token.pickle')
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentialsPath, SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open(tokensPickle, 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Invalid arguments")
        exit(1)
    quickAdd(sys.argv[1])
