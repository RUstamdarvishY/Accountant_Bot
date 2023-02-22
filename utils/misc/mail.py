import smtplib
from email.message import EmailMessage
from pathlib import Path

from decouple import config


def send_email(reciever):
    email_user = config('EMAIL_USER')
    email_password = config('EMAIL_PASSWORD')
    body = 'Расходы за промежуток времени с графиками'

    msg = EmailMessage()
    msg['subject'] = "Ваши расходы"
    msg['From'] = email_user
    msg['To'] = reciever
    msg.set_content(body)

    with open(Path.absolute('graphs.pdf') + 'rb') as f:
        file_data = f.read()
        file_name = f.name[-10:]  # graphs.pdf

    msg.add_attachment(file_data, maintype='application',
                       subtype='octet-stream', filename=file_name)

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(email_user, email_password)

        smtp.send_message(msg)
