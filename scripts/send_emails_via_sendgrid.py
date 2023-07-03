import os
import csv
import sys
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from sendgrid.helpers.mail import To

csv_file_name = sys.argv[1]
to_emails = []

with open(csv_file_name) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader, None)
    for row in csv_reader:
        to_emails.append(
            To(email=row[0],
               substitutions={
                   '-name-': row[1],
                   '-url-': row[5],
               })
        )

print(f'Emails to be sent to the following email adresses (total: {len(to_emails)}):\n')
for i in to_emails:
    print(i.email)

do_send_ = input('Really send emails? (y/N)? ')

if do_send_.lower() != 'y':
    sys.exit()


# Replace these with your email addresses and names
to_emails_test = [
    To(email='norbert@preining.info',
       name='Norbert Preining',
       substitutions={
           '-name-': 'Norbert',
           '-url-': 'URL1',
       }),
    To(email='preining@logic.at',
       name='Norbert Preining',
       substitutions={
           '-name-': 'NorbertLogic',
           '-url-': 'URL2',
       }),
]

message = Mail(
    from_email=('office@fossasia.org', 'FOSSASIA Office'),
    to_emails=to_emails,
    subject='TEST EMAIL Access codes for Wikimania',
    plain_text_content="""Hi -name-

Here is your access token:
   -url-

A better email is hopefully written by Mario!

Enjoy

The FOSSASIA Team
""",
    is_multiple=True)

try:
    sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sendgrid_client.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)

