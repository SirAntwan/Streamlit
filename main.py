import streamlit as st
import streamlit.components.v1 as components
import json

# Define the HTML and JavaScript for the drag-and-drop interface with Flexbox layout
sortable_html = """
    <div style="display: flex; justify-content: space-between;">
        <!-- Left Column (Components List) -->
        <div style="width: 45%; border-right: 1px solid #ccc; padding-right: 10px;">
            <h3>Drag and Drop Survey Elements:</h3>
            <ul id="items" style="list-style: none; padding-left: 0;">
                <li id="text_input" style="padding: 10px; border: 1px solid #ccc; margin-bottom: 5px;">Text Input</li>
                <li id="radio" style="padding: 10px; border: 1px solid #ccc; margin-bottom: 5px;">Multiple Choice (Radio)</li>
                <li id="slider" style="padding: 10px; border: 1px solid #ccc; margin-bottom: 5px;">Slider</li>
            </ul>
        </div>
        
        <!-- Right Column (Survey Canvas) -->
        <div style="width: 45%; padding-left: 10px;">
            <h3>Survey Canvas:</h3>
            <ul id="canvas" style="list-style: none; padding-left: 0; min-height: 200px; border: 1px dashed #ccc;">
            </ul>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/sortablejs@1.14.0/Sortable.min.js"></script>
    <script>
        var itemsEl = document.getElementById('items');
        var canvasEl = document.getElementById('canvas');

        // Make the components list draggable but not sortable
        new Sortable(itemsEl, {
            animation: 150,
            sort: false,  // Disable sorting in the components list
            group: {
                name: 'shared',
                pull: 'clone',  // Allow components to be dragged out but not moved
                put: false      // Prevent dropping back into the original list
            },
        });

        // Make the canvas list also draggable and sortable
        new Sortable(canvasEl, {
            animation: 150,
            group: {
                name: 'shared',  // Enable dragging between lists
                pull: false,     // Disable dragging from the canvas
                put: true        // Allow dropping components into the canvas
            },
            onAdd: function (evt) {
                var newItem = evt.item;
                newItem.id = evt.item.id + '_' + Date.now(); // Unique ID for each new item

                // Ensure it doesn't appear in the original list again
                newItem.style.padding = "10px";
                newItem.style.border = "1px solid #ccc";
                newItem.style.marginBottom = "5px";

                // Send the updated canvas order to Streamlit
                updateCanvas();
            },
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
            // Post the canvas order to the parent document (Streamlit)
            window.parent.postMessage(JSON.stringify({type: 'canvas_order', order: order}), '*');
        }
    </script>
"""

# Render the drag-and-drop interface
components.html(sortable_html, height=400, key="drag_drop_survey")

# Initialize session state for storing survey structure
if 'survey_structure' not in st.session_state:
    st.session_state.survey_structure = []

# Capture messages from frontend
message = st.experimental_get_query_params().get('canvas_order', None)

# Process the canvas order and update the session state
if message:
    st.session_state.survey_structure = json.loads(message[0])

# Display current survey structure
st.write("Current Survey Structure:", st.session_state.survey_structure)
