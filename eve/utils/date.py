# coding:utf8
import datetime
import time
import re
import pytz

timezone = pytz.timezone('Asia/Saigon') #set your timezone
DATE_RE = re.compile('\d+-\d+-\d+)(\s\d+:\d+:\d+)*|(\d+\/\d+\/\d+')


def getCurrentDateStr(date_type=False, datetime_type=True):
    if date_type:
        return datetime.datetime.now().strftime('%Y-%m-%d')
    if datetime_type:
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def parseLocalDatetimeToUTC(self, loalDatetime):
    return timezone.localize(loalDatetime).astimezone(pytz.utc)


def parseUTCDatetimeToLocal(self, utcDatetime):
    return utcDatetime.astimezone(timezone)


def parseDateString(dateStr):
    if not dateStr:
        return None
    if type(dateStr) == unicode:
        dateStr = dateStr.encode('utf8')
    mDate = DATE_RE.search(dateStr)
    if mDate:
        dateStr = mDate.group()
    else:
        return None
    # dateStr = dateStr.strip().split(".")[0]
    # dateStr = dateStr.replace('年', '-').replace('月', '-').replace('日', '')
    if len(dateStr) <= 5 and len(dateStr) >= 4:
        if dateStr[-1] == '-':
            dateStr += '01-01'
        else:
            dateStr += '-01-01'
    if len(dateStr) <= 7 and dateStr[-1] != '-':
        dateStr += '-01'
    if (len(dateStr) == 8 and dateStr[-1] == '-'):
        dateStr += '01'
    if len(dateStr) == 7 and dateStr[-1] == '-':
        dateStr += '01'
    if dateStr == '':
        return None
    try:
        if dateStr.find(':') > -1:
            dateArray = datetime.datetime.strptime(dateStr, "%Y-%m-%d %H:%M:%S")
        else:
            dateArray = datetime.datetime.strptime(dateStr, "%Y-%m-%d")
    except:
        dateArray = None
    if (not dateArray) or dateArray.year < 1900:
        return None
    return parseLocalDatetimeToUTC(dateArray)


def parseToTimestamp(datetime):
    return int(time.mktime(datetime.timetuple()))


if __name__ == '__main__':
    print parseToTimestamp(datetime.datetime.now())
