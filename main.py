import streamlit as st
import streamlit.components.v1 as components
import json

# Set the page to wide mode to ensure full width of the screen is used
st.set_page_config(layout="wide")

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
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/sortablejs@1.14.0/Sortable.min.js"></script>
    <script>
        var itemsEl = document.getElementById('items');
        var canvasEl = document.getElementById('canvas');

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
                }});

                if (newItem.id.startsWith('text_input')) {{
                    var inputBox = document.createElement('input');
                    inputBox.type = 'text';
                    inputBox.placeholder = 'Type your question here...';
                    inputBox.classList.add('input-box');
                    newItem.appendChild(inputBox);
                }}

                if (newItem.id.startsWith('radio')) {{
                    var optionCount = 2;
                    function createOptionBox(optionNumber) {{
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
                        removeButton.addEventListener('click', function () {{
                            optionsContainer.removeChild(optionContainer);
                            optionCount -= 1;
                        }});

                        optionContainer.appendChild(newOptionBox);
                        optionContainer.appendChild(removeButton);

                        return optionContainer;
                    }}

                    var questionBox = document.createElement('input');
                    questionBox.type = 'text';
                    questionBox.placeholder = 'Type your multiple choice question...';
                    questionBox.classList.add('input-box');

                    var optionsContainer = document.createElement('div');
                    var option1Container = createOptionBox(1);
                    var option2Container = createOptionBox(2);
                    optionsContainer.appendChild(option1Container);
                    optionsContainer.appendChild(option2Container);

                    var addButton = document.createElement('button');
                    addButton.textContent = 'Add Option';
                    addButton.classList.add('add-option-btn');

                    newItem.appendChild(questionBox);
                    newItem.appendChild(optionsContainer);
                    newItem.appendChild(addButton);

                    addButton.addEventListener('click', function () {{
                        optionCount += 1;
                        var newOptionContainer = createOptionBox(optionCount);
                        optionsContainer.appendChild(newOptionContainer);
                    }});
                }}

                if (newItem.id.startsWith('slider')) {{
                    var sliderQuestionBox = document.createElement('input');
                    sliderQuestionBox.type = 'text';
                    sliderQuestionBox.placeholder = 'Type your slider question...';
                    sliderQuestionBox.classList.add('input-box');

                    var minLabelBox = document.createElement('input');
                    minLabelBox.type = 'text';
                    minLabelBox.placeholder = 'Min Label';
                    minLabelBox.classList.add('input-box');

                    var maxLabelBox = document.createElement('input');
                    maxLabelBox.type = 'text';
                    maxLabelBox.placeholder = 'Max Label';
                    maxLabelBox.classList.add('input-box');

                    var minValueBox = document.createElement('input');
                    minValueBox.type = 'number';
                    minValueBox.placeholder = 'Min Value (Default 0)';
                    minValueBox.classList.add('input-box');

                    var maxValueBox = document.createElement('input');
                    maxValueBox.type = 'number';
                    maxValueBox.placeholder = 'Max Value (Default 100)';
                    maxValueBox.classList.add('input-box');

                    newItem.appendChild(sliderQuestionBox);
                    newItem.appendChild(minLabelBox);
                    newItem.appendChild(maxLabelBox);
                    newItem.appendChild(minValueBox);
                    newItem.appendChild(maxValueBox);
                }}

                newItem.appendChild(removeComponentButton);
                canvasEl.appendChild(newItem);
            }}
        }});
    </script>
"""

# Render the HTML/JS interface
components.html(sortable_html, height=1000)

# Initialize the session state to store the survey structure if not present
if 'survey_structure' not in st.session_state:
    st.session_state.survey_structure = []

# Function to handle messages from the drag-and-drop interface
def handle_message():
    message = st.experimental_get_query_params().get('message', None)
    if message:
        # Parse the message and update session state
        message_data = json.loads(message[0])
        st.session_state.survey_structure = message_data

# Call the handler to update survey structure
handle_message()

# Button to generate the code (code generation goes here)
if st.button("Generate Survey Code"):
    # Generate Python code based on `st.session_state.survey_structure`
    total_number_pages = len(st.session_state.survey_structure) + 1
    generated_code = f"""
import streamlit as st
import requests
import json

# Survey title and description
st.title("{survey_title}")
st.write("{survey_description}")

# Initialize session state for responses
if "current_page" not in st.session_state:
    st.session_state["current_page"] = 1

    """

    for idx, component in enumerate(st.session_state.survey_structure):
        if component["type"] == "text_input":
            generated_code += f"""
# Page {idx + 1} - Text Input
if st.session_state["current_page"] == {idx + 1}:
    st.text_input("{component['question']}")
            """
        elif component["type"] == "radio":
            generated_code += f"""
# Page {idx + 1} - Multiple Choice
if st.session_state["current_page"] == {idx + 1}:
    st.radio("{component['question']}", options={component['options']})
            """
        elif component["type"] == "slider":
            generated_code += f"""
# Page {idx + 1} - Slider
if st.session_state["current_page"] == {idx + 1}:
    st.slider("{component['question']}", min_value={component['min_value']}, max_value={component['max_value']})
            """

    # Display the generated code
    st.code(generated_code, language="python")
