from __future__ import print_function # google api must be on first line
import os

# google imports
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload
from app.extensions import db
from flask import g


SCOPES = ['https://www.googleapis.com/auth/drive']
RESUME_FOLDER_ID = "1mC7JhJA4WLp8pT7pb98NNgtSZPzqkGAn"
# credentials go in same folder as this file
# file name should be whatever creds is on line 28/29
def google_drive_auth(userfile):
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './app/utils/client_id.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    print("got here in google")
    service = build('drive', 'v3', credentials=creds)
    return get_file_in_google_drive(service, userfile)

def get_file_in_google_drive(google_api_call, file_to_upload):
    # puts a file in google drive only not specific folder
    print("made it to get_file_in_google_drive function")
    user_data = db.child("users").child(g.user['localId']).get().val() 
    print(user_data)
    if user_data['resume_id'] != '': #checks to see if a user has a resume already in database
        print("file being updated")
        update_file(google_api_call, file_to_upload, user_data['resume_id'])
    else:
        print("new file created")
        use_as_filename = user_data['last_name'] + '_' + user_data['first_name']
        file_metadata = {
        'name': use_as_filename, #this name appears on google drive
        'parents': "" #put google folder ID inside of quotes to get file in that folder
        }
        media = MediaFileUpload(file_to_upload)
        file_to_google_drive = google_api_call.files().create(body=file_metadata,
                                            media_body=media,
                                            fields="id").execute()
        print(file_to_google_drive['id'])
        db.child("users").child(g.user["localId"]).update({"resume_id": file_to_google_drive['id']})


def update_file(service, userfile, file_id): #works
        print("This is the first time i prtin file_id in update the file", file_id)
        media = MediaFileUpload(userfile)
        service.files().update(media_body=media,
                                fileId=file_id).execute()