import streamlit as st
import streamlit.components.v1 as components

# Title of the app
st.title("Drag-and-Drop Survey Builder")

# Sidebar with draggable components
with st.sidebar:
    st.header("Survey Components")
    st.markdown('<div draggable="true" ondragstart="drag(event)" id="textInput" style="margin: 10px; padding: 10px; background-color: lightgray; border-radius: 5px;">Text Input</div>', unsafe_allow_html=True)
    st.markdown('<div draggable="true" ondragstart="drag(event)" id="checkbox" style="margin: 10px; padding: 10px; background-color: lightgray; border-radius: 5px;">Checkbox</div>', unsafe_allow_html=True)
    st.markdown('<div draggable="true" ondragstart="drag(event)" id="multipleChoice" style="margin: 10px; padding: 10px; background-color: lightgray; border-radius: 5px;">Multiple Choice</div>', unsafe_allow_html=True)

# Survey canvas section
st.subheader("Survey Canvas")

# Add drag and drop functionality using an iframe with custom HTML and JavaScript
components.html("""
    <div style="display: flex;">
        <div id="survey-canvas" ondrop="drop(event)" ondragover="allowDrop(event)" 
             style="width: 100%; min-height: 400px; padding: 20px; border: 1px solid black; background-color: #f9f9f9;">
            <h3>Survey Canvas</h3>
            <p>Drop components here</p>
        </div>
    </div>

    <script>
        function allowDrop(ev) {
            ev.preventDefault();  // Necessary to allow drops
        }

        function drag(ev) {
            ev.dataTransfer.setData("text", ev.target.id);  // Pass the component ID
        }

        function drop(ev) {
            ev.preventDefault();  // Necessary to handle drop
            var data = ev.dataTransfer.getData("text");  // Get the dragged element's ID
            var nodeCopy = document.getElementById(data).cloneNode(true);  // Clone the dragged element
            nodeCopy.id = data + Math.random();  // Assign a unique ID to prevent duplicates
            nodeCopy.style.margin = "10px";  // Adjust margins for dropped elements
            ev.target.appendChild(nodeCopy);  // Append the cloned element to the canvas
        }
    </script>
    """, height=500)
