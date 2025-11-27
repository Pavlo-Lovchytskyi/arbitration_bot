import requests

from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
from dateutil.parser import parse


def get_url(url: str) -> str:
    html = requests.get(url=url).text
    return html

def parse_date(date_str: str) -> tuple:
    try:
        dt = parse(date_str, fuzzy=True)
        return dt.year, dt.month, dt.day
    except:
        return None

def get_info() -> list:
    html = get_url("https://icoanalytics.org/token-generation-events/")
    soup = bs(html, "lxml")

    names = [n.text.strip() for n in soup.select("h5.cointitle")]

    dates = [d.text.strip() for d in soup.select("div.hpt-col3")[1:]]

    links = [a["href"] for a in soup.select("a.t-project-link")]

    result = []
    for i in range(len(names)):
        name = names[i] if i < len(names) else ""
        date_str = dates[i] if i < len(dates) else ""
        link = links[i] if i < len(links) else ""
        result.append((name, link, date_str))

    return result

def print_coin():
    coins = get_info()
    today = datetime.today()
    week_later = today + timedelta(days=7)

    result = []

    for name, url, date_str in coins:
        parsed = parse_date(date_str)
        if not parsed:
            continue

        year, month, day = parsed
        listing_date = datetime(year, month, day)

        if today <= listing_date <= week_later:
            date_text = listing_date.strftime("%d.%m.%Y")
            result.append(f"{name}   {date_text}   {url}")

    return "\n".join(result)
