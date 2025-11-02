# generate_workbook.py
import os
import sys
import pandas as pd
from openpyxl import Workbook
from datetime import datetime

# Ensure project libs on path
proj_root = os.path.expanduser(os.path.join("~", "FlightDeck"))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

from libs.strategy_engine import generate_signal_for_ticker

# Configurable paths
WATCHLIST_PATH = r"C:\Users\jtahm\FlightDeck\Passenger_List.csv"
OUTPUT_PATH = r"C:\Users\jtahm\FlightDeck\Output\FlightDeck_Signals.xlsx"

def load_watchlist(path: str):
    df = pd.read_csv(path).squeeze()
    if hasattr(df, "dropna"):
        return df.dropna().tolist()
    return list(df)

def build_workbook(tickers):
    wb = Workbook()
    ws_signals = wb.active
    ws_signals.title = "Runway_Clearance"
    ws_no_signal = wb.create_sheet("Holding_Pattern")
    ws_log = wb.create_sheet("Tower_Log")
    return wb, ws_signals, ws_no_signal, ws_log

def append_result_rows(ws_signals, ws_no_signal, ws_log, res):
    ticker = res.get("ticker")
    error = res.get("error")
    close = res.get("close")
    ma50 = res.get("ma50")
    signal = res.get("signal")

    if error:
        ws_log.append([ticker, f"Error: {error}"])
        return

    if signal:
        ws_signals.append([ticker, close, ma50, "Long Signal"])
    else:
        ws_no_signal.append([ticker, close, ma50, "No Signal"])

def main():
    tickers = load_watchlist(WATCHLIST_PATH)
    wb, ws_signals, ws_no_signal, ws_log = build_workbook(tickers)

    for ticker in tickers:
        try:
            res = generate_signal_for_ticker(ticker)
            append_result_rows(ws_signals, ws_no_signal, ws_log, res)
        except Exception as e:
            ws_log.append([ticker, f"Error: {str(e)}"])

    ws_log.append(["Generated", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

    # Ensure output dir exists
    out_dir = os.path.dirname(OUTPUT_PATH)
    os.makedirs(out_dir, exist_ok=True)

    wb.save(OUTPUT_PATH)
    print(f"Workbook saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()