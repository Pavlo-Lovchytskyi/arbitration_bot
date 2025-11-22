import re
from listings.const import MONTHS


months = MONTHS

def parse_date(date_str):
    date_str = date_str.strip()

    if date_str == "N/A":
        return None

    full_date = re.match(r"([A-Za-z]+) (\d{1,2}), (\d{4})", date_str)
    if full_date:
        month = months[full_date.group(1)]
        day = int(full_date.group(2))
        year = int(full_date.group(3))
        return year, month, day

    month_year = re.match(r"([A-Za-z]+) (\d{4})", date_str)
    if month_year:
        month = months[month_year.group(1)]
        year = int(month_year.group(2))
        return year, month

    quarter = re.match(r"Q([1-4]) (\d{4})", date_str)
    if quarter:
        q = int(quarter.group(1))
        year = int(quarter.group(2))
        month = (q - 1) * 3 + 1
        return year, month

    if re.match(r"\d{4}$", date_str):
        return int(date_str), None

    return None
