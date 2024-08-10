import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import altair as alt

# Set page title
st.set_page_config(page_title="Assignment Tracker", layout="wide")

# Initialize session state
if 'assignments' not in st.session_state:
    st.session_state.assignments = []

# Main title
st.title("Assignment Tracker")

# Sidebar for adding new assignments
with st.sidebar:
    st.header("Add New Assignment")
    course = st.text_input("Course")
    assignment_name = st.text_input("Assignment Name")
    due_date = st.date_input("Due Date")
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    status = st.selectbox("Status", ["Not Started", "In Progress", "Completed"])

    if st.button("Add Assignment"):
        new_assignment = {
            "Course": course,
            "Assignment": assignment_name,
            "Due Date": due_date,
            "Priority": priority,
            "Status": status,
            "Days Left": (due_date - datetime.now().date()).days
        }
        st.session_state.assignments.append(new_assignment)
        st.success("Assignment added successfully!")

# Main content area
col1, col2 = st.columns(2)

with col1:
    st.header("Assignment List")
    if st.session_state.assignments:
        df = pd.DataFrame(st.session_state.assignments)
        df = df.sort_values("Due Date")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No assignments added yet. Use the sidebar to add assignments.")

    if st.button("Clear All Assignments"):
        st.session_state.assignments = []
        st.success("All assignments cleared!")

with col2:
    st.header("Assignment Analytics")
    if st.session_state.assignments:
        df = pd.DataFrame(st.session_state.assignments)

        # Priority Distribution
        st.subheader("Priority Distribution")
        priority_counts = df['Priority'].value_counts()
        st.bar_chart(priority_counts)

        # Status Distribution
        st.subheader("Status Distribution")
        status_counts = df['Status'].value_counts()
        st.bar_chart(status_counts)

        # Timeline Chart
        st.subheader("Assignment Timeline")
        timeline_chart = alt.Chart(df).mark_circle().encode(
            x='Due Date:T',
            y='Course:N',
            color='Priority:N',
            size='Days Left:Q',
            tooltip=['Assignment', 'Due Date', 'Priority', 'Status', 'Days Left']
        ).interactive()
        st.altair_chart(timeline_chart, use_container_width=True)

        # Upcoming Deadlines
        st.subheader("Upcoming Deadlines")
        upcoming = df[df['Days Left'] > 0].sort_values('Days Left').head(5)
        for _, row in upcoming.iterrows():
            st.write(f"**{row['Assignment']}** ({row['Course']}) - Due in {row['Days Left']} days")


