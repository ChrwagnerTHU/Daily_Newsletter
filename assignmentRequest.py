from calendar import Calendar
import json
from sqlite3 import SQLITE_CREATE_INDEX
from O365 import Account, MSGraphProtocol
import datetime as dt

def getAssignmentsOutlook(USER, __location__):

    global CLIENT_ID
    global SECRET_ID
    global CALENDAR
    global CAL_DONE

    with open (__location__ + "/config.json", "r") as f:
        data = json.load(f)

        CLIENT_ID = data['User'][USER]['CLIENT_ID']
        SECRET_ID = data['User'][USER]['SECRET_ID']
        CALENDAR = data['User'][USER]['CALENDAR']
        CAL_DONE = data['User'][USER]['CAL_DONE']

    credentials = (CLIENT_ID, SECRET_ID)

    protocol = MSGraphProtocol(defualt_resource=CALENDAR)
    scopes = ['Calendars.Read']
    account= Account(credentials, protocol=protocol)

    # TODO: Dynamic test if account has still to be authenticated
    # if account.authenticate(scopes=scopes):
    #     print('Authenticated!')

    schedule = account.schedule()
    calendar = schedule.get_default_calendar()

    currentDay = dt.datetime.now().day
    currentMonth = dt.datetime.now().month
    currentYear = dt.datetime.now().year

    # Query to get Entries for current day
    q = calendar.new_query('start').greater_equal(dt.datetime(currentYear, currentMonth, currentDay, 0, 1))
    q.chain('and').on_attribute('end').less_equal(dt.datetime(currentYear, currentMonth, currentDay, 23, 59))

    events = calendar.get_events(query=q, include_recurring=False) 

    for event in events:
        text = event.subject + " von: " + event.start.strftime("%H.%M") + " Uhr - bis: " + event.end.strftime("%H.%M") + " Uhr<br>"

    if 'text' in locals():
        size = len(text)
        text = text[:size - 4]
        return text
    else:
        return "Heute sind keine Einträge im Kalender"

def getAssignmentsGmail(USER, __location__):
    return "Uminplemented"

def getAssignmentsGmx(USER, __location__):
    return "Uminplemented"
