from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from pathlib import Path
import smtplib

from utils.db_api.orm_func import get_email


subject = ''


message = MIMEMultipart()
message['from'] = 'Accountant Bot'
message['to'] = get_email()
message['subject'] = 'Ваши расходы'
message.attach(MIMEText(subject, 'plain'))
message.attach(MIMEImage(Path('graphs.pdf').read_bytes))


with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.loggin('test_user@gmail.com', 'password')
    smtp.send_message(message)
