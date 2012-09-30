"""
Utility functions.
"""
import smtplib
from django.conf import settings


def send_mail(
    to=settings.COMMITTEE_EMAIL,
    subject="Message from the Sub Aqua site",
    message="Blank message.",
    reply_to=None
    ):

    gmail_user = settings.GMAIL_SEND_USER
    gmail_pass = settings.GMAIL_SEND_PASS

    if not reply_to:
        reply_to = gmail_user

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pass)
    body = "\r\n".join([
        'From: %s' % gmail_user,
        'To: %s' % to,
        'Reply-To: %s' % reply_to,
        'Subject: %s' % subject,
        '', # Empty line separates header from message.
        message
    ])
    print "Body is \r\n", body
    server.sendmail(gmail_user, to, body)

    server.quit()
