import calendar
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import openpyxl  # Ensure this is installed

rules = {
    "onsite": {
        "1to20": 7,
        "21to50": 5,
        "+50": 4,
    },
    "remote": {
        "1to20": 3,
        "21to50": 3,
        "+50": 2,
    },
}


# Function to add an item to the list
def add_item():
    name = st.session_state["name"]
    number = st.session_state["number"]
    date = st.session_state["date"]

    # Determine weeks apart based on number and visit type
    if 1 <= number <= 20:
        weeks_apart_onsite = rules["onsite"]["1to20"]
        weeks_apart_remote = rules["remote"]["1to20"]
    elif 21 <= number <= 50:
        weeks_apart_onsite = rules["onsite"]["21to50"]
        weeks_apart_remote = rules["remote"]["21to50"]
    elif number > 50:
        weeks_apart_onsite = rules["onsite"]["+50"]
        weeks_apart_remote = rules["remote"]["+50"]

    visits = []
    current_date = date
    for i in range(
        39
    ):  # 3 years = 52 weeks/year * 3 years / onsite weeks (onsite every 7 weeks max)
        current_date += timedelta(weeks=weeks_apart_onsite)
        visits.append(
            {
                "name": name,
                "number": number,
                "date": date,
                "visit_date": current_date,
                "type": "onsite",
            }
        )
        remote_visit_date = current_date + timedelta(weeks=weeks_apart_remote)
        visits.append(
            {
                "name": name,
                "number": number,
                "date": date,
                "visit_date": remote_visit_date,
                "type": "remote",
            }
        )

    st.session_state["items"].extend(visits)


# Function to remove an item from the list
def remove_item(index):
    st.session_state["items"].pop(index)


# Function to generate calendar dataframe
def generate_calendar_df(year, month, items):
    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.monthdayscalendar(year, month)
    df = pd.DataFrame(month_days)
    df.columns = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    df = df.replace(0, "")  # Replace 0 with empty string to hide those squares

    # Add visits to the calendar
    for item in items:
        visit_date = item["visit_date"]
        if visit_date.year == year and visit_date.month == month:
            day = visit_date.day
            # Find the week and day of week
            for week_num, week in enumerate(month_days):
                if day in week:
                    day_of_week = week.index(day)
                    color = "blue" if item["type"] == "onsite" else "green"
                    df.iat[week_num, day_of_week] = (
                        f'<div style="background-color: {color}; color: white; height: 100%; display: flex; align-items: center; justify-content: center;">{day} - {item["name"]}</div>'
                    )

    return df


# Function to export data to Excel
def export_to_excel(items):
    df = pd.DataFrame(items)
    df = df[["name", "visit_date", "type"]]
    df.columns = ["Name", "Date", "Type of Visit"]
    df.to_excel("schedule.xlsx", index=False)
    st.success("Schedule exported to schedule.xlsx")


if __name__ == "__main__":
    if "items" not in st.session_state:
        st.session_state["items"] = []

    # Sidebar for input fields to add a new item
    with st.sidebar:
        st.text_input("Name", key="name")
        st.number_input("Number", key="number", step=1)
        st.date_input("Date", key="date")
        st.button("Add Item", on_click=add_item)

        # Display the list of items
        st.write("Items:")
        for i, item in enumerate(st.session_state["items"]):
            st.write(
                f"{i+1}. Name: {item['name']}, Number: {item['number']}, Date: {item['date']}, Visit Date: {item['visit_date']}, Type: {item['type']}"
            )
            st.button(
                f"Remove {item['name']}",
                key=f"remove_{i}",
                on_click=remove_item,
                args=(i,),
            )

    # Export to Excel button
    st.button(
        "Export to Excel", on_click=export_to_excel, args=(st.session_state["items"],)
    )
    
    # Main page for scrollable calendar
    st.write(f"## Scrollable Calendar")

    # Use the entire width of the website
    st.markdown(
        """
        <style>
        body {
            background-color: #121212;
            color: #ffffff;
        }
        .reportview-container .main .block-container{
            max-width: 100%;
            padding-top: 0rem;
            padding-right: 1rem;
            padding-left: 1rem;
            padding-bottom: 0rem;
            background-color: #121212;
            color: #ffffff;
        }
        .sidebar .sidebar-content {
            background-color: #1f1f1f;
            color: #ffffff;
        }
        .sidebar .sidebar-content .block-container {
            background-color: #1f1f1f;
            color: #ffffff;
        }
        .dataframe {
            height: 600px;
            overflow-y: scroll;
            background-color: #1e1e1e;
            color: #ffffff;
        }
        .dataframe th {
            background: #333333;
            position: sticky;
            top: 0;
            color: #ffffff;
        }
        .dataframe td, .dataframe th {
            width: 14.28%;
            text-align: center;
            height: 100px; /* Adjust this value to increase height */
        }
        .dataframe td {
            font-size: 16px; /* Adjust this value to change text size */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Display the calendar for the next 3 years
    start_date = datetime.now()
    months_to_display = 36  # 3 years

    for i in range(months_to_display):
        year_offset = (start_date.month + i - 1) // 12
        month = (start_date.month + i - 1) % 12 + 1
        year = start_date.year + year_offset

        st.write(f"### {calendar.month_name[month]} {year}")
        cal_df = generate_calendar_df(year, month, st.session_state["items"])

        # Convert dataframe to HTML with embedded styles
        html = cal_df.to_html(escape=False)
        st.markdown(html, unsafe_allow_html=True)
        st.write("")  # Add a blank space between months

