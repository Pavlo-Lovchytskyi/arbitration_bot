import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
from listings.validators import parse_date


def get_url(url) -> str:
    html = requests.get(url=url).text
    return html

def get_info() -> list:
    html = get_url(url="https://coinmarketcap.com/upcoming/")
    soup = bs(html, "lxml")

    rows = soup.select("tbody tr")

    coins = []

    for row in rows:
        link_tag = row.select_one("a[href]")
        if not link_tag:
            continue

        name = link_tag.text.strip()
        href = link_tag["href"].strip()
        full_link = "https://coinmarketcap.com" + href

        tds = row.select("td")
        if len(tds) >= 3:
            first_listing = tds[2].text.strip()
        else:
            first_listing = "N/A"

        coins.append((name, full_link, first_listing))
    return coins

def print_coin():
    coins = get_info()
    today = datetime.today()
    week_later = today + timedelta(days=7)

    result = []

    for name, url, date_str in coins:
        parsed = parse_date(date_str)
        if not parsed:
            continue

        year, month = parsed[0], parsed[1] if len(parsed) > 1 else None
        day = parsed[2] if len(parsed) > 2 else 1

        if not month:
            continue

        listing_date = datetime(year, month, day)

        if today <= listing_date <= week_later:
            date_text = listing_date.strftime("%d.%m.%Y")
            result.append(f"{name}   {date_text}   {url}")

    return "\n".join(result)
