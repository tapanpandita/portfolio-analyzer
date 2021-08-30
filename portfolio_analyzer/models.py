from dataclasses import dataclass


@dataclass
class Row:
    action: str
    time: str
    isin: str
    ticker: str
    name: str
    num_shares: str
    price_per_share: str
    currency_pps: str
    exchange_rate: str
    result: str
    total: str
    withholding_tax: str
    currency_withholding_tax: str
    charge_amount: str
    transaction_fee: str
    finra_fee: str
    notes: str
    id: str
    currency_conversion_fee: str