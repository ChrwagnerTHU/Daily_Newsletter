import json
from logging import exception
import os

from datetime import date
from string import Template 
from bs4 import BeautifulSoup

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import python_weather
import asyncio

import assignmentRequest

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

# Outlook Calendar API
def get_appointments(__location__):
    # TODO: Get diffrent Calendar providers
    domain = CALENDAR[CALENDAR.index('@') + 1 : ]
    if not domain == "":
        if "outlook" in domain or "hotmail" in domain:
            return assignmentRequest.getAssignmentsOutlook(NAME, __location__)
        elif "gmx" in domain:
            return "Kalender für @gmx ist noch nicht implementiert"
        elif "web" in domain:
            return "Kalender für @web ist noch nicht implementiert"
        elif "gmail" in domain:
            return "Kalender für @gmail ist noch nicht implementiert"
        else:
            return "Kalender ist für die Domain " + domain + " noch nicht implementiert"
    else:
        return ""

# TODO: Get Stockmarket data
def get_stockData():
    return""

# Main method
def main():

    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    # Define global variables
    global SENDER
    global PWD
    global MAILSERVER
    global PORT
    global RECIEVER
    global LOCATION
    global NAME
    global CALENDAR

    # Read Config file
    with open (__location__ + "/ressource/config.json", "r") as f:
        data = json.load(f)

        SENDER = data['App']['SENDER']
        PWD = data['App']['PWD']
        MAILSERVER = data['App']['MAILSERVER']
        PORT = data['App']['PORT']

        log = ""
        newLog = ""
        
        # For each user contained in config file do the folowing
        for user in data['User']:
            # Try sending newsletter
            count = 0
            try:
                # Try sending max five times
                while count <= 5:
                # Read log file
                    with open (__location__ + "/ressource/log.txt") as l:
                        log = l.read()
                        # Check if todays newsletter has already been sent
                        if not (user + " -- " + get_date()) in log or not (user + " -- " + get_date()) in newLog:
                            RECIEVER = data['User'][user]['RECIEVER']
                            LOCATION = data['User'][user]['LOCATION']
                            CALENDAR = data['User'][user]['CALENDAR']
                            NAME = user

                            # Get Weather Information
                            weather = asyncio.run(get_weather(LOCATION))
                            with open (__location__ + "/ressource/weatherDict.json", "r") as w:
                                data = json.load(w)
                                weatherDesc = data['Weather'][weather[1]]
                                w.close()

                            # Get Appointments
                            appointments = get_appointments(__location__)

                            # Get stock data
                            stock = get_stockData()

                            # Get Mail Template
                            mailTemplate = open(__location__ + '/ressource/mailTemplate.html', 'r')

                            # Set data into template
                            content = mailTemplate.read()
                            content = Template(content).safe_substitute(name=NAME)
                            content = Template(content).safe_substitute(date_today=get_date())
                            content = Template(content).safe_substitute(location=LOCATION)
                            content = Template(content).safe_substitute(avg=weather[2])
                            content = Template(content).safe_substitute(desc=weatherDesc)
                            content = Template(content).safe_substitute(temp=weather[0])
                            content = Template(content).safe_substitute(appointmentsToday=appointments)
                            content = Template(content).safe_substitute(stockDev=stock)

                            # Send mail
                            send_mail(content)
                            newLog = user + " -- " + get_date() + "\n"
                            break
                        l.close()
            except:
                pass
        # Update log file
        with open (__location__ + "/ressource/log.txt", "a") as l:
            l.write(log + newLog)
            l.close()
        f.close()




if __name__ == '__main__':
    main()