import json, requests
from bs4 import BeautifulSoup
from string import Template 
import datetime as dt
import os


def getEvents(location):

    URL = "https://www.regioactive.de/events/$locCode/$location/veranstaltungen-party-konzerte/$date"
    currentDay = dt.datetime.now().day
    currentMonth = dt.datetime.now().month
    currentYear = dt.datetime.now().year
    locCodeStr = ""

    __location__ = os.path.dirname(os.path.abspath(__file__))

    with open (__location__ + "/ressource/eventlocationDict.json", "r") as f:
        locCode = json.load(f)
        locCodeStr = locCode['Location'][location]
        f.close()

    URL = Template(URL).safe_substitute(location=location)
    URL = Template(URL).safe_substitute(date=str(currentYear)+"-"+str(currentMonth)+"-"+str(currentDay))
    URL = Template(URL).safe_substitute(locCode=locCodeStr)

    res = requests.get(URL)
    soup = BeautifulSoup(res.text, "lxml")

    # data = json.loads(soup.find("div", class_="media-body"))
    divTag = soup.find_all("div", {"class": "media-body"})

    result = ""

    cName = ""
    cStart = ""
    cEnd = ""
    cLoc = ""

    for tag in divTag:
        feature = tag.find_all("div", {"class": "featured"})

        # Check if event is a sponsored event
        if feature:
            continue

        name = tag.find_all("span", {"class": "summary"})
        dtStart = tag.find_all("span", {"class": "dtstart"})
        dtEnd = tag.find_all("span", {"class": "dtend"})
        loc = tag.find_all("span", {"class": "locstring"})

        try:
            cName = name[0].text
        except:
            pass
        try:
            cStart = dtStart[0].text
        except:
            pass
        try:
            cEnd = dtEnd[0].text
        except:
            pass
        try:
            cLoc = loc[0].text
        except:
            pass

        cName = cName + " "
        
        if cEnd:
            cEnd = " bis " + cEnd
        
        if  cLoc:
            cLoc = " " + cLoc


        itResult = cName + cStart + cEnd + cLoc + "<br>"
        result = result + itResult + "<br>"

        cName = ""
        cStart = ""
        cEnd = ""
        cLoc = ""
    
    return(result)