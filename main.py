import streamlit as st
import streamlit.components.v1 as components
import json

# Set the page to wide mode to ensure the full width of the screen is used
st.set_page_config(layout="wide")

# Define the HTML for including the external CSS and JS files
sortable_html = """
    <link rel="stylesheet" type="text/css" href="style.css">
    <div>
        <!-- Left Column (Components List) -->
        <div class="left-column">
            <h3>Drag and Drop Survey Elements:</h3>
            <ul id="items" style="list-style: none; padding-left: 0;">
                <li id="text_input" style="padding: 10px; border: 1px solid #ccc; margin-bottom: 5px;">Text Question</li>
                <li id="radio" style="padding: 10px; border: 1px solid #ccc; margin-bottom: 5px;">Multiple Choice (Radio)</li>
                <li id="slider" style="padding: 10px; border: 1px solid #ccc; margin-bottom: 5px;">Slider</li>
            </ul>
        </div>
        
        <!-- Right Column (Survey Canvas) -->
        <div class="right-column">
            <h3>Survey Canvas:</h3>
            <ul id="canvas" style="min-height: 400px;"></ul>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/sortablejs@1.14.0/Sortable.min.js"></script>
    <script src="script.js"></script>
"""

# Render drag-and-drop interface in Streamlit
components.html(sortable_html, height=1200)

# Initialize the session state to store the survey structure if not present
if 'survey_structure' not in st.session_state:
    st.session_state.survey_structure = []

# Function to handle messages from the drag-and-drop interface
def handle_message():
    # Try capturing the canvas order from URL parameters
    message = st.experimental_get_query_params().get("canvas_order")
    if message:
        st.session_state.survey_structure = json.loads(message[0])  # Save the order in session_state

# Handle messages (to capture the drag-and-drop order)
handle_message()

# Display current survey structure for debugging
st.write("Current Survey Structure:", st.session_state.survey_structure)
