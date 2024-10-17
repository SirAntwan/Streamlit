import streamlit as st
import requests
import json

# Global variables
total_number_pages = 24
placeholder_buttons = None

st.set_page_config(page_title="Example Survey",)

# Radio Options
q1_radio_options         = ["Weekly", "Monthly", "Semi-annually", "Annually", "Less than Annually", "Never"]
yes_no_NotSure_radio_options = ["Yes", "No", "Not sure"]
yes_no_radio_options         = ["Yes", "No"]
frequency_radio_options      = ["Always", "Most of the time", "About half the time", "Sometimes", "Never"]


# Function that records radio element changes 
def radio_change(element, state, key):
    st.session_state[state] = element.index(st.session_state[key]) # Setting previously selected option

# Function that disables the last button while data is uploaded to IPFS 
def button_disable():
    st.session_state["disabled"] = True

# Changing the App title

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
             options   = q1_radio_options, 
             index     = None if st.session_state["Q1"] == None else st.session_state["Q1"],
             key       = 'Q1_radio', 
             on_change = radio_change, 
             args      = (q1_radio_options, "Q1", "Q1_radio",))
    
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


# Page 24
elif st.session_state["current_page"]  == 7:
   
    st.markdown('<p class="big-font">Thank you for participating! <br> Click on the button below to submit your answers. </p>', unsafe_allow_html=True)

    st.button('Submit Responses', disabled = st.session_state["disabled"], on_click = button_disable)

    if st.session_state["disabled"]:    
        with st.spinner(r"$\textsf{\normalsize Storing data on IPFS and Ethereum. This operation might take a few minutes. Please wait to receive your confirmation code!}$"):
            try:
                response = {'file': json.dumps({"Q1":q1_radio_options[st.session_state["Q1"]],
                                                "Q2":yes_no_NotSure_radio_options[st.session_state["Q2"]],
                                                "Q3":yes_no_NotSure_radio_options[st.session_state["Q3"]],
                                                "Q4":yes_no_NotSure_radio_options[st.session_state["Q4"]],
                                                "Q5":frequency_radio_options[st.session_state["Q5"]]
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