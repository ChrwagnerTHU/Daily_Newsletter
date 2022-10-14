#! /usr/bin/python3

import json
import os

from datetime import date
from re import X
from string import Template 

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import python_weather
import asyncio

import schedule
import time

import assignmentRequest
import wikiRand
import eventsToday



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
            avg = forecasts.temperature
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
            return ""
        elif "web" in domain:
            return ""
        elif "gmail" in domain:
            return ""
        else:
            return ""
    else:
        return ""

# TODO: Get Stockmarket data
def get_stockData():
    return""

# Main method
def main():

    _ose(_location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

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
            sent = False
            # Try sending max five times
            while count <= 5 and not sent:
                try:
                # Read log file
                    with open (__location__ + "/ressource/log.txt") as l:
                        log = l.read()
                        logUser = user + " -- " + get_date()
                        # Check if todays newsletter has already been sent
                        if not logUser in log:
                            RECIEVER = data['User'][user]['RECIEVER']
                            LOCATION = data['User'][user]['LOCATION']
                            CALENDAR = data['User'][user]['CALENDAR']
                            NAME = user

                            # Get Weather Information
                            weather = asyncio.run(get_weather(LOCATION))

                            # Get Appointments
                            # appointments = get_appointments(__location__)
                            appointments = ""

                            events = eventsToday.getEvents(LOCATION)

                            # Get stock data
                            stock = get_stockData()

                            # Get random Wikipedia Article
                            wiki = wikiRand.main()

                            # Get Mail Template
                            mailTemplate = open(__location__ + '/ressource/mailTemplate.html', 'r')

                            with open (__location__ + "/ressource/htmlDict.json", "r") as h:

                                snipped = json.load(h)

                                # Set general data into template
                                content = mailTemplate.read()
                                content = Template(content).safe_substitute(name=NAME)
                                content = Template(content).safe_substitute(date_today=get_date())

                                # Set Weather data into Template
                                if weather:
                                    with open (__location__ + "/ressource/weatherDict.json", "r") as w:
                                        data = json.load(w)
                                        weatherDesc = data['Weather'][weather[1]]
                                        if not weatherDesc:
                                            weatherDesc = weather[1]
                                        w.close()
                                    weatherSnipped = snipped['WEATHER']
                                    weatherSnipped = Template(weatherSnipped).safe_substitute(location=LOCATION)
                                    weatherSnipped = Template(weatherSnipped).safe_substitute(avg=weather[2])
                                    weatherSnipped = Template(weatherSnipped).safe_substitute(desc=weatherDesc)
                                    weatherSnipped = Template(weatherSnipped).safe_substitute(temp=weather[0])
                                    content = Template(content).safe_substitute(weatherTemplate=weatherSnipped)
                                else:
                                    content = Template(content).safe_substitute(weatherTemplate="")

                                # Set Calendar data into Template
                                if appointments:
                                    calendarSnipped = snipped['CALENDAR']
                                    calendarSnipped = Template(calendarSnipped).safe_substitute(appointmentsToday=appointments)
                                    content = Template(content).safe_substitute(appointmentsTemplate=calendarSnipped)
                                else:
                                    content = Template(content).safe_substitute(appointmentsTemplate="")

                                # Set Stock data into Template
                                if stock:
                                    stockSnipped = snipped['CALENDAR']
                                    stockSnipped = Template(stockSnipped).safe_substitute(stockDev=stock)
                                    content = Template(content).safe_substitute(stockTemplate=stockSnipped)
                                else:
                                    content = Template(content).safe_substitute(stockTemplate="")

                                # Set Wiki article into Template
                                if wiki:
                                    wikiSnipped = snipped['WIKI']
                                    wikiSnipped = Template(wikiSnipped).safe_substitute(wikiUrl=wiki['Link'])
                                    wikiSnipped = Template(wikiSnipped).safe_substitute(wikiText=wiki['Header'])
                                    content = Template(content).safe_substitute(wikiTemplate=wikiSnipped)
                                else:
                                    content = Template(content).safe_substitute(wikiTemplate="")

                                if events:
                                    eventsSnipped = snipped['EVENTS']
                                    eventsSnipped = Template(eventsSnipped).safe_substitute(eventsToday=events)
                                    eventsSnipped = Template(eventsSnipped).safe_substitute(location=LOCATION)
                                    content = Template(content).safe_substitute(eventsTemplate=eventsSnipped)
                                else:
                                    content = Template(content).safe_substitute(eventsTemplate="")

                            h.close()
                            
                            # Send mail
                            send_mail(content)
                            newLog = logUser + "\n"
                            sent = True
                            break
                        else:
                            sent = True
                        l.close()
                except Exception as e:
                    print(str(e))
                    count = count + 1
        # Update log file
        with open (__location__ + "/ressource/log.txt", "a") as l:
            l.write(newLog)
            l.close()
        f.cl)

if __name__ == '__main__':
    schedule.every().day.at("06:00").do(main)
    schedule.every().day.at("07:00").do(main)
    schedule.every().day.at("23:20").do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)