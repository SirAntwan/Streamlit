import streamlit as st

# Placeholder to store created survey components
if "survey" not in st.session_state:
    st.session_state.survey = []

# Function to add a question to the survey
def add_question(question_type, question_text, options=None):
    question = {"type": question_type, "text": question_text, "options": options}
    st.session_state.survey.append(question)

# Display UI to add questions
st.title("Drag and Drop Survey Builder")

question_text = st.text_input("Enter question text:")
question_type = st.selectbox("Select question type", ["Radio", "Checkbox", "Text"])

if question_type in ["Radio", "Checkbox"]:
    options = st.text_area("Enter options (comma-separated)").split(",")
    if st.button("Add Question"):
        add_question(question_type, question_text, options)
else:
    if st.button("Add Question"):
        add_question(question_type, question_text)

# Display created questions
if st.session_state.survey:
    st.write("Current Survey:")
    for i, question in enumerate(st.session_state.survey):
        st.write(f"Q{i+1}: {question['text']} ({question['type']})")


def generate_python_code(survey):
    python_code = "import streamlit as st\n\n"
    python_code += "st.title('Generated Survey')\n\n"
    
    for i, question in enumerate(survey):
        if question['type'] == 'Radio':
            python_code += f"st.radio('{question['text']}', {question['options']})\n\n"
        elif question['type'] == 'Checkbox':
            python_code += f"st.checkbox('{question['text']}', {question['options']})\n\n"
        elif question['type'] == 'Text':
            python_code += f"st.text_input('{question['text']}')\n\n"
    
    return python_code

if st.button("Generate Python Code"):
    code = generate_python_code(st.session_state.survey)
    st.code(code, language='python')
