



from bs4 import BeautifulSoup

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def outer_func(a,b):
    b=int(b)
    soup = BeautifulSoup(a, 'html.parser')

    td_tags = soup.find_all('td', {'class': 'decisionboxf'})

    text_list=[]

    for td in td_tags:
        text_list.append(td.text.replace("\u30000","").replace("\u3000","").replace("\t",""))

    data=[]
    for i in range(0, len(td_tags), 12):
        data.append(text_list[i:i+12])

    schedule = {
        "１": {'start': '08:50', 'end': '10:30'},
        "２": {'start': '10:40', 'end': '12:20'},
        "３": {'start': '13:10', 'end': '14:50'},
        "４": {'start': '15:05', 'end': '16:45'},
        "５": {'start': '17:00', 'end': '18:40'},
        "６": {'start': '18:55', 'end': '20:35'},
        "７": {'start': '20:45', 'end': '21:35'}
    }
    days = {'月': 0, '火': 1, '水': 2, '木': 3, '金': 4, '土': 5, '日': 6}
    semester={0:"春学期          ",
    1:"秋学期          " }

    def setday(n):
        try:
            n = days[n]  
            today = datetime.datetime.now()
            weekday = int(today.weekday())
            daylow = today + datetime.timedelta(days=n - weekday)
            return str(daylow.date())
        except:
            return -1

    parent_table = soup.find('table', {"cellspacing":"1","cellpadding":"0","width":"100%","border":"0"})
    child_element=parent_table.find_all("a")

    linklist=[]
    for link in child_element:
        linklist.append(link.get('href'))



    loc = {
        "早稲田": "〒169-0051 東京都新宿区西早稲田１丁目６−１",
        "戸山": "〒162-0052 東京都新宿区戸山１丁目２４−１",
        "所沢":"〒359-1164 埼玉県所沢市三ケ島２丁目５７９−１５",
        "西早稲田（旧大久保）":"〒169-8555 東京都新宿区大久保３丁目４−１"
    }
    print(semester[b])

    events=[]
    for t,i in enumerate(data):
        if setday(i[1])!=-1 and i[0]==semester[b]:
            events.append({
            'summary': i[5],
            'location': loc[i[7]],
            'description': i[6]+" "+i[7]+" "+i[8]+" "+linklist[t]+" ",
            'start': {
                'dateTime': setday(i[1])+'T'+schedule[i[2]]["start"]+":00"+"+09:00",
                'timeZone': 'Asia/Tokyo',
            },
            'end': {
                'dateTime': setday(i[1])+'T'+schedule[i[2]]["end"]+":00"+"+09:00",
                'timeZone': 'Asia/Tokyo',
            },
            'recurrence': [
                'RRULE:FREQ=WEEKLY;'
            ],
            'attendees': [
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                {'method': 'popup', 'minutes': 15},
                ],
            },
            })

    return events

def loop(service,ls):
        for i in ls:
            event = service.events().insert(calendarId='primary', body=i).execute()
