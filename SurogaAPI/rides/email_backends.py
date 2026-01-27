import smtplib
from email.mime.text import MIMEText
from requests_oauthlib import OAuth2Session

class OAuth2SMTPBackend:
    def __init__(self, oauth2_token):
        self.oauth2_token = oauth2_token

    def send_email(self, subject, body, from_email, to_emails):
        # Connect to SMTP server
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.ehlo()
        server.starttls()

        # OAuth2 authentication
        auth_string = f'user={from_email}\1auth=Bearer {self.oauth2_token}\1\1'
        server.docmd('AUTH', 'XOAUTH2 ' + auth_string)

        # Prepare email
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = ', '.join(to_emails)

        # Send email
        server.sendmail(from_email, to_emails, msg.as_string())
        server.quit()