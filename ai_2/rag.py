import streamlit as st
import os
from dotenv import load_dotenv
from utils import extract_text_from_pdf, initialize_vector_index, get_response

# Load environment variables
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    print("GOOGLE_API_KEY not found in .env file")
    st.error("GOOGLE_API_KEY not found. Please check your .env file.")

# Streamlit page configuration
st.set_page_config(page_title="Your AI Assistant", page_icon="📚", layout="wide")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "vector_index" not in st.session_state:
    st.session_state.vector_index = None
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

# Custom CSS for modern UI
st.markdown("""
<style>
    .chat-container {
        background-color: #f5f5f5;
        border-radius: 10px;
        padding: 20px;
        height: 70vh;
        overflow-y: auto;
        border: 1px solid #e0e0e0;
    }
    .user-message {
        background-color: #007bff;
        color: white;
        border-radius: 15px;
        padding: 10px 15px;
        margin: 10px;
        max-width: 70%;
        align-self: flex-end;
    }
    .bot-message {
        background-color: #ffffff;
        color: black;
        border-radius: 15px;
        padding: 10px 15px;
        margin: 10px;
        max-width: 70%;
        border: 1px solid #e0e0e0;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
        padding: 20px;
    }
    .stButton>button {
        background-color: #007bff;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for PDF upload and processing
with st.sidebar:
    st.header("📄 Upload PDFs")
    uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)
    if uploaded_files:
        print(f"Uploaded {len(uploaded_files)} PDF files")
        st.session_state.uploaded_files = uploaded_files
    if st.button("Process PDFs"):
        if st.session_state.uploaded_files:
            with st.spinner("Processing PDFs..."):
                try:
                    print("Starting PDF processing...")
                    all_text = ""
                    for pdf in st.session_state.uploaded_files:
                        print(f"Processing PDF: {pdf.name}")
                        text = extract_text_from_pdf(pdf)
                        all_text += text + "\n\n"
                    print(f"Total extracted text length: {len(all_text)} characters")
                    st.session_state.vector_index = initialize_vector_index(all_text, google_api_key)
                    st.success("PDFs processed successfully!")
                except Exception as e:
                    print(f"Error processing PDFs: {str(e)}")
                    st.error(f"Error processing PDFs: {str(e)}")
        else:
            print("No PDF files uploaded")
            st.error("Please upload at least one PDF file.")

    # Display uploaded files
    if st.session_state.uploaded_files:
        st.subheader("Uploaded Files")
        for file in st.session_state.uploaded_files:
            st.write(f"📎 {file.name}")

# Main chat interface
st.title("📚 Your AI Assistant")
st.markdown("Ask questions about your uploaded PDFs, and get answers powered by C & K Management Ltd.")

# Chat container
with st.container():
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-message">{message["content"]}</div>', unsafe_allow_html=True)

# Input box and send button
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Your question:", placeholder="Ask about your PDFs...")
    submit_button = st.form_submit_button("Send")

# Process user input
if submit_button and user_input:
    if not st.session_state.vector_index:
        print("No vector index available. Please process PDFs first.")
        st.error("Please upload and process PDFs first.")
    else:
        with st.spinner("Generating response..."):
            try:
                print(f"User submitted question: {user_input}")
                st.session_state.messages.append({"role": "user", "content": user_input})
                response = get_response(user_input, st.session_state.vector_index, google_api_key)
                print(f"Assistant response: {response}")
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()
            except Exception as e:
                print(f"Error generating response: {str(e)}")
                st.error(f"Error generating response: {str(e)}")