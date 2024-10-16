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
        function allowDrop(ev) {
            ev.preventDefault();  // Allows dropping by preventing default behavior
        }

        function drag(ev) {
            ev.dataTransfer.setData("text", ev.target.id);  // Store the ID of the dragged element
            console.log("Drag started: ", ev.target.id);  // Debugging: log the ID of the dragged element
        }

        function drop(ev) {
            ev.preventDefault();
            var data = ev.dataTransfer.getData("text");  // Get the ID of the dragged element
            console.log("Dropped: ", data);  // Debugging: log the ID of the dropped element

            // Find the dragged element by its ID
            var draggedElement = document.getElementById(data);
            if (draggedElement) {
                // Clone the dragged element
                var clone = draggedElement.cloneNode(true);
                clone.id = data + Math.random();  // Assign a new unique ID
                ev.target.appendChild(clone);  // Append the clone to the canvas
            } else {
                console.log("Element not found with ID: ", data);
            }
        }
    </script>
    """, height=500)
