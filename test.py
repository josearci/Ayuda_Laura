import streamlit as st
import pandas as pd
import calendar
from datetime import datetime


# Function to generate calendar dataframe
def generate_calendar_df(year, month):
    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.monthdayscalendar(year, month)
    df = pd.DataFrame(month_days)
    df.columns = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    df = df.replace(0, "")  # Replace 0 with empty string to hide those squares
    return df


# Initial date setup
current_date = datetime.now()
current_year = current_date.year
current_month = current_date.month

# Generate and display calendar for multiple months
months_to_display = 12

st.write(f"## Scrollable Calendar")

# Use the entire width of the website
st.markdown(
    """
    <style>
    .reportview-container .main .block-container{
        max-width: 100%;
        padding-top: 0rem;
        padding-right: 1rem;
        padding-left: 1rem;
        padding-bottom: 0rem;
    }
    .dataframe {
        height: 600px;
        overflow-y: scroll;
    }
    .dataframe th {
        background: #f1f3f4;
        position: sticky;
        top: 0;
    }
    .dataframe td, .dataframe th {
        width: 14.28%;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

for i in range(months_to_display):
    year_offset = (current_month + i - 1) // 12
    month = (current_month + i - 1) % 12 + 1
    year = current_year + year_offset

    st.write(f"### {calendar.month_name[month]} {year}")
    cal_df = generate_calendar_df(year, month)
    st.dataframe(cal_df)
    st.write("")  # Add a blank space between months
