import streamlit as st
import streamlit.components.v1 as components

# Title of the app
st.title("Drag-and-Drop Survey Builder")

# Sidebar with components list
with st.sidebar:
    st.header("Survey Components")
    # Draggable components
    st.markdown(
        """
        <div id="components-list">
            <div draggable="true" ondragstart="drag(event)" id="textInput" style="margin: 10px; padding: 10px; background-color: lightgray;">
                Text Input
            </div>
            <div draggable="true" ondragstart="drag(event)" id="checkbox" style="margin: 10px; padding: 10px; background-color: lightgray;">
                Checkbox
            </div>
            <div draggable="true" ondragstart="drag(event)" id="multipleChoice" style="margin: 10px; padding: 10px; background-color: lightgray;">
                Multiple Choice
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Survey canvas section
st.subheader("Survey Canvas")

# Add drag and drop functionality using an iframe with custom HTML
components.html(f"""
    <div style="display: flex;">
        <div id="components-list" style="width: 40%; padding: 10px; border-right: 1px solid black;">
            <h3>Components</h3>
            <div draggable="true" ondragstart="drag(event)" id="textInput" style="margin: 10px; padding: 10px; background-color: lightgray;">
                Text Input
            </div>
            <div draggable="true" ondragstart="drag(event)" id="checkbox" style="margin: 10px; padding: 10px; background-color: lightgray;">
                Checkbox
            </div>
            <div draggable="true" ondragstart="drag(event)" id="multipleChoice" style="margin: 10px; padding: 10px; background-color: lightgray;">
                Multiple Choice
            </div>
        </div>
        <div id="survey-canvas" ondrop="drop(event)" ondragover="allowDrop(event)" style="width: 60%; min-height: 400px; padding: 20px; border: 1px solid black;">
            <h3>Survey Canvas</h3>
            <p>Drop components here</p>
        </div>
    </div>

    <script>
        function allowDrop(ev) {{
            ev.preventDefault();
        }}

        function drag(ev) {{
            ev.dataTransfer.setData("text", ev.target.id);
        }}

        function drop(ev) {{
            ev.preventDefault();
            var data = ev.dataTransfer.getData("text");
            var nodeCopy = document.getElementById(data).cloneNode(true);
            ev.target.appendChild(nodeCopy);
        }}
    </script>
""", height=500)
