# Import core requirements: Streamlit for web UI, Pandas for dataset handling, and datetime for dates
import streamlit as st
import pandas as pd
from datetime import datetime, date

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Task Scheduler Tool",
    page_icon="📅",
    layout="wide"
)

# ---------------------------------------------------------
# 2. SESSION STATE & DATA STORAGE
# ---------------------------------------------------------
# Initialize session state to maintain active task list across user interactions
if "tasks" not in st.session_state:
    st.session_state.tasks = pd.DataFrame([
        {
            "Task ID": 1,
            "Task Name": "Submit Codtech Task 2",
            "Category": "Internship",
            "Priority": "High",
            "Due Date": date(2026, 9, 10),
            "Status": "Completed"
        },
        {
            "Task ID": 2,
            "Task Name": "Build Inventory Management UI",
            "Category": "Internship",
            "Priority": "Medium",
            "Due Date": date(2026, 9, 15),
            "Status": "In Progress"
        },
        {
            "Task ID": 3,
            "Task Name": "Prepare Data Structures Notes",
            "Category": "Academics",
            "Priority": "Low",
            "Due Date": date(2026, 9, 20),
            "Status": "Pending"
        }
    ])

# Access current task dataset
df = st.session_state.tasks

# ---------------------------------------------------------
# 3. HEADER SECTION
# ---------------------------------------------------------
st.title("📅 Smart Task Scheduler Tool")
st.caption("Organize, prioritize, and track your project tasks and deadlines.")
st.markdown("---")

# ---------------------------------------------------------
# 4. METRICS & KPI DASHBOARD
# ---------------------------------------------------------
# Compute dynamic task performance counters
total_tasks = len(df)
completed_tasks = len(df[df["Status"] == "Completed"])
pending_tasks = len(df[df["Status"] != "Completed"])
high_priority = len(df[(df["Priority"] == "High") & (df["Status"] != "Completed")])

# Layout real-time status indicators in 4 columns
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Tasks", total_tasks)
col2.metric("Completed", completed_tasks)
col3.metric("Pending / In Progress", pending_tasks)
col4.metric("High Priority Urgent", high_priority, delta_color="inverse")

st.markdown("---")

# ---------------------------------------------------------
# 5. SIDEBAR NAVIGATION CONTROLS
# ---------------------------------------------------------
st.sidebar.header("Task Management")
action = st.sidebar.radio(
    "Navigation",
    ["View Tasks", "Add New Task", "Update Task Status"]
)

# ---------------------------------------------------------
# 6. ACTION HANDLERS
# ---------------------------------------------------------

# Option A: View and Filter Schedule
if action == "View Tasks":
    st.subheader("📋 Scheduled Tasks")

    # Interactive Filter Dropdowns
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        status_filter = st.selectbox("Filter by Status", ["All", "Pending", "In Progress", "Completed"])
    with col_f2:
        priority_filter = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])

    # Query processing logic based on user filter selections
    filtered_df = df.copy()
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df["Status"] == status_filter]
    if priority_filter != "All":
        filtered_df = filtered_df[filtered_df["Priority"] == priority_filter]

    # Render filtered table in wide display
    st.dataframe(filtered_df, use_container_width=True)

# Option B: Schedule New Task Entry
elif action == "Add New Task":
    st.subheader("➕ Schedule a New Task")

    # Form layout with clean validation reset
    with st.form("add_task_form", clear_on_submit=True):
        task_name = st.text_input("Task Name")
        category = st.selectbox("Category", ["Internship", "Academics", "Personal", "Project"])
        priority = st.selectbox("Priority", ["High", "Medium", "Low"])
        due_date = st.date_input("Due Date", min_value=date.today())

        submitted = st.form_submit_button("Add Task")

        # Process task submission
        if submitted:
            if task_name:
                new_id = len(st.session_state.tasks) + 1
                new_task = {
                    "Task ID": new_id,
                    "Task Name": task_name,
                    "Category": category,
                    "Priority": priority,
                    "Due Date": due_date,
                    "Status": "Pending"
                }
                # Add row to state dataframe
                st.session_state.tasks = pd.concat(
                    [st.session_state.tasks, pd.DataFrame([new_task])],
                    ignore_index=True
                )
                st.success(f"Task '{task_name}' added successfully!")
                st.rerun()
            else:
                st.error("Please provide a task name.")

# Option C: Update Completion Status
elif action == "Update Task Status":
    st.subheader("🔄 Update Task Progress")
    if not df.empty:
        task_to_update = st.selectbox("Select Task", df["Task Name"].tolist())
        new_status = st.selectbox("Update Status", ["Pending", "In Progress", "Completed"])

        if st.button("Save Changes"):
            # Locate task record and update its current status
            st.session_state.tasks.loc[
                st.session_state.tasks["Task Name"] == task_to_update, "Status"
            ] = new_status
            st.success(f"Updated status for '{task_to_update}' to '{new_status}'!")
            st.rerun()