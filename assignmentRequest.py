from calendar import Calendar
import json
from sqlite3 import SQLITE_CREATE_INDEX
from O365 import Account, MSGraphProtocol, FileSystemTokenBackend
import datetime as dt
from calendar import monthrange
import os.path


def getAssignmentsOutlook(USER, __location__):

    global CLIENT_ID
    global SECRET_ID
    global CALENDAR

    with open (__location__ + "/ressource/config.json", "r") as f:
        data = json.load(f)

        CLIENT_ID = data['User'][USER]['CLIENT_ID']
        SECRET_ID = data['User'][USER]['SECRET_ID']
        CALENDAR = data['User'][USER]['CALENDAR']

    credentials = (CLIENT_ID, SECRET_ID)

    protocol = MSGraphProtocol(defualt_resource=CALENDAR)
    scopes = ['Calendars.Read']
    token_backend = FileSystemTokenBackend(token_path=__location__, token_filename='o365_token.txt')
    account = Account(credentials, token_backend=token_backend, protocol=protocol)
    
    # Check if token has already been created
    if not account.is_authenticated:
        account.authenticate(scopes=scopes)

    schedule = account.schedule()
    calendar = schedule.get_default_calendar()

    currentDay = dt.datetime.now().day
    currentMonth = dt.datetime.now().month
    currentYear = dt.datetime.now().year

    #Check if currentDate + 1 is in new month and create query
    if currentMonth == 12 and currentDay == 31:
        q = calendar.new_query('start').greater_equal(dt.date(currentYear, currentMonth, currentDay))
        q.chain('and').on_attribute('start').less_equal(dt.datetime(currentYear + 1, 1, 1))
    elif currentDay + 1 > monthrange(currentYear, currentMonth)[1]:
        q = calendar.new_query('start').greater_equal(dt.date(currentYear, currentMonth, currentDay))
        q.chain('and').on_attribute('start').less_equal(dt.datetime(currentYear,  currentMonth + 1, 1))
    else:
        q = calendar.new_query('start').greater_equal(dt.date(currentYear, currentMonth, currentDay))
        q.chain('and').on_attribute('start').less_equal(dt.datetime(currentYear, currentMonth, currentDay + 1))

    # Query to get Entries for current day
    events = calendar.get_events(query=q, include_recurring=False) 

    result = ""
    for event in events:
        result = event.subject + " von: " + event.start.strftime("%H.%M") + " Uhr - bis: " + event.end.strftime("%H.%M") + " Uhr<br>"

    if result:
        size = len(result)
        result = result[:size - 4]
        return result
    else:
        return "Heute sind keine Einträge im Kalender"

# TODO: Implement Method
def getAssignmentsGmail(USER, __location__):
    return "Uminplemented"

# TODO: Implement Method
def getAssignmentsGmx(USER, __location__):
    return "Uminplemented"

if __name__ == '__main__':
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    getAssignmentsOutlook("Christopher", __location__)