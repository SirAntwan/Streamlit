import streamlit as st
import json
import requests
import web3

# Global variables
total_number_pages = 24
placeholder_buttons = None

# Radio Options
q1_radio_options = ["Weekly", "Monthly", "Semi-annually", "Annually", "Less than Annually", "Never"]
yes_no_NotSure_radio_options = ["Yes", "No", "Not sure"]
yes_no_radio_options = ["Yes", "No"]
frequency_radio_options = ["Always", "Most of the time", "About half the time", "Sometimes", "Never"]

# Function to initialize session state for the survey
def initialize_survey():
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = 1
        st.session_state["Q1"] = None
        st.session_state["Q2"] = None
        st.session_state["Q3"] = None
        st.session_state["Q4"] = None
        st.session_state["Q5"] = None
        st.session_state["survey_loaded"] = False
        st.session_state["disabled"] = False

# Function to import and load an existing survey
def import_survey(uploaded_file):
    try:
        data = json.load(uploaded_file)
        st.session_state["survey_loaded"] = True
        st.session_state.update(data)  # Load the survey data into session state
        st.success("Survey successfully loaded!")
    except Exception as e:
        st.error(f"Failed to load survey: {e}")

# Function to export the current survey to a JSON file
def export_survey():
    survey_data = {
        "Q1": st.session_state.get("Q1"),
        "Q2": st.session_state.get("Q2"),
        "Q3": st.session_state.get("Q3"),
        "Q4": st.session_state.get("Q4"),
        "Q5": st.session_state.get("Q5")
    }
    return json.dumps(survey_data, indent=4)

# Function that records radio element changes 
def radio_change(element, state, key):
    st.session_state[state] = element.index(st.session_state[key])

# Page title and Upload section
st.set_page_config(page_title="Survey Import & Edit Example",)

st.title("Survey Import & Edit Example")
st.markdown("<style>.big-font {font-size:24px;}</style>", unsafe_allow_html=True)

# Initialize survey state
initialize_survey()

# File uploader to import existing surveys
uploaded_file = st.file_uploader("Upload a survey (JSON format)", type="json")
if uploaded_file:
    import_survey(uploaded_file)

# Export button to download the current survey as a JSON file
if st.session_state["survey_loaded"]:
    export_data = export_survey()
    st.download_button(label="Export Survey", data=export_data, file_name="exported_survey.json", mime="application/json")

# Progress bar and navigation for existing surveys
if st.session_state["survey_loaded"]:

    # Page 1: Display introduction
    if st.session_state["current_page"] == 1:
        st.markdown('<p class="big-font">Welcome to the survey editing interface!</p>', unsafe_allow_html=True)

        if st.button("Next"):
            st.session_state["current_page"] += 1
            st.rerun()

    # Page 2: Edit Question 1
    elif st.session_state["current_page"] == 2:
        st.radio(label="How frequently do you visit a healthcare provider to receive care for a medical problem?", 
                 options=q1_radio_options, 
                 index=st.session_state.get("Q1", None),
                 key='Q1_radio', 
                 on_change=radio_change, 
                 args=(q1_radio_options, "Q1", "Q1_radio",))

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Back"):
                st.session_state["current_page"] -= 1
                st.rerun()
        with col2:
            if st.button("Next"):
                if st.session_state["Q1"] is not None:
                    st.session_state["current_page"] += 1
                    st.rerun()
                else:
                    st.warning("Please answer this question")

    # Add similar editing logic for other questions in subsequent pages.
    # After reaching the last page, allow submission of the survey for storage.

    # Page 24: Submission page
    if st.session_state["current_page"] == 24:
        st.markdown('<p class="big-font">Thank you for editing the survey! Click to submit your responses.</p>', unsafe_allow_html=True)
        if st.button("Submit Responses"):
            st.success("Responses submitted successfully!")

    st.progress(st.session_state["current_page"] / total_number_pages)

