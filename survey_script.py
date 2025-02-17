import streamlit as st
import requests
import json
import web3

total_number_pages = 3
placeholder_buttons = None



# Function that records radio element changes
def radio_change(element, state, key):
   st.session_state[state] = element.index(st.session_state[key]) # Setting previously selected option

def multi_change(element, state, key):
   st.session_state[state] = []
   for selected_option in st.session_state[key]:
       st.session_state[state].append(selected_option)

# Function that disables the last button while data is uploaded to IPFS
def button_disable():
   st.session_state['disabled'] = True

def answer_change(state, key):
   st.session_state[state] = st.session_state[key]

st.set_page_config(page_title='IPFS-Based Survey',)
st.title('')

st.markdown("<style>.row-widget.stButton {text-align: center;}</style>", unsafe_allow_html=True)
st.markdown("<style>.big-font {font-size:24px;}</style>", unsafe_allow_html=True)


if "current_page" not in st.session_state:
    st.session_state["current_page"] = 1
    st.session_state["disabled"] = False

# Page 1; Video
if st.session_state["current_page"]  == 1:

    st.markdown("""<p class="big-font"></p>""", unsafe_allow_html=True)

    st.video("") 
    placeholder = st.empty()

    if st.button('Next', key='next_button_page_1'):
        all_answered = True
        if all_answered:
            st.session_state["current_page"] += 1
            st.rerun()
        else:
            with placeholder.container():
                st.warning("Please answer all the questions on this page.", icon="⚠️")

    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")


elif st.session_state["current_page"] == 2:

    placeholder = st.empty()

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back'):
            st.session_state["current_page"] -= 1
            st.rerun()
    with col2:
        if st.button('Next'):
            all_answered = True
            if all_answered:
                st.session_state["current_page"] += 1
                st.rerun()
            else:
                with placeholder.container():
                    st.warning("Please answer all the questions on this page.", icon="⚠️")

    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")


elif st.session_state["current_page"] == 3:

    placeholder = st.empty()

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back'):
            st.session_state["current_page"] -= 1
            st.rerun()
    with col2:
        if st.button('Next'):
            all_answered = True
            if all_answered:
                st.session_state["current_page"] += 1
                st.rerun()
            else:
                with placeholder.container():
                    st.warning("Please answer all the questions on this page.", icon="⚠️")

    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")


