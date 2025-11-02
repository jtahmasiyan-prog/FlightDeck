import os
from libs import strategy_engine as se

def test_run_creates_workbook(tmp_path):
    # Prepare temp watchlist
    watchlist = tmp_path / "watchlist.csv"
    watchlist.write_text("AAPL\nMSFT\n")

    out_dir = tmp_path / "out"
    out_dir.mkdir()
    out_path = str(out_dir / "test_signals.xlsx")

    result = se.run(
        watchlist_path=str(watchlist),
        output_path=out_path,
        long_only=True,
        ma_window=5,
    )

    assert isinstance(result, dict)
    assert "output" in result
    assert os.path.exists(result["output"])
    assert result["tickers"] == 2
