import streamlit as st
import streamlit.components.v1 as components
import json

# Step 1: Create the HTML + JavaScript for the drag-and-drop interface
sortable_html = """
    <div>
        <h3>Drag and Drop Survey Elements:</h3>
        <ul id="items" style="list-style-type: none; padding-left: 0;">
            <li id="text_input" style="padding: 10px; border: 1px solid #ccc; margin-bottom: 5px;">Text Input</li>
            <li id="radio" style="padding: 10px; border: 1px solid #ccc; margin-bottom: 5px;">Multiple Choice (Radio)</li>
            <li id="slider" style="padding: 10px; border: 1px solid #ccc; margin-bottom: 5px;">Slider</li>
        </ul>
    </div>
    
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
                // Send the order to Streamlit via postMessage
                window.parent.postMessage({type: 'order', order: order}, '*');
            },
        });
    </script>
"""

# Step 2: Render the HTML and JavaScript inside the Streamlit app
components.html(sortable_html, height=300)

# Step 3: Create a placeholder to store the survey structure
if 'survey_structure' not in st.session_state:
    st.session_state.survey_structure = []

# Step 4: Capture the order from the postMessage event
# You can listen to the JavaScript postMessage in Streamlit
def handle_message():
    message = st.experimental_get_query_params()
    if "order" in message:
        st.session_state.survey_structure = json.loads(message["order"][0])

# Step 5: Display the order of the elements that were dragged
handle_message()

# Show the current survey structure (element order)
st.write("### Survey Structure:")
st.write(st.session_state.survey_structure)

# Add a button to preview the survey
if st.button("Preview Survey"):
    for item in st.session_state.survey_structure:
        if item == 'text_input':
            st.text_input("Enter your name:")
        elif item == 'radio':
            st.radio("Choose your favorite fruit:", ["Apple", "Banana", "Orange"])
        elif item == 'slider':
            st.slider("Rate your experience:", 1, 10)
