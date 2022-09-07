from datetime import date
from string import Template 
from bs4 import BeautifulSoup

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import python_weather
import asyncio

SENDER = 'cw_assistant@gmx.de'
RECIEVER = 'christopher-wagner.ruhp@hotmail.de'
PWD = 'GMXPW2022$'
MAILSERVER = 'mail.gmx.de'
PORT = 587
LOCATION = 'Ulm'

# Metod returns current date in readable format
def get_date():
    return date.today().strftime("%d.%m.%Y")

# Method for sending mail containing the newsletter
def send_mail(content):
    s = smtplib.SMTP(MAILSERVER, PORT)
    s.starttls()
    s.login(SENDER, PWD)

    msg = MIMEMultipart('alternative')
    msg['From'] = SENDER
    msg['To'] = RECIEVER
    msg['Subject'] = 'Newsletter vom: ' + get_date()
    msg.attach(MIMEText(content, 'html'))

    s.send_message(msg)
    del msg
    s.quit()

async def get_weather(location):
    async with python_weather.Client() as client:
        weather = await client.get(location)
        temp = weather.current.temperature
        desc = weather.current.description
        avg = ""
        for forecasts in weather.forecasts:
            avg = forecasts.average_temperature
            break
        return temp, desc, avg


# Main method
def main():
    # Change day to todays date
    template = open('mailTemplate.html', 'r')
    content = template.read()
    content = Template(content).safe_substitute(date_today=get_date())

    weather = asyncio.run(get_weather(LOCATION))

    content = Template(content).safe_substitute(location=LOCATION)
    content = Template(content).safe_substitute(avg=weather[2])
    content = Template(content).safe_substitute(desc=weather[1])
    content = Template(content).safe_substitute(temp=weather[0])

    send_mail(content)

if __name__ == '__main__':
    main()
