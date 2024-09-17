import smtplib
import threading
from os import getenv

from django.core.mail import BadHeaderError, EmailMessage


class EmailThread(threading.Thread):
    def __init__(
        self, subject: str,
        html_content: str,
        sender: str,
        recipient_list: list[str],
        dev_mode: bool = False,
    ):
        super().__init__()
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        self.sender = sender
        self.dev_mode = dev_mode

    def run(self):
        if self.dev_mode:
            return

        try:
            msg = EmailMessage(
                self.subject, self.html_content,
                self.sender, self.recipient_list
            )
            msg.content_subtype = 'html'
            msg.send()
        except (BadHeaderError, smtplib.SMTPException, ConnectionError):
            pass


def send_html_mail(
    subject: str,
    html_content: str,
    recipient_list: list[str],
    sender: str = getenv('EMAIL_HOST_USER', ''),
    dev_mode: bool = False,
):
    if not sender:
        return

    EmailThread(
        subject=subject,
        html_content=html_content,
        sender=sender,
        recipient_list=recipient_list,
        dev_mode=dev_mode,
    ).start()
