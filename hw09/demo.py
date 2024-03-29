#!/usr/bin/env python3
# Based pm: https://github.com/googleworkspace/python-samples/tree/master/sheets/quickstart
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START sheets_quickstart]
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import time, sys
import os

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1asFw9GoAoRBbMQnt-QN3eEDT9FBEG2nq19e1OhVP6-A'
SAMPLE_RANGE_NAME = 'A2'

temp = {}
w1_path="/sys/class/hwmon"
if (not os.path.exists(w1_path)):
    print("MAX31820 has not config yet.")

f1=open(w1_path+"/hwmon0/temp1_input", "r")
f2=open(w1_path+"/hwmon1/temp1_input", "r")
f3=open(w1_path+"/hwmon2/temp1_input", "r")

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
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
                'credentials.json', SCOPES)
            # creds = flow.run_local_server(port=0)
            creds = flow.run_console()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    global service
    service = build('sheets', 'v4', credentials=creds)

if __name__ == '__main__':
    main()
    try:
        while(True):
            f1.seek(0)
            f2.seek(0)
            f3.seek(0)
            temp[0] = f1.read()[:-1]
            temp[1] = f2.read()[:-1]
            temp[2] = f3.read()[:-1]
            print("Temperature: "+temp[0]+" | "+ temp[1]+" | "+ temp[2], end='\r')
            # Call the Sheets API
            sheet = service.spreadsheets()
            values = [ [time.time()/60/60/24+ 25569 - 4/24, temp[0], temp[1], temp[2]]]
            body = {'values': values}
            result = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range=SAMPLE_RANGE_NAME,
                                        valueInputOption='USER_ENTERED', 
                                        body=body
                                        ).execute()
            #print(result)
            time.sleep(600)
    except KeyboardInterrupt:
        f1.close()
        f2.close()
        f3.close()
# [END sheets_quickstart]
