from dotenv import load_dotenv
import os
import streamlit as st
import requests
import re

load_dotenv()

API_ENDPOINT = "https://api.openai.com/v1/chat/completions"

# Display warning message with note about refreshing
st.warning("Important note: Please refresh the page by pressing Ctrl+Shift+R to reset everytime")
def remove_comments_and_docstrings(source):
    # Remove comments and docstrings from the code
    source = re.sub(r'(?<!\\)\".*?(?<!\\)\"', '', source, flags=re.DOTALL)
    source = re.sub(r"(?<!\\)'.*?(?<!\\)'", '', source, flags=re.DOTALL)
    source = re.sub(r'(?m)^ *#.*\n?', '', source)
    return source.strip()

def generate_contract_info(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "max_tokens": 4096,
        "temperature": 0.5,
        "n": 1,
        "messages": [
            {"role": "system", "content": "I want you to act as a smart contract code explainer you need properly and elaborately explain all the functions and methods in the code without missing any of the method or function and how does those functions and methods works to user without any technical jargon, Your name is 'Explainable Blockchain', refuse to answer other questions except solidity and smart contract code."},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(API_ENDPOINT, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except Exception as err:
        st.write("Sorry, I couldn't understand the smart contract. Please check your input and try again.")


def download_explanation(explanation):
    with open('explanation.txt', 'w') as f:
        f.write(explanation)
    st.download_button(
        label="Download Explanation",
        data=open('explanation.txt', 'rb').read(),
        file_name='explanation.txt',
        mime='text/plain'
    )

st.title("Explainable Blockchain")

st.write("I'm a smart contract interpreter for Ethereum written in Solidity. Please provide me with the contract you would like me to explain and validate.")

sample_contracts = {
    "Example Contract": "pragma solidity ^0.8.0;\n\ncontract Example {\n    uint256 public value;\n\n    function setValue(uint256 _value) public {\n        value = _value;\n    }\n}",
    "Another Contract": "pragma solidity ^0.8.0;\n\ncontract Another {\n    string public greeting;\n\n    constructor(string memory _greeting) {\n        greeting = _greeting;\n    }\n}"
}

contract_code = None
contract_text = None
uploaded_file = st.file_uploader("Upload Ethereum smart contract file (.sol)", type=["sol"])

if uploaded_file is not None:
    contract_code = remove_comments_and_docstrings(uploaded_file.read().decode("utf-8"))
    print(contract_code)
    st.write("The following smart contracts are available from the uploaded file:")
    contracts = re.findall("contract\s+(\w+)\s*\{", contract_code)
    contract_selection = st.selectbox("Select a smart contract to explain", contracts)
    contract = contract_code  # assign uploaded contract to `contract` variable
else:
    contract_text = st.text_input("Or enter the smart contract you would like me to explain and validate:")
    contract = remove_comments_and_docstrings(contract_text.strip()) if contract_text else None


# Display sample smart contracts for user to select
st.write("Or select a sample smart contract to test the system:")

sample_contract_names = list(sample_contracts.keys())
selected_sample_contract = st.selectbox("Select a sample smart contract to test the system:", sample_contract_names)

if contract_text:
    contract = contract_text
elif selected_sample_contract:
    contract = sample_contracts[selected_sample_contract]
else:
    contract = None
# contract_text = st.text_input("Or enter the smart contract you would like me to explain and validate:")

if st.button("Explain and Validate"):
    if contract or contract_text:
        if not contract:
            contract = contract_text
        if contract_code:
            contract = contract_code
        explanation = generate_contract_info(contract)
        try:
            st.write(explanation['choices'][0]['message']['content'])
            download_explanation(explanation['choices'][0]['message']['content'])
        except:
            pass

    else:
        st.write("Please enter a smart contract to explain and validate.")


#Display the selected contract code
if uploaded_file is not None:
    st.write(f"Here's the code for the '{contract_selection}' smart contract:")
    st.code(contract_code, language='solidity')