"""Build a simple sqlite database from the BAPD's JSON data"""

import sqlite_utils


def preprocess_data(raw_data: dict) -> dict:
    """
    Parse timeseries data for each county; inserting the county name
    into each record and return a dict of lists, one for each series
    """
    all_series = {}

    for county in raw_data.keys():
        county_name_clean = county.replace("_", " ").title()
        series_list = list(raw_data[county]["series"].keys())

        for series in series_list:
            # create stub in container for series
            if all_series.get(series):
                pass
            else:
                all_series[series] = []

            records = raw_data.get(county) \
                              .get("series") \
                              .get(series)

            for record in records:
                county_info = {"county": county_name_clean}
                record.update(county_info)
                all_series[series].append(record)

    return all_series


def setup_db(db_path: str) -> sqlite_utils.Database:
    # Set a compound primary key on 'date' and 'county', since we only have one
    # observation per day. This will allow easy upserts to the DB without knowing
    # or keeping track of an ID.

    db = sqlite_utils.Database(db_path)

    db["cases"].create({
        "date": str,
        "county": str,
        "cases": int,
        "cumul_cases": int,
    }, pk=("date", "county"))

    db["deaths"].create({
        "date": str,
        "county": str,
        "deaths": int,
        "cumul_deaths": int
    }, pk=("date", "county"))

    db["tests"].create({
        "date": str,
        "county": str,
        "tests": int,
        "positive": int,
        "negative": int,
        "pending": int,
        "cumul_tests": int,
        "cumul_pos": int,
        "cumul_neg": int,
        "cumul_pend": int,
        "positivity": float
    }, pk=("date", "county"))

    return db


def insert_records(processed_data: dict, db: sqlite_utils.Database) -> None:
    cases = processed_data.get("cases")
    deaths = processed_data.get("deaths")
    tests = processed_data.get("tests")

    db["cases"].insert_all(cases)
    db["deaths"].insert_all(deaths)
    db["tests"].insert_all(tests)

    return None
