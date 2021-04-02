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


def transform_demographic_data(raw_data: dict) -> list:
    """
    Extract and transform data on different demographic groups from
    a nested dict into a list of dicts, in a 'tidy' data format
    """
    transformed_data = []

    for county in raw_data.keys():
        county_name_clean = county.replace("_", " ").title()
        update_time = raw_data.get(county).get("update_time")

        datasets = ["case_totals", "death_totals"]

        for dataset in datasets:
            data = raw_data.get(county).get(dataset)

            if data:
                for k, v in data.items():
                    # Datasets are structured with keys describing a
                    # demographic category (e.g. "gender") and values being
                    # either a dict or a list of dicts, with key-value pairs
                    # giving the group name (e.g "female") and the value for
                    # the metric

                    category = k

                    if isinstance(v, dict):
                        for group, value in v.items():

                            record = {
                                "county": county_name_clean,
                                "update_time": update_time,
                                "category": category,
                                "group": group,
                                "metric": dataset,
                                "value": value
                            }

                            transformed_data.append(record)

                    elif isinstance(v, list):
                        for _ in v:
                            for group, value in _.items():
                                if category == "age_group":
                                    group = _.get("group")
                                    value = _.get("raw_count")

                                else:
                                    pass

                                record = {
                                    "county": county_name_clean,
                                    "update_time": update_time,
                                    "category": category,
                                    "group": group,
                                    "metric": dataset,
                                    "value": value
                                }

                            transformed_data.append(record)

                else:
                    pass

    return transformed_data


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

    db["demographic_totals"].create({
        "county": str,
        "update_time": str,
        "category": str,
        "group": str,
        "metric": str,
        "value": int
    }, pk=("county", "update_time", "category", "group", "metric"))

    return db
