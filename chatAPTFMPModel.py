import json

import requests


def get_financial_data(ticker):
    api_key = "83968f6306c788e28e55925ceabc45e1"
    url = "https://financialmodelingprep.com/api/v3/financials/income-statement/{}?apikey={}".format(
        ticker, api_key
    )
    response = requests.get(url)
    data = json.loads(response.text)
    return data["financials"]


def calc_intrinsic_value(financial_data, required_return=0.1):
    # Get the free cash flow for the next 10 years
    free_cash_flow = financial_data[0]["Free Cash Flow"]
    growth_rate = financial_data[0]["Growth Rate"]

    # Calculate the intrinsic value using the Gordon Growth Model
    intrinsic_value = free_cash_flow / (required_return - growth_rate)

    return intrinsic_value


ticker = "AAPL"
financial_data = get_financial_data(ticker)
print(financial_data)
intrinsic_value = calc_intrinsic_value(financial_data)
print(intrinsic_value)
