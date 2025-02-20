import streamlit as st
import requests
import json
import web3

total_number_pages = 7
placeholder_buttons = None

Q2_radio_options = ["Yes","No"]
Q4_radio_options = ["Option 1 multi","Option 2 multi"]
Q5_radio_options = ["Option 1 Radio","Option 2 Radio"]
Q6_radio_options = ["Green","Red","Blue","Yellow"]
Q7_radio_options = ["Yes","No","Ur dumb"]
Q10_radio_options = ["IDK","Of Course","STFU!!!!!","Inner demons"]


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
st.title('Newest Test')

st.markdown("<style>.row-widget.stButton {text-align: center;}</style>", unsafe_allow_html=True)
st.markdown("<style>.big-font {font-size:24px;}</style>", unsafe_allow_html=True)


if "current_page" not in st.session_state:
    st.session_state["current_page"] = 1
    st.session_state["Q1"] = None
    st.session_state["Q2"] = None
    st.session_state["Q3"] = None
    st.session_state["Q4"] = None
    st.session_state["Q5"] = None
    st.session_state["Q6"] = None
    st.session_state["Q7"] = None
    st.session_state["Q8"] = None
    st.session_state["Q9"] = None
    st.session_state["Q10"] = None
    st.session_state["disabled"] = False

# Page 1; Video
if st.session_state["current_page"]  == 1:

    st.markdown("""<p class="big-font">This is a Test of the latest version of the survey builder Tool</p>""", unsafe_allow_html=True)

    st.video("https://www.youtube.com/watch?v=aJb6Dov0jlM") 
    st.text_area(label     = "This is a text Question and should allow any text input. This should appear on the first page.", 
             value= "" if st.session_state["Q1"] == None else st.session_state["Q1"],
             key       = 'Q1_text', 
             on_change = answer_change,
             args      = ( "Q1", "Q1_text",))

    st.markdown("""<style> div[class*="stText"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 18px;}</style> <br><br>""", unsafe_allow_html=True)


    st.selectbox(label     = "Selecting Box", 
             options   = Q2_radio_options, 
             index     = None if st.session_state["Q2"] == None else st.session_state["Q2"], 
             key       = 'Q2_radio', 
             on_change = radio_change, 
             args      = (Q2_radio_options, "Q2", "Q2_radio",))

    st.markdown("""<style> div[class*="stSelectbox"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 18px;}</style> <br><br>""", unsafe_allow_html=True)


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

    st.image("http://t3.gstatic.com/licensed-image?q=tbn:ANd9GcTF_OQ101nRiHil4w5295pqLf5M8axplaqmwCthHGgdqlu21bMsP8VmMdl4zkPUnW2pgcNWEWJyl-Y46P1J_d8") 
    st.session_state["Q3"] = 5 
    st.slider(label="This is a slider question that allows a numeric input between two numbers. This should appear on the second page.",min_value=0,max_value=10, 
                           value= st.session_state["Q3"], 
                           key = "Q3_slider",
                           on_change = answer_change, 
                           args = ("Q3", "Q3_slider",))
    st.markdown("""<style> div[class*="stSlider"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 18px;}</style> <br><br>""", unsafe_allow_html=True)


    st.multiselect(label     = "This is a multiselect question where you can select multiple answers. This should appear on the second page.", 
             default   = None if st.session_state["Q4"] == None else st.session_state["Q4"], 
             options   = Q4_radio_options, 
             key       = 'Q4_multi', 
             on_change = multi_change, 
             args      = (Q4_radio_options, "Q4", "Q4_multi",))

    st.markdown("""<style> div[class*="stMulti"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 18px;}</style> <br><br>""", unsafe_allow_html=True)


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
            if st.session_state["Q4"] == None or st.session_state["Q4"] == []:
                all_answered = False
            if all_answered:
                st.session_state["current_page"] += 1
                st.rerun()
            else:
                with placeholder.container():
                    st.warning("Please answer all the questions on this page.", icon="⚠️")

    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")


elif st.session_state["current_page"] == 3:

    st.markdown("""<p style='font-size:18px;'>My Life</p>""", unsafe_allow_html=True)
    st.radio(label     = "This is a multiple choice question where you can choose one of the following. This should appear on the third page.", 
             options   = Q5_radio_options, 
             index     = None if st.session_state["Q5"] == None else st.session_state["Q5"], 
             key       = 'Q5_radio', 
             on_change = radio_change, 
             args      = (Q5_radio_options, "Q5", "Q5_radio",))

    st.markdown("""<style> div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 18px;}</style> <br><br>""", unsafe_allow_html=True)


    st.radio(label     = "Fav Color?", 
             options   = Q6_radio_options, 
             index     = None if st.session_state["Q6"] == None else st.session_state["Q6"], 
             key       = 'Q6_radio', 
             on_change = radio_change, 
             args      = (Q6_radio_options, "Q6", "Q6_radio",))

    st.markdown("""<style> div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 18px;}</style> <br><br>""", unsafe_allow_html=True)


    st.multiselect(label     = "Party Time", 
             default   = None if st.session_state["Q7"] == None else st.session_state["Q7"], 
             options   = Q7_radio_options, 
             key       = 'Q7_multi', 
             on_change = multi_change, 
             args      = (Q7_radio_options, "Q7", "Q7_multi",))

    st.markdown("""<style> div[class*="stMulti"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 18px;}</style> <br><br>""", unsafe_allow_html=True)


    placeholder = st.empty()

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back'):
            st.session_state["current_page"] -= 1
            st.rerun()
    with col2:
        if st.button('Next'):
            all_answered = True
            if st.session_state["Q5"] == None or st.session_state["Q5"] == []:
                all_answered = False
            if st.session_state["Q6"] == None or st.session_state["Q6"] == []:
                all_answered = False
            if st.session_state["Q7"] == None or st.session_state["Q7"] == []:
                all_answered = False
            if all_answered:
                st.session_state["current_page"] += 1
                st.rerun()
            else:
                with placeholder.container():
                    st.warning("Please answer all the questions on this page.", icon="⚠️")

    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")


elif st.session_state["current_page"] == 4:

    st.session_state["Q8"] = 50
    st.slider(label="Happiness Scale",min_value=0,max_value=100, 
                           value= st.session_state["Q8"], 
                           key = "Q8_slider",
                           on_change = answer_change, 
                           args = ("Q8", "Q8_slider",))
    st.markdown("""<style> div[class*="stSlider"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 18px;}</style> <br><br>""", unsafe_allow_html=True)


    st.text_area(label     = "Why are you this happy/unhappy?", 
             value= "" if st.session_state["Q9"] == None else st.session_state["Q9"],
             key       = 'Q9_text', 
             on_change = answer_change,
             args      = ( "Q9", "Q9_text",))

    st.markdown("""<style> div[class*="stText"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 18px;}</style> <br><br>""", unsafe_allow_html=True)


    placeholder = st.empty()

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back'):
            st.session_state["current_page"] -= 1
            st.rerun()
    with col2:
        if st.button('Next'):
            all_answered = True
            if st.session_state["Q8"] == None or st.session_state["Q8"] == []:
                all_answered = False
            if st.session_state["Q9"] == None or st.session_state["Q9"] == []:
                all_answered = False
            if all_answered:
                st.session_state["current_page"] += 1
                st.rerun()
            else:
                with placeholder.container():
                    st.warning("Please answer all the questions on this page.", icon="⚠️")

    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")


elif st.session_state["current_page"] == 5:

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


elif st.session_state["current_page"] == 6:

    st.radio(label     = "I like cheese?", 
             options   = Q10_radio_options, 
             index     = None if st.session_state["Q10"] == None else st.session_state["Q10"], 
             key       = 'Q10_radio', 
             on_change = radio_change, 
             args      = (Q10_radio_options, "Q10", "Q10_radio",))

    st.markdown("""<style> div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 18px;}</style> <br><br>""", unsafe_allow_html=True)


    placeholder = st.empty()

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back'):
            st.session_state["current_page"] -= 1
            st.rerun()
    with col2:
        if st.button('Next'):
            all_answered = True
            if st.session_state["Q10"] == None or st.session_state["Q10"] == []:
                all_answered = False
            if all_answered:
                st.session_state["current_page"] += 1
                st.rerun()
            else:
                with placeholder.container():
                    st.warning("Please answer all the questions on this page.", icon="⚠️")

    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")


elif st.session_state["current_page"] == 7:

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


