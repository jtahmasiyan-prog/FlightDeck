import streamlit as st
from libs.data_loaders import load_market_snapshot

st.title('FlightDeck — Market Snapshot')
try:
    df = load_market_snapshot()
    st.write(f'Rows: {len(df)}')
    st.dataframe(df.head(50))
except Exception as e:
    st.error(f'Read error: {e}')
