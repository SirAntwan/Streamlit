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
        /* Your existing CSS here */
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
                    // Similar logic for radio buttons
                }}

                if (newItem.id.startsWith('slider')) {{
                    // Similar logic for slider questions
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
