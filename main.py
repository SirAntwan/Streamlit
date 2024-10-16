import streamlit as st
import streamlit.components.v1 as components
import json

# Initial components already on the canvas (can be modified to any starting structure)
initial_canvas = [
    {"id": "text_input", "type": "Text Input"},
    {"id": "radio", "type": "Multiple Choice (Radio)"},
    {"id": "slider", "type": "Slider"},
]

# Render the drag-and-drop interface with two columns: 
# One for dragging components and one for the canvas
sortable_html = """
    <div style="display: flex; justify-content: space-between; height: 400px;">
        <!-- Left Panel: Available Components -->
        <div style="width: 30%; padding-right: 20px; height: 100%; overflow-y: auto; border: 1px solid #ccc;">
            <h3>Available Components:</h3>
            <ul id="components" style="list-style: none; padding-left: 0;">
                <li id="text_input" class="draggable" style="padding: 10px; border: 1px solid #ccc; margin-bottom: 5px;">Text Input</li>
                <li id="radio" class="draggable" style="padding: 10px; border: 1px solid #ccc; margin-bottom: 5px;">Multiple Choice (Radio)</li>
                <li id="slider" class="draggable" style="padding: 10px; border: 1px solid #ccc; margin-bottom: 5px;">Slider</li>
            </ul>
        </div>
        
        <!-- Right Panel: Survey Canvas -->
        <div style="width: 65%; height: 100%; overflow-y: auto; border: 1px dashed #ccc;">
            <h3>Survey Canvas:</h3>
            <ul id="canvas" style="list-style: none; padding-left: 0; min-height: 300px;">
                <!-- Pre-filled canvas with initial components -->
                <li id="text_input" style="padding: 10px; border: 1px solid #ccc; margin-bottom: 5px;">Text Input</li>
                <li id="radio" style="padding: 10px; border: 1px solid #ccc; margin-bottom: 5px;">Multiple Choice (Radio)</li>
                <li id="slider" style="padding: 10px; border: 1px solid #ccc; margin-bottom: 5px;">Slider</li>
            </ul>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/sortablejs@1.14.0/Sortable.min.js"></script>
    <script>
        var componentsList = document.getElementById('components');
        var canvasList = document.getElementById('canvas');

        // Make the left panel draggable but do not remove items after dragging
        new Sortable(componentsList, {
            animation: 150,
            group: "shared",
            sort: false, // Do not allow sorting in the left panel
            onEnd: function (evt) {
                let itemId = evt.item.id;

                // Clone dragged item and append it to the canvas
                var newItem = document.createElement('li');
                newItem.id = itemId + '_' + Date.now();  // Unique ID for each dropped item
                newItem.innerText = evt.item.innerText;
                newItem.style.padding = "10px";
                newItem.style.border = "1px solid #ccc";
                newItem.style.marginBottom = "5px";
                newItem.style.cursor = "grab";

                // Remove the last component before appending a new on

                // Add the new item
                canvasList.appendChild(newItem);

                if (canvasList.lastChild) {
                    canvasList.removeChild(canvasList.lastChild);
                }

                // Send the updated canvas order to Streamlit
                updateCanvas();
            },
        });

        // Make the right panel (canvas) draggable and sortable
        new Sortable(canvasList, {
            animation: 150,
            group: "shared",
            onEnd: function () {
                updateCanvas();
            },
        });

        // Send the updated canvas order to Streamlit
        function updateCanvas() {
            let order = [];
            document.querySelectorAll('#canvas li').forEach(function(el) {
                order.push(el.id);
            });
            window.parent.postMessage({type: 'canvas_order', order: order}, '*');
        }
    </script>
"""

# Render the drag-and-drop interface
components.html(sortable_html, height=500)

# Initialize session state for the canvas items if not already initialized
if 'canvas_items' not in st.session_state:
    st.session_state.canvas_items = ['text_input', 'radio', 'slider']  # Start with initial canvas components

# Capture and handle incoming messages from the frontend
def handle_message():
    message = st.experimental_get_query_params()
    if "canvas_order" in message:
        new_order = json.loads(message["canvas_order"][0])

        # Update canvas items in session state
        st.session_state.canvas_items = new_order

# Handle message updates
handle_message()

# Function to generate the survey based on the canvas structure
def generate_survey():
    st.write("### Survey Preview:")
    for item in st.session_state.canvas_items:
        if item.startswith('text_input'):
            st.text_input("Enter your name:")
        elif item.startswith('radio'):
            st.radio("Choose your favorite fruit:", ["Apple", "Banana", "Orange"])
        elif item.startswith('slider'):
            st.slider("Rate your experience:", 1, 10)

# Button to preview the survey
if st.button("Preview Survey"):
    generate_survey()

# Function to generate Python code based on the survey structure
def generate_code():
    code = "import streamlit as st\n\n"
    code += "def main():\n"
    for item in st.session_state.canvas_items:
        if item.startswith("text_input"):
            code += "    st.text_input('Enter your name:')\n"
        elif item.startswith("radio"):
            code += "    st.radio('Choose your favorite fruit:', ['Apple', 'Banana', 'Orange'])\n"
        elif item.startswith("slider"):
            code += "    st.slider('Rate your experience:', 1, 10)\n"
    code += "\nif __name__ == '__main__':\n    main()"
    
    return code

# Button to download the generated Python code
if st.button("Generate Python Code"):
    code = generate_code()
    st.code(code, language='python')
    st.download_button("Download Python Code", code, file_name="survey.py")
