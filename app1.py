import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Parent Timer", icon="👶")

# --- DATABASE CONNECTION ---
# This connects to a Google Sheet so data stays forever
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("👶 Baby Time Tracker")

# --- LOGIN / USER SELECTION ---
user = st.sidebar.selectbox("Select Parent", ["Select Name", "Parent A", "Parent B"])

if user != "Select Name":
    st.sidebar.success(f"Logged in as: {user}")
    
    # --- PUNCH CLOCK LOGIC ---
    if "start_time" not in st.session_state:
        st.session_state.start_time = None

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🚀 Start Time", use_container_width=True):
            st.session_state.start_time = datetime.now()
            st.info(f"Check-in at: {st.session_state.start_time.strftime('%H:%M:%S')}")

    with col2:
        if st.button("🛑 Stop & Log", use_container_width=True):
            if st.session_state.start_time:
                end_time = datetime.now()
                duration = end_time - st.session_state.start_time
                hours = round(duration.total_seconds() / 3600, 2)
                
                # Create a new entry
                new_data = pd.DataFrame([{
                    "Parent": user,
                    "Start": st.session_state.start_time.strftime("%Y-%m-%d %H:%M"),
                    "End": end_time.strftime("%Y-%m-%d %H:%M"),
                    "Total Hours": hours
                }])
                
                # Save to Google Sheets
                existing_data = conn.read()
                updated_df = pd.concat([existing_data, new_data], ignore_index=True)
                conn.update(data=updated_df)
                
                st.session_state.start_time = None
                st.success(f"Logged {hours} hours!")
            else:
                st.error("You haven't started a timer yet!")

    # --- HISTORY ---
    st.divider()
    st.subheader("Recent Logs")
    history = conn.read()
    st.dataframe(history.tail(10), use_container_width=True)

else:
    st.warning("Please select your name in the sidebar to begin.")
