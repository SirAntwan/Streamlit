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

        // Make the components list draggable
        new Sortable(itemsEl, {
            animation: 150,
            onEnd: function (evt) {
                // Create a new item element for the canvas
                var newItem = document.createElement('li');
                newItem.id = evt.item.id + '_' + Date.now(); // Unique ID for each item
                newItem.innerText = evt.item.innerText;
                newItem.style.padding = "10px";
                newItem.style.border = "1px solid #ccc";
                newItem.style.marginBottom = "5px";
                canvasEl.appendChild(newItem);
                
                // Send the updated canvas order to Streamlit
                updateCanvas();
            },
        });

        // Make the canvas list also draggable
        new Sortable(canvasEl, {
            animation: 150,
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
components.html(sortable_html, height=400)

# Initialize the session state to store the survey structure if not present
if 'survey_structure' not in st.session_state:
    st.session_state.survey_structure = []

# Function to handle messages from the drag-and-drop interface
def handle_message():
    # Use experimental_get_query_params to capture the canvas order
    message = st.experimental_get_query_params()
    if "canvas_order" in message:
        st.session_state.survey_structure = json.loads(message["canvas_order"][0])  # Save the order in session_state

# Handle messages (to capture the drag-and-drop order)
handle_message()

# Function to generate the survey based on the order in st.session_state
def generate_survey():
    st.write("### Preview your survey:")
    for item in st.session_state.survey_structure:
        if item.startswith('text_input'):
            st.text_input(f"Enter your name (Text Input {item.split('_')[-1]}):")
        elif item.startswith('radio'):
            st.radio(f"Choose your favorite fruit (Radio {item.split('_')[-1]}):", ["Apple", "Banana", "Orange"])
        elif item.startswith('slider'):
            st.slider(f"Rate your experience (Slider {item.split('_')[-1]}):", 1, 10)

# Button to preview the survey
if st.button("Preview Survey"):
    generate_survey()

# Function to generate Python code based on the survey structure
def generate_code():
    code = "import streamlit as st\n\n"
    code += "def main():\n"
    for item in st.session_state.survey_structure:
        if item.startswith("text_input"):
            code += f"    st.text_input('Enter your name (Text Input {item.split('_')[-1]}):')\n"
        elif item.startswith("radio"):
            code += f"    st.radio('Choose your favorite fruit (Radio {item.split('_')[-1]}):', ['Apple', 'Banana', 'Orange'])\n"
        elif item.startswith("slider"):
            code += f"    st.slider('Rate your experience (Slider {item.split('_')[-1]}):', 1, 10)\n"
    code += "\nif __name__ == '__main__':\n    main()"
    
    return code

# Allow the user to download the generated Python code
if st.button("Generate Python Code"):
    code = generate_code()
    st.code(code, language='python')
    st.download_button("Download Python Code", code, file_name="survey.py")
