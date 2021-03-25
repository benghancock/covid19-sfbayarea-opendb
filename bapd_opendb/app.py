import argparse
import sqlite3
import sqlite_utils

from pathlib import Path
from bapd_opendb import data_fetcher
from bapd_opendb import build_db

DB_PATH = "BAPD_OPENDB.db"


def parse_args():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)

    mode.add_argument(
        "--init",
        action="store_true",
        help="Initialize a new database with fresh data"
    )

    mode.add_argument(
        "--upsert",
        action="store_true",
        help="Fetch data and do an update-or-insert operation"
    )

    return parser.parse_args()


def main():
    args = parse_args()
    raw_data = data_fetcher.fetch_latest_data()
    unified_series = build_db.make_unified_timeseries(raw_data)

    if args.init:
        try:
            db = build_db.setup_db(DB_PATH)
            db["timeseries"].insert_all(unified_series)
            print(f"Set up new database as {DB_PATH}")

        except sqlite3.OperationalError:
            print(f"Could not create new database {DB_PATH}")
            print("Have you already created it?")

    elif args.upsert:
        if Path(DB_PATH).is_file():
            db = sqlite_utils.Database(DB_PATH)
            print(f"Upserting data ...")

            db["timeseries"].upsert_all(
                unified_series,
                pk=("date", "county", "metric")
            )

            print(f"Successfully upserted data to {DB_PATH}")

        else:
            print("Database doesn't exist yet")
            print("Try running with the '--init' option")


if __name__ == "__main__":
    main()
