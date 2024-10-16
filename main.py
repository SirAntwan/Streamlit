import streamlit as st
import streamlit.components.v1 as components

# Title of the app
st.title("Drag-and-Drop Survey Builder")

# Sidebar with draggable components
with st.sidebar:
    st.header("Survey Components")
    st.markdown('<div draggable="true" ondragstart="drag(event)" id="textInput" style="margin: 10px; padding: 10px; background-color: lightgray;">Text Input</div>', unsafe_allow_html=True)
    st.markdown('<div draggable="true" ondragstart="drag(event)" id="checkbox" style="margin: 10px; padding: 10px; background-color: lightgray;">Checkbox</div>', unsafe_allow_html=True)
    st.markdown('<div draggable="true" ondragstart="drag(event)" id="multipleChoice" style="margin: 10px; padding: 10px; background-color: lightgray;">Multiple Choice</div>', unsafe_allow_html=True)

# Survey canvas section
st.subheader("Survey Canvas")

# Add drag and drop functionality using an iframe with custom HTML
components.html("""
    <div style="display: flex;">
        <div id="survey-canvas" ondrop="drop(event)" ondragover="allowDrop(event)" style="width: 100%; min-height: 400px; padding: 20px; border: 1px solid black; background-color: #f9f9f9;">
            <h3>Survey Canvas</h3>
            <p>Drop components here</p>
        </div>
    </div>

    <script>
        // Allow dropping by preventing default behavior
        function allowDrop(ev) {
            ev.preventDefault();
        }

        // Store the dragged item's ID
        function drag(ev) {
            ev.dataTransfer.setData("text", ev.target.id);
        }

        // Handle dropping the item onto the canvas
        function drop(ev) {
            ev.preventDefault();
            var data = ev.dataTransfer.getData("text");
            var draggedElement = document.getElementById(data).cloneNode(true);
            draggedElement.id = data + Math.random();  // Ensure unique ID for new elements
            ev.target.appendChild(draggedElement);
        }
    </script>
    """, height=500)
