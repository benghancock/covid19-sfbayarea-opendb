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


def make_unified_timeseries(raw_data: dict) -> list:
    """
    Transform several separate timeseries data sets into one
    set of 'tidy' records that can be made into a single table
    """
    unified_series = []
    all_series = preprocess_data(raw_data)

    for series, records in all_series.items():

        for record in records:

            date = record.get("date")
            county = record.get("county")

            for k, v in record.items():

                if k != "county" and k != "date":
                    tidy_record = {
                        "date": date,
                        "county": county,
                        "metric": k,
                        "value": v
                    }

                    unified_series.append(tidy_record)

    return unified_series


def setup_db(db_path: str) -> sqlite_utils.Database:
    """
    Set up the database with appropriate columns and composite PK
    """
    db = sqlite_utils.Database(db_path)

    db["timeseries"].create({
        "date": str,
        "county": str,
        "metric": str,
        "value": int,
    }, pk=("date", "county", "metric"))

    return db
