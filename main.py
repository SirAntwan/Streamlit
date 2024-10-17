import streamlit as st
from streamlit_dnd import dnd

# Initialize session state
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = 0

def add_question(question_type, question_text):
    st.session_state.questions.append({'type': question_type, 'text': question_text})

def display_questions():
    for i, q in enumerate(st.session_state.questions):
        st.write(f"{i + 1}. {q['text']} ({q['type']})")
        if q['type'] == 'radio':
            options = st.multiselect(f"Select options for {q['text']}", ["Option 1", "Option 2", "Option 3"])
            st.session_state.questions[i]['options'] = options

# Survey Page
st.title("Drag-and-Drop Survey Builder")

# Adding Drag-and-Drop functionality
with st.form(key='survey_form'):
    # Create a drag-and-drop area for question types
    question_types = ["radio", "checkbox", "text", "slider"]  # Extend this list as needed
    dnd_data = dnd.drag_and_drop("Drag questions here", question_types)

    if dnd_data:
        question_text = st.text_input("Enter your question text")
        if st.button("Add Question"):
            add_question(dnd_data, question_text)
    
    # Display current questions
    st.write("Current Questions:")
    display_questions()

    # Navigation buttons
    if st.button("Next Page"):
        st.session_state.current_page += 1
        st.write(f"Navigating to page {st.session_state.current_page}...")

    if st.button("Submit Survey"):
        st.write("Survey submitted!")
        st.write(st.session_state.questions)

