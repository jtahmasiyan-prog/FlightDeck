import streamlit as st
import pandas as pd, pathlib

p = pathlib.Path(r'C:\Users\jtahm\Documents\TradingDashboard\Trading_Cockpit.xlsx')
st.title('FlightDeck — Market Snapshot')
try:
    df = pd.read_excel(p, sheet_name='Market Snapshot', engine='openpyxl')
    st.write(f'Rows: {len(df)}')
    st.dataframe(df.head(50))
except Exception as e:
    st.error(f'Read error: {e}')
