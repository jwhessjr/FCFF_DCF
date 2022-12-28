import json

import requests


def get_financial_data(ticker):
    url = "https://query1.finance.yahoo.com/v10/finance/quoteSummary/{}?formatted=true&lang=en-US&region=US&modules=financialData".format(
        ticker
    )
    # response = requests.get(url)
    # data = json.loads(response.text)
    # return data["quoteSummary"]["result"][0]["financialData"]

    try:
        # Make the API request
        response = requests.get(url)

        # Parse the JSON response
        data = json.loads(response.text)
    except json.decoder.JSONDecodeError:
        # Handle the error
        print("Error parsing JSON response")


def calc_intrinsic_value(financial_data, required_return=0.1):
    # Get the free cash flow for the next 10 years
    free_cash_flow = financial_data["freeCashflow"]["raw"]
    growth_rate = financial_data["growthRate"]["raw"]

    # Calculate the intrinsic value using the Gordon Growth Model
    intrinsic_value = free_cash_flow / (required_return - growth_rate)

    return intrinsic_value


ticker = "AAPL"
financial_data = get_financial_data(ticker)
intrinsic_value = calc_intrinsic_value(financial_data)
print(intrinsic_value)
