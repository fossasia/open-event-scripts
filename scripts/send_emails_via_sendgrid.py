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
    from_email=('info@eventyay.com', 'Mario Behling - Eventyay'),
    to_emails=to_emails,
    subject='Your Wikimania Free Ticket',
    plain_text_content="""Hello,

You are receiving this email from the Eventyay platform, which is used to run Wikimania 2023. 

As part of your scholarship, the Wikimania team has reserved a free ticket for you. Please register for free by following this link:

   -url-

The link is valid for one ticket.

Wikimania 2023 will run from 16–19 August in Singapore at the Suntec Singapore Convention and Exhibition Centre and online. Workshops, hackathon and pre-conference activities happen on 15 August while post-conference and city tours happen on 20 August, so please plan to stay for those if you are interested!

Should you encounter any issues, please respond to this email.

Thank you and best regards,

Mario and the Eventyay Team
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

