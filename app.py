# 1. Imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import streamlit as st
import os

# 2. Load environment
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# 3. Initialize model
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

# 4. Initialize message history with sesssion state
if "messages" not in st.session_state:
    st.session_state.messages = [SystemMessage(content="You are a helpful medical assistant.")]

# Template (optional)
chat_template = ChatPromptTemplate([
    SystemMessage(content="You are a helpful medical assistant and provide accurate information to your patients with reference to his medical history."),
])

# Define response generator
def generate_response(query):
    st.session_state.messages.append(HumanMessage(content=query))
    response = model.invoke(st.session_state.messages)
    st.session_state.messages.append(AIMessage(content=response.content))
    return response.content

# Streamlit page config
st.title("🔗 MediSync AI")

with st.form("my_form"):
    text = st.text_area("Enter your query :")
    submitted = st.form_submit_button("Submit")

    if not GOOGLE_API_KEY:
        st.warning("Please enter your Gemini API key in .env file!", icon="⚠")

    if submitted and GOOGLE_API_KEY:
        output = generate_response(text)
        st.success(output)
