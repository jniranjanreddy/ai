## integrate openai with langchain
import os
import dotenv
dotenv.load_dotenv()
from langchain.llms import OpenAI

import streamlit as st

# Streamlit framework
openai_key = os.getenv("OPENAI_API_KEY")
openai_api_base = os.getenv("OPENAI_API_BASE")

st.title("OpenAI with LangChain")
input_text = st.text_input("Enter your text here")


if input_text:
    llm = OpenAI(
        temperature=0, 
        model_name="gpt-3.5-turbo", 
        openai_api_key=openai_key,
        openai_api_base=openai_api_base
    )
    st.write(llm.invoke(input_text))


