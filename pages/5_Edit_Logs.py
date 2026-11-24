# pages/5_Edit_Logs.py: UPDATE many rows at once, spreadsheet style.
import streamlit as st

import queries
from db import connect

conn = connect()

st.title("Edit logs")
st.write("Click a date or status to change it, then Save.")

logs = queries.all_logs(conn)

# DATA EDITOR: a table you can type in. It hands back the edited copy.
# We let you type ANY status here, on purpose. Is anything stopping bad data?
edited = st.data_editor(
    logs,
    hide_index=True,
    disabled=["log_id", "crop"],  # these columns can't be edited
)

if st.button("Save"):
    error = queries.save_logs(conn, edited)
    if error:
        st.error(f"The database said no: {error}")
    else:
        st.success("Saved.")
