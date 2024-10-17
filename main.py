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

        #canvas {
            list-style: none;
            padding-left: 0;
            border: 1px dashed #ccc;
            min-height: 200px;
            transition: all 0.3s ease;
        }

        /* Increase the width of text boxes */
        .input-box {
            width: 80%;
            padding: 5px;
            margin-top: 5px;
            margin-bottom: 5px;
            display: block;
        }

        .add-option-btn {
            margin-top: 10px;
            background-color: #007bff;
            color: white;
            border: none;
            padding: 8px;
            cursor: pointer;
        }

        .add-option-btn:hover {
            background-color: #0056b3;
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

                // Add a text box for the Text Question component
                if (newItem.id.startsWith('text_input')) {
                    var inputBox = document.createElement('input');
                    inputBox.type = 'text';
                    inputBox.placeholder = 'Type your question here...';
                    inputBox.classList.add('input-box');
                    newItem.appendChild(inputBox);
                }

                // Add functionality for the Multiple Choice (Radio) component
                if (newItem.id.startsWith('radio')) {
                    // Add a text box for the question
                    var questionBox = document.createElement('input');
                    questionBox.type = 'text';
                    questionBox.placeholder = 'Type your multiple choice question...';
                    questionBox.classList.add('input-box');

                    // Add two text boxes for the initial options
                    var option1Box = document.createElement('input');
                    option1Box.type = 'text';
                    option1Box.placeholder = 'Option 1';
                    option1Box.classList.add('input-box');

                    var option2Box = document.createElement('input');
                    option2Box.type = 'text';
                    option2Box.placeholder = 'Option 2';
                    option2Box.classList.add('input-box');

                    // Add a button to add more options dynamically
                    var addButton = document.createElement('button');
                    addButton.textContent = 'Add Option';
                    addButton.classList.add('add-option-btn');
                    
                    // Container for options
                    var optionsContainer = document.createElement('div');
                    optionsContainer.appendChild(option1Box);
                    optionsContainer.appendChild(option2Box);

                    // Append the question box and options container to the new item
                    newItem.appendChild(questionBox);
                    newItem.appendChild(optionsContainer);
                    newItem.appendChild(addButton);

                    // Add event listener to the button to add new options dynamically
                    addButton.addEventListener('click', function () {
                        var newOptionBox = document.createElement('input');
                        newOptionBox.type = 'text';
                        newOptionBox.placeholder = 'New Option';
                        newOptionBox.classList.add('input-box');
                        optionsContainer.appendChild(newOptionBox);
                    });
                }

                updateCanvas();
            },
            onEnd: function () {
                updateCanvas();
            },
        });

        // Send the canvas items back to Streamlit
        function updateCanvas() {
            let order = [];
            document.querySelectorAll('#canvas li').forEach(function(el) {
                order.push(el.id);
            });

            window.parent.postMessage({type: 'canvas_order', order: order}, '*');
        }

        window.addEventListener('load', function() {
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
