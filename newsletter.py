import json
import os

from datetime import date
from string import Template 
from bs4 import BeautifulSoup

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import python_weather
import asyncio
 
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

# Method get current weather forecast for set location
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

    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    global SENDER
    global PWD
    global MAILSERVER
    global PORT
    global RECIEVER
    global LOCATION
    global NAME

    with open (__location__ + "/config.json", "r") as f:
        data = json.load(f)

        SENDER = data['App']['SENDER']
        PWD = data['App']['PWD']
        MAILSERVER = data['App']['MAILSERVER']
        PORT = data['App']['PORT']

        for user in data['User']:
            RECIEVER = data['User'][user][0]
            LOCATION = data['User'][user][1]
            NAME = user

            mailTemplate = open(__location__ + '/mailTemplate.html', 'r')

            weather = asyncio.run(get_weather(LOCATION))
            with open (__location__ + "/weatherDict.json", "r") as f:
                data = json.load(f)
                weatherDesc = data['Weather'][weather[1]]

            content = mailTemplate.read()
            content = Template(content).safe_substitute(name=NAME)
            content = Template(content).safe_substitute(date_today=get_date())
            content = Template(content).safe_substitute(location=LOCATION)
            content = Template(content).safe_substitute(avg=weather[2])
            content = Template(content).safe_substitute(desc=weatherDesc)
            content = Template(content).safe_substitute(temp=weather[0])

            send_mail(content)

if __name__ == '__main__':
    main()
