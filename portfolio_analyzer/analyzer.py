import datetime
from decimal import Decimal

from dateutil import parser

from .utils import xirr
from .models import Row
from .csv_parser import get_processed_rows


def get_ticker_value(ticker:str) -> Decimal:
    values = {
        "VUSA": Decimal("6533.46"),
    }
    return values[ticker]


def get_total_shares(ticker:str, rows:list[Row]) -> Decimal:
    total_shares = Decimal("0")

    for row in rows:
        if row.ticker == ticker:
            if "buy" in row.action:
                total_shares += Decimal(row.num_shares)
            if "sell" in row.action:
                total_shares -= Decimal(row.num_shares)

    return total_shares


def get_all_tickers_with_total_shares(rows:list[Row]) -> dict:
    tickers = {}

    for row in rows:
        if row.ticker not in tickers:
            tickers[row.ticker] = get_total_shares(row.ticker, rows)

    return tickers


def get_xirr_for_ticker(ticker:str, rows:list[Row]) -> float:
    cashflows = []

    for row in rows:
        if row.ticker == ticker:
            if row.action == "Market buy":
                cashflows.append((parser.parse(row.time).date(), -1 * float(Decimal(row.total))))
            if row.action == "Market sell":
                cashflows.append((parser.parse(row.time).date(), float(Decimal(row.total))))

    cashflows.append((datetime.datetime.now().date(), float(get_ticker_value(ticker))))
    ticker_xirr = xirr(cashflows)
    return ticker_xirr


def get_total_cashflows(rows: list[Row], current_value: Decimal) -> list[tuple]:
    cashflows = [(parser.parse(row.time).date(), -1 * float(Decimal(row.total))) for row in rows if row.action == "Deposit"]
    cashflows.append((datetime.datetime.now().date(), float(current_value)))
    return cashflows


def get_summary(filepath: str, current_value: Decimal) -> list[list]:
    rows = get_processed_rows(filepath)
    total_deposits = sum(
        [Decimal(row.total) for row in rows if row.action == "Deposit"]
    )
    cashflows = get_total_cashflows(rows, current_value)
    returns = xirr(cashflows)
    table = [
        ["Total Deposits", f"£{'{:,}'.format(total_deposits)}"],
        ["Current Portfolio Value", f"£{'{:,}'.format(current_value)}"],
        ["Portfolio Returns", f"£{'{:,}'.format(current_value - total_deposits)} ({(current_value - total_deposits)*100/total_deposits:.2f}%)"],
        ["Portfolio XIRR", f"{returns*100:.2f}%"],
    ]
    return table


# table2 = [
#     ["VUSA", f"{get_xirr_for_ticker('VUSA', rows)*100:.2f}%", f"{get_total_shares('VUSA', rows)}"],
# ]
# print(tabulate(table2, ["Ticker", "XIRR", "Total Shares Owned"], tablefmt="fancy_grid"))
# print(get_all_tickers_with_total_shares(rows))