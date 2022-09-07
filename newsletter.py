import json

from datetime import date
from string import Template 
from bs4 import BeautifulSoup

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import python_weather
import asyncio
 
# Define global variables and set with config from config.json
def init():
    with open ("config.json", "r") as f:
        global SENDER
        global PWD
        global MAILSERVER
        global PORT
        global RECIEVER
        global LOCATION

        SENDER = f.Data.SENDER
        PWD = f.Data.PWD
        MAILSERVER = f.Data.MAILSERVER
        PORT = f.Data.PORT
        RECIEVER = f.User.RECIEVER
        LOCATION = f.User.LOCATION

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

# TODO: Read Appointments from Calendar
def get_appointments():
    # Outlook Calendar API
    return""

# TODO: Get Stockmarket data
def get_stockData():
    return""

# Main method
def main():
    mailTemplate = open('mailTemplate.html', 'r')
    weather = asyncio.run(get_weather(LOCATION))

    content = mailTemplate.read()
    content = Template(content).safe_substitute(date_today=get_date())
    content = Template(content).safe_substitute(location=LOCATION)
    content = Template(content).safe_substitute(avg=weather[2])
    content = Template(content).safe_substitute(desc=weather[1])
    content = Template(content).safe_substitute(temp=weather[0])

    send_mail(content)

if __name__ == '__main__':
    init()
    main()