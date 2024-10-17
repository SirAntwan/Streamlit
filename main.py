import streamlit as st
import streamlit.components.v1 as components
import json

# Define the HTML and JavaScript for the drag-and-drop interface using Bootstrap for the layout
sortable_html = """
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css">

    <div class="container-fluid" style="padding-left: 0px;">
        <div class="row">
            <!-- Left Column (Components List) -->
            <div class="col-2 px-0" style="border-right: 1px solid #ccc; position: fixed; left: 0; top: 0; bottom: 0; height: 100%; background-color: #f8f9fa; padding-top: 20px; overflow-y: auto;">
                <h3 class="text-center">Drag and Drop Survey Elements:</h3>
                <ul id="items" class="list-unstyled">
                    <li id="text_input" class="p-2 border mb-2">Text Question</li>
                    <li id="radio" class="p-2 border mb-2">Multiple Choice (Radio)</li>
                    <li id="slider" class="p-2 border mb-2">Slider</li>
                </ul>
            </div>
            
            <!-- Right Column (Survey Canvas) -->
            <div class="col offset-2" style="padding-left: 20px;">
                <h3>Survey Canvas:</h3>
                <ul id="canvas" class="list-unstyled" style="min-height: 400px; border: 1px dashed #ccc;">
                </ul>
            </div>
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

                // Add a text box for the Text Question component
                if (newItem.id.startsWith('text_input')) {
                    var inputBox = document.createElement('input');
                    inputBox.type = 'text';
                    inputBox.placeholder = 'Type your question here...';
                    inputBox.style.display = 'block';
                    inputBox.style.marginTop = '5px';

                    newItem.appendChild(inputBox);
                }

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
            window.parent.postMessage({type: 'canvas_order', order: order}, '*');
        }
    </script>
"""

# Render drag-and-drop interface in Streamlit
components.html(sortable_html, height=600)

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
