import streamlit as st
import streamlit.components.v1 as components
import json

# Set the page to wide mode to ensure the full width of the screen is used
st.set_page_config(layout="wide")

# Function to generate Python code for the survey
def generate_python_code(title, description, survey_elements):
    # Start of the Python code template
    code = f'''
import streamlit as st
import requests
import json

# Global variables
total_number_pages = {len(survey_elements) + 1}
placeholder_buttons = None

# Function that records radio element changes 
def radio_change(element, state, key):
    st.session_state[state] = element.index(st.session_state[key])  # Setting previously selected option

# Function that disables the last button while data is uploaded to IPFS 
def button_disable():
    st.session_state["disabled"] = True

# Changing the App title
st.set_page_config(page_title="IPFS-Based Survey")

# Page title
st.title("{title}")

# The following code centralizes all the buttons
st.markdown("<style>.row-widget.stButton {{text-align: center;}}</style>", unsafe_allow_html=True)

# The following code helps with the font size of text labels
st.markdown("<style>.big-font {{font-size:24px;}}</style>", unsafe_allow_html=True)  

# Initialize state
if "current_page" not in st.session_state:
    st.session_state["current_page"] = 1
    st.session_state["disabled"] = False
    '''
    
    # Add session state for each survey element
    for idx, element in enumerate(survey_elements):
        code += f'    st.session_state["Q{idx + 1}"] = None\n'

    # Page 1: Survey description
    code += f'''
# Page 1: Survey Introduction
if st.session_state["current_page"] == 1:

    st.markdown(f'<p class="big-font">{description}</p>', unsafe_allow_html=True)

    if st.button('Next'):
        st.session_state["current_page"] += 1
        st.rerun()

    # Progress bar
    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")
    '''

    # Generate code for each survey element on subsequent pages
    for idx, element in enumerate(survey_elements, start=2):
        if element["type"] == "radio":
            options = json.dumps(element["options"])
            code += f'''
# Page {idx}: Multiple Choice (Radio) Question
elif st.session_state["current_page"] == {idx}:

    q{idx - 1}_radio_options = {options}

    st.radio(label="{element['question']}", 
             options=q{idx - 1}_radio_options, 
             index=None if st.session_state["Q{idx - 1}"] == None else st.session_state["Q{idx - 1}"],
             key="Q{idx - 1}_radio", 
             on_change=radio_change, 
             args=(q{idx - 1}_radio_options, "Q{idx - 1}", "Q{idx - 1}_radio",))

st.markdown('<style> div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 24px;}</style> <br><br>', unsafe_allow_html=True)
    placeholder = st.empty()

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back'):
            st.session_state["current_page"] -= 1
            st.rerun()

    with col2:
        if st.button('Next'):
            if st.session_state["Q{idx - 1}"] != None:
                st.session_state["current_page"] += 1
                st.rerun()
            else:
                with placeholder.container():
                    st.warning("Please answer all the questions on this page.", icon="⚠️")

    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")
            '''

        elif element["type"] == "text_input":
            code += f'''
# Page {idx}: Text Input Question
elif st.session_state["current_page"] == {idx}:

    st.text_input(label="{element['question']}", 
                  value=None if st.session_state["Q{idx - 1}"] == None else st.session_state["Q{idx - 1}"],
                  key="Q{idx - 1}_input")

    placeholder = st.empty()

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back'):
            st.session_state["current_page"] -= 1
            st.rerun()

    with col2:
        if st.button('Next'):
            if st.session_state["Q{idx - 1}"] != None:
                st.session_state["current_page"] += 1
                st.rerun()
            else:
                with placeholder.container():
                    st.warning("Please answer all the questions on this page.", icon="⚠️")

    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")
            '''

        elif element["type"] == "slider":
            min_val, max_val = element["min"], element["max"]
            code += f'''
# Page {idx}: Slider Question
elif st.session_state["current_page"] == {idx}:

    st.slider(label="{element['question']}", 
              min_value={min_val}, max_value={max_val}, 
              value=None if st.session_state["Q{idx - 1}"] == None else st.session_state["Q{idx - 1}"],
              key="Q{idx - 1}_slider")

    placeholder = st.empty()

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back'):
            st.session_state["current_page"] -= 1
            st.rerun()

    with col2:
        if st.button('Submit'):
            if st.session_state["Q{idx - 1}"] != None:
                st.success("Thank you for your feedback!")
                # Code for submission and IPFS upload can go here
            else:
                with placeholder.container():
                    st.warning("Please answer all the questions on this page.", icon="⚠️")

    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")
            '''

    return code


# Add a text box for survey title and description
title = st.text_input("Survey Title", value="My Survey")
description = st.text_area("Survey Description", value="This is a description for the survey.")

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
                <li id="radio" style="padding: 10px; border: 1px solid #ccc; margin-bottom: 5px;">Multiple Choice</li>
                <li id="slider" style="padding: 10px; border: 1px solid #ccc; margin-bottom: 5px;">Slider Question</li>
            </ul>
        </div>

        <div class="right-column">
            <h3>Survey Preview</h3>
            <ul id="canvas"></ul>
        </div>
    </div>

    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.min.js"></script>
    <script>
        var counter = 0;

        // Make the items draggable to the canvas
        $("#items li").draggable({
            helper: "clone"
        });

        // Make the canvas a droppable area
        $("#canvas").droppable({
            accept: "#items li",
            drop: function(event, ui) {
                var type = ui.helper.attr("id");
                var id = counter++;
                if (type === "text_input") {
                    $(this).append(
                        '<li class="component-container" data-type="text_input" data-id="' + id + '">' +
                        '<label for="question">Text Question:</label>' +
                        '<input type="text" class="input-box question" name="question" data-id="' + id + '" />' +
                        '<button class="remove-component-btn" onclick="$(this).closest(\'li\').remove();">X</button>' +
                        '</li>'
                    );
                } else if (type === "radio") {
                    $(this).append(
                        '<li class="component-container" data-type="radio" data-id="' + id + '">' +
                        '<label for="question">Multiple Choice Question:</label>' +
                        '<input type="text" class="input-box question" name="question" data-id="' + id + '" placeholder="Enter your question" />' +
                        '<div class="options-container">' +
                        '<input type="text" class="input-box option" placeholder="Option 1" data-id="' + id + '" />' +
                        '<input type="text" class="input-box option" placeholder="Option 2" data-id="' + id + '" />' +
                        '</div>' +
                        '<button class="add-option-btn" onclick="addOption(this);">Add Option</button>' +
                        '<button class="remove-component-btn" onclick="$(this).closest(\'li\').remove();">X</button>' +
                        '</li>'
                    );
                } else if (type === "slider") {
                    $(this).append(
                        '<li class="component-container" data-type="slider" data-id="' + id + '">' +
                        '<label for="question">Slider Question:</label>' +
                        '<input type="text" class="input-box question" name="question" data-id="' + id + '" placeholder="Enter your question" />' +
                        '<input type="number" class="input-box min-value" name="min_value" placeholder="Min value" data-id="' + id + '" />' +
                        '<input type="number" class="input-box max-value" name="max_value" placeholder="Max value" data-id="' + id + '" />' +
                        '<button class="remove-component-btn" onclick="$(this).closest(\'li\').remove();">X</button>' +
                        '</li>'
                    );
                }
            }
        });

        // Add new options for radio buttons
        function addOption(button) {
            var optionsContainer = $(button).prev(".options-container");
            var optionCount = optionsContainer.children(".option").length + 1;
            optionsContainer.append('<input type="text" class="input-box option" placeholder="Option ' + optionCount + '" />');
        }

        // Function to collect the survey data in JSON format
        window.collectSurveyData = function() {
            var surveyElements = [];
            $("#canvas li").each(function() {
                var element = {};
                element.type = $(this).data("type");
                element.id = $(this).data("id");

                if (element.type === "text_input") {
                    element.question = $(this).find(".question").val();
                } else if (element.type === "radio") {
                    element.question = $(this).find(".question").val();
                    element.options = [];
                    $(this).find(".option").each(function() {
                        element.options.push($(this).val());
                    });
                } else if (element.type === "slider") {
                    element.question = $(this).find(".question").val();
                    element.min = $(this).find(".min-value").val();
                    element.max = $(this).find(".max-value").val();
                }

                surveyElements.push(element);
            });

            return JSON.stringify(surveyElements);
        };
    </script>
"""

# Embed the HTML in the Streamlit app
components.html(sortable_html, height=700)

# Button to generate the Python code
if st.button("Generate Python Code"):
    # Collect the survey data
    survey_data = components.html("return collectSurveyData();")

    if survey_data:
        # Generate Python code based on the collected survey data
        survey_elements = json.loads(survey_data)
        python_code = generate_python_code(title, description, survey_elements)

        # Display the generated code
        st.code(python_code, language="python")
