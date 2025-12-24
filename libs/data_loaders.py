import pandas as pd, pathlib

def load_market_snapshot():
    p = pathlib.Path(r'C:\Users\jtahm\Documents\TradingDashboard\Trading_Cockpit.xlsx')
    return pd.read_excel(p, sheet_name='Market Snapshot', engine='openpyxl')
