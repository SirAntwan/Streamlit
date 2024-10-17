import streamlit as st
import requests
import json
import web3

# Global variables
total_number_pages = 24
placeholder_buttons = None

# Radio Options
period_radio_options         = ["Weekly", "Monthly", "Semi-annually", "Annually", "Less than Annually", "Never"]
yes_no_NotSure_radio_options = ["Yes", "No", "Not sure"]
yes_no_radio_options         = ["Yes", "No"]
frequency_radio_options      = ["Always", "Most of the time", "About half the time", "Sometimes", "Never"]
importance_radio_options     = ["Extremely important", "Very important", "Moderately important", "Slightly important", "Not at all important"]
q7_radio_options             = ["When I see a new doctor I want him/her to have access to my previous medical records.",
                                "When I see a new doctor I do not want him/her to have access to my previous medical records.",
                                "Not sure"]
q12_radio_options            = ["Share my information automatically unless I say not to share it.",
                                "Share my information automatically in an emergency situation, but otherwise do not share unless I provide my consent.",
                                "Share my information only after I provide my consent."]
q14_radio_options            = ["Paper consent form", "Electronic consent", "Both paper and electronic consent", "Not sure", "Not Applicable"]
q15_radio_options            = ["Fill out a form at my provider's office", "Use the consent app"]
q17_radio_options            = ["18-24 years old", "25-34 years old", "35-44 years old", "45-54 years old", "55-64 years old", "65+ years old"]
q18_radio_options            = ["Male", "Female", "Non-binary/third gender", "Prefer not to say"]
q19_radio_options            = ["Asian or Pacific Islander", "Black or African American", "Hispanic or Latino", "Native American or Alaska Native",
                                "White or Caucasian", "Multiracial/Biracial/Other"]
q20_radio_options            = ["Less than high school", "High school education", "Some college", "College degree or higher"]
q21_radio_options            = ["\$0-\$24,999", "\$25,000-\$49,999",  "\$50,000-\$74,999", 
                                 "\$75,000-\$99,999", "\$100,000-\$149,999", "\$150,000-\$199,999", "\$200,000 and up"]
q22_radio_options            = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", 
                                "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", 
                                "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", 
                                "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York",
                                "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", 
                                "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
                                "West Virginia", "Wisconsin", "Wyoming", "I do not live in the United States"]

# Function that records radio element changes 
def radio_change(element, state, key):
    st.session_state[state] = element.index(st.session_state[key]) # Setting previously selected option

# Function that disables the last button while data is uploaded to IPFS 
def button_disable():
    st.session_state["disabled"] = True

# Changing the App title
st.set_page_config(page_title="IPFS-Based Survey",)

# Page title
st.title('Patient Consent for HIE')

# The following code centralizes all the buttons
st.markdown("<style>.row-widget.stButton {text-align: center;}</style>", unsafe_allow_html=True)

# The following code helps with the font size of text labels
st.markdown("<style>.big-font {font-size:24px;}</style>", unsafe_allow_html=True)   

# Initialize state
if "current_page" not in st.session_state:
    st.session_state["current_page"] = 1
    st.session_state["Q1"]  = None
    st.session_state["Q2"]  = None
    st.session_state["Q3"]  = None
    st.session_state["Q4"]  = None
    st.session_state["Q5"]  = None
    st.session_state["Q6"]  = None
    st.session_state["Q7"]  = None
    st.session_state["Q8"]  = None
    st.session_state["Q9"]  = None
    st.session_state["Q10"] = None
    st.session_state["Q11"] = None
    st.session_state["Q12"] = None
    st.session_state["Q13"] = None
    st.session_state["Q14"] = None
    st.session_state["Q15"] = None
    st.session_state["Q16"] = None
    st.session_state["Q17"] = None
    st.session_state["Q18"] = None
    st.session_state["Q19"] = None
    st.session_state["Q20"] = None
    st.session_state["Q21"] = None
    st.session_state["Q22"] = None
    st.session_state["Q23"] = None
    st.session_state["Q24"] = None
    st.session_state["disabled"] = False


# Page 1; Video
if st.session_state["current_page"]  == 1:

    st.markdown("""<p class="big-font">
                This survey asks questions about your views and preferences regarding how your healthcare providers have access to your medical information and to what extent you are in control of that access.  <br><br>
                Health information exchange or HIE is the process of either transferring patient health information electronically (e.g., from a primary care physician to a specialist) or granting access to patient health information maintained digitally by a specific person or organization. The information could reside in an electronic medical record system or other digital repository maintained by a health provider (e.g., hospital, doctor’s office) or in a personal health record maintained by the patient on a personal computer or online. <br><br>
                Health information exchange has the goal of making all relevant medical information about you available to your healthcare providers when they are making decisions about your care. The expected value of having access to all relevant medical information includes more timely and accurate treatment, fewer redundant tests, and better-quality outcomes. However, the concern with health information exchange is that as information is made more accessible, the potential for misuse of that information increases. <br><br>
                Some states have an opt-in requirement where patients must give consent before HIE is allowed, while other states have an opt-out requirement where HIE is allowed unless the patient specifically withdraws consent. Some states have not established specific HIE consent requirements leaving that decision to individual health providers. The process of documenting patient consent for HIE is almost always a paper-based process where the patient fills out and signs a paper consent form at their provider’s office and the provider stores the signed document. Because consent requirements vary from state to state, consent for HIE must be managed separately in each state where a patient receives care or where existing medical information resides. <br><br> 
                The video below provides additional information about HIE in the context of Arizona.                
                </p>""", unsafe_allow_html=True)
    st.video("https://www.youtube.com/watch?v=aJb6Dov0jlM")
   
    if  st.button('Next'):
       st.session_state["current_page"] += 1
       st.rerun()

    # Progress bar
    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")

# Page 2; Q1
elif st.session_state["current_page"]  == 2:

    st.radio(label     = "How frequently do you visit a healthcare provider to receive care for a medical problem?", 
             options   = period_radio_options, 
             index     = None if st.session_state["Q1"] == None else st.session_state["Q1"],
             key       = 'Q1_radio', 
             on_change = radio_change, 
             args      = (period_radio_options, "Q1", "Q1_radio",))
    
    # The code below changes the font size of the above radio's label. The last two <br> tags create extra space before the buttons
    st.markdown("""<style> div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 24px;}</style> <br><br>""", unsafe_allow_html=True)

    # Placeholder for a potential warning message    
    placeholder = st.empty()

    # Back/Next buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back'):
            st.session_state["current_page"] -= 1
            st.rerun()

    with col2:
        if st.button('Next'):
            if st.session_state["Q1"] != None:
                st.session_state["current_page"] += 1
                st.rerun()
            else: # Adding warning message to the placeholder
                with placeholder.container():
                    st.warning(f"Please answer all the questions on this page.", icon="⚠️")

    # Progress bar
    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")

# Page 3; Q2
elif st.session_state["current_page"]  == 3:

    st.radio(label     = "When receiving care for a medical problem, was there EVER a time when an important part of your health information was NOT available to your care provider to make a decision about your care at the time of your scheduled appointment?",
             options   = yes_no_NotSure_radio_options, 
             index     = None if st.session_state["Q2"] == None else st.session_state["Q2"],
             key       = 'Q2_radio', 
             on_change = radio_change, 
             args      = (yes_no_NotSure_radio_options, "Q2", "Q2_radio",))
    
    # The code below changes the font size of the above radio's label. The last two <br> tags create extra space before the buttons
    st.markdown("""<style> div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 24px;}</style> <br><br>""", unsafe_allow_html=True)

    # Placeholder for a potential warning message    
    placeholder = st.empty()

    # Back/Next buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back'):
            st.session_state["current_page"] -= 1
            st.rerun()

    with col2:
        if st.button('Next'):
            if st.session_state["Q2"] != None:
                st.session_state["current_page"] += 1
                st.rerun()
            else: # Adding warning message to the placeholder
                with placeholder.container():
                    st.warning(f"Please answer all the questions on this page.", icon="⚠️")

    # Progress bar
    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")

# Page 4; Q3
elif st.session_state["current_page"]  == 4:

    st.radio(label     = "When receiving care for a medical problem, was there EVER a time when you received conflicting information from different doctors or health care professionals?",
             options   = yes_no_NotSure_radio_options, 
             index     = None if st.session_state["Q3"] == None else st.session_state["Q3"],
             key       = 'Q3_radio', 
             on_change = radio_change, 
             args      = (yes_no_NotSure_radio_options, "Q3", "Q3_radio",))
    
    # The code below changes the font size of the above radio's label. The last two <br> tags create extra space before the buttons
    st.markdown("""<style> div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 24px;}</style> <br><br>""", unsafe_allow_html=True)

    # Placeholder for a potential warning message    
    placeholder = st.empty()

    # Back/Next buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back'):
            st.session_state["current_page"] -= 1
            st.rerun()

    with col2:
        if st.button('Next'):
            if st.session_state["Q3"] != None:
                st.session_state["current_page"] += 1
                st.rerun()
            else: # Adding warning message to the placeholder
                with placeholder.container():
                    st.warning(f"Please answer all the questions on this page.", icon="⚠️")

    # Progress bar
    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")

# Page 5; Q4
elif st.session_state["current_page"]  == 5:

    st.radio(label     = "When receiving care for a medical problem, was there EVER a time when a doctor ordered a medical test that you felt was unnecessary because the test had already been done?",
             options   = yes_no_NotSure_radio_options, 
             index     = None if st.session_state["Q4"] == None else st.session_state["Q4"],
             key       = 'Q4_radio', 
             on_change = radio_change, 
             args      = (yes_no_NotSure_radio_options, "Q4", "Q4_radio",))
    
    # The code below changes the font size of the above radio's label. The last two <br> tags create extra space before the buttons
    st.markdown("""<style> div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 24px;}</style> <br><br>""", unsafe_allow_html=True)

    # Placeholder for a potential warning message    
    placeholder = st.empty()

    # Back/Next buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back'):
            st.session_state["current_page"] -= 1
            st.rerun()

    with col2:
        if st.button('Next'):
            if st.session_state["Q4"] != None:
                st.session_state["current_page"] += 1
                st.rerun()
            else: # Adding warning message to the placeholder
                with placeholder.container():
                    st.warning(f"Please answer all the questions on this page.", icon="⚠️")

    # Progress bar
    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")

# Page 6; Q5
elif st.session_state["current_page"]  == 6:

    st.radio(label     = "When you need care or treatment, how often does your healthcare provider know important information about your medical history?",
             options   = frequency_radio_options, 
             index     = None if st.session_state["Q5"] == None else st.session_state["Q5"],
             key       = 'Q5_radio', 
             on_change = radio_change, 
             args      = (frequency_radio_options, "Q5", "Q5_radio",))
    
    # The code below changes the font size of the above radio's label. The last two <br> tags create extra space before the buttons
    st.markdown("""<style> div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 24px;}</style> <br><br>""", unsafe_allow_html=True)

    # Placeholder for a potential warning message    
    placeholder = st.empty()

    # Back/Next buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back'):
            st.session_state["current_page"] -= 1
            st.rerun()

    with col2:
        if st.button('Next'):
            if st.session_state["Q5"] != None:
                st.session_state["current_page"] += 1
                st.rerun()
            else: # Adding warning message to the placeholder
                with placeholder.container():
                    st.warning(f"Please answer all the questions on this page.", icon="⚠️")

    # Progress bar
    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")

# Page 7; Q6
elif st.session_state["current_page"]  == 7:

    st.radio(label     = "How important is it that your healthcare providers have access to ALL of your medical information to make care decisions?",
             options   = importance_radio_options, 
             index     = None if st.session_state["Q6"] == None else st.session_state["Q6"],
             key       = 'Q6_radio', 
             on_change = radio_change, 
             args      = (importance_radio_options, "Q6", "Q6_radio",))
    
    # The code below changes the font size of the above radio's label. The last two <br> tags create extra space before the buttons
    st.markdown("""<style> div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 24px;}</style> <br><br>""", unsafe_allow_html=True)

    # Placeholder for a potential warning message    
    placeholder = st.empty()

    # Back/Next buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back'):
            st.session_state["current_page"] -= 1
            st.rerun()

    with col2:
        if st.button('Next'):
            if st.session_state["Q6"] != None:
                st.session_state["current_page"] += 1
                st.rerun()
            else: # Adding warning message to the placeholder
                with placeholder.container():
                    st.warning(f"Please answer all the questions on this page.", icon="⚠️")

    # Progress bar
    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")

# Page 8; Q7
elif st.session_state["current_page"]  == 8:

    st.radio(label     = "Which of the following statements comes closest to expressing your overall view of how you prefer that information from your medical records are handled?",
             options   = q7_radio_options, 
             index     = None if st.session_state["Q7"] == None else st.session_state["Q7"],
             key       = 'Q7_radio', 
             on_change = radio_change, 
             args      = (q7_radio_options, "Q7", "Q7_radio",))
    
    # The code below changes the font size of the above radio's label. The last two <br> tags create extra space before the buttons
    st.markdown("""<style> div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 24px;}</style> <br><br>""", unsafe_allow_html=True)

    # Placeholder for a potential warning message    
    placeholder = st.empty()

    # Back/Next buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back'):
            st.session_state["current_page"] -= 1
            st.rerun()

    with col2:
        if st.button('Next'):
            if st.session_state["Q7"] != None:
                st.session_state["current_page"] += 1
                st.rerun()
            else: # Adding warning message to the placeholder
                with placeholder.container():
                    st.warning(f"Please answer all the questions on this page.", icon="⚠️")

    # Progress bar
    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")

# Page 9; Q8
elif st.session_state["current_page"]  == 9:

    st.radio(label     = "When selecting a healthcare provider, how important is it that they participate in a health information exchange that enables them to access ALL of your medical information?",
             options   = importance_radio_options, 
             index     = None if st.session_state["Q8"] == None else st.session_state["Q8"],
             key       = 'Q8_radio', 
             on_change = radio_change, 
             args      = (importance_radio_options, "Q8", "Q8_radio",))
    
    # The code below changes the font size of the above radio's label. The last two <br> tags create extra space before the buttons
    st.markdown("""<style> div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 24px;}</style> <br><br>""", unsafe_allow_html=True)

    # Placeholder for a potential warning message    
    placeholder = st.empty()

    # Back/Next buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back'):
            st.session_state["current_page"] -= 1
            st.rerun()

    with col2:
        if st.button('Next'):
            if st.session_state["Q8"] != None:
                st.session_state["current_page"] += 1
                st.rerun()
            else: # Adding warning message to the placeholder
                with placeholder.container():
                    st.warning(f"Please answer all the questions on this page.", icon="⚠️")

    # Progress bar
    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")

# Page 10; Q9
elif st.session_state["current_page"]  == 10:

    st.radio(label     = "Should patients have full control over which healthcare providers can access their medical information?",
             options   = yes_no_radio_options, 
             index     = None if st.session_state["Q9"] == None else st.session_state["Q9"],
             key       = 'Q9_radio', 
             on_change = radio_change, 
             args      = (yes_no_radio_options, "Q9", "Q9_radio",))
    
    # The code below changes the font size of the above radio's label. The last two <br> tags create extra space before the buttons
    st.markdown("""<style> div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 24px;}</style> <br><br>""", unsafe_allow_html=True)

    # Placeholder for a potential warning message    
    placeholder = st.empty()

    # Back/Next buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back'):
            st.session_state["current_page"] -= 1
            st.rerun()

    with col2:
        if st.button('Next'):
            if st.session_state["Q9"] != None:
                st.session_state["current_page"] += 1
                st.rerun()
            else: # Adding warning message to the placeholder
                with placeholder.container():
                    st.warning(f"Please answer all the questions on this page.", icon="⚠️")

    # Progress bar
    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")

# Page 11; Q10
elif st.session_state["current_page"]  == 11:

    st.radio(label     = "Are you aware of your rights as a patient to limit who can access your medical records for your own care and treatment?",
             options   = yes_no_radio_options, 
             index     = None if st.session_state["Q10"] == None else st.session_state["Q10"],
             key       = 'Q10_radio', 
             on_change = radio_change, 
             args      = (yes_no_radio_options, "Q10", "Q10_radio",))
    
    # The code below changes the font size of the above radio's label. The last two <br> tags create extra space before the buttons
    st.markdown("""<style> div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 24px;}</style> <br><br>""", unsafe_allow_html=True)

    # Placeholder for a potential warning message    
    placeholder = st.empty()

    # Back/Next buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back'):
            st.session_state["current_page"] -= 1
            st.rerun()

    with col2:
        if st.button('Next'):
            if st.session_state["Q10"] != None:
                st.session_state["current_page"] += 1
                st.rerun()
            else: # Adding warning message to the placeholder
                with placeholder.container():
                    st.warning(f"Please answer all the questions on this page.", icon="⚠️")

    # Progress bar
    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")

# Page 12; Q11
elif st.session_state["current_page"]  == 12:

    st.radio(label     = "How important is having control over which healthcare providers have access to your medical information?",
             options   = importance_radio_options, 
             index     = None if st.session_state["Q11"] == None else st.session_state["Q11"],
             key       = 'Q11_radio', 
             on_change = radio_change, 
             args      = (importance_radio_options, "Q11", "Q11_radio",))
    
    # The code below changes the font size of the above radio's label. The last two <br> tags create extra space before the buttons
    st.markdown("""<style> div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 24px;}</style> <br><br>""", unsafe_allow_html=True)

    # Placeholder for a potential warning message    
    placeholder = st.empty()

    # Back/Next buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back'):
            st.session_state["current_page"] -= 1
            st.rerun()

    with col2:
        if st.button('Next'):
            if st.session_state["Q11"] != None:
                st.session_state["current_page"] += 1
                st.rerun()
            else: # Adding warning message to the placeholder
                with placeholder.container():
                    st.warning(f"Please answer all the questions on this page.", icon="⚠️")

    # Progress bar
    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")

# Page 13; Q12
elif st.session_state["current_page"]  == 13:

    st.radio(label     = "Which of the following options would you prefer when it comes to permission needed to have your health information shared electronically between providers for medical care?",
             options   = q12_radio_options, 
             index     = None if st.session_state["Q12"] == None else st.session_state["Q12"],
             key       = 'Q12_radio', 
             on_change = radio_change, 
             args      = (q12_radio_options, "Q12", "Q12_radio",))
    
    # The code below changes the font size of the above radio's label. The last two <br> tags create extra space before the buttons
    st.markdown("""<style> div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 24px;}</style> <br><br>""", unsafe_allow_html=True)

    # Placeholder for a potential warning message    
    placeholder = st.empty()

    # Back/Next buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back'):
            st.session_state["current_page"] -= 1
            st.rerun()

    with col2:
        if st.button('Next'):
            if st.session_state["Q12"] != None:
                st.session_state["current_page"] += 1
                st.rerun()
            else: # Adding warning message to the placeholder
                with placeholder.container():
                    st.warning(f"Please answer all the questions on this page.", icon="⚠️")

    # Progress bar
    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")

# Page 14; Q13
elif st.session_state["current_page"]  == 14:

    st.radio(label     = "Do you recall ever giving consent for health information exchange?",
             options   = yes_no_radio_options, 
             index     = None if st.session_state["Q13"] == None else st.session_state["Q13"],
             key       = 'Q13_radio', 
             on_change = radio_change, 
             args      = (yes_no_radio_options, "Q13", "Q13_radio",))
    
    # The code below changes the font size of the above radio's label. The last two <br> tags create extra space before the buttons
    st.markdown("""<style> div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 24px;}</style> <br><br>""", unsafe_allow_html=True)

    # Placeholder for a potential warning message    
    placeholder = st.empty()

    # Back/Next buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back'):
            st.session_state["current_page"] -= 1
            st.rerun()

    with col2:
        if st.button('Next'):
            if st.session_state["Q13"] != None:
                st.session_state["current_page"] += 1
                st.rerun()
            else: # Adding warning message to the placeholder
                with placeholder.container():
                    st.warning(f"Please answer all the questions on this page.", icon="⚠️")

    # Progress bar
    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")

# Page 15; Q14
elif st.session_state["current_page"]  == 15:

    st.radio(label     = "If you answered yes to the previous questions, was the consent process completed on a paper form or was it done electronically?",
             options   = q14_radio_options, 
             index     = None if st.session_state["Q14"] == None else st.session_state["Q14"],
             key       = 'Q14_radio', 
             on_change = radio_change, 
             args      = (q14_radio_options, "Q14", "Q14_radio",))
    
    # The code below changes the font size of the above radio's label. The last two <br> tags create extra space before the buttons
    st.markdown("""<style> div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 24px;}</style> <br><br>""", unsafe_allow_html=True)

    # Placeholder for a potential warning message    
    placeholder = st.empty()

    # Back/Next buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back'):
            st.session_state["current_page"] -= 1
            st.rerun()

    with col2:
        if st.button('Next'):
            if st.session_state["Q14"] != None:
                st.session_state["current_page"] += 1
                st.rerun()
            else: # Adding warning message to the placeholder
                with placeholder.container():
                    st.warning(f"Please answer all the questions on this page.", icon="⚠️")

    # Progress bar
    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")

# Page 16; Video + Q15 + Q16
elif st.session_state["current_page"]  == 16:

    st.markdown("""<p class="big-font">
                Watch the video below, which explains both the current format for granting and revoking the electronic exchange of your individual health information and an app alternative that is not currently available, but could be offered.                
                </p>""", unsafe_allow_html=True)
    st.video("https://www.youtube.com/watch?v=pJQt-pjSFTk")

    #Q15
    st.radio(label     = "Based on the options presented in the video, how would you prefer to manage your health information exchange consent?",
             options   = q15_radio_options, 
             index     = None if st.session_state["Q15"] == None else st.session_state["Q15"],
             key       = 'Q15_radio', 
             on_change = radio_change, 
             args      = (q15_radio_options, "Q15", "Q15_radio",))
    
    # The code below changes the font size of the above radio's label. The last two <br> tags create extra space before the buttons
    st.markdown("""<style> div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 24px;}</style> <br><br>""", unsafe_allow_html=True)


    #Q16
    st.session_state["Q16"] = st.text_area("Why did you choose the above option?", st.session_state["Q16"])

    # The code below changes the font size of the above radio's label. The last two <br> tags create extra space before the buttons
    st.markdown("""<style> div[class*="stTextArea"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 24px;}</style> <br><br>""", unsafe_allow_html=True)

    # Placeholder for a potential warning message    
    placeholder = st.empty()

    # Back/Next buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back'):
            st.session_state["current_page"] -= 1
            st.rerun()

    with col2:
        if st.button('Next'):
            if st.session_state["Q15"] != None and st.session_state["Q16"] != None:
                st.session_state["current_page"] += 1
                st.rerun()
            else: # Adding warning message to the placeholder
                with placeholder.container():
                    st.warning(f"Please answer all the questions on this page.", icon="⚠️")

    # Progress bar
    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")
    
# Page 17; Q17
elif st.session_state["current_page"]  == 17:

    st.radio(label     = "How old are you?",
             options   = q17_radio_options, 
             index     = None if st.session_state["Q17"] == None else st.session_state["Q17"],
             key       = 'Q17_radio', 
             on_change = radio_change, 
             args      = (q17_radio_options, "Q17", "Q17_radio",))
    
    # The code below changes the font size of the above radio's label. The last two <br> tags create extra space before the buttons
    st.markdown("""<style> div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 24px;}</style> <br><br>""", unsafe_allow_html=True)

    # Placeholder for a potential warning message    
    placeholder = st.empty()

    # Back/Next buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back'):
            st.session_state["current_page"] -= 1
            st.rerun()

    with col2:
        if st.button('Next'):
            if st.session_state["Q17"] != None:
                st.session_state["current_page"] += 1
                st.rerun()
            else: # Adding warning message to the placeholder
                with placeholder.container():
                    st.warning(f"Please answer all the questions on this page.", icon="⚠️")

    # Progress bar
    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")

# Page 18; Q18
elif st.session_state["current_page"]  == 18:

    st.radio(label     = "How do you describe yourself?",
             options   = q18_radio_options, 
             index     = None if st.session_state["Q18"] == None else st.session_state["Q18"],
             key       = 'Q18_radio', 
             on_change = radio_change, 
             args      = (q18_radio_options, "Q18", "Q18_radio",))
    
    # The code below changes the font size of the above radio's label. The last two <br> tags create extra space before the buttons
    st.markdown("""<style> div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 24px;}</style> <br><br>""", unsafe_allow_html=True)

    # Placeholder for a potential warning message    
    placeholder = st.empty()

    # Back/Next buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back'):
            st.session_state["current_page"] -= 1
            st.rerun()

    with col2:
        if st.button('Next'):
            if st.session_state["Q18"] != None:
                st.session_state["current_page"] += 1
                st.rerun()
            else: # Adding warning message to the placeholder
                with placeholder.container():
                    st.warning(f"Please answer all the questions on this page.", icon="⚠️")

    # Progress bar
    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")

# Page 19; Q19
elif st.session_state["current_page"]  == 19:

    st.radio(label     = "Which of the following best describes you?",
             options   = q19_radio_options, 
             index     = None if st.session_state["Q19"] == None else st.session_state["Q19"],
             key       = 'Q19_radio', 
             on_change = radio_change, 
             args      = (q19_radio_options, "Q19", "Q19_radio",))
    
    # The code below changes the font size of the above radio's label. The last two <br> tags create extra space before the buttons
    st.markdown("""<style> div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 24px;}</style> <br><br>""", unsafe_allow_html=True)

    # Placeholder for a potential warning message    
    placeholder = st.empty()

    # Back/Next buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back'):
            st.session_state["current_page"] -= 1
            st.rerun()

    with col2:
        if st.button('Next'):
            if st.session_state["Q19"] != None:
                st.session_state["current_page"] += 1
                st.rerun()
            else: # Adding warning message to the placeholder
                with placeholder.container():
                    st.warning(f"Please answer all the questions on this page.", icon="⚠️")

    # Progress bar
    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")

# Page 20; Q20
elif st.session_state["current_page"]  == 20:

    st.radio(label     = "What is the highest level of education you have completed?",
             options   = q20_radio_options, 
             index     = None if st.session_state["Q20"] == None else st.session_state["Q20"],
             key       = 'Q20_radio', 
             on_change = radio_change, 
             args      = (q20_radio_options, "Q20", "Q20_radio",))
    
    # The code below changes the font size of the above radio's label. The last two <br> tags create extra space before the buttons
    st.markdown("""<style> div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 24px;}</style> <br><br>""", unsafe_allow_html=True)

    # Placeholder for a potential warning message    
    placeholder = st.empty()

    # Back/Next buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back'):
            st.session_state["current_page"] -= 1
            st.rerun()

    with col2:
        if st.button('Next'):
            if st.session_state["Q20"] != None:
                st.session_state["current_page"] += 1
                st.rerun()
            else: # Adding warning message to the placeholder
                with placeholder.container():
                    st.warning(f"Please answer all the questions on this page.", icon="⚠️")

    # Progress bar
    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")

# Page 21; Q21
elif st.session_state["current_page"]  == 21:

    st.radio(label     = "What is your approximate average household income?",
             options   = q21_radio_options, 
             index     = None if st.session_state["Q21"] == None else st.session_state["Q21"],
             key       = 'Q21_radio', 
             on_change = radio_change, 
             args      = (q21_radio_options, "Q21", "Q21_radio",))
    
    # The code below changes the font size of the above radio's label. The last two <br> tags create extra space before the buttons
    st.markdown("""<style> div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 24px;}</style> <br><br>""", unsafe_allow_html=True)

    # Placeholder for a potential warning message    
    placeholder = st.empty()

    # Back/Next buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back'):
            st.session_state["current_page"] -= 1
            st.rerun()

    with col2:
        if st.button('Next'):
            if st.session_state["Q21"] != None:
                st.session_state["current_page"] += 1
                st.rerun()
            else: # Adding warning message to the placeholder
                with placeholder.container():
                    st.warning(f"Please answer all the questions on this page.", icon="⚠️")

    # Progress bar
    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")

# Page 22; Q22
elif st.session_state["current_page"]  == 22:

    st.selectbox(label     = "In which state do you currently reside?",
                 options   = q22_radio_options, 
                 index     = None if st.session_state["Q22"] == None else st.session_state["Q22"],
                 key       = 'Q22_radio', 
                 on_change = radio_change, 
                 args      = (q22_radio_options, "Q22", "Q22_radio",))
    
    # The code below changes the font size of the above radio's label. The last two <br> tags create extra space before the buttons
    st.markdown("""<style> div[class*="stSelectbox"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 24px;}</style> <br><br>""", unsafe_allow_html=True)

    # Placeholder for a potential warning message    
    placeholder = st.empty()

    # Back/Next buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back'):
            st.session_state["current_page"] -= 1
            st.rerun()

    with col2:
        if st.button('Next'):
            if st.session_state["Q22"] != None:
                st.session_state["current_page"] += 1
                st.rerun()
            else: # Adding warning message to the placeholder
                with placeholder.container():
                    st.warning(f"Please answer all the questions on this page.", icon="⚠️")

    # Progress bar
    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")
    
# Page 23; Q23
elif st.session_state["current_page"]  == 23:

    st.radio(label     = "Is there one doctor's group, health center, or clinic you usually go to for most of your medical care?",
             options   = yes_no_radio_options, 
             index     = None if st.session_state["Q23"] == None else st.session_state["Q23"],
             key       = 'Q23_radio', 
             on_change = radio_change, 
             args      = (yes_no_radio_options, "Q23", "Q23_radio",))
    
    # The code below changes the font size of the above radio's label. The last two <br> tags create extra space before the buttons
    st.markdown("""<style> div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 24px;}</style> <br><br>""", unsafe_allow_html=True)

    # Placeholder for a potential warning message    
    placeholder = st.empty()

    # Back/Next buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back'):
            st.session_state["current_page"] -= 1
            st.rerun()

    with col2:
        if st.button('Next'):
            if st.session_state["Q23"] != None:
                st.session_state["current_page"] += 1
                st.rerun()
            else: # Adding warning message to the placeholder
                with placeholder.container():
                  st.warning(f"Please answer all the questions on this page.", icon="⚠️")

    # Progress bar
    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")

# Page 24
elif st.session_state["current_page"]  == 24:
   
    st.markdown('<p class="big-font">Thank you for participating! <br> Click on the button below to submit your answers. </p>', unsafe_allow_html=True)

    st.button('Submit Responses', disabled = st.session_state["disabled"], on_click = button_disable)

    if st.session_state["disabled"]:    
        with st.spinner(r"$\textsf{\normalsize Storing data on IPFS and Ethereum. This operation might take a few minutes. Please wait to receive your confirmation code!}$"):
            try:
                response = {'file': json.dumps({"Q1":period_radio_options[st.session_state["Q1"]],
                                                "Q2":yes_no_NotSure_radio_options[st.session_state["Q2"]],
                                                "Q3":yes_no_NotSure_radio_options[st.session_state["Q3"]],
                                                "Q4":yes_no_NotSure_radio_options[st.session_state["Q4"]],
                                                "Q5":frequency_radio_options[st.session_state["Q5"]],
                                                "Q6":importance_radio_options[st.session_state["Q6"]],
                                                "Q7":q7_radio_options[st.session_state["Q7"]], 
                                                "Q8":importance_radio_options[st.session_state["Q8"]],
                                                "Q9":yes_no_radio_options[st.session_state["Q9"]],
                                                "Q10":yes_no_radio_options[st.session_state["Q10"]],
                                                "Q11":importance_radio_options[st.session_state["Q11"]],
                                                "Q12":q12_radio_options[st.session_state["Q12"]], 
                                                "Q13":yes_no_radio_options[st.session_state["Q13"]], 
                                                "Q14":q14_radio_options[st.session_state["Q14"]], 
                                                "Q15":q15_radio_options[st.session_state["Q15"]], 
                                                "Q16":st.session_state["Q16"],
                                                "Q17":q17_radio_options[st.session_state["Q17"]], 
                                                "Q18":q18_radio_options[st.session_state["Q18"]], 
                                                "Q19":q19_radio_options[st.session_state["Q19"]], 
                                                "Q20":q20_radio_options[st.session_state["Q20"]], 
                                                "Q21":q21_radio_options[st.session_state["Q21"]],
                                                "Q22":q22_radio_options[st.session_state["Q22"]], 
                                                "Q23":yes_no_radio_options[st.session_state["Q23"]],
                                            })
                            }   


                response = requests.post('https://ipfs.infura.io:5001/api/v0/add', 
                                        files=response, 
                                        auth=(st.secrets["username"], st.secrets["password"]))
                
                IPFS_hash = response.json()["Hash"]
                print(IPFS_hash)
            
                # Connect to the Ethereum blockchain
                w3 = web3.Web3(web3.HTTPProvider(st.secrets["infura"]))
            
                # Create a contract instance. Address is equal to the address of the smart contract
                contract = w3.eth.contract(address= "0x42b76d8c32f914630627Bf924BD1e06055673cF8", abi = '[ { "anonymous": false, "inputs": [ { "indexed": false, "internalType": "string", "name": "data", "type": "string" } ], "name": "Store", "type": "event" }, { "inputs": [ { "internalType": "string", "name": "_IPFSHash", "type": "string" } ], "name": "storeHash", "outputs": [], "stateMutability": "nonpayable", "type": "function" } ]')

                # Call your function: 11155111 is Sepolia's id
                call_function = contract.functions.storeHash(IPFS_hash).build_transaction({"chainId": 11155111, 
                                                                                        "from": "0x3Eb5abC0c5FeDCe75854A61163b7ee63baE71567",
                                                                                        "nonce": w3.eth.get_transaction_count("0x3Eb5abC0c5FeDCe75854A61163b7ee63baE71567")}) # Initialize address nonce

                # Sign transaction
                signed_tx = w3.eth.account.sign_transaction(call_function, private_key=st.secrets["pk"])

                # Send transaction
                send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

                # Wait for transaction receipt
                tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

                print(tx_receipt)

                st.success('Data successfully stored. Thank you for taking the survey!', icon="✅")
                st.info(f'The IPFS hash is: {IPFS_hash}', icon="ℹ️")
                st.info(f'The Ethereum hash is: {tx_receipt.logs[0].transactionHash.hex()}', icon="ℹ️")

                st.markdown('<p class="big-font">Please report your IPFS and Ethereum Hash to receive your payment.</p>', unsafe_allow_html=True)

            except Exception as e:
                print(e)
                st.error(f'An error ocurred. Here is the error message: {e}', icon="🚨")

    # Progress bar
    st.progress(st.session_state["current_page"]/total_number_pages, text="Progress")