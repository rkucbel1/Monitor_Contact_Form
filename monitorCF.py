#Check for new messages in the contact database table and forward message by email
import requests
import json
import smtplib
from email.message import EmailMessage
import os

email_to = os.environ.get('EMAIL_TO')
email_from = os.environ.get('EMAIL_FROM')
email_psswd = os.environ.get('EMAIL_APP_PSSWD')
link = os.environ.get('LINK_CONTACT')
token = os.environ.get('PA_API_TOKEN')
smtp_server = os.environ.get('EMAIL_SMTP_SERVER')

def send_email(name, email, message, time):

    msg = EmailMessage()
    msg['Subject'] = 'Contact from: ' + email
    msg['From'] = email_from
    msg['To'] = email_to
    msg.set_content('From: ' + name + '\n\n' + 'At: ' + time + '\n\n' + message)

    print('sending email...')

    with smtplib.SMTP_SSL(smtp_server, 465) as smtp:
        smtp.login(email_from, email_psswd)
        smtp.send_message(msg)

def flip_Y_to_N(id, name, email, message, timestring):
    
    url = link + str(id) + '/'
    headers = {'Authorization': token}

    payload = {
       'name': name,
       'email': email,
       'message': message,
       'time_string': timestring,
       'is_new_message': 'N',
    }

    resp = requests.put(url, headers=headers, data=payload)
    print(resp)

#From the contact database table, load the messages
url = link
data = requests.get(url)
contacts = json.loads(data.text)

#Check the messages if they are new and email it if yes. Then mark it as old
for contact in contacts:
    if contact['is_new_message'] == 'Y':
        print('id', contact['id'], '=> NEW')
        flip_Y_to_N(contact['id'], contact['name'], contact['email'], contact['message'], contact['time_string'])
        send_email(contact['name'], contact['email'], contact['message'], contact['time_string'])
    else:
        print('id', contact['id'], '=> OLD')
