import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib
from datetime import datetime

load_dotenv()

email_sender = os.getenv("EMAIL_SENDER")
email_password = os.getenv("EMAIL_PASSWORD")
email_receiver = os.getenv("EMAIL_RECEIVERS")

def send_email():
    def read_text_file(file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                return content
        except FileNotFoundError:
            print("File not found.")
        except Exception as e:
            print("An error occurred:", e)

    file_path = "data/report.txt"  

    content = read_text_file(file_path)

    def get_today_date_and_day():
        today = datetime.now()
        today_date = today.strftime("%Y-%m-%d")
        day_name = today.strftime("%A")
        return today_date, day_name

    date, day = get_today_date_and_day()
    subject = f'Next Tech Lab Standup @ {date} ({day})'
    body = read_text_file(file_path)

    em = EmailMessage()
    em["From"] = email_sender
    em['To'] = email_receiver
    em["Subject"] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())