import threading, uuid
from django.conf import settings
from django.core.mail import send_mail
from django.core.cache import cache

class send_verification_email(threading.Thread):
    def __init__(self, email, tok):
        self.email = email
        self.tok = tok
        threading.Thread.__init__(self)
    def run(self):
        try:
            subject = "Link to verify the your Account"
            message = f"The link to verify your email is\n http://127.0.0.1:8000/api/verify/{self.tok}/."
            email_from = settings.EMAIL_HOST_USER
            print("Email send started")
            send_mail(subject , message ,email_from ,[self.email])
            print("Email send finished")
        except Exception as e:
            print(e)
