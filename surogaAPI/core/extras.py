
import threading
import logging
import requests
import json
from azure.identity import ClientSecretCredential
from django.conf import settings

#from django.core.mail import EmailMessage

"""
Core Application Extra Utilities - Suroga API

This file provides supplementary utility classes and functions that augment the functionality of the Core application 
within the Suroga API. These utilities are not directly bound to models or views but provide important 
background capabilities such as asynchronous email sending.

Utility classes and functions included in this module:
- EmailThread: A utility class that extends Python's threading.Thread to enable asynchronous email sending. This allows 
  the application to send emails without blocking the response cycle of the request handler, improving the user experience by 
  decreasing wait times for actions that include email sending.

Usage of this class should be limited to lightweight background tasks to avoid resource-heavy operations that could interfere 
with the main thread's performance. For more heavy-duty background task handling, consider using a more robust job queuing 
system such as Celery with Redis/RabbitMQ.

Maintainer: Carlos Leandro
Last updated: 15/3/2024

Example usage:
from core.extras import EmailThread
from django.core.mail import EmailMessage

msg = EmailMessage('Subject', 'Message', to=['recipient@example.com'])
EmailThread(msg).start()
"""

# The EmailThread class inherits from Python's built-in Thread class to send emails asyncronously.
class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email_message = email
        super().__init__()  # Cleaner thread initialization

    def run(self):

        credential = ClientSecretCredential(
            tenant_id=settings.O365_MAIL_TENANT_ID,
            client_id=settings.O365_MAIL_CLIENT_ID,
            client_secret=settings.O365_MAIL_CLIENT_SECRET
        )

        # Access token retrieval
        token = credential.get_token("https://graph.microsoft.com/.default")
        access_token = token.token

        # Send email request
        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
        }

        response = requests.post(
            'https://graph.microsoft.com/v1.0/users/api@suroga.com/sendMail',
            json=self.email_message,
            headers=headers
        )

        if response.status_code == 202:
            print("Email sent successfully!")
        else:
            print(f"Failed to send email. Status code: {response.status_code}, {response.text}")

    
