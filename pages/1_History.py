# pages/1_History.py: READ. Pick a bed, see its visits.
import streamlit as st

import queries
from db import connect

conn = connect()

st.title("History")

# SIDEBAR: anything inside "with st.sidebar:" shows up in the left sidebar
with st.sidebar:
    crop = st.selectbox("Pick a bed", queries.crops(conn))

visits = queries.history(conn, crop)

# TABS: the same data two ways. Only the open tab is shown.
table_tab, count_tab = st.tabs(["Visits", "Count by status"])
with table_tab:
    st.dataframe(visits, hide_index=True)
with count_tab:
    st.bar_chart(visits["status"].value_counts())

# DOWNLOAD: hand the user a CSV of what they're looking at
st.download_button(
    "Download as CSV",
    visits.to_csv(index=False),
    file_name=f"{crop}_history.csv",
)
