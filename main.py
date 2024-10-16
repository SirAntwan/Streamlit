import streamlit as st
import streamlit.components.v1 as components
import json

# Define the HTML and JavaScript for the drag-and-drop interface
sortable_html = """
    <div style="display: flex; justify-content: space-between; height: 400px;">
        <div style="width: 30%; padding-right: 20px; height: 100%; overflow-y: auto; border: 1px solid #ccc;">
            <h3>Available Components:</h3>
            <ul id="components" style="list-style: none; padding-left: 0;">
                <li id="text_input" class="draggable" style="padding: 10px; border: 1px solid #ccc; margin-bottom: 5px; cursor: grab;">Text Input</li>
                <li id="radio" class="draggable" style="padding: 10px; border: 1px solid #ccc; margin-bottom: 5px; cursor: grab;">Multiple Choice (Radio)</li>
                <li id="slider" class="draggable" style="padding: 10px; border: 1px solid #ccc; margin-bottom: 5px; cursor: grab;">Slider</li>
            </ul>
        </div>
        <div style="width: 65%; height: 100%; overflow-y: auto; border: 1px dashed #ccc;">
            <h3>Survey Canvas:</h3>
            <ul id="canvas" style="list-style: none; padding-left: 0; min-height: 300px;">
            </ul>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/sortablejs@1.14.0/Sortable.min.js"></script>
    <script>
        var componentsList = document.getElementById('components');
        var canvasList = document.getElementById('canvas');

        // Make the components list draggable
        new Sortable(componentsList, {
            animation: 150,
            group: "shared", // Use the same group for both lists
            sort: false, // Disable sorting in this list
            onEnd: function (evt) {
                let itemId = evt.item.id;

                // Create a new item element for the canvas
                var newItem = document.createElement('li');
                newItem.id = itemId + '_' + Date.now(); // Unique ID for each item
                newItem.innerText = evt.item.innerText;
                newItem.style.padding = "10px";
                newItem.style.border = "1px solid #ccc";
                newItem.style.marginBottom = "5px";
                newItem.style.cursor = "grab";
                canvasList.appendChild(newItem);
                
                // Send the updated canvas order to Streamlit
                updateCanvas();
            },
        });

        // Make the canvas list also draggable
        new Sortable(canvasList, {
            animation: 150,
            group: "shared",
            onEnd: function () {
                updateCanvas();
            },
        });

        // Function to send the canvas items back to Streamlit
        function updateCanvas() {
            let order = [];
            document.querySelectorAll('#canvas li').forEach(function(el) {
                order.push(el.id);
            });
            window.parent.postMessage({type: 'canvas_order', order: order}, '*');
        }
    </script>
"""

# Render the drag-and-drop interface
components.html(sortable_html, height=500)

# Initialize the session state to store canvas items
if 'canvas_items' not in st.session_state:
    st.session_state.canvas_items = []

# Function to handle messages from the drag-and-drop interface
def handle_message():
    message = st.experimental_get_query_params()
    if "canvas_order" in message:
        st.session_state.canvas_items = json.loads(message["canvas_order"][0])  # Save the order in session_state

# Handle messages (to capture the drag-and-drop order)
handle_message()

# Function to generate the survey based on the order in st.session_state
def generate_survey():
    st.write("### Preview your survey:")
    for item in st.session_state.canvas_items:
        if item.startswith('text_input'):
            st.text_input("Enter your name:")
        elif item.startswith('radio'):
            st.radio("Choose your favorite fruit:", ["Apple", "Banana", "Orange"])
        elif item.startswith('slider'):
            st.slider("Rate your experience:", 1, 10)

# Button to preview the survey
if st.button("Preview Survey"):
    generate_survey()
