import streamlit as st

# Initialize session state to store dropped components
if "canvas_components" not in st.session_state:
    st.session_state.canvas_components = []

# Function to handle component drop
def drop_component(component):
    st.session_state.canvas_components.append(component)

# Sidebar with draggable components
with st.sidebar:
    st.header("Survey Components")
    if st.button("Text Input"):
        drop_component("Text Input")
    if st.button("Checkbox"):
        drop_component("Checkbox")
    if st.button("Multiple Choice"):
        drop_component("Multiple Choice")

# Survey canvas
st.subheader("Survey Canvas")
st.write("Drop components here:")

# Display the dropped components in the canvas
for component in st.session_state.canvas_components:
    if component == "Text Input":
        st.text_input("Sample Text Input")
    elif component == "Checkbox":
        st.checkbox("Sample Checkbox")
    elif component == "Multiple Choice":
        st.radio("Sample Multiple Choice", options=["Option 1", "Option 2", "Option 3"])
