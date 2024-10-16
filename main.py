import streamlit as st
import streamlit.components.v1 as components
import json

# Define the HTML and JavaScript for drag-and-drop interface (using Sortable.js)
sortable_html = """
    <h3>Drag and Drop Survey Elements:</h3>
    <ul id="items" style="list-style: none; padding-left: 0;">
        <li id="text_input" style="padding: 10px; border: 1px solid #ccc; margin-bottom: 5px;">Text Input</li>
        <li id="radio" style="padding: 10px; border: 1px solid #ccc; margin-bottom: 5px;">Multiple Choice (Radio)</li>
        <li id="slider" style="padding: 10px; border: 1px solid #ccc; margin-bottom: 5px;">Slider</li>
    </ul>

    <script src="https://cdn.jsdelivr.net/npm/sortablejs@1.14.0/Sortable.min.js"></script>
    <script>
        var el = document.getElementById('items');
        new Sortable(el, {
            animation: 150,
            onEnd: function (evt) {
                let order = [];
                document.querySelectorAll('#items li').forEach(function(el) {
                    order.push(el.id);
                });
                // Send the order back to Streamlit via postMessage
                window.parent.postMessage({type: 'order', order: order}, '*');
            },
        });
    </script>
"""

# Render drag-and-drop interface in Streamlit
components.html(sortable_html, height=300)

# Initialize the session state to store survey structure if not present
if 'survey_structure' not in st.session_state:
    st.session_state.survey_structure = []

# Function to handle messages from the drag-and-drop interface
def handle_message():
    # Use experimental_get_query_params to mock message capture
    message = st.experimental_get_query_params()
    if "order" in message:
        st.session_state.survey_structure = json.loads(message["order"][0])  # Save the order in session_state

# Handle messages (to capture the drag-and-drop order)
handle_message()

# Function to generate the survey based on the order in st.session_state
def generate_survey():
    st.write("### Preview your survey:")
    for item in st.session_state.survey_structure:
        if item == 'text_input':
            st.text_input("Enter your name:")
        elif item == 'radio':
            st.radio("Choose your favorite fruit:", ["Apple", "Banana", "Orange"])
        elif item == 'slider':
            st.slider("Rate your experience:", 1, 10)

# Button to preview the survey
if st.button("Preview Survey"):
    generate_survey()

# Function to generate Python code based on the survey structure
def generate_code():
    code = "import streamlit as st\n\n"
    code += "def main():\n"
    for item in st.session_state.survey_structure:
        if item == "text_input":
            code += "    st.text_input('Enter your name:')\n"
        elif item == "radio":
            code += "    st.radio('Choose your favorite fruit:', ['Apple', 'Banana', 'Orange'])\n"
        elif item == "slider":
            code += "    st.slider('Rate your experience:', 1, 10)\n"
    code += "\nif __name__ == '__main__':\n    main()"
    
    return code

# Allow the user to download the generated Python code
if st.button("Generate Python Code"):
    code = generate_code()
    st.code(code, language='python')
    st.download_button("Download Python Code", code, file_name="survey.py")
