from bs4 import BeautifulSoup
import requests
import argparse
import pandas as pd
import time
import sys

URL_FORMAT = "https://dateandtime.info/citysunrisesunset.php?id={country_id}&month={month}&year=2021"

COUNTRY_TO_ID = {
    "ireland": 2964574, # Dublin
    "finland": 652590,  # Kittilä
    "ecuador": 3652462  # Quito
}

def scrape_month(country_id, month):
    month_data = []
    page = requests.get(URL_FORMAT.format(**locals()))
    soup = BeautifulSoup(page.text, features="lxml")
    # It's the second table with this class.
    table = soup.find_all("table", class_="sunrise_table")[1]
    for row in table.find_all("tr"):
        cells = row.find_all("td")
        if not cells:
            pass
        elif len(cells) == 5:
            date = extract_date(cells[0])
            sunrise = extract_time(cells[1])
            sunset = extract_time(cells[2])
            month_data.append((date, sunrise, sunset))
        elif len(cells) == 4 and "Midnight sun" in cells[1].text:
            date = extract_date(cells[0])
            month_data.append((date, "0:00", "23:59"))
        elif len(cells) == 4 and "Polar night" in cells[1].text:
            date = extract_date(cells[0])
            month_data.append((date, "0:00", "0:00"))
        else:
            print(f"error: dunno how to parse these fuggin cells!")
            for i, cell in enumerate(cells):
                print("==========")
                print("cell", i+1)
                print(cell)
            sys.exit(1)
    return month_data

def parse_time(t):
    # Woops, copy/pasted this from the notebook.
    hour, minute = map(int, t.split(":"))
    return 60*hour + minute

def extract_date(cell):
    return cell.text.strip().replace("  ", " ")

def extract_time(cell):
    return cell.text.strip().split("\n")[0]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--name",
        choices=list(COUNTRY_TO_ID.keys()))
    args = parser.parse_args()

    country_name = args.name
    country_id = COUNTRY_TO_ID[country_name]

    data = dict(month=[], date=[], sunrise=[], sunset=[])
    days = 0
    for month in range(1, 13):
        print(f"Downloading month {month}")
        month_data = scrape_month(country_id, month)
        for date, sunrise, sunset in month_data:
            data["month"].append(month)
            data["date"].append(date)
            data["sunrise"].append(sunrise)
            data["sunset"].append(sunset)
            days += 1
        time.sleep(1) # avoid rate-limiting, maybe

    if days != 365:
        # this ain't no damned leap year
        print("error: only", days, "days")
        print("not saving data")
        sys.exit(1)

    df = pd.DataFrame(data)
    df.to_csv(f"{country_name}.csv")

if __name__ == "__main__":
    main()

