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

    entVal = hg_dcflib.get_entVal(company, myApiKey)
    # print(entVal)
    sharesOutstanding = entVal[0]
    # print(sharesOutstanding)
    marketCap = entVal[1]
    # print(marketCap)

    price = hg_dcflib.get_price(company, myApiKey)
    print(price)

    # incStmnt.to_csv(f"{tckr}_incomeStatement.csv")
    # balSht.to_csv(f"{tckr}_balanceSheet.csv")
    # cfStmnt.to_csv(f"{tckr}_cashflowStatement.csv")

    print(incStmnt)
    print(balSht)
    print(cshFlw)


if __name__ == "__main__":
    main()
