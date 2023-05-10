# Daily_Newsletter
This repository contains some python scripts to assemble a personalized newsletter.

## INFO
This repository is work in progress! Some features or translations might be missing. This newsletter is designed to be sent in German.<br>
Feel free to get some inspiration or use it as it is!

## Configuration
In the folder `resscource` adjust the `config.json`file:

### App
The `App`section handles the Mail sender. 
|Option|Explanation|
|---|---|
|`SENDER`|Senders Email address|
|`PWD`|The password of the senders mail account|
|`MAILSERVER`|The mailserver address|
|`PORT`|Mailport|
|`WEATHER_API`|Your API Key from OpenWeatherMap<br>Get the key [here](https://openweathermap.org/api)

### User
The `User` section handles the "subscribed" users to recieve a newsletter
|Option|Explanation|
|---|---|
|`User1`|Name of the reciever|
|`RECIEVER`|Mail address of the reciever|
|`LOCATION`|Location string to get the weather and the events info from|
|`CALENDAR`|Link to .ics file of calendar. If you don't want to add the calendar, simly leave it empty ("")|

## Event Location 
The file `eventLocationDict.json` contains several locations. If your location isn't in this list, simply add it by looking at [this](https://www.regioactive.de/events/14356/berlin/veranstaltungen-party-konzerte) website. This example is for Berlin. Copy the name and the id, which appears in front of the name in the URL.

## Run it
Run it on a daily basis by adding a CronJob
```
crontab -e
```
Add the following line to send the newsletter every day at 6 in the morning
```
00 06 * * * python3 /home/usr/pathToDir/Daily_Newsletter/newsletter.py
```
