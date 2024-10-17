import streamlit as st
import streamlit.components.v1 as components
import json

# Set the page to wide mode to ensure the full width of the screen is used
st.set_page_config(layout="wide")

# Define the HTML and JavaScript for the drag-and-drop interface
sortable_html = """
    <style>
        body {
            margin: 0;
            padding: 0;
        }

        .left-column {
            width: 20%;
            border-right: 1px solid #ccc;
            position: fixed;
            left: 0;
            top: 0;
            height: 100%;
            background-color: #f8f9fa;
            padding-top: 20px;
            overflow-y: auto;
        }
        .right-column {
            margin-left: 20%;  
            padding-left: 20px;
        }

        /* Dynamically adjustable height for canvas */
        #canvas {
            list-style: none;
            padding-left: 0;
            border: 1px dashed #ccc;
            min-height: 200px;
            transition: all 0.3s ease;
        }
    </style>

    <div>
        <div class="left-column">
            <h3>Drag and Drop Survey Elements:</h3>
            <ul id="items" style="list-style: none; padding-left: 0;">
                <li id="text_input" style="padding: 10px; border: 1px solid #ccc; margin-bottom: 5px;">Text Question</li>
                <li id="radio" style="padding: 10px; border: 1px solid #ccc; margin-bottom: 5px;">Multiple Choice (Radio)</li>
                <li id="slider" style="padding: 10px; border: 1px solid #ccc; margin-bottom: 5px;">Slider</li>
            </ul>
        </div>

        <div class="right-column">
            <h3>Survey Canvas:</h3>
            <ul id="canvas"></ul>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/sortablejs@1.14.0/Sortable.min.js"></script>
    <script>
        var itemsEl = document.getElementById('items');
        var canvasEl = document.getElementById('canvas');

        // Make the components list draggable but not sortable
        new Sortable(itemsEl, {
            animation: 150,
            sort: false,
            group: {
                name: 'shared',
                pull: 'clone',  
                put: false      
            },
        });

        // Make the canvas list also draggable and sortable
        new Sortable(canvasEl, {
            animation: 150,
            group: {
                name: 'shared',  
                pull: false,     
                put: true        
            },
            onAdd: function (evt) {
                var newItem = evt.item;
                newItem.id = evt.item.id + '_' + Date.now(); // Unique ID

                // Ensure it doesn't appear in the original list again
                newItem.style.padding = "10px";
                newItem.style.border = "1px solid #ccc";
                newItem.style.marginBottom = "5px";

                if (newItem.id.startsWith('text_input')) {
                    var inputBox = document.createElement('input');
                    inputBox.type = 'text';
                    inputBox.placeholder = 'Type your question here...';
                    inputBox.style.display = 'block';
                    inputBox.style.marginTop = '5px';
                    newItem.appendChild(inputBox);
                }

                updateCanvasHeight();
                updateCanvas();
            },
            onEnd: function () {
                updateCanvasHeight();
                updateCanvas();
            },
        });

        // Adjust canvas height dynamically based on content
        function updateCanvasHeight() {
            var canvasHeight = canvasEl.scrollHeight;
            document.getElementById('canvas').style.minHeight = canvasHeight + 'px';
            window.parent.postMessage({height: document.body.scrollHeight}, "*");
        }

        // Send the canvas items back to Streamlit
        function updateCanvas() {
            let order = [];
            document.querySelectorAll('#canvas li').forEach(function(el) {
                order.push(el.id);
            });

            window.parent.postMessage({type: 'canvas_order', order: order}, '*');
        }

        window.addEventListener('load', function() {
            updateCanvasHeight();
            window.parent.postMessage({height: document.body.scrollHeight}, "*");
        });
    </script>
"""

# Render the HTML/JS interface
components.html(sortable_html, height=1000)

# Initialize the session state to store the survey structure if not present
if 'survey_structure' not in st.session_state:
    st.session_state.survey_structure = []

# Function to handle messages from the drag-and-drop interface
def handle_message():
    message = st.experimental_get_query_params().get("canvas_order")
    if message:
        st.session_state.survey_structure = json.loads(message[0]) 

handle_message()
