
from datetime import datetime, time, timedelta
from dateutil.rrule import rrulestr
import requests
from icalendar import Calendar

import os.path
import json


def getAssignments(USER, __location__):

    appointments = ""

    with open (__location__ + "/ressource/config.json", "r") as f:
        data = json.load(f)
        ICS = data['User'][USER]['CALENDAR']
    
    if not ICS:
        return ""

    response = requests.get(ICS)

    ical_data = response.text
    calendar = Calendar.from_ical(ical_data)

    today_min = datetime.combine(datetime.today(), time.min)
    today_max = datetime.combine(datetime.today(), time.max)
    tomorrow = datetime.combine(datetime.today() + timedelta(days=1), time.min)

    for event in calendar.walk("VEVENT"):
        start = event.get("DTSTART").dt
        end = event.get("DTEND").dt

        try:
            if not start.time():
                start = datetime.combine(start, datetime.min.time())
                end = datetime.combine(end, datetime.min.time())
        except:
            start = datetime.combine(start, datetime.min.time())
            end = datetime.combine(end, datetime.min.time())
        
        try:
            start = start.replace(tzinfo=None)
            end = end.replace(tzinfo=None)
        except:
            pass

        occurrences = ""
            
        if 'RRULE' in event:
            recurrence_rule = event['RRULE']
            rule = rrulestr(recurrence_rule.to_ical().decode())
            occurrences = [occ.replace(tzinfo=None) for occ in rule]

        if (today_min <= start <= today_max) or ([dt for dt in occurrences if today_min <= dt <= today_max]) :
            if start.time() == time.min:
                appointments = appointments + event.get("SUMMARY") + "<br><br>"
            elif end >= tomorrow :
                appointments = appointments + event.get("SUMMARY") + " von: " + str(event.get("DTSTART").dt.strftime("%H:%M")) + " Uhr<br><br>"
            else:
                appointments = appointments + event.get("SUMMARY") + " von: " + str(event.get("DTSTART").dt.strftime("%H:%M")) + " bis: " + str(event.get("DTEND").dt.strftime("%H:%M")) + " Uhr<br><br>"
    
    # Remove last <br>
    appointments = appointments[:-4]
    return appointments
    

if __name__ == '__main__':
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    getAssignments("Christopher", __location__)