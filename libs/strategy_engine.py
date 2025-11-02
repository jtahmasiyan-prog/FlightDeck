# libs/strategy_engine.py
# Minimal, robust strategy engine helper functions used by your generator.

import time
import math
from typing import Optional
import pandas as pd
import yfinance as yf


def _download_with_retries(ticker: str, period: str = "3mo", interval: str = "1d",
                           max_retries: int = 3, backoff: float = 0.5) -> Optional[pd.DataFrame]:
    """Download OHLCV from yfinance with simple retry/backoff."""
    last_exc = None
    for attempt in range(max_retries):
        try:
            df = yf.download(ticker, period=period, interval=interval,
                             progress=False, auto_adjust=True)
            return df
        except Exception as e:
            last_exc = e
            time.sleep(backoff * (2 ** attempt))
    raise last_exc


def _squeeze_close(df: pd.DataFrame) -> pd.Series:
    """Return a clean Series of Close prices indexed by Date."""
    if df is None or df.empty:
        raise ValueError("Empty dataframe passed to _squeeze_close")

    if isinstance(df.columns, pd.MultiIndex):
        df = df.copy()
        df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]

    close = df.get("Close")
    if close is None:
        for alt in ("close", "Adj Close", "AdjClose"):
            if alt in df.columns:
                close = df[alt]
                break
        if close is None:
            raise KeyError("Close column not found in DataFrame")

    if isinstance(close, pd.DataFrame):
        if close.shape[1] == 1:
            close = close.iloc[:, 0]
        else:
            numeric_cols = [c for c in close.columns if pd.api.types.is_numeric_dtype(close[c])]
            close = close[numeric_cols[0]] if numeric_cols else close.iloc[:, 0]

    def _unwrap_element(v):
        if isinstance(v, pd.Series) or isinstance(v, (list, tuple)) or hasattr(v, "shape") and getattr(v, "size", None) == 1:
            try:
                return float(pd.Series(v).squeeze())
            except Exception:
                try:
                    import numpy as _np
                    arr = _np.asarray(v)
                    return float(arr.ravel()[-1])
                except Exception:
                    return float("nan")
        return v

    return close.apply(_unwrap_element)


def generate_signal_for_ticker(ticker: str) -> dict:
    try:
        df = _download_with_retries(ticker)
        close_series = _squeeze_close(df)
        ma50_series = close_series.rolling(window=50).mean()

        last_close = float(close_series.iloc[-1])
        last_ma = float(ma50_series.iloc[-1])

        if isinstance(last_close, pd.Series) or isinstance(last_ma, pd.Series):
            raise ValueError("Non-scalar values detected in close or MA50")

        signal = last_close > last_ma if not math.isnan(last_close) and not math.isnan(last_ma) else False

        return {
            "ticker": ticker,
            "close": last_close,
            "ma50": last_ma,
            "signal": signal,
            "error": None
        }
    except Exception as e:
        return {
            "ticker": ticker,
            "close": None,
            "ma50": None,
            "signal": False,
            "error": str(e)
        }