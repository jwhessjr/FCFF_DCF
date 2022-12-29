"""This library is a collection of functions used in the Hess Group DCF model."""


import json
from urllib.request import urlopen

import certifi
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Read statements from Financial Modeling Prep


def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)


# Function to get the income statement and extract the required fields


def get_incStmnt(company, myApiKey):
    url = f"https://financialmodelingprep.com/api/v3/income-statement/{company}?period=quarter&limit=20&apikey={myApiKey}"
    data = get_jsonparsed_data(url)
    incStmnt = {}
    netIncome = []
    interestIncome = []
    totalRevenue = []
    incomeBeforeTax = []
    incomeTaxExpense = []
    ebit = []
    indx = 0
    for year in range(5):
        for qtr in range(indx + 4):
            yearNetIncome = (
                data[indx]["netIncome"]
                + data[indx + 1]["netIncome"]
                + data[indx + 2]["netIncome"]
                + data[indx + 3]["netIncome"]
            )

            yearIntIncome = (
                data[indx]["interestIncome"]
                + data[indx + 1]["interestIncome"]
                + data[indx + 2]["interestIncome"]
                + data[indx + 3]["interestIncome"]
            )

            yearTotalRevenue = (
                data[indx]["revenue"]
                + data[indx + 1]["revenue"]
                + data[indx + 2]["revenue"]
                + data[indx + 3]["revenue"]
            )

            yearIncBeforeTax = (
                data[indx]["incomeBeforeTax"]
                + data[indx + 1]["incomeBeforeTax"]
                + data[indx + 2]["incomeBeforeTax"]
                + data[indx + 3]["incomeBeforeTax"]
            )

            yearTaxExpense = (
                data[indx]["incomeTaxExpense"]
                + data[indx + 1]["incomeTaxExpense"]
                + data[indx + 2]["incomeTaxExpense"]
                + data[indx + 3]["incomeTaxExpense"]
            )

            yearEbit = (
                data[indx]["operatingIncome"]
                + data[indx + 1]["operatingIncome"]
                + data[indx + 2]["operatingIncome"]
                + data[indx + 3]["operatingIncome"]
            )

        netIncome.append(yearNetIncome)
        # print(f"Net Income = {yearNetIncome}")
        interestIncome.append(yearIntIncome)
        # print(f"Interest Income = {yearIntIncome}")
        totalRevenue.append(yearTotalRevenue)
        # print(f"Total Revenue = {yearTotalRevenue}")
        incomeBeforeTax.append(yearIncBeforeTax)
        # print(f"Income Before Tax = {yearIncBeforeTax}")
        incomeTaxExpense.append(yearTaxExpense)
        # print(f"Tax Expense = {yearTaxExpense}")
        ebit.append(yearEbit)
        # print(f"EBIT = {yearEbit}")
        indx += 4
        if indx > 16:
            break
    incStmnt["netIncome"] = netIncome
    incStmnt["interestIncome"] = interestIncome
    incStmnt["totalRevenue"] = totalRevenue
    incStmnt["incomeBeforeTax"] = incomeBeforeTax
    incStmnt["incomeTaxExpense"] = incomeTaxExpense
    incStmnt["ebit"] = ebit

    return incStmnt


# Function to get the balance sheet and extract the required fields


def get_balSht(company, myApiKey):
    url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{company}?period=quarter&limit=20&apikey={myApiKey}"
    data = get_jsonparsed_data(url)
    balSht = {}
    cashAndEquivalents = [
        data[0]["cashAndShortTermInvestments"],
        data[4]["cashAndShortTermInvestments"],
        data[8]["cashAndShortTermInvestments"],
        data[12]["cashAndShortTermInvestments"],
        data[16]["cashAndShortTermInvestments"],
    ]
    currentAssets = [
        data[0]["totalCurrentAssets"],
        data[4]["totalCurrentAssets"],
        data[8]["totalCurrentAssets"],
        data[12]["totalCurrentAssets"],
        data[16]["totalCurrentAssets"],
    ]
    totalAssets = [
        data[0]["totalAssets"],
        data[4]["totalAssets"],
        data[8]["totalAssets"],
        data[12]["totalAssets"],
        data[16]["totalAssets"],
    ]
    accountsPayable = [
        data[0]["accountPayables"],
        data[4]["accountPayables"],
        data[8]["accountPayables"],
        data[12]["accountPayables"],
        data[16]["accountPayables"],
    ]
    stockholdersEquity = [
        data[0]["totalStockholdersEquity"],
        data[4]["totalStockholdersEquity"],
        data[8]["totalStockholdersEquity"],
        data[12]["totalStockholdersEquity"],
        data[16]["totalStockholdersEquity"],
    ]
    currentLiabilities = [
        data[0]["totalCurrentLiabilities"],
        data[4]["totalCurrentLiabilities"],
        data[8]["totalCurrentLiabilities"],
        data[12]["totalCurrentLiabilities"],
        data[16]["totalCurrentLiabilities"],
    ]
    liabilities = [
        data[0]["totalLiabilities"],
        data[4]["totalLiabilities"],
        data[8]["totalLiabilities"],
        data[12]["totalLiabilities"],
        data[16]["totalLiabilities"],
    ]
    shortTermDebt = [
        data[0]["shortTermDebt"],
        data[4]["shortTermDebt"],
        data[8]["shortTermDebt"],
        data[12]["shortTermDebt"],
        data[16]["shortTermDebt"],
    ]

    balSht["cashAndCashEquivalents"] = cashAndEquivalents
    balSht["totalCurrentAssets"] = currentAssets
    balSht["totalAssets"] = totalAssets
    balSht["accountsPayable"] = accountsPayable
    balSht["shortTermDebt"] = shortTermDebt
    balSht["totalCurrentLiabilities"] = currentLiabilities
    balSht["totalLiabilities"] = liabilities
    balSht["totalStockholdersEquity"] = stockholdersEquity

    return balSht


# Function to get the cash flow statement and extract the required fields


def get_cshFlw(company, myApiKey):
    url = f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{company}?period=quarter&limit=20&apikey={myApiKey}"
    data = get_jsonparsed_data(url)
    cshFlw = {}
    depreciation = []
    capex = []
    acquisition = []
    stockBuyBack = []
    dividends = []
    indx = 0
    for year in range(5):
        for qtr in range(indx + 4):
            yearCapex = (
                data[indx]["capitalExpenditure"]
                + data[indx + 1]["capitalExpenditure"]
                + data[indx + 2]["capitalExpenditure"]
                + data[indx + 3]["capitalExpenditure"]
            )

            yearDeprec = (
                data[indx]["depreciationAndAmortization"]
                + data[indx + 1]["depreciationAndAmortization"]
                + data[indx + 2]["depreciationAndAmortization"]
                + data[indx + 3]["depreciationAndAmortization"]
            )
            yearAcquisition = (
                data[indx]["acquisitionsNet"]
                + data[indx + 1]["acquisitionsNet"]
                + data[indx + 2]["acquisitionsNet"]
                + data[indx + 3]["acquisitionsNet"]
            )
            yearStockBuyBack = (
                data[indx]["commonStockRepurchased"]
                + data[indx + 1]["commonStockRepurchased"]
                + data[indx + 2]["commonStockRepurchased"]
                + data[indx + 3]["commonStockRepurchased"]
            )
            yearDividends = (
                data[indx]["dividendsPaid"]
                + data[indx + 1]["dividendsPaid"]
                + data[indx + 2]["dividendsPaid"]
                + data[indx + 3]["dividendsPaid"]
            )
        capex.append(yearCapex)
        depreciation.append(yearDeprec)
        acquisition.append(yearAcquisition)
        stockBuyBack.append(yearStockBuyBack)
        dividends.append(yearDividends)
        indx += 4
        if indx > 16:
            break

    cshFlw["depreciation"] = depreciation
    cshFlw["capex"] = capex
    cshFlw["acquisition"] = acquisition
    cshFlw["stockBuyBack"] = stockBuyBack
    cshFlw["dividendsPaid"] = dividends

    return cshFlw


# Function to get the current share price, shares outstanding, and market cap


def get_quote(company, myApiKey):
    url = f"https://financialmodelingprep.com/api/v3/quote/{company}?apikey={myApiKey}"
    data = get_jsonparsed_data(url)
    # print(data)
    price = data[0]["price"]
    sharesOutstanding = data[0]["sharesOutstanding"]
    marketCap = data[0]["marketCap"]
    entQuote = price, sharesOutstanding, marketCap
    return entQuote


def get_riskFree():
    url = "https://www.cnbc.com/quotes/US10Y"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    result = soup.find(class_="QuoteStrip-lastPrice")
    riskFree = float(result.text[:-1]) / 100
    print(f"Risk Free Rate {riskFree}")
    return riskFree


def get_industry(company):
    indName = pd.read_excel("data/indname.xlsx", sheet_name="US by industry")
    for index, row in indName.iterrows():
        try:
            if company == row["Exchange:Ticker"].split(":")[1]:
                industry = row["Industry Group"]
                print(f"Industry Group {industry}")
            else:
                continue
        except TypeError:
            continue
        except AttributeError:
            continue
    return industry


def get_beta(industry):

    beta = pd.read_excel("data/betas.xlsx", sheet_name="Industry Averages", skiprows=9)

    for index, row in beta.iterrows():
        try:

            if industry in row["Industry Name"]:
                unleveredBeta = row["Unlevered beta corrected for cash"]
            else:
                continue
        except TypeError:
            continue
    print(f"Beta {unleveredBeta}")
    return unleveredBeta


def get_default_spread(intCover):
    defaultSpread = pd.read_excel(
        "/Users/jhess/Documents/Investing/Damodaran Reference/defaultSpread.xlsx"
    )

    # for col in defaultSpread.columns:
    #     print(col)

    for index in defaultSpread.index:
        if (
            intCover > defaultSpread["GT"][index]
            and intCover < defaultSpread["LT"][index]
        ):
            return defaultSpread["Spread"][index]
        else:
            continue
    # print(defa
    # ultSpread)
    # print(defaultSpread.index)

