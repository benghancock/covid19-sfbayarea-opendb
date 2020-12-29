"""Build a simple sqlite database from the BAPD's JSON data"""

import json
import sqlite_utils

db = sqlite_utils.Database("../covid19_sfbayarea.db")

# Pre-process the data by inserting the county name into each record.
with open("../data/data.v2.json") as data_file:
    data = json.load(data_file)

cases = []

for county in data.keys():
    county_cases = data[county]["series"].get("cases")

    for record in county_cases:
        county_name_clean = county.replace("_", " ").title()
        county_info = {"county": county_name_clean}
        record.update(county_info)
        cases.append(record)

# Set a compound primary key on 'date' and 'county', since we only have one
# observation per day. This will allow easy upserts to the DB without knowing
# or keeping track of an ID.

db["cases"].create({
    "date": str,
    "county": str,
    "cases": int,
    "cumul_cases": int,
}, pk=("date", "county"))

db["cases"].insert_all(cases)
