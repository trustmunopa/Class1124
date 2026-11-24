# app.py: the home page
import streamlit as st

import queries
from db import connect, reset

st.set_page_config(page_title="Garden Beds", page_icon="🌱", layout="wide")

conn = connect()

st.title("Garden Beds")
st.write("Pick a page in the sidebar.")

# METRICS: three big numbers in a row. st.columns splits the page side by side.
t = queries.totals(conn)
col1, col2, col3 = st.columns(3)
col1.metric("Beds", int(t["beds"]))
col2.metric("Visits logged", int(t["visits"]))
col3.metric("Different statuses", int(t["statuses"]))

# Two tables side by side
left, right = st.columns(2)
with left:
    st.subheader("Beds")
    st.dataframe(queries.beds(conn), hide_index=True)
with right:
    st.subheader("Statuses")
    st.dataframe(queries.status_counts(conn), hide_index=True)

# CHART: Streamlit draws a bar chart straight from a DataFrame
st.subheader("Visits per bed")
st.bar_chart(queries.visits_per_crop(conn), x="crop", y="visits")

st.caption(f"Logs with no bed: {queries.orphan_count(conn)}")

# RESET: throw away garden.db so the app bakes a fresh one from the migrations
if st.button("Reset garden"):
    conn.close()
    reset()
    st.rerun()
