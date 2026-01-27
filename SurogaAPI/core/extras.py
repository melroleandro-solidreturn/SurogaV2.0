
import threading
import logging
import requests
import json
from azure.identity import ClientSecretCredential
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
import smtplib

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
class EmailThreadOld(threading.Thread):

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



class EmailThread(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        super().__init__()

    
    def run(self):
        try:
            # Extrai dados do dicionário
            msg = self.email_message["message"]
            subject = msg["subject"]
            body = msg["body"]["content"]
            content_type = msg["body"]["contentType"].lower()
            
            # Converte destinatários para lista simples
            to_emails = [
                recipient["emailAddress"]["address"] 
                for recipient in msg["toRecipients"]
            ]
            
            # Cria objeto de e-mail
            email = EmailMultiAlternatives(
                subject=subject,
                body=body if content_type == "text" else "",
                from_email=settings.CONTABO_SMTP_USER,
                to=to_emails
            )
            
            # Adiciona versão HTML se necessário
            if content_type == "html":
                email.attach_alternative(body, "text/html")
            
            # Configura conexão SMTP
            email.connection = self.get_smtp_connection()
            
            # Envia o e-mail
            email.send(fail_silently=False)
            print("Email enviado com sucesso via SMTP!")

        except smtplib.SMTPResponseException as e:
            print(f"SMTP Error {e.smtp_code}: {e.smtp_error}")
        except smtplib.SMTPServerDisconnected as e:
            print(f"Server disconnected: {str(e)}")
        except OSError as e:
            print(f"OS Error: {str(e)}")
        
    def get_smtp_connection(self):
        from django.core.mail import get_connection
        
        # Adicione logs detalhados
        print(f"Conectando a {settings.CONTABO_SMTP_HOST}:{settings.CONTABO_SMTP_PORT}")
        print(f"TLS: {settings.CONTABO_SMTP_USE_TLS}, SSL: {settings.CONTABO_SMTP_USE_SSL}")

        # Configuração SMTP da Contabo (ajuste conforme seu servidor)
        return get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host=settings.CONTABO_SMTP_HOST,  # Ex: 'smtp.contabo.com'
            port=settings.CONTABO_SMTP_PORT,  # Ex: 587
            username=settings.CONTABO_SMTP_USER,  # Ex: 'api@greenconnections.eu'
            password=settings.CONTABO_SMTP_PASSWORD,
            use_tls=settings.CONTABO_SMTP_USE_TLS,  # True para porta 587
            use_ssl=settings.CONTABO_SMTP_USE_SSL  # True para porta 465
        )    
