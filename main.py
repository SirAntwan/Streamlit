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

        .remove-option-btn {
            background-color: #dc3545;
            color: white;
            border: none;
            padding: 5px;
            cursor: pointer;
        }

        .remove-option-btn:hover {
            background-color: #c82333;
        }

        .remove-component-btn {
            position: absolute;
            right: 10px;
            top: 10px;
            background-color: #dc3545;
            color: white;
            border: none;
            font-size: 20px;
            font-weight: bold;
            cursor: pointer;
            padding: 5px 10px;
        }

        .remove-component-btn:hover {
            background-color: #c82333;
        }

        .component-container {
            position: relative;
            padding-right: 40px;  /* Ensure space for the 'X' button */
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
                newItem.classList.add('component-container');  // To ensure proper layout

                // Add a "Remove Component" button as 'X' to delete the whole component
                var removeComponentButton = document.createElement('button');
                removeComponentButton.textContent = 'X';
                removeComponentButton.classList.add('remove-component-btn');

                removeComponentButton.addEventListener('click', function () {
                    canvasEl.removeChild(newItem);  // Remove the entire component
                });

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
                    var optionCount = 2; // Initial options are 2
                    
                    // Function to create a new option box with remove button
                    function createOptionBox(optionNumber) {
                        var optionContainer = document.createElement('div');
                        optionContainer.style.display = 'flex';
                        optionContainer.style.alignItems = 'center';
                        
                        var newOptionBox = document.createElement('input');
                        newOptionBox.type = 'text';
                        newOptionBox.placeholder = 'Option ' + optionNumber;
                        newOptionBox.classList.add('input-box');
                        
                        var removeButton = document.createElement('button');
                        removeButton.textContent = 'Remove';
                        removeButton.classList.add('remove-option-btn');
                        removeButton.style.marginLeft = '10px';
                        
                        // Remove the option when clicked
                        removeButton.addEventListener('click', function () {
                            optionsContainer.removeChild(optionContainer);
                            optionCount -= 1;  // Reduce the option count by 1
                        });

                        optionContainer.appendChild(newOptionBox);
                        optionContainer.appendChild(removeButton);

                        return optionContainer;
                    }

                    // Add a text box for the question
                    var questionBox = document.createElement('input');
                    questionBox.type = 'text';
                    questionBox.placeholder = 'Type your multiple choice question...';
                    questionBox.classList.add('input-box');

                    // Container for options
                    var optionsContainer = document.createElement('div');

                    // Initial options with remove buttons
                    var option1Container = createOptionBox(1);
                    var option2Container = createOptionBox(2);
                    
                    optionsContainer.appendChild(option1Container);
                    optionsContainer.appendChild(option2Container);

                    // Add a button to add more options dynamically
                    var addButton = document.createElement('button');
                    addButton.textContent = 'Add Option';
                    addButton.classList.add('add-option-btn');

                    // Append the question box, options container, and add button to the new item
                    newItem.appendChild(questionBox);
                    newItem.appendChild(optionsContainer);
                    newItem.appendChild(addButton);

                    // Add event listener to the button to add new options dynamically
                    addButton.addEventListener('click', function () {
                        optionCount += 1;
                        var newOptionContainer = createOptionBox(optionCount);  // Create new option with remove button
                        optionsContainer.appendChild(newOptionContainer);
                    });
                }

                // Add functionality for the Slider component
                if (newItem.id.startsWith('slider')) {
                    // Add a text box for the question
                    var questionBox = document.createElement('input');
                    questionBox.type = 'text';
                    questionBox.placeholder = 'Type your slider question...';
                    questionBox.classList.add('input-box');
                    
                    // Add inputs for labels on both sides of the slider
                    var minLabelBox = document.createElement('input');
                    minLabelBox.type = 'text';
                    minLabelBox.placeholder = 'Label for min value';
                    minLabelBox.classList.add('input-box');

                    var maxLabelBox = document.createElement('input');
                    maxLabelBox.type = 'text';
                    maxLabelBox.placeholder = 'Label for max value';
                    maxLabelBox.classList.add('input-box');
                    
                    // Add inputs for min and max slider values
                    var minValueBox = document.createElement('input');
                    minValueBox.type = 'number';
                    minValueBox.placeholder = 'Min value';
                    minValueBox.classList.add('input-box');

                    var maxValueBox = document.createElement('input');
                    maxValueBox.type = 'number';
                    maxValueBox.placeholder = 'Max value';
                    maxValueBox.classList.add('input-box');
                    
                    // Append everything to the new slider component
                    newItem.appendChild(questionBox);
                    newItem.appendChild(minLabelBox);
                    newItem.appendChild(maxLabelBox);
                    newItem.appendChild(minValueBox);
                    newItem.appendChild(maxValueBox);
                    
                    // Create a slider element
                    var slider = document.createElement('input');
                    slider.type = 'range';
                    slider.min = minValueBox.value || 0;  // Default min value
                    slider.max = maxValueBox.value || 100;  // Default max value
                    slider.value = (slider.max - slider.min) / 2; // Default position in the middle
                    slider.style.width = '100%';
                    
                    // Update slider min and max values based on input
                    minValueBox.addEventListener('change', function () {
                        slider.min = minValueBox.value;
                        slider.value = Math.max(slider.value, slider.min); // Adjust slider if needed
                    });

                    maxValueBox.addEventListener('change', function () {
                        slider.max = maxValueBox.value;
                        slider.value = Math.min(slider.value, slider.max); // Adjust slider if needed
                    });

                    // Append the slider to the new item
                    newItem.appendChild(slider);
                }

                // Append the Remove Component button ('X') to the new item
                newItem.appendChild(removeComponentButton);

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
