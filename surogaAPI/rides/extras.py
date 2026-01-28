
import threading
import logging
import requests
import json
from azure.identity import ClientSecretCredential
from django.conf import settings
from rides.models import Booking
from core.extras import EmailThread 
from django.template.loader import render_to_string


class BookRoomThread(threading.Thread):
    def __init__(self, booking_pk, start_time, end_time):
        threading.Thread.__init__(self)
        self.booking_pk = booking_pk
        self.start_time = start_time
        self.end_time = end_time

    def run(self):
        url = settings.WEBRTC_URL_BOOKING
        headers = {
            "Authorization": f"Token {settings.WEBRTC_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "start_time": self.start_time,
            "end_time": self.end_time,
        }

        booking = Booking.objects.get(pk=self.booking_pk)
                
        Failed = False
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            if response.status_code == 201:
                output = response.json()
                booking = Booking.objects.get(pk=self.booking_pk)
                booking.MeetingURL = output["room"]
                booking.MeetingPasswd = output["pw"] 
                booking.save()
                print("Booking successful:", output)
            else:
                Failed = True
        except Exception as e:
            Failed = True
        
        if Failed:
            mail_backoffice = settings.EMAILMARKET
            
            message = render_to_string('emails_backoffice/booking_status_changed.html', {
                'UserID': booking.user.pk,
                'User': booking.user.username,
                'RideID': booking.ride.pk if booking.ride else None,  
                'Title': booking.ServiceTitle,
                'BookedID': booking.pk,
                'RideURL': settings.DOMAIN+'/admin/rides/ride/'+str(booking.ride.pk)+'/change/' if booking.ride else None,
                'BookingURL': settings.DOMAIN+'/admin/rides/booking/'+str(booking.pk)+'/change/',
                'STATUS': 'Failed Booking virtual room',
            })
            
            # Define email message
            email_message = {
                "message": {
                    "subject": 'Support: Booking virtual room Failed',
                    "body": {
                        "contentType": "Text",
                        "content": message
                    },
                    "toRecipients": [
                        {
                            "emailAddress": {
                                "address":  mail_backoffice
                            }
                        }
                    ]
                }
            }
            
            EmailThread(email_message).start()




# Create and start the thread
def book_room_async(booking_pk, start_time, end_time):
    booking_thread = BookRoomThread(booking_pk, start_time, end_time)
    booking_thread.start()
    
