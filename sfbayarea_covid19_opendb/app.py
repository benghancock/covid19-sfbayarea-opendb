from sfbayarea_covid19_opendb import data_fetcher
from sfbayarea_covid19_opendb import build_db


def main():
    raw_data = data_fetcher.fetch_latest_data()
    processed_data = build_db.preprocess_data(raw_data)


if __name__ == "__main__":
    main()
