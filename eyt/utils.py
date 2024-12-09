import requests
from dotenv import load_dotenv
import os


def send_email_via_api(subject, message, recipient_email, reply_to_email):
    load_dotenv()
    api_key = os.getenv('SENDINBLUE_API_KEY')  # Replace with your Brevo API key
    url = 'https://api.brevo.com/v3/smtp/email'
    headers = {
        'Content-Type': 'application/json',
        'api-key': api_key,
    }
    data = {
        'sender': {'name': 'Table Tennis Website', 'email': 'eduardo.tomoike@hotmail.com'},
        'to': [{'email': recipient_email}],
        'replyTo': {'email': reply_to_email},  # Set the "Reply-To" header
        'subject': subject,
        'htmlContent': f'''
        <p>{message}</p>
        <p>You can reply to this email directly to contact the sender.</p>
    ''',
    }
    response = requests.post(url, json=data, headers=headers)
    return response.status_code, response.json()
