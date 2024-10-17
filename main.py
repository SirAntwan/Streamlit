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

        // Function to update survey structure in the backend
        function updateSurveyStructure() {{
            var structure = [];
            var canvasItems = canvasEl.children;
            for (var i = 0; i < canvasItems.length; i++) {{
                var item = canvasItems[i];
                var componentType = item.id.split('_')[0];
                
                var component = {{
                    type: componentType
                }};
                
                if (componentType === 'text_input') {{
                    component.question = item.querySelector('input').value;
                }}
                if (componentType === 'radio') {{
                    component.question = item.querySelector('input').value;
                    var options = item.querySelectorAll('.input-box');
                    component.options = Array.from(options).map(opt => opt.value);
                }}
                if (componentType === 'slider') {{
                    component.question = item.querySelector('input[type="text"]').value;
                    component.min_label = item.querySelector('input[placeholder="Min Label"]').value;
                    component.max_label = item.querySelector('input[placeholder="Max Label"]').value;
                    component.min_value = item.querySelector('input[type="number"][placeholder="Min Value (Default 0)"]').value || 0;
                    component.max_value = item.querySelector('input[type="number"][placeholder="Max Value (Default 100)"]').value || 100;
                }}
                structure.push(component);
            }}
            
            // Send the updated structure to the backend
            var message = encodeURIComponent(JSON.stringify(structure));
            window.location.href = "?message=" + message;
        }}

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
                    updateSurveyStructure();
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
                            updateSurveyStructure();
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
                        updateSurveyStructure();
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
                updateSurveyStructure();
            }},
            onSort: function () {{
                updateSurveyStructure();
            }},
            onRemove: function () {{
                updateSurveyStructure();
            }}
        }});
    </script>
"""

# Display the drag-and-drop interface in the Streamlit app
components.html(sortable_html, height=600)

# Check for survey structure updates from the front-end
if 'message' in st.experimental_get_query_params():
    survey_structure_json = st.experimental_get_query_params()['message'][0]
    st.session_state['survey_structure'] = json.loads(survey_structure_json)

# Display the current survey structure as JSON
if 'survey_structure' in st.session_state:
    st.write("Current Survey Structure:", st.session_state['survey_structure'])

# Code generation for Python based on the survey structure
generated_code = """
import streamlit as st

total_number_pages = {total_number_pages}
placeholder_buttons = None

# Function that records radio element changes 
def radio_change(element, state, key):
    st.session_state[state] = element.index(st.session_state[key]) # Setting previously selected option

# Function that disables the last button while data is uploaded to IPFS 
def button_disable():
    st.session_state["disabled"] = True

# Changing the App title
st.set_page_config(page_title="IPFS-Based Survey")

# Survey title and description
st.title("{survey_title}")
st.write("{survey_description}")
"""
# Display the generated code
st.code(generated_code, language="python")
