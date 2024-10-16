import streamlit as st
import streamlit.components.v1 as components

# Initialize session state for storing dropped components
if "dropped_components" not in st.session_state:
    st.session_state.dropped_components = []

# Sidebar with draggable components
with st.sidebar:
    st.header("Survey Components")
    st.markdown('<div draggable="true" ondragstart="drag(event)" id="text_input" style="margin: 10px; padding: 10px; background-color: lightblue;">Text Input</div>', unsafe_allow_html=True)
    st.markdown('<div draggable="true" ondragstart="drag(event)" id="checkbox" style="margin: 10px; padding: 10px; background-color: lightgreen;">Checkbox</div>', unsafe_allow_html=True)
    st.markdown('<div draggable="true" ondragstart="drag(event)" id="multiple_choice" style="margin: 10px; padding: 10px; background-color: lightcoral;">Multiple Choice</div>', unsafe_allow_html=True)

# Drop area (canvas)
st.subheader("Survey Canvas")

# Render the dropped components in the Streamlit session state
for comp in st.session_state.dropped_components:
    if comp == "text_input":
        st.text_input("Text Input")
    elif comp == "checkbox":
        st.checkbox("Checkbox")
    elif comp == "multiple_choice":
        st.radio("Multiple Choice", ["Option 1", "Option 2", "Option 3"])

# Add custom HTML + JS to handle drag-and-drop in the frontend
components.html(f"""
    <div style="border: 2px solid black; min-height: 300px; padding: 10px;" ondrop="drop(event)" ondragover="allowDrop(event)">
        <p>Drop components here:</p>
    </div>

    <script>
        function allowDrop(ev) {{
            ev.preventDefault();
            console.log("Allow drop event triggered");
        }}

        function drag(ev) {{
            console.log("Dragging: ", ev.target.id);
            ev.dataTransfer.setData("text", ev.target.id);
        }}

        function drop(ev) {{
            ev.preventDefault();
            var data = ev.dataTransfer.getData("text");
            console.log("Dropped component: ", data);
            // Send the dropped component to Streamlit's session state via an iframe form
            var iframe = document.createElement('iframe');
            iframe.style.display = 'none';
            iframe.src = '/?component=' + data;
            document.body.appendChild(iframe);
        }}
    </script>
""", height=350)

# Parse the URL for dropped component
query_params = st.experimental_get_query_params()
if "component" in query_params:
    dropped_component = query_params["component"][0]
    if dropped_component not in st.session_state.dropped_components:
        st.session_state.dropped_components.append(dropped_component)
