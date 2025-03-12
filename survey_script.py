import streamlit as st
import requests
import json
import web3

total_number_pages = 4
placeholder_buttons = None

Q2_radio_options = ["A","B"]
Q4_radio_options = [""]


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
st.title('Test 1')

st.markdown("<style>.row-widget.stButton {text-align: center;}</style>", unsafe_allow_html=True)
st.markdown("<style>.big-font {font-size:24px;}</style>", unsafe_allow_html=True)


if "current_page" not in st.session_state:
    st.session_state["current_page"] = 1
    st.session_state["Q1"] = None
    st.session_state["Q2"] = None
    st.session_state["Q3"] = None
    st.session_state["Q4"] = None
    st.session_state["disabled"] = False

# Page 1; Video
if st.session_state["current_page"]  == 1:

    st.markdown("""<p class="big-font">I am describing this survey.</p>""", unsafe_allow_html=True)

    st.text_area(label     = "Do you like pie?", 
             value= "" if st.session_state["Q1"] == None else st.session_state["Q1"],
             key       = 'Q1_text', 
             on_change = answer_change,
             args      = ( "Q1", "Q1_text",))

    st.markdown("""<style> div[class*="stText"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 18px;}</style> <br><br>""", unsafe_allow_html=True)


    st.radio(label     = "MC Question", 
             options   = Q2_radio_options, 
             index     = None if st.session_state["Q2"] == None else st.session_state["Q2"], 
             key       = 'Q2_radio', 
             on_change = radio_change, 
             args      = (Q2_radio_options, "Q2", "Q2_radio",))

    st.markdown("""<style> div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 18px;}</style> <br><br>""", unsafe_allow_html=True)


    placeholder = st.empty()

    if st.button('Next', key='next_button_page_1'):
        all_answered = True
        if st.session_state["Q1"] == None or st.session_state["Q1"] == []:
            all_answered = False
        if st.session_state["Q2"] == None or st.session_state["Q2"] == []:
            all_answered = False
        if all_answered:
            st.session_state["current_page"] += 1
            st.rerun()
        else:
            with placeholder.container():
                st.warning("Please answer all the questions on this page.", icon="⚠️")

    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")


elif st.session_state["current_page"] == 2:

    st.video("https://www.youtube.com/watch?v=qJxi122kxgQ") 
    st.markdown("""<p style='font-size:18px;'>Go Luka!</p>""", unsafe_allow_html=True)
    st.image("https://th.bing.com/th/id/OIP.M7inwN-YD5ycRt1VWQ9dCQHaEK?rs=1&pid=ImgDetMain") 
    st.markdown("""<p style='font-size:18px;'>Youtube</p>""", unsafe_allow_html=True)
    if st.session_state["Q3"] == None:
        st.session_state["Q3"] = 5
    st.slider(label="You messing with it?",min_value=0,max_value=10, 
             value= st.session_state["Q3"], 
             key = "Q3_slider",
             on_change = answer_change, 
             args = ("Q3", "Q3_slider",))
    st.markdown("""<style> div[class*="stSlider"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 18px;}</style> <br><br>""", unsafe_allow_html=True)


    placeholder = st.empty()

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back'):
            st.session_state["current_page"] -= 1
            st.rerun()
    with col2:
        if st.button('Next'):
            all_answered = True
            if st.session_state["Q3"] == None or st.session_state["Q3"] == []:
                all_answered = False
            if all_answered:
                st.session_state["current_page"] += 1
                st.rerun()
            else:
                with placeholder.container():
                    st.warning("Please answer all the questions on this page.", icon="⚠️")

    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")


elif st.session_state["current_page"] == 3:

    st.markdown("""<p style='font-size:18px;'>Page!</p>""", unsafe_allow_html=True)
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


elif st.session_state["current_page"] == 4:

    st.selectbox(label     = "1234567890asdfghjkl  No answer select question", 
             options   = Q4_radio_options, 
             index     = None if st.session_state["Q4"] == None else st.session_state["Q4"], 
             key       = 'Q4_radio', 
             on_change = radio_change, 
             args      = (Q4_radio_options, "Q4", "Q4_radio",))

    st.markdown("""<style> div[class*="stSelectbox"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 18px;}</style> <br><br>""", unsafe_allow_html=True)


    placeholder = st.empty()

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back'):
            st.session_state["current_page"] -= 1
            st.rerun()
    with col2:
        if st.button('Next'):
            all_answered = True
            if st.session_state["Q4"] == None or st.session_state["Q4"] == []:
                all_answered = False
            if all_answered:
                st.session_state["current_page"] += 1
                st.rerun()
            else:
                with placeholder.container():
                    st.warning("Please answer all the questions on this page.", icon="⚠️")

    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")


