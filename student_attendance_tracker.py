import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px
import plotly.graph_objects as go
from datetime import date


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Bloom Attendance",
    page_icon="🌷",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# FILE NAMES
# ============================================================

STUDENTS_FILE = "students.json"
ATTENDANCE_FILE = "attendance.json"


# ============================================================
# PASTEL COLOR PALETTE
# ============================================================

CREAM = "#FFFDF8"
LAVENDER = "#EDE7F6"
LILAC = "#D8C4E8"
BLUSH = "#F7D6D0"
PEACH = "#F9D8B4"
SAGE = "#DCEAD8"
MINT = "#CFE8DD"
BUTTER = "#F8E8B0"
ROSE = "#D98282"
PLUM = "#665466"
TEXT = "#544854"
WHITE = "#FFFFFF"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       MAIN BACKGROUND
       ====================================================== */

    .stApp {
        background:
        linear-gradient(
            135deg,
            #FFFDF8 0%,
            #FAF5F0 45%,
            #F3EDF5 100%
        );
    }


    /* ======================================================
       SIDEBAR
       ====================================================== */

    section[data-testid="stSidebar"] {
        background:
        linear-gradient(
            180deg,
            #EDE7F6 0%,
            #F7D6D0 50%,
            #DCEAD8 100%
        );
    }


    section[data-testid="stSidebar"] h1 {
        color: #665466 !important;
        font-weight: 800 !important;
    }


    section[data-testid="stSidebar"] p {
        color: #665466 !important;
    }


    section[data-testid="stSidebar"] label {
        color: #665466 !important;
        font-weight: 700 !important;
    }


    /* ======================================================
       HEADINGS
       ====================================================== */

    h1 {
        color: #544854 !important;
        font-weight: 800 !important;
    }


    h2 {
        color: #665466 !important;
        font-weight: 750 !important;
    }


    h3 {
        color: #765F70 !important;
    }


    /* ======================================================
       METRIC CARDS
       ====================================================== */

    div[data-testid="metric-container"] {
        background: #FFFFFF;
        border: 1px solid #E9DFE8;
        border-radius: 18px;
        padding: 18px;
        box-shadow:
            0 6px 20px rgba(102, 84, 102, 0.08);
    }


    div[data-testid="metric-container"] label {
        color: #857785 !important;
        font-weight: 650 !important;
    }


    div[data-testid="metric-container"] div {
        color: #665466 !important;
        font-weight: 800 !important;
    }


    /* ======================================================
       BUTTONS
       ====================================================== */

    .stButton > button {
        background: #D98282;
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 700;
        padding: 10px 18px;
    }


    .stButton > button:hover {
        background: #C76F70;
        color: white;
    }


    /* ======================================================
       FORMS
       ====================================================== */

    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.96);
        border: 1px solid #EADFE8;
        border-radius: 20px;
        padding: 26px;
        box-shadow:
            0 8px 24px rgba(102, 84, 102, 0.07);
    }


    /* ======================================================
       INPUTS
       ====================================================== */

    input,
    textarea {
        border-radius: 10px !important;
    }


    /* ======================================================
       TABS
       ====================================================== */

    button[data-baseweb="tab"] {
        color: #766675;
        font-weight: 700;
    }


    button[data-baseweb="tab"][aria-selected="true"] {
        color: #D98282;
    }


    /* ======================================================
       PROGRESS BAR
       ====================================================== */

    div[data-testid="stProgress"] > div > div > div {
        background:
        linear-gradient(
            90deg,
            #D8C4E8,
            #F7D6D0,
            #DCEAD8
        );
    }


    /* ======================================================
       DATAFRAME
       ====================================================== */

    div[data-testid="stDataFrame"] {
        border-radius: 15px;
        overflow: hidden;
    }


    /* ======================================================
       DIVIDER
       ====================================================== */

    hr {
        border-top: 1px solid #E7DDE6;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# JSON FUNCTIONS
# ============================================================

def load_json(filename):

    if not os.path.exists(filename):
        return []

    try:
        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except (json.JSONDecodeError, FileNotFoundError):

        return []


def save_json(filename, data):

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )


# ============================================================
# SESSION STATE
# ============================================================

if "students" not in st.session_state:

    st.session_state.students = load_json(
        STUDENTS_FILE
    )


if "attendance" not in st.session_state:

    st.session_state.attendance = load_json(
        ATTENDANCE_FILE
    )


# ============================================================
# GLOBAL DATA VARIABLES
# ============================================================

students = st.session_state.students
attendance_records = st.session_state.attendance


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def find_student(student_id):

    for student in st.session_state.students:

        if student["student_id"] == student_id:
            return student

    return None


def calculate_attendance(
    student_id,
    subject=None
):

    records = [

        record
        for record in st.session_state.attendance

        if record["student_id"] == student_id
    ]


    if subject is not None:

        records = [

            record
            for record in records

            if record["subject"] == subject
        ]


    if not records:
        return 0


    present_count = sum(

        1

        for record in records

        if record["status"] == "Present"
    )


    return round(
        present_count / len(records) * 100,
        2
    )


def refresh_data():

    st.session_state.students = load_json(
        STUDENTS_FILE
    )

    st.session_state.attendance = load_json(
        ATTENDANCE_FILE
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🌷 Bloom")

    st.caption(
        "Student Attendance Tracker"
    )

    st.divider()

    page = st.radio(
        "Navigate",
        [
            "🏡 Home",
            "👩‍🎓 Students",
            "🌼 Mark Attendance",
            "📖 Reports"
        ]
    )

    st.divider()

    st.write("💾 **Storage**")
    st.caption("Local JSON files")

    st.write("🗂️ **Database**")
    st.caption("Not used")


# ============================================================
# HOME / DASHBOARD
# ============================================================

if page == "🏡 Home":

    st.title("🌷 Bloom Attendance")

    st.write(
        "A soft and simple way to monitor student attendance."
    )

    st.divider()

    refresh_data()

    students = st.session_state.students
    attendance_records = st.session_state.attendance


    # ========================================================
    # BASIC CALCULATIONS
    # ========================================================

    total_students = len(students)

    total_records = len(
        attendance_records
    )


    present_count = sum(

        1

        for record
        in attendance_records

        if record["status"] == "Present"
    )


    absent_count = (
        total_records - present_count
    )


    if total_records > 0:

        overall_percentage = round(

            present_count
            /
            total_records
            *
            100,

            2
        )

    else:

        overall_percentage = 0


    # ========================================================
    # TOP METRICS
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "👩‍🎓 Students",
        total_students
    )


    col2.metric(
        "📚 Records",
        total_records
    )


    col3.metric(
        "🌿 Present",
        present_count
    )


    col4.metric(
        "🌸 Attendance",
        f"{overall_percentage}%"
    )


    st.divider()


    if not attendance_records:

        st.info(
            "🌱 No attendance data yet. "
            "Register students and start marking attendance."
        )

    else:

        # ====================================================
        # SECTION 1
        # ATTENDANCE GAUGE
        # ====================================================

        st.subheader(
            "🌸 Overall Attendance"
        )


        left, right = st.columns(
            [1.3, 0.7]
        )


        with left:

            gauge = go.Figure(

                go.Indicator(

                    mode="gauge+number",

                    value=overall_percentage,

                    number={
                        "suffix": "%",
                        "font": {
                            "size": 38,
                            "color": PLUM
                        }
                    },

                    gauge={

                        "axis": {
                            "range": [0, 100]
                        },

                        "bar": {
                            "color": ROSE
                        },

                        "bgcolor": "#F5EEF3",

                        "borderwidth": 0,

                        "steps": [

                            {
                                "range": [
                                    0,
                                    50
                                ],

                                "color": "#F8E1DE"
                            },

                            {
                                "range": [
                                    50,
                                    75
                                ],

                                "color": "#F9EAD6"
                            },

                            {
                                "range": [
                                    75,
                                    100
                                ],

                                "color": "#DCEAD8"
                            }
                        ]
                    }
                )
            )


            gauge.update_layout(

                height=330,

                margin=dict(
                    l=20,
                    r=20,
                    t=20,
                    b=10
                ),

                paper_bgcolor="rgba(0,0,0,0)"
            )


            st.plotly_chart(
                gauge,
                use_container_width=True
            )


        with right:

            st.subheader(
                "🌼 Attendance Status"
            )


            if overall_percentage >= 75:

                st.success(
                    "🌿 Good attendance"
                )

            elif overall_percentage >= 60:

                st.warning(
                    "🍑 Needs attention"
                )

            else:

                st.error(
                    "🌸 Low attendance"
                )


            st.metric(
                "Present Classes",
                present_count
            )


            st.metric(
                "Absent Classes",
                absent_count
            )


        st.divider()


        # ====================================================
        # SECTION 2
        # STUDENT ATTENDANCE COMPARISON
        # ====================================================

        st.subheader(
            "🪻 Student Attendance Comparison"
        )


        ranking = []


        for student in students:

            percentage = calculate_attendance(
                student["student_id"]
            )


            ranking.append(

                {
                    "Student":
                        student["name"],

                    "Attendance":
                        percentage
                }
            )


        ranking_df = pd.DataFrame(
            ranking
        )


        if not ranking_df.empty:

            ranking_df = ranking_df.sort_values(
                "Attendance",
                ascending=True
            )


            fig = px.bar(

                ranking_df,

                x="Attendance",

                y="Student",

                orientation="h",

                text="Attendance",

                color="Attendance",

                color_continuous_scale=[

                    "#F7D6D0",

                    "#F9D8B4",

                    "#F8E8B0",

                    "#DCEAD8"
                ],

                range_x=[0, 100]
            )


            fig.update_traces(

                texttemplate="%{text}%",

                textposition="outside"
            )


            fig.update_layout(

                height=430,

                xaxis_title="Attendance %",

                yaxis_title="",

                coloraxis_showscale=False,

                paper_bgcolor="rgba(0,0,0,0)",

                plot_bgcolor="rgba(0,0,0,0)"
            )


            st.plotly_chart(

                fig,

                use_container_width=True
            )


        st.divider()


        # ====================================================
        # SECTION 3
        # DEPARTMENT-WISE ATTENDANCE
        # ====================================================

        st.subheader(
            "🏫 Department-wise Attendance"
        )


        department_rows = []


        for student in students:

            percentage = calculate_attendance(

                student["student_id"]
            )


            department_rows.append(

                {
                    "Department":
                        student["department"],

                    "Attendance":
                        percentage
                }
            )


        if department_rows:

            department_df = pd.DataFrame(
                department_rows
            )


            department_df = (

                department_df

                .groupby(
                    "Department"
                )

                ["Attendance"]

                .mean()

                .reset_index()
            )


            department_df["Attendance"] = (

                department_df["Attendance"]

                .round(2)
            )


            fig = px.bar(

                department_df,

                x="Department",

                y="Attendance",

                text="Attendance",

                color="Department",

                color_discrete_sequence=[

                    "#D8C4E8",

                    "#F7D6D0",

                    "#F9D8B4",

                    "#DCEAD8",

                    "#CFE8DD",

                    "#F8E8B0"
                ]
            )


            fig.update_traces(

                texttemplate="%{text}%",

                textposition="outside"
            )


            fig.update_layout(

                title="Average Attendance by Department",

                yaxis_title="Attendance %",

                xaxis_title="Department",

                yaxis_range=[0, 100],

                height=420,

                paper_bgcolor="rgba(0,0,0,0)",

                plot_bgcolor="rgba(0,0,0,0)"
            )


            st.plotly_chart(

                fig,

                use_container_width=True
            )


        st.divider()


        # ====================================================
        # SECTION 4
        # SUBJECT-WISE PRESENT VS ABSENT
        # ====================================================

        st.subheader(
            "📚 Subject-wise Attendance Distribution"
        )


        if attendance_records:

            subject_df = pd.DataFrame(
                attendance_records
            )


            subject_summary = (

                subject_df

                .groupby(
                    [
                        "subject",
                        "status"
                    ]
                )

                .size()

                .reset_index(
                    name="Count"
                )
            )


            fig = px.bar(

                subject_summary,

                x="subject",

                y="Count",

                color="status",

                barmode="stack",

                color_discrete_map={

                    "Present":
                        "#DCEAD8",

                    "Absent":
                        "#F7D6D0"
                }
            )


            fig.update_layout(

                title="Present vs Absent by Subject",

                xaxis_title="Subject",

                yaxis_title="Number of Classes",

                height=450,

                paper_bgcolor="rgba(0,0,0,0)",

                plot_bgcolor="rgba(0,0,0,0)"
            )


            st.plotly_chart(

                fig,

                use_container_width=True
            )


        st.divider()


        # ====================================================
        # SECTION 5
        # DONUT CHART
        # ====================================================

        st.subheader(
            "🌸 Attendance Status Overview"
        )


        status_count = pd.DataFrame(

            {
                "Status": [
                    "Present",
                    "Absent"
                ],

                "Count": [
                    present_count,
                    absent_count
                ]
            }
        )


        fig = px.pie(

            status_count,

            names="Status",

            values="Count",

            hole=0.60,

            color="Status",

            color_discrete_map={

                "Present":
                    "#DCEAD8",

                "Absent":
                    "#F7D6D0"
            }
        )


        fig.update_traces(

            textinfo="percent+label",

            textfont_size=14
        )


        fig.update_layout(

            title="Overall Attendance Distribution",

            height=420,

            paper_bgcolor="rgba(0,0,0,0)"
        )


        st.plotly_chart(

            fig,

            use_container_width=True
        )


        st.divider()


        # ====================================================
        # SECTION 6
        # MONTHLY ATTENDANCE TREND
        # ====================================================

        st.subheader(
            "📅 Monthly Attendance Trend"
        )


        trend_df = pd.DataFrame(
            attendance_records
        )


        trend_df["date"] = pd.to_datetime(
            trend_df["date"]
        )


        trend_df["Month"] = (

            trend_df["date"]

            .dt.to_period("M")

            .astype(str)
        )


        monthly = (

            trend_df

            .groupby(
                [
                    "Month",
                    "status"
                ]
            )

            .size()

            .reset_index(
                name="Count"
            )
        )


        fig = px.line(

            monthly,

            x="Month",

            y="Count",

            color="status",

            markers=True,

            color_discrete_map={

                "Present":
                    "#DCEAD8",

                "Absent":
                    "#F7D6D0"
            }
        )


        fig.update_layout(

            title="Monthly Attendance Pattern",

            xaxis_title="Month",

            yaxis_title="Attendance Records",

            height=420,

            paper_bgcolor="rgba(0,0,0,0)",

            plot_bgcolor="rgba(0,0,0,0)"
        )


        st.plotly_chart(

            fig,

            use_container_width=True
        )


        st.divider()


        # ====================================================
        # SECTION 7
        # ATTENDANCE RANGE DISTRIBUTION
        # ====================================================

        st.subheader(
            "🌿 Attendance Range Distribution"
        )


        range_data = []


        for student in students:

            percentage = calculate_attendance(

                student["student_id"]
            )


            if percentage >= 90:

                category = "90-100%"

            elif percentage >= 75:

                category = "75-89%"

            elif percentage >= 60:

                category = "60-74%"

            else:

                category = "Below 60%"


            range_data.append(

                {
                    "Student":
                        student["name"],

                    "Attendance Range":
                        category
                }
            )


        if range_data:

            range_df = pd.DataFrame(
                range_data
            )


            distribution = (

                range_df

                ["Attendance Range"]

                .value_counts()

                .reset_index()
            )


            distribution.columns = [

                "Attendance Range",

                "Students"
            ]


            order = [

                "90-100%",

                "75-89%",

                "60-74%",

                "Below 60%"
            ]


            distribution[
                "Attendance Range"
            ] = pd.Categorical(

                distribution[
                    "Attendance Range"
                ],

                categories=order,

                ordered=True
            )


            distribution = (

                distribution

                .sort_values(
                    "Attendance Range"
                )
            )


            fig = px.bar(

                distribution,

                x="Attendance Range",

                y="Students",

                text="Students",

                color="Attendance Range",

                color_discrete_sequence=[

                    "#DCEAD8",

                    "#CFE8DD",

                    "#F8E8B0",

                    "#F7D6D0"
                ]
            )


            fig.update_traces(

                textposition="outside"
            )


            fig.update_layout(

                title="Students by Attendance Range",

                xaxis_title="Attendance Range",

                yaxis_title="Number of Students",

                height=400,

                showlegend=False,

                paper_bgcolor="rgba(0,0,0,0)",

                plot_bgcolor="rgba(0,0,0,0)"
            )


            st.plotly_chart(

                fig,

                use_container_width=True
            )


# ============================================================
# STUDENTS PAGE
# ============================================================

elif page == "👩‍🎓 Students":

    st.title("👩‍🎓 Student Corner")

    st.write(
        "Register students and organize your class information."
    )

    st.divider()


    students = st.session_state.students


    add_tab, directory_tab = st.tabs(

        [
            "🌷 Add Student",
            "📚 Student Directory"
        ]
    )


    # ========================================================
    # ADD STUDENT
    # ========================================================

    with add_tab:

        st.subheader(
            "Create Student Profile"
        )


        with st.form(
            "student_form"
        ):

            col1, col2 = st.columns(2)


            with col1:

                student_id = st.text_input(

                    "Student ID",

                    placeholder="23CSE001"
                )


                student_name = st.text_input(

                    "Student Name",

                    placeholder="Priyanka"
                )


                department = st.selectbox(

                    "Department",

                    [
                        "CSE",
                        "ECE",
                        "EEE",
                        "MECH",
                        "CIVIL",
                        "IT",
                        "AIML",
                        "DS"
                    ]
                )


            with col2:

                year = st.selectbox(

                    "Year",

                    [
                        "1st Year",
                        "2nd Year",
                        "3rd Year",
                        "4th Year"
                    ]
                )


                section = st.selectbox(

                    "Section",

                    [
                        "A",
                        "B",
                        "C",
                        "D",
                        "E"
                    ]
                )


                email = st.text_input(

                    "Email",

                    placeholder="student@gmail.com"
                )


            submit = st.form_submit_button(

                "🌸 Save Student",

                use_container_width=True
            )


            if submit:

                student_id = (

                    student_id

                    .strip()

                    .upper()
                )


                student_name = (

                    student_name

                    .strip()
                )


                if not student_id:

                    st.error(
                        "Please enter Student ID."
                    )


                elif not student_name:

                    st.error(
                        "Please enter student name."
                    )


                elif find_student(
                    student_id
                ):

                    st.error(
                        "This Student ID already exists."
                    )


                else:

                    new_student = {

                        "student_id":
                            student_id,

                        "name":
                            student_name,

                        "department":
                            department,

                        "year":
                            year,

                        "section":
                            section,

                        "email":
                            email.strip()
                    }


                    st.session_state.students.append(
                        new_student
                    )


                    save_json(

                        STUDENTS_FILE,

                        st.session_state.students
                    )


                    st.success(

                        "🌷 Student added successfully!"
                    )


                    st.rerun()


    # ========================================================
    # DIRECTORY
    # ========================================================

    with directory_tab:

        st.subheader(
            "📚 Student Directory"
        )


        students = st.session_state.students


        if not students:

            st.info(
                "No students registered yet."
            )

        else:

            search = st.text_input(

                "🔎 Search student",

                placeholder="Search by name or ID"
            )


            directory_df = pd.DataFrame(
                students
            )


            if search:

                directory_df = directory_df[

                    directory_df["name"]

                    .str.contains(

                        search,

                        case=False,

                        na=False
                    )

                    |

                    directory_df["student_id"]

                    .str.contains(

                        search,

                        case=False,

                        na=False
                    )
                ]


            st.dataframe(

                directory_df,

                use_container_width=True,

                hide_index=True
            )


# ============================================================
# MARK ATTENDANCE PAGE
# ============================================================

elif page == "🌼 Mark Attendance":

    st.title("🌼 Mark Attendance")

    st.write(
        "Record daily attendance in a few simple steps."
    )

    st.divider()


    students = st.session_state.students


    if not students:

        st.warning(

            "Please register students "
            "before marking attendance."
        )


    else:

        student_options = {}


        for student in students:

            display_name = (

                f"{student['student_id']} - "

                f"{student['name']}"
            )


            student_options[
                display_name
            ] = student["student_id"]


        with st.form(

            "attendance_form"
        ):

            date_value = st.date_input(

                "📅 Date",

                value=date.today()
            )


            selected_student = st.selectbox(

                "👩‍🎓 Student",

                list(
                    student_options.keys()
                )
            )


            subject = st.selectbox(

                "📚 Subject",

                [
                    "Data Structures",
                    "Database Management",
                    "Operating Systems",
                    "Computer Networks",
                    "Artificial Intelligence",
                    "Machine Learning",
                    "Web Development",
                    "Java Programming",
                    "Mathematics",
                    "Other"
                ]
            )


            status = st.radio(

                "Attendance",

                [
                    "Present",
                    "Absent"
                ],

                horizontal=True
            )


            remarks = st.text_area(

                "📝 Remarks",

                placeholder="Optional note"
            )


            save_button = st.form_submit_button(

                "🌷 Save Attendance",

                use_container_width=True
            )


            if save_button:

                student_id = student_options[
                    selected_student
                ]


                date_string = str(
                    date_value
                )


                duplicate = any(

                    record["student_id"]
                    == student_id

                    and record["date"]
                    == date_string

                    and record["subject"]
                    == subject

                    for record
                    in st.session_state.attendance
                )


                if duplicate:

                    st.error(

                        "This attendance record "
                        "already exists."
                    )


                else:

                    new_record = {

                        "student_id":
                            student_id,

                        "date":
                            date_string,

                        "subject":
                            subject,

                        "status":
                            status,

                        "remarks":
                            remarks.strip()
                    }


                    st.session_state.attendance.append(

                        new_record
                    )


                    save_json(

                        ATTENDANCE_FILE,

                        st.session_state.attendance
                    )


                    st.success(

                        "🌿 Attendance saved successfully!"
                    )


                    st.rerun()


# ============================================================
# REPORTS PAGE
# ============================================================

elif page == "📖 Reports":

    st.title("📖 Attendance Reports")

    st.write(
        "See how each student is performing across subjects."
    )

    st.divider()


    students = st.session_state.students


    if not students:

        st.info(

            "No students registered yet. "
            "Go to Students and add a student first."
        )


    else:

        student_options = {}


        for student in students:

            label = (

                f"{student['student_id']} - "

                f"{student['name']}"
            )


            student_options[
                label
            ] = student["student_id"]


        selected = st.selectbox(

            "👩‍🎓 Choose Student",

            list(
                student_options.keys()
            )
        )


        student_id = student_options[
            selected
        ]


        student = find_student(
            student_id
        )


        records = [

            record

            for record
            in st.session_state.attendance

            if record["student_id"]
            == student_id
        ]


        # ====================================================
        # STUDENT PROFILE
        # ====================================================

        st.subheader(
            f"🌷 {student['name']}"
        )


        st.caption(

            f"{student['student_id']}  •  "

            f"{student['department']}  •  "

            f"{student['year']}  •  "

            f"Section {student['section']}"
        )


        st.divider()


        # ====================================================
        # SUMMARY
        # ====================================================

        total_classes = len(
            records
        )


        present_classes = sum(

            1

            for record in records

            if record["status"]
            == "Present"
        )


        absent_classes = (

            total_classes

            - present_classes
        )


        if total_classes > 0:

            percentage = round(

                present_classes
                /
                total_classes
                *
                100,

                2
            )

        else:

            percentage = 0


        col1, col2, col3, col4 = st.columns(4)


        col1.metric(

            "📚 Classes",

            total_classes
        )


        col2.metric(

            "🌿 Present",

            present_classes
        )


        col3.metric(

            "🍑 Absent",

            absent_classes
        )


        col4.metric(

            "🌸 Percentage",

            f"{percentage}%"
        )


        st.progress(

            min(
                percentage / 100,
                1
            )
        )


        if percentage >= 75:

            st.success(

                "🌿 Great! Attendance is at or above 75%."
            )


        elif percentage >= 60:

            st.warning(

                "🍑 Attendance needs some improvement."
            )


        else:

            st.error(

                "🌸 Attendance is currently very low."
            )


        # ====================================================
        # REPORT VISUALIZATIONS
        # ====================================================

        if records:

            records_df = pd.DataFrame(
                records
            )


            # =================================================
            # SUBJECT PERFORMANCE
            # =================================================

            st.divider()


            st.subheader(

                "📚 Subject Performance"
            )


            subject_rows = []


            for subject_name in sorted(

                records_df[
                    "subject"
                ].unique()
            ):

                subject_records = records_df[

                    records_df[
                        "subject"
                    ]

                    == subject_name
                ]


                subject_total = len(
                    subject_records
                )


                subject_present = (

                    subject_records[
                        "status"
                    ]

                    == "Present"

                ).sum()


                subject_percentage = round(

                    subject_present

                    /

                    subject_total

                    *

                    100,

                    2
                )


                subject_rows.append(

                    {

                        "Subject":
                            subject_name,

                        "Attendance":
                            subject_percentage
                    }
                )


            subject_df = pd.DataFrame(

                subject_rows
            )


            fig = px.bar(

                subject_df,

                y="Subject",

                x="Attendance",

                orientation="h",

                text="Attendance",

                color="Attendance",

                color_continuous_scale=[

                    "#F7D6D0",

                    "#F9D8B4",

                    "#F8E8B0",

                    "#DCEAD8"
                ],

                range_x=[0, 100]
            )


            fig.update_traces(

                texttemplate="%{text}%",

                textposition="outside"
            )


            fig.update_layout(

                height=430,

                xaxis_title="Attendance %",

                yaxis_title="",

                coloraxis_showscale=False,

                paper_bgcolor="rgba(0,0,0,0)",

                plot_bgcolor="rgba(0,0,0,0)"
            )


            st.plotly_chart(

                fig,

                use_container_width=True
            )


            # =================================================
            # ATTENDANCE HEATMAP
            # =================================================

            st.subheader(

                "🌼 Attendance Calendar"
            )


            heatmap = records_df.copy()


            heatmap["Value"] = heatmap[
                "status"
            ].map(

                {
                    "Present": 1,

                    "Absent": 0
                }
            )


            heatmap = heatmap.pivot_table(

                index="subject",

                columns="date",

                values="Value",

                aggfunc="mean"
            )


            if not heatmap.empty:

                fig = px.imshow(

                    heatmap,

                    aspect="auto",

                    color_continuous_scale=[

                        "#F7D6D0",

                        "#F8E8B0",

                        "#DCEAD8"
                    ],

                    zmin=0,

                    zmax=1,

                    labels={

                        "x": "Date",

                        "y": "Subject",

                        "color": "Attendance"
                    }
                )


                fig.update_layout(

                    height=420,

                    paper_bgcolor="rgba(0,0,0,0)",

                    plot_bgcolor="rgba(0,0,0,0)"
                )


                st.plotly_chart(

                    fig,

                    use_container_width=True
                )


            # =================================================
            # DAILY TIMELINE
            # =================================================

            st.subheader(

                "🗓️ Daily Attendance Timeline"
            )


            daily_data = (

                records_df

                .groupby(

                    [
                        "date",
                        "status"
                    ]

                )

                .size()

                .reset_index(

                    name="Count"
                )
            )


            fig = px.area(

                daily_data,

                x="date",

                y="Count",

                color="status",

                color_discrete_map={

                    "Present":
                        "#DCEAD8",

                    "Absent":
                        "#F7D6D0"
                }
            )


            fig.update_layout(

                height=360,

                paper_bgcolor="rgba(0,0,0,0)",

                plot_bgcolor="rgba(0,0,0,0)"
            )


            st.plotly_chart(

                fig,

                use_container_width=True
            )


            # =================================================
            # HISTORY
            # =================================================

            st.subheader(

                "📋 Attendance History"
            )


            history = records_df.sort_values(

                "date",

                ascending=False
            )


            st.dataframe(

                history,

                use_container_width=True,

                hide_index=True
            )


        else:

            st.info(

                "No attendance records available "
                "for this student yet."
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()


st.caption(

    "🌷 Bloom Attendance  •  "
    "Python + Streamlit + Pandas + Plotly + JSON"
)