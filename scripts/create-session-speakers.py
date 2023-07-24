import pandas as pd
from datetime import datetime
import readline  # noqa
import sys
from getpass import getpass
from dataclasses import dataclass

import requests
import csv
import re
import sys
import json

event_id = '5'
fn = 'Wikimania Sessions and Speakers.xlsx'

session_type_times = {
    "Entertainment session": 30,
    "Lecture": 20,
    "Lecture 15 minute": 15,
    "Lecture 30 minute": 30,
    "Lecture 60 minute": 60,
    "Lightning talk": 10,
    "Lightning talk 5 minute": 5,
    "Meetup": 60,
    "Meetup 120 minute": 120,
    "Open discussion 20 minute": 20,
    "Panel": 60,
    "Panel 30 minute": 30,
    "Panel 40 minute": 40,
    "Panel 45 minute": 45,
    "Poster session": 2,
    "Roundtable / open discussion": 60,
    "Roundtable discussion 30 minute": 30,
    "Roundtable discussion 40 minute": 40,
    "Roundtable discussion 45 minute": 45,
    "Roundtable discussion 90 minute": 90,
    "Summit": 135,
    "Wikiwomen Lecture": 12,
    "Workshop": 60,
    "Workshop 120 minute": 120,
    "Workshop 30 minute": 30,
    "Workshop 40 minute": 40,
    "Workshop 45 minute": 45,
    "Workshop 90 minute": 90,
    "Workshop All day 390 minutes": 390,
    "Workshop Half Day 165 minutes": 165,
}

speakers = pd.read_excel(fn, index_col='ID', sheet_name="Speakers", )
sessions = pd.read_excel(fn, index_col='ID', sheet_name="Sessions")

# print(speakers)

# print(sessions)

# collect tracks
tracks = sessions['Track'].unique()
session_types = sessions['Session type'].unique()
# print(f"Tracks: {tracks}")


# event_identifier = '41dbcda9'
api_url = 'http://localhost:8080/v1'
# event_url = api_url + '/events/' + event_identifier

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2OTAxODQxNzgsIm5iZiI6MTY5MDE4NDE3OCwianRpIjoiODA3MDNiYjctM2NhNC00NmY4LWJjMDAtZWU5ODRiMTQ2MjdkIiwiZXhwIjoxNjkwMjcwNTc4LCJpZGVudGl0eSI6MSwiZnJlc2giOnRydWUsInR5cGUiOiJhY2Nlc3MiLCJjc3JmIjoiMTRjOWMxNDYtNDA0ZS00ZjZiLTk0NTUtYWI5MTU3YzMyNjNhIn0.wVErUWDRsTJolNmIb_4rC4Uynf0ZlQcU-XQIfXGWdUk"


# event = requests.get(event_url, timeout=10).json()


create_track_url = api_url + '/tracks'
create_session_type_url = api_url + '/session-types'
create_speaker_url = api_url + '/speakers'
create_session_url = api_url + '/sessions'

speaker_id_to_eventyay_id = dict()
track_to_eventyay_id = dict()
session_type_to_eventyay_id = dict()
session_id_to_eventyay_id = dict()

session_type_to_session_eventyay_ids = dict()
speaker_id_to_session_eventyay_ids = dict()

# for dry running a fake response class
NEXT_NR = 1

@dataclass
class FakeResponse:
    status_code: int = 201
    def json(self):
        global NEXT_NR
        n = NEXT_NR
        NEXT_NR += 1
        return({"data": {"id": n}})

# try to get a token
def get_token():
    username = 'open_event_test_User@fossasia.org'
    password = 'fossasia'

    auth = requests.post(
        'http://localhost:8080/auth/session',
        json={'email': username, 'password': password},
        timeout=10
    )
    if auth.status_code != 200:
        print('Auth Error:', auth.json())
        sys.exit(-1)
    token = auth.json()['access_token']
    # print (f"ACCESS TOKEN = {token}")
    return token

def create_tracks():
    for t in tracks:
        data = {
            "data": {
                "relationships": {
                    "event": {
                        "data": {
                            "type": "event",
                            "id": event_id
                        }
                    }
                },
                "attributes": {
                    "name": t,
                    # "description": "description",
                    # TODO separate colors for tracks?
                    "color": "#a04b4b"
                },
                "type": "track"
            }
        }
        if DRY_RUN:v
            response = FakeResponse()
        else:
            response = requests.post(
                create_track_url,
                json=data,
                headers={
                    'Content-Type': 'application/vnd.api+json',
                    'Authorization': 'JWT ' + token,
                },
                timeout=10
            )
        if response.status_code == 201:
            # print('Track created')
            track_to_eventyay_id[t] = response.json()['data']['id']
        elif response.status_code == 403:
            # Handle Error
            # TODO we need API to get track id!!
            print(f'Track already exists: {t}')
            track_to_eventyay_id[t] = 'unknown'
        elif response.status_code != 201:
            print('Error: ', t, response, response.content)
            track_to_eventyay_id[t] = 'error'

def create_sessions():
    for idx, row in sessions.iterrows():
        data = {
            "data": {
                "relationships": {
                    "event": {
                        "data": {
                            "type": "event",
                            "id": event_id
                        }
                    },
                    "track": {
                        "data": {
                            "type": "track",
                            "id": track_to_eventyay_id[row['Track']]
                        }
                    }
                },
                "attributes": {
                    "title": row['Proposal title'],
                    # "subtitle": "Title",
                    # "level": "Expert",
                    "short-abstract": row['Abstract'],
                    "long-abstract": row['Description'],
                    #"comments": "Comment",
                    #"starts-at": "2099-06-01T10:00:00.500127+00:00",
                    #"ends-at": "2099-06-01T11:00:00.500127+00:00",
                    "language": row['Language'],
                    #"slides-url": "http://example.com/example",
                    #"video-url": "http://example.com/example",
                    #"audio-url": "http://example.com/example",
                    #"signup-url": "http://example.com/example",
                    "state": "accepted",
                    #"created-at": "2017-05-01T01:24:47.500127+00:00",
                    # "deleted-at": null,
                    #"submitted-at": "2017-05-01T01:24:47.500127+00:00",
                    #"is-mail-sent": false,
                    #"last-modified-at": "2017-05-01T01:24:47.500127+00:00"
                },
                "type": "session"
            }
        }
        if DRY_RUN:
            response = FakeResponse()
        else:
            response = requests.post(
                create_session_url,
                json=data,
                headers={
                    'Content-Type': 'application/vnd.api+json',
                    'Authorization': 'JWT ' + token,
                },
                timeout=10
            )

        if response.status_code == 201:
            # print('Session created')
            id = response.json()['data']['id']
            session_id_to_eventyay_id[idx] = id
            for speaker_id in row['Speaker IDs'].split():
                if speaker_id in speaker_id_to_session_eventyay_ids:
                    speaker_id_to_session_eventyay_ids[speaker_id].append(id)
                else:
                    speaker_id_to_session_eventyay_ids[speaker_id] = [id]
            
            session_type = row['Session type']
            if session_type in session_type_to_session_eventyay_ids:
                session_type_to_session_eventyay_ids[session_type].append(id)
            else:
                session_type_to_session_eventyay_ids[session_type] = [id]
        elif response.status_code == 403:
            # Handle Error
            # TODO we need API to get session id!!!
            print(f"Session already exists {idx}")
            session_id_to_eventyay_id[idx] = 'unknown'
        elif response.status_code != 201:
            print('Error: ', response, response.content)
            session_id_to_eventyay_id[idx] = 'error'
    

def create_session_types():
    for t in session_types:
        minutes = session_type_times[t]
        hours = minutes // 60
        remmin = minutes % 60
        session_time = "{:02d}:{:02d}".format(hours, remmin)
        data = {
            "data": {
                "relationships": {
                    "event": {
                        "data": {
                            "type": "event",
                            "id": event_id
                        }
                    },
                    "sessions": {
                        "data": [
                            {
                                "type": "session",
                                "id": id
                            } for id in session_type_to_session_eventyay_ids[t]
                        ]
                    }
                },
                "attributes": {
                    "name": t,
                    "length": session_time,
                },
                "type": "session-type"
            }
        }
        if DRY_RUN:
            response = FakeResponse()
        else:
            response = requests.post(
                create_session_type_url,
                json=data,
                headers={
                    'Content-Type': 'application/vnd.api+json',
                    'Authorization': 'JWT ' + token,
                },
                timeout=10
            )
        if response.status_code == 201:
            # print('Session Type created')
            session_type_to_eventyay_id[t] = response.json()['data']['id']
        elif response.status_code == 403:
            # Handle Error
            # TODO we need API to get session type id!!
            print(f"Session Type already exists: {t}")
            session_type_to_eventyay_id[t] = 'unknown'
        elif response.status_code != 201:
            print('Error: ', t, response, response.content)
            session_type_to_eventyay_id[t] = 'error'



def create_speakers():
    for idx, row in speakers.iterrows():
        data = { 
            "data": {
                "type": "speaker",
                "relationships": {
                    "event": {
                        "data": {
                            "type": "event",
                            "id": event_id
                        }
                    },
                    "sessions": {
                        "data": [
                            {
                                "type": "session",
                                "id": id
                            } for id in speaker_id_to_session_eventyay_ids[idx]
                        ]
                    }
                },
                "attributes": {
                    "email": row['E-Mail']
                }
            }
        }
        if not pd.isna(row['Biography']):
            data['data']['attributes']['short-biography'] = row['Biography']
        if not pd.isna(row['Picture']):
            data['data']['attributes']['photo-url'] = row['Picture']
        if not pd.isna(row['Name']):
            data['data']['attributes']['name'] = row['Name']
        else:
            data['data']['attributes']['name'] = "Anonymous"

        #print("Creating speaker:")
        #print(f"   name: {row['Name']}")
        #print(f"   email: {row['E-Mail']}")
        #print(f"   photo-url: {row['Picture']}")
        if DRY_RUN:
            response = FakeResponse()
        else:
            response = requests.post(
                create_speaker_url,
                json=data,
                headers={
                    'Content-Type': 'application/vnd.api+json',
                    'Authorization': 'JWT ' + token,
                },
                timeout=10
            )

        if response.status_code == 201:
            # print('Speaker created')
            speaker_id_to_eventyay_id[idx] = response.json()['data']['id']
        elif response.status_code == 403:
            # Handle Error
            # TODO we need API to get speaker id!!!
            print(f"Speaker already exists: {row['E-Mail']}")
            speaker_id_to_eventyay_id[idx] = 'unknown'
        elif response.status_code != 201:
            print('Error: ', row['E-Mail'], response, response.content)
            speaker_id_to_eventyay_id[idx] = 'error'

    


# print(f"speaker_id_to_eventyay_id = {speaker_id_to_event_id}")

def do_checks():
    ret = True
    # checks
    # - session speaker ids can be found
    # - session speaker name is the same as the names found via speakers
    for idx, row in sessions.iterrows():
        #print(f"Session Id = {idx}")
        #print(f"    speaker id = {row['Speaker IDs']}")
        #print(f"   session speaker names: {row['Speaker names']}")
        speaker_ids = row['Speaker IDs'].split()
        speaker_name_combined = ''
        for sid in speaker_ids:
            #print(f"   speaker id:    {sid}")
            #print(f"   speaker email: {speakers['E-Mail'][sid]}")
            sn = "" if pd.isna(speakers['Name'][sid]) else speakers['Name'][sid]
            #print(f"   speaker name: {speakers['Name'][sid]}")
            if speaker_name_combined:
                speaker_name_combined += f"\n{sn}"
            else:
                speaker_name_combined = sn
        if not speaker_name_combined == row['Speaker names']:
            print(f"WARN name discrepancies in session {idx}!")
            ret = False
    return(ret)

          
def check_session_type_time_vs_duration():
    for idx, row in sessions.iterrows():
        t = row['Session type']
        du = row['Duration']
        minutes = session_type_times[t]
        hours = minutes // 60
        remmin = minutes % 60
        session_time = "{:02d}:{:02d}".format(hours, remmin)
        if not minutes == du:
            print("Time discrepancy")
            print(f"   Session ID = {idx}")
            print(f"   session type = {t}")
            print(f"   session type length = {minutes}")
            print(f"   duration = {du}")



DRY_RUN = True
if not do_checks():
    print("Inconsistencies found, aborting")
    sys.exit(1)
print("=========== checking session times against durations of sessions =====")
check_session_type_time_vs_duration()
create_tracks()
print(json.dumps({"track_ids": track_to_eventyay_id}))
create_sessions()
print(json.dumps({"session_ids": session_id_to_eventyay_id}))
create_session_types()
print(json.dumps({"session_type_ids": session_type_to_eventyay_id}))
print(json.dumps({"session_type_to_session_eventyay_ids": session_type_to_session_eventyay_ids}))
create_speakers()
print(json.dumps({"speaker_ids": speaker_id_to_eventyay_id}))
print(json.dumps({"speaker_to_session_ids": speaker_id_to_session_eventyay_ids}))

DRY_RUN = False
speaker_id_to_eventyay_id = dict()
track_to_eventyay_id = dict()
session_type_to_eventyay_id = dict()
session_id_to_eventyay_id = dict()

session_type_to_session_eventyay_ids = dict()
speaker_id_to_session_eventyay_ids = dict()

yn = input("Actually do the import? [y/N] ")
if yn == 'y' or yn == 'Y':
    pass
else:
    print("Ok, stopping here!")
    sys.exit(0)
create_tracks()
print(json.dumps({"track_ids": track_to_eventyay_id}))
create_sessions()
print(json.dumps({"session_ids": session_id_to_eventyay_id}))
create_session_types()
print(json.dumps({"session_type_ids": session_type_to_eventyay_id}))
print(json.dumps({"session_type_to_session_eventyay_ids": session_type_to_session_eventyay_ids}))
create_speakers()
print(json.dumps({"speaker_ids": speaker_id_to_eventyay_id}))
print(json.dumps({"speaker_to_session_ids": speaker_id_to_session_eventyay_ids}))
