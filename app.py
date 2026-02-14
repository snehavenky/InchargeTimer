import streamlit as st
import pandas as pd
from datetime import datetime

st.title("👨‍👩‍👧 Family Time Tracker")

# Simple sidebar for inputs
st.sidebar.header("Log New Entry")
parent = st.sidebar.selectbox("Parent Name", ["Parent A", "Parent B"])
date = st.sidebar.date_input("Date", datetime.now())
hours = st.sidebar.number_input("Hours Spent", min_value=0.1, max_value=24.0, value=1.0)
notes = st.sidebar.text_area("Notes (optional)")

if st.sidebar.button("Log Time"):
    new_data = {"Parent": parent, "Date": str(date), "Hours": hours, "Notes": notes}
    # In a real app, you would save this to a database (like Google Sheets or Supabase)
    st.success(f"Logged {hours} hours for {parent}!")

# Visualization Section
st.subheader("Time Distribution Summary")
# Placeholder data for visual example
data = pd.DataFrame({
    "Parent": ["Parent A", "Parent B"],
    "Total Hours": [45, 38] 
})
st.bar_chart(data.set_index("Parent"))
