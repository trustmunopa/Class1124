# pages/2_Add_Visit.py: CREATE. Add a visit.
import datetime

import streamlit as st

import queries
from db import connect

conn = connect()

st.title("Add a visit")
crop = st.selectbox("Pick a bed", queries.crops(conn))

with st.form("add_visit"):
    visit_date = st.date_input("Visit date")
    status = st.selectbox("Status", ["seeded", "sprouting", "harvesting", "fallow", "failed"])
    if st.form_submit_button("Add visit"):
        # VALIDATION: check the input BEFORE it goes to the database
        if visit_date > datetime.date.today():
            st.warning("That date is in the future. Pick today or earlier.")
        else:
            queries.add_visit(conn, crop, visit_date, status)
            st.success(f"Added a visit for {crop}.")
