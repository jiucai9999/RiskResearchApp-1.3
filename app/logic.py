import statistics
import json
import pandas as pd
from .db import get_conn

def calc_position(account, risk_percent, entry, stop, target):
    loss = abs(entry - stop)
    if loss == 0:
        raise ValueError("止损不能等于入场价")

    risk_amt = account * risk_percent / 100
    position = risk_amt / loss
    rr = abs(target - entry) / loss
    return position, rr

def calc_institution_stats(prices: dict):
    if not prices:
        return None, None, None, None

    values = list(prices.values())
    return (
        sum(values) / len(values),
        statistics.median(values),
        max(values),
        min(values),
    )

def load_trades(product=None):
    conn = get_conn()
    if product:
        df = pd.read_sql(
            "SELECT * FROM trades WHERE product=? ORDER BY time ASC",
            conn,
            params=(product,)
        )
    else:
        df = pd.read_sql("SELECT * FROM trades ORDER BY time ASC", conn)
    conn.close()
    return df
