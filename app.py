import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Tech Lead Attendance Tracker", layout="centered")

st.title("📉 Tech Lead Attendance Tracker")
st.markdown("Track reasons for less attendance of Tech Leads")

# Input form
with st.form("attendance_form"):
    name = st.text_input("👤 Tech Lead Name")
    date = st.date_input("📅 Date", datetime.today())
    attended = st.selectbox("✅ Attended?", ["Yes", "No"])
    reason = ""
    if attended == "No":
        reason = st.text_area("📝 Reason for absence")
    submit = st.form_submit_button("Submit")

# Save to CSV
if submit:
    new_data = pd.DataFrame([[name, date, attended, reason]],
                            columns=["Name", "Date", "Attended", "Reason"])
    try:
        existing = pd.read_csv("attendance.csv")
        df = pd.concat([existing, new_data], ignore_index=True)
    except FileNotFoundError:
        df = new_data
    df.to_csv("attendance.csv", index=False)
    st.success("Submitted successfully!")

# Display data
st.subheader("📊 Attendance Records")
try:
    df = pd.read_csv("attendance.csv")
    st.dataframe(df)
    st.write(f"Total records: {len(df)}")
    st.write(f"Attendance Rate: {round((df['Attended'] == 'Yes').mean() * 100, 2)}%")
except FileNotFoundError:
    st.info("No data yet. Submit a form to get started.")
