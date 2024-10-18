import streamlit as st
import streamlit.components.v1 as components
import json

# Set the page to wide mode to ensure full width of the screen is used
st.set_page_config(layout="wide")

# Initialize component count in session state
if 'component_count' not in st.session_state:
    st.session_state['component_count'] = 0

# Text input for survey title and description
survey_title = st.text_input("Survey Title", "Your Survey Title")
survey_description = st.text_area("Survey Description", "Enter a description for your survey here...")

# Define the HTML and JavaScript for the drag-and-drop interface
sortable_html = f"""
    <style>
        body {{
            margin: 0;
            padding: 0;
        }}
        .left-column {{
            width: 20%;
            border-right: 1px solid #ccc;
            position: fixed;
            left: 0;
            top: 0;
            height: 100%;
            background-color: #f8f9fa;
            padding-top: 20px;
            overflow-y: auto;
        }}
        .right-column {{
            margin-left: 20%;  
            padding-left: 20px;
        }}
        #canvas {{
            list-style: none;
            padding-left: 0;
            border: 1px dashed #ccc;
            min-height: 200px;
            transition: all 0.3s ease;
        }}
        .input-box {{
            width: 80%;
            padding: 5px;
            margin-top: 5px;
            margin-bottom: 5px;
            display: block;
        }}
        .add-option-btn {{
            margin-top: 10px;
            background-color: #007bff;
            color: white;
            border: none;
            padding: 8px;
            cursor: pointer;
        }}
        .add-option-btn:hover {{
            background-color: #0056b3;
        }}
        .remove-option-btn {{
            background-color: #dc3545;
            color: white;
            border: none;
            padding: 5px;
            cursor: pointer;
        }}
        .remove-option-btn:hover {{
            background-color: #c82333;
        }}
        .remove-component-btn {{
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
        }}
        .remove-component-btn:hover {{
            background-color: #c82333;
        }}
        .component-container {{
            position: relative;
            padding-right: 40px;
        }}
    </style>

    <div>
        <div class="left-column">
            <h3>Drag and Drop Survey Elements:</h3>
            <ul id="items" style="list-style: none; padding-left: 0;">
                <li id="text_input" style="padding: 10px; border: 1px solid #ccc; margin-bottom: 5px;">Text Question</li>
                <li id="radio" style="padding: 10px; border: 1px solid #ccc; margin-bottom: 5px;">Multiple Choice (Radio)</li>
                <li id="slider" style="padding: 10px; border: 1px solid #ccc; margin-bottom: 5px;">Slider Question</li>
            </ul>
        </div>

        <div class="right-column">
            <h3>Survey Canvas:</h3>
            <ul id="canvas"></ul>
            <div id="component_count">Total Components: {st.session_state['component_count']}</div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/sortablejs@1.14.0/Sortable.min.js"></script>
    <script>
        var itemsEl = document.getElementById('items');
        var canvasEl = document.getElementById('canvas');
        var componentCountEl = document.getElementById('component_count');

        // Function to update the component count in both the UI and the backend
        function updateComponentCount() {{
            var count = canvasEl.children.length;
            componentCountEl.textContent = 'Total Components: ' + count;

            // Send the updated count back to Streamlit via a query parameter
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "/?component_count=" + count, true);
            xhr.send();
        }}

        // Make the components list draggable but not sortable
        new Sortable(itemsEl, {{
            animation: 150,
            sort: false,
            group: {{
                name: 'shared',
                pull: 'clone',
                put: false
            }},
        }});

        // Make the canvas list also draggable and sortable
        new Sortable(canvasEl, {{
            animation: 150,
            group: {{
                name: 'shared',
                pull: false,
                put: true
            }},
            onAdd: function (evt) {{
                var newItem = evt.item;
                newItem.id = evt.item.id + '_' + Date.now(); // Unique ID

                newItem.style.padding = "10px";
                newItem.style.border = "1px solid #ccc";
                newItem.style.marginBottom = "5px";
                newItem.classList.add('component-container');

                var removeComponentButton = document.createElement('button');
                removeComponentButton.textContent = 'X';
                removeComponentButton.classList.add('remove-component-btn');
                removeComponentButton.addEventListener('click', function () {{
                    canvasEl.removeChild(newItem);
                    updateComponentCount(); // Update the count when an item is removed
                }});

                // Add component-specific elements
                if (newItem.id.startsWith('text_input')) {{
                    var inputBox = document.createElement('input');
                    inputBox.type = 'text';
                    inputBox.placeholder = 'Type your question here...';
                    inputBox.classList.add('input-box');
                    newItem.appendChild(inputBox);
                }}

                if (newItem.id.startsWith('radio')) {{
    // Create input for the question text
    var questionBox = document.createElement('input');
    questionBox.type = 'text';
    questionBox.placeholder = 'Type your multiple choice question...';
    questionBox.classList.add('input-box');
    
    // Create a container for options
    var optionsContainer = document.createElement('div');
    
    // Function to create a single option box
    function createOptionBox(optionNumber) {{
        var optionContainer = document.createElement('div');
        optionContainer.style.display = 'flex';
        optionContainer.style.alignItems = 'center';
        
        var optionBox = document.createElement('input');
        optionBox.type = 'text';
        optionBox.placeholder = 'Option ' + optionNumber;
        optionBox.classList.add('input-box');
        
        var removeButton = document.createElement('button');
        removeButton.textContent = 'Remove';
        removeButton.classList.add('remove-option-btn');
        removeButton.style.marginLeft = '10px';
        
        removeButton.addEventListener('click', function () {{
            optionsContainer.removeChild(optionContainer);
     }});
        
        optionContainer.appendChild(optionBox);
        optionContainer.appendChild(removeButton);
        
        return optionContainer;
    }}

    // Add initial options
    var option1 = createOptionBox(1);
    var option2 = createOptionBox(2);
    optionsContainer.appendChild(option1);
    optionsContainer.appendChild(option2);

    // Button to add more options
    var addOptionButton = document.createElement('button');
    addOptionButton.textContent = 'Add Option';
    addOptionButton.classList.add('add-option-btn');
    
    addOptionButton.addEventListener('click', function () {{
        var optionCount = optionsContainer.children.length + 1;
        var newOption = createOptionBox(optionCount);
        optionsContainer.appendChild(newOption);
    }});

    // Append the question box, options container, and add button to the new item
    newItem.appendChild(questionBox);
    newItem.appendChild(optionsContainer);
    newItem.appendChild(addOptionButton);
}}


                if (newItem.id.startsWith('slider')) {{
    // Create input for the slider question
    var questionBox = document.createElement('input');
    questionBox.type = 'text';
    questionBox.placeholder = 'Type your slider question...';
    questionBox.classList.add('input-box');
    
    // Create input for minimum label
    var minLabelBox = document.createElement('input');
    minLabelBox.type = 'text';
    minLabelBox.placeholder = 'Min Label';
    minLabelBox.classList.add('input-box');

    // Create input for maximum label
    var maxLabelBox = document.createElement('input');
    maxLabelBox.type = 'text';
    maxLabelBox.placeholder = 'Max Label';
    maxLabelBox.classList.add('input-box');
    
    // Create input for minimum value
    var minValueBox = document.createElement('input');
    minValueBox.type = 'number';
    minValueBox.placeholder = 'Min Value (Default 0)';
    minValueBox.classList.add('input-box');

    // Create input for maximum value
    var maxValueBox = document.createElement('input');
    maxValueBox.type = 'number';
    maxValueBox.placeholder = 'Max Value (Default 100)';
    maxValueBox.classList.add('input-box');

    // Append the slider inputs to the new item
    newItem.appendChild(questionBox);
    newItem.appendChild(minLabelBox);
    newItem.appendChild(maxLabelBox);
    newItem.appendChild(minValueBox);
    newItem.appendChild(maxValueBox);
                }}


                newItem.appendChild(removeComponentButton);
                canvasEl.appendChild(newItem);
                updateComponentCount(); // Update the count when an item is added
            }}
        }});
    </script>
"""

# Render the HTML/JS interface
components.html(sortable_html, height=1000)

# Update the component count in the backend
if st.experimental_get_query_params().get('component_count'):
    st.session_state['component_count'] = int(st.experimental_get_query_params()['component_count'][0])

# Display the current component count
st.write(f"Current number of components: {st.session_state['component_count']}")

# Button to generate the code (code generation goes here)
if st.button("Generate Survey Code"):
    # Generate Python code based on st.session_state.survey_structure
    total_number_pages = len(st.session_state.survey_structure) + 1
    generated_code = f"""
import streamlit as st

total_number_pages = {total_number_pages}

st.set_page_config(page_title="Survey App")

# Survey title and description
st.title("{survey_title}")
st.write("{survey_description}")
"""
    # Display the generated code
    st.code(generated_code, language="python")