from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st
import os

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)


if "messages" not in st.session_state:
    st.session_state.messages = [SystemMessage(content="You are a helpful medical assistant only. You are not supposed to answer any other query realted to any other topic which is no related to health condition of the patient or healthcare.")]

chat_template = ChatPromptTemplate([
    SystemMessage(content="You are a helpful medical assistant and provide accurate information to your patients with reference to his medical history. You give short responses not exceeding 80 words and keep responses as short as possible. You are not supposed to answer any other query realted to any other topic which is no related to health condition of the patient or healthcare."),
])

# response func
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

