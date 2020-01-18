import smtplib
from email.message import EmailMessage

from typing import Text

class SendEmailWapper():
    @staticmethod
    def send(sender_email: Text, sender_password: Text, receiver_email: Text, subject: Text, body: Text) -> bool:
        try:
            s = smtplib.SMTP("smtp.gmail.com", 587)
            s.starttls()
            s.login(sender_email, sender_password)

            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = sender_email
            msg.set_content(body)

            msg['To'] = receiver_email
            s.send_message(msg)
            s.quit()
            return True
        except:
            return False

