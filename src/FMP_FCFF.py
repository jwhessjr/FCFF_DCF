import sqlite3
from datetime import datetime
from sqlite3 import Error

import hg_dcflib


def main():
    company = input("Input company ticker: ").upper()
    print(company)
    EQPREM = 0.0569  # Damodaran 20220701
    industry = hg_dcflib.get_industry(company)
    print(f"Industry: {industry}")
    leveredBeta = hg_dcflib.get_beta(industry)
    riskFree = hg_dcflib.get_riskFree()
    growthPeriod = int(input("Input growth period: "))
    # long term a company can't grow faster than the economy in which it operates
    STABLEGROWTH = 0.021  # CAGR last 10 years
    # the unlevered beta for the industry in which the firm opeerates
    stableBeta = 1.0
    with open("data/apiKey.txt") as f:
        myApiKey = f.readline()

    incStmnt = hg_dcflib.get_incStmnt(company, myApiKey)

    balSht = hg_dcflib.get_balSht(company, myApiKey)

    cshFlw = hg_dcflib.get_cshFlw(company, myApiKey)

    entQuote = hg_dcflib.get_quote(company, myApiKey)
    print(entQuote)
    price = entQuote[0]
    sharesOutstanding = entQuote[1]
    marketCap = entQuote[2]

    opInc = float(incStmnt["ebit"][0])
    capex = float(cshFlw["capex"][0] * -1)
    deprec = float(cshFlw["depreciation"][0])
    incTax = incStmnt["incomeTaxExpense"][0]
    effTaxRate = incTax / opInc
    bvDebt = float(balSht["totalLiabilities"][0])
    bvEquity = float(balSht["totalStockholdersEquity"][0])
    cash = float(balSht["cashAndCashEquivalents"][0])

    # Calculate Current Year Non Cash Working Capital
    currYearWorkingCap = (
        balSht["totalCurrentAssets"][0] - balSht["cashAndCashEquivalents"][0]
    ) - (balSht["totalCurrentLiabilities"][0] - balSht["shortTermDebt"][0])

    # Calculate Prior Year Non Cash Working Capitalß
    priorYearWorkingCap = (
        balSht["totalCurrentAssets"][1] - balSht["cashAndCashEquivalents"][1]
    ) - (balSht["totalCurrentLiabilities"][1] - balSht["shortTermDebt"][1])

    # Calculate Change in Non Cash Working Capital
    chngWorkingCap = currYearWorkingCap - priorYearWorkingCap

    # incStmnt.to_csv(f"{company}_incomeStatement.csv")
    # balSht.to_csv(f"{company}_balanceSheet.csv")
    # cshFlw.to_csv(f"{company}_cashflowStatement.csv")

    # Calculate Free Cash Flow to the Firm
    fcff = opInc - capex + deprec - chngWorkingCap
    print(f"Operating Income = {opInc}")
    print(f"Capex = {capex}")
    print(f"Depreciation = {deprec}")
    print(f"Change in Working Capital = {chngWorkingCap}")
    print(f"Free Cash Flow to Firm = {fcff}")
    print(f"Effective Tax Rate = {effTaxRate}")
    print(f"Income Tax = {incTax}")

    # Calculate Griwth Rate in Operating Income
    firmReinvestment = capex - deprec + chngWorkingCap
    print(f"Reinvestment = {firmReinvestment}")
    reinvestmentRate = firmReinvestment / opInc
    print(f"Reinvestment Rate = {reinvestmentRate}")
    ROC = (opInc * (1 - effTaxRate)) / (bvDebt + bvEquity - cash)
    print(f"Return on Capital = {ROC}")
    expGrowthOpInc = reinvestmentRate * ROC
    print(f"Expected Growth in Op Income = {expGrowthOpInc}")

    # Calculate Expected Free Cash Flow to Firm
    expectedFCFF = []
    for year in range(growthPeriod):
        if year == 0:
            expectedFCFF.append(fcff * (1 + expGrowthOpInc))
        else:
            expectedFCFF.append(expectedFCFF[year - 1] * (1 + expGrowthOpInc))
    print(f"Expected FCFF = {expectedFCFF}")


if __name__ == "__main__":
    main()
