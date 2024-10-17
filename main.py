import streamlit as st
import json
import os
import importlib.util
import tempfile

# Global constants
total_number_pages = 24
placeholder_buttons = None

# Function to dynamically load the survey from a Python script
def load_survey_from_script(file_path):
    try:
        spec = importlib.util.spec_from_file_location("survey_module", file_path)
        survey_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(survey_module)
        return survey_module
    except Exception as e:
        st.error(f"Error loading survey from script: {e}")
        return None

# Function to initialize the survey state (from imported script)
def initialize_survey(survey_module):
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = 1
        st.session_state.update({f"Q{i}": None for i in range(1, 6)})  # Example of loading initial questions
        st.session_state["survey_loaded"] = True
        st.session_state["disabled"] = False
        st.session_state["radio_options"] = {
            "Q1": survey_module.q1_radio_options,
            "Q2": survey_module.yes_no_NotSure_radio_options,
            "Q3": survey_module.yes_no_radio_options,
            "Q4": survey_module.frequency_radio_options
        }

# Function to render the survey questions
def render_question(question_label, options, question_key):
    st.radio(label=question_label, 
             options=options, 
             index=st.session_state.get(question_key, None), 
             key=question_key,
             on_change=lambda: st.session_state.update({question_key: st.session_state[question_key]}))

# Function to handle exporting the modified survey to JSON
def export_survey_to_json():
    survey_data = {f"Q{i}": st.session_state.get(f"Q{i}") for i in range(1, 6)}
    return json.dumps(survey_data, indent=4)

# Streamlit app layout
st.title("Survey Import & Edit (Python Script)")

# File uploader to import the Python script defining the survey
uploaded_file = st.file_uploader("Upload a survey Python script (.py)", type="py")

if uploaded_file:
    # Create a temporary file to save the uploaded script
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    # Load the survey from the uploaded Python script
    survey_module = load_survey_from_script(tmp_file_path)
    if survey_module:
        st.success("Survey loaded successfully!")
        initialize_survey(survey_module)

        # Navigate and edit the survey
        if st.session_state["survey_loaded"]:
            if st.session_state["current_page"] == 1:
                st.markdown("### Page 1: Edit Question 1")
                render_question("How frequently do you visit a healthcare provider?", st.session_state["radio_options"]["Q1"], "Q1")
            
            # Additional pages and questions would follow similar logic
            elif st.session_state["current_page"] == 2:
                st.markdown("### Page 2: Edit Question 2")
                render_question("Have you ever experienced conflicting medical advice?", st.session_state["radio_options"]["Q2"], "Q2")

            # Navigation buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.session_state["current_page"] > 1 and st.button("Back"):
                    st.session_state["current_page"] -= 1
            with col2:
                if st.session_state["current_page"] < total_number_pages and st.button("Next"):
                    st.session_state["current_page"] += 1

            # Submit page or export
            if st.session_state["current_page"] == total_number_pages:
                st.markdown("### Thank you for completing the survey!")
                if st.button("Submit"):
                    st.success("Survey submitted successfully!")

            # Export button to download the modified survey
            export_data = export_survey_to_json()
            st.download_button(label="Export Survey to JSON", data=export_data, file_name="modified_survey.json", mime="application/json")

# Cleanup temp files
if uploaded_file:
    os.remove(tmp_file_path)
