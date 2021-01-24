"""Module for handling data fetching"""

import requests


BAPD_JSONDATA_URL = "https://raw.githubusercontent.com/sfbrigade/stop-covid19-sfbayarea/master/data/data.v2.json"


def fetch_latest_data():
    r = requests.get(url=BAPD_JSONDATA_URL)
    data = r.json()
    return data
