from concurrent.futures import ThreadPoolExecutor
import json
import os
import requests
from functools import partial

from jsonschema import validate
from jsonschema.exceptions import ValidationError
from sqlalchemy.orm import Session

from ctw_assignment.model import FinancialData, Base
from ctw_assignment import get_db_conn
BASE_URL = "www.alphavantage.co"


def get_raw_data(session, apikey, ticker):
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": ticker,
        "apikey": apikey,
        "outputsize": "compact",
    }
    url = f"https://{BASE_URL}/query"
    r = session.get(url, params=params)
    # Raise if status is not successful
    r.raise_for_status()

    data = r.json()
    return data


def map_response_to_rows(data):
    symbol = data["Meta Data"]["2. Symbol"]
    return [
        {
            "symbol": symbol,
            "date": date,
            "open_price": daily_data["1. open"],
            "close_price": daily_data["4. close"],
            "volume": daily_data["6. volume"]
        }
        for date, daily_data
        in data["Time Series (Daily)"].items()
    ]


def main():
    tickers = ["IBM", "AAPL"]
    apikey = os.environ["APIKEY"]
    

    with open("src/ctw_assignment/api_response_schema.json", "rb") as f:
        schema = json.load(f)
    engine = get_db_conn()
    Base.metadata.create_all(engine)

    with (
        requests.Session() as request_session,
        ThreadPoolExecutor(max_workers=3) as executor,
        Session(engine) as db_session,
    ):
        part = partial(get_raw_data, request_session, apikey)
        results = executor.map(part, tickers)

        valid, invalid = [], []
        for result in results:
            try:
                validate(result, schema)
            except ValidationError:
                invalid += map_response_to_rows(result)
            else:
                valid += map_response_to_rows(result)

        if valid:
            db_session.bulk_insert_mappings(FinancialData, valid)
            db_session.commit()
