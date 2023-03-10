// generate a calendar for a given month and year
// the calendar is a list of strings
// each string represents a week
// the days of the week are numbered 0 to 6
// 0 is Sunday, 6 is Saturday
// the days of the month are numbered 1 to 31
// the first day of the month is the day of the week
// on which it falls
// the last day of the month is the day of the week
// on which it falls
// the calendar is a list of strings
// each string represents a week
// the days of the week are numbered 0 to 6
// 0 is Sunday, 6 is Saturday
// the days of the month are numbered 1 to 31
// the first day of the month is the day of the week
// on which it falls
// the last day of the month is the day of the week
// on which it falls

import calendar
import datetime

def get_calendar(month, year):
    cal = calendar.monthcalendar(year, month)
    cal = [week for week in cal if week[0] != 0]
    cal = [week for week in cal if week[-1] != 0]
    return cal

def get_weekday(day, month, year):
    return datetime.date(year, month, day).weekday()

def get_month_name(month):
    return datetime.date(2000, month, 1).strftime('%B')

def get_month_length(month, year):
    return calendar.monthrange(year, month)[1]

def get_calendar(month, year):
    cal = calendar.monthcalendar(year, month)
    cal = [week for week in cal if week[0] != 0]
    cal = [week for week in cal if week[-1] != 0]
    return cal

def get_weekday(day, month, year):
    return datetime.date(year, month, day).weekday()

def get_month_name(month):
    return datetime.date(2000, month, 1).strftime('%B')

def get_month_length(month, year):
    return calendar.monthrange(year, month)[1]

def get_calendar(month, year):
    cal = calendar.monthcalendar(year, month)
    cal = [week for week in cal if week[0] != 0]
    cal = [week for week in cal if week[-1] != 0]
    return cal


def get_weekday(day, month, year):
    return datetime.date(year, month, day).weekday()


def get_month_name(month):
    return datetime.date(2000, month, 1).strftime('%B')


    

