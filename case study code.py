# ==============================
# STOCK MARKET ANALYZER PROGRAM
# ==============================

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ==============================
# Utility Function
# ==============================

def check_good_stock(percentage):
    """Check whether stock is good based on return."""
    if percentage > 10:
        return "Very Good "
    elif percentage > 0:
        return "Good "
    else:
        return "Not Good "


# ==============================
# 1. Company Stock Analysis
# ==============================

def company_stock_analysis():
    ticker = input("Enter company ticker symbol: ").upper()
    year = input("Enter year (example: 2023): ")

    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"

    stock = yf.download(ticker, start=start_date, end=end_date)

    if stock.empty:
        print("Invalid ticker or no data available.")
        return

    first_price = stock["Close"].iloc[0].item()
    last_price = stock["Close"].iloc[-1].item()

    percent_change = ((last_price - first_price) / first_price) * 100

    print("\n----- Stock Analysis -----")
    print("Starting Price:", round(first_price, 2))
    print("Closing Price:", round(last_price, 2))
    print("Percentage Change:", round(percent_change, 2), "%")
    print("Stock Performance:", check_good_stock(percent_change))

    # Plot
    plt.figure()
    plt.plot(stock["Close"])
    plt.title(f"{ticker} Closing Prices ({year})")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid()
    plt.show()


# ==============================
# 2. Compare Companies
# ==============================

def compare_companies():
    tickers = input("Enter up to 3 ticker symbols separated by space: ").upper().split()

    if len(tickers) == 0 or len(tickers) > 3:
        print("Enter between 1 and 3 tickers.")
        return

    year = input("Enter year (example: 2023): ")
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"

    plt.figure()

    returns = {}

    for ticker in tickers:
        stock = yf.download(ticker, start=start_date, end=end_date)

        if stock.empty:
            print(f"No data for {ticker}")
            continue

        first_price = stock["Close"].iloc[0].item()
        last_price = stock["Close"].iloc[-1].item()

        percent_change = ((last_price - first_price) / first_price) * 100
        returns[ticker] = percent_change

        plt.plot(stock["Close"], label=ticker)

    if len(returns) == 0:
        return

    best_stock = max(returns, key=returns.get)

    print("\nAnnual Returns:")
    for k, v in returns.items():
        print(k, ":", round(v, 2), "%")

    print("\nBest Performing Stock:", best_stock)
    print("Performance:", check_good_stock(returns[best_stock]))

    plt.title("Company Comparison")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid()
    plt.show()


# ==============================
# 3. Portfolio Simulator
# ==============================

def portfolio_simulator():
    try:
        total_investment = float(input("Enter total investment amount: "))
    except ValueError:
        print("Invalid investment amount.")
        return

    tickers = input("Enter ticker symbols separated by space: ").upper().split()

    if len(tickers) == 0:
        print("Please enter at least one ticker.")
        return

    allocations = []
    total_allocation = 0

    # Get allocation %
    for ticker in tickers:
        try:
            percent_input = input(f"Enter allocation % for {ticker}: ")
            percent = float(percent_input.replace("%", ""))
        except ValueError:
            print("Invalid percentage entered.")
            return

        allocations.append(percent)
        total_allocation += percent

    if total_allocation != 100:
        print("Allocation must sum to 100%")
        return

    year = input("Enter year (example: 2023): ")
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"

    portfolio_values = None

    for i in range(len(tickers)):
        stock = yf.download(tickers[i], start=start_date, end=end_date)

        if stock.empty:
            print(f"No data for {tickers[i]}")
            return

        # Normalize price
        normalized = stock["Close"] / stock["Close"].iloc[0]

        invested_amount = total_investment * (allocations[i] / 100)
        stock_value = normalized * invested_amount

        if portfolio_values is None:
            portfolio_values = stock_value
        else:
            portfolio_values = portfolio_values.add(stock_value, fill_value=0)

    #  FIXED PART
    final_value = portfolio_values.iloc[-1].sum()
    total_return = ((final_value - total_investment) / total_investment) * 100

    print("\n----- Portfolio Result -----")
    print("Final Portfolio Value:", round(final_value, 2))
    print("Total Return:", round(total_return, 2), "%")
    print("Portfolio Performance:", check_good_stock(total_return))

    # Plot
    plt.figure()
    plt.plot(portfolio_values)
    plt.title("Portfolio Growth")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value")
    plt.grid()
    plt.show()

# ==============================
# 4. Yearly Sector Performance
# ==============================

def sector_performance():

    sectors = {
        1: {"name": "Technology", "stocks": ["AAPL", "MSFT", "GOOGL"]},
        2: {"name": "Automobile", "stocks": ["TSLA", "F", "GM"]},
        3: {"name": "Banking", "stocks": ["JPM", "BAC", "WFC"]}
    }

    print("\nAvailable Sectors:")
    for key in sectors:
        print(key, ".", sectors[key]["name"])

    choice = int(input("Select sector number: "))

    if choice not in sectors:
        print("Invalid choice")
        return

    year = input("Enter year (example: 2023): ")
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"

    stocks = sectors[choice]["stocks"]
    returns = {}

    for ticker in stocks:
        stock = yf.download(ticker, start=start_date, end=end_date)

        if stock.empty:
            continue

        first_price = stock["Close"].iloc[0].item()
        last_price = stock["Close"].iloc[-1].item()

        percent_change = ((last_price - first_price) / first_price) * 100
        returns[ticker] = percent_change

    if len(returns) == 0:
        print("No data available.")
        return

    sorted_returns = sorted(returns.items(), key=lambda x: x[1], reverse=True)

    print("\n----- Ranking -----")
    for stock, value in sorted_returns:
        print(stock, ":", round(value, 2), "%")

    print("\nBest Performer:", sorted_returns[0][0])
    print("Worst Performer:", sorted_returns[-1][0])

    # Bar Plot
    plt.figure()
    plt.bar(returns.keys(), returns.values())
    plt.title(f"{sectors[choice]['name']} Sector Performance ({year})")
    plt.xlabel("Companies")
    plt.ylabel("Annual Return (%)")
    plt.grid()
    plt.show()


# ==============================
# Main Menu Loop
# ==============================

while True:
    print("\n========== STOCK MARKET ANALYZER ==========")
    print("1. Company Stock Analysis")
    print("2. Compare Companies (up to 3)")
    print("3. Portfolio Simulator")
    print("4. Yearly Sector Performance Analyzer")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        company_stock_analysis()
    elif choice == "2":
        compare_companies()
    elif choice == "3":
        portfolio_simulator()
    elif choice == "4":
        sector_performance()
    elif choice == "5":
        print("Exiting Program... Thank You!")
        break
    else:
        print("Invalid choice. Please try again.")