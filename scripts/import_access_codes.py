from datetime import datetime
import readline  # noqa
import sys
from getpass import getpass

import requests
import csv
import json

event_identifier = sys.argv[1]
api_url = 'https://api.eventyay.com/v1'
event_url = api_url + '/events/' + event_identifier

event = requests.get(event_url).json()

print('Event:', event['data']['attributes']['name'])

csv_file_name = sys.argv[2]

access_codes = []

with open(csv_file_name) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader, None)
    for row in csv_reader:
        access_codes.append(
            dict(code=row[0], max_quantity=int(row[1]), marketer_id=row[2], ticket_type=row[3])
        )

print(
    f'Data to be imported {len(access_codes)}:\n\n',
    json.dumps(access_codes, indent=2),
)

import_ = input('Import? (y/N)? ')

if import_.lower() != 'y':
    sys.exit()

username = input('Email: ')
password = getpass()

auth = requests.post(
    'https://api.eventyay.com/auth/session',
    json={'email': username, 'password': password},
)
if auth.status_code != 200:
    print('Auth Error:', auth.json())
    sys.exit(-1)
token = auth.json()['access_token']


created = 0
for code in access_codes:
    data = {
        "data": {
            "attributes": {
                "code": code["code"],
                "max_quantity": code["max_quantity"],
                "is-active": True,
                "tickets-number": code['max_quantity'],
                "access-url": f'https://eventyay.com/e/{event_identifier}?code={code["code"]}',
                "valid-from": datetime.now().astimezone().isoformat(),
                "valid-till": event['data']['attributes']['ends-at']
            },
            "type": "access-code",
            "relationships": {
                "event": {"data": {"id": event['data']['id'], "type": "event"}},
                "marketer": {"data": {"id": code["marketer_id"], "type": "user"}},
                "tickets": {"data": [{"id": code["ticket_type"], "type": "ticket"}]}
            },
        }
    }

    access_code_url = api_url + '/access-codes'

    response = requests.post(
        access_code_url,
        json=data,
        headers={
            'Content-Type': 'application/vnd.api+json',
            'Authorization': 'JWT ' + token,
        },
    )

    if response.status_code == 201:
        print(f'{code["code"]}: Access Code created')
        created += 1
    elif response.status_code == 409:
        # Handle Error
        print(f'{code["code"]}: Access Code already exists')
    elif response.status_code != 201:
        print('Error: ', response, response.content)
    
print(f'{created} access codes created')
