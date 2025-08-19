
import calendar
import datetime
import xlsxwriter

options = {
    "first-weekday": 0,  # Start the week on a certain day (0: Monday ~ 6: Sunday)
    "day-rows": 5,  # The number of lines occupied per day should be greater than or equal to 1
    "day-cols": 2  # The number of columns occupied per day should be greater than or equal to 1
}

styles = {
    # Header of the calendar
    "header": {"align":"center", "bg_color":"#A6A6A6"},

    # The style of the day block, the first item is the style of the first week, the second item is the style of the second week, and so on.
    "day-block": [{"bg_color":"#C8C8C8"},{"bg_color":"#D9D9D9"}],

    # style day header
    "day-header": {"align":"left"},   

    # block of the day
    "day-text": {},

    # blank day
    "blank-day": {"align":"center", "valign":"vcenter", "bg_color":"#EAEAEA"}, 
}

# styles["day-block"] = [{"bg_color":"#C8C8C8"}]*5+[{"bg_color":"#D9D9D9"}]*2
# styles["blank-day"] = {"align":"center", "valign":"vcenter", "bg_color":"#EAEAEA"}

# styles["header"]["font_size"] = 12
# styles["day-header"]["font_size"] = 12
# styles["day-text"]["italic"] = True

cells_format = {}
cells_value = {}


def write_format(row, col, append_format: dict):
    cell = xlsxwriter.worksheet.xl_rowcol_to_cell_fast(row, col)
    fmt = cells_format[cell].copy() if cell in cells_format else {}
    fmt.update(append_format)
    cells_format[cell] = fmt


def write_formats(s_row, s_col, e_row, e_col, append_format: dict):
    for row in range(s_row, e_row + 1):
        for col in range(s_col, e_col + 1):
            write_format(row, col, append_format)


def write_value(row, col, value):
    cell = xlsxwriter.worksheet.xl_rowcol_to_cell_fast(row, col)
    cells_value[cell] = value


def write_finish(wb: xlsxwriter.Workbook,
                 ws: xlsxwriter.Workbook.worksheet_class):
    values, formats = set(cells_value.keys()), set(cells_format.keys())
    for c in values.difference(formats):
        ws.write(c, cells_value[c])
    for c in values.intersection(formats):
        ws.write(c, cells_value[c], wb.add_format(cells_format[c]))
    for c in formats.difference(values):
        ws.write_blank(c, None, wb.add_format(cells_format[c]))


def generate(year, month, filename):

    fwd = options["first-weekday"]
    calendar.setfirstweekday(fwd)
    weekdays = calendar.monthcalendar(year, month)

    workbook = xlsxwriter.Workbook(filename)
    ws = workbook.add_worksheet()

    rows = 1 + len(weekdays) * options["day-rows"]
    cols = 7 * options["day-cols"]

    span = options["day-cols"]
    for x in range(0, 7 * span, span):
        ws.merge_range(0, x, 0, x + span - 1, None)

    center = {"align": "center"}

    weekdays_title = ["Day: " + d for d in "MTWTFSS"]
    weekdays_title = weekdays_title[fwd:] + weekdays_title[:fwd]
    for x in range(7):
        write_value(0, x * span, weekdays_title[x])
        write_format(0, x * span, styles["header"])

    for w in range(len(weekdays)):
        for d in range(7):
            y, x = 1 + w * options["day-rows"], d * span
            write_formats(y, x, y+options["day-rows"]-1, x+options["day-cols"]-1, styles["day-block"][(w*7+d)%len(styles["day-block"])])
            if weekdays[w][d] == 0:
                ws.merge_range(y, x, y+options["day-rows"]-1, x+options["day-cols"]-1, None)
                write_format(y, x, styles["blank-day"])
            else:
                write_value(y, x, str(weekdays[w][d]) + " day")
                write_format(y, x, styles["day-header"])
                for i in range(1, options["day-rows"]):
                    ws.merge_range(y+i, x, y+i, x+options["day-cols"]-1, None)
                    write_formats(y+i, x, y+i, x+options["day-cols"]-1, styles["day-text"])
            

    border_top = {"top": 1}
    border_bottom = {"bottom": 1}
    border_left = {"left": 1}
    border_right = {"right": 1}

    write_formats(0, 0, 0, cols - 1, border_top)
    write_formats(1, 0, 1, cols - 1, border_top)
    write_formats(0, 0, rows - 1, 0, border_left)

    for col in range(options["day-cols"] - 1, cols, options["day-cols"]):
        write_formats(0, col, rows - 1, col, border_right)

    for row in range(options["day-rows"], rows, options["day-rows"]):
        write_formats(row, 0, row, cols - 1, border_bottom)

    if weekdays[0][0] == 0:
        x = (weekdays[0].index(1)-1) * options["day-cols"]
        write_value(1, x, str(month)+"Marzo")
        write_format(1,x, {"font_size":9+2*options["day-rows"]})

    write_finish(workbook, ws)

    workbook.close()


if __name__ == '__main__':
    today = datetime.date.today()
    filename = "%d-%03d.xlsx" % (today.year, today.month)
    generate(today.year, today.month, filename)
"""

from datetime import date, datetime
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
import pandas as pd

load_dotenv()


def test_dotenv():
    print(os.getenv("RESULTS"))
    res = Path(os.getenv("RESULTS"))
    print(res.exists())


def create_calendar(start_year: int,
                    end_year: int,
                    start_month: Optional[int] = 1,
                    end_month: Optional[int] = 12,
                    start_day: Optional[int] = 1,
                    end_day: Optional[int] = 31,
                    show_year: bool = True,
                    show_quarters: bool = True,
                    show_week_no: bool = True,
                    show_date: bool = True,
                    freq: str = 'D',
                    only_business_days: bool = False):
    """
"""
    :param start_year:
    :param end_year:
    :param show_quarters:
    :param freq: 'D': day, 'M': month, 'Q', quarter.
    :param only_business_days:
    :return:
    """
"""
    mycalendar: pd.DataFrame = pd.date_range(start=date(year=start_year, month=start_month, day=start_day),
                                             end=date(year=end_year, month=end_month, day=end_day),
                                             freq=freq).to_frame(index=False, name="dt_time")
    if show_year:
        mycalendar["year"] = mycalendar.dt_time.dt.year

    if show_quarters:
        mycalendar["quarter_no"] = mycalendar.dt_time.dt.quarter

    if show_quarters:
        mycalendar["quarter_year"] = mycalendar.quarter_no.astype(str) + "-" + mycalendar.dt_time.dt.year.astype(str)

    if show_week_no:
        mycalendar["week_no"] = mycalendar.dt_time.dt.isocalendar().week

    if show_week_no:
        mycalendar["week_year"] = mycalendar.week_no.astype(str) + "-" + mycalendar.dt_time.dt.year.astype(str)

    if show_week_no and show_quarters:
        mycalendar["week_quarter_year"] = mycalendar.week_no.astype(str) + "-" + mycalendar.quarter_no.astype(str) + "-" + mycalendar.dt_time.dt.year.astype(str)

    if not show_date:
        mycalendar.drop("date", axis=1, inplace=True)

    if show_date:
        mycalendar["day_name"] = mycalendar.dt_time.dt.day_name()
        mycalendar["day_of_month_no"] = mycalendar.dt_time.dt.day
        mycalendar["day_of_year_no"] = mycalendar.dt_time.dt.dayofyear
        mycalendar["day_of_week_no"] = mycalendar.dt_time.dt.dayofweek

    mycalendar["date"] = mycalendar.dt_time.dt.date
    mycalendar["month_name"] = mycalendar.dt_time.dt.month_name()

    return mycalendar


if __name__ == "__main__":
    # test_dotenv()
    mycal = create_calendar(start_year=2023, end_year=2023)

    res = Path(os.getenv("RESULTS"))
    mycal.to_excel(res / f'{datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")}_mycal.xlsx', index=False)
    """