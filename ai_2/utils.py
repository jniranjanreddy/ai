import io
import time
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from google.api_core.exceptions import ResourceExhausted

def extract_text_from_pdf(pdf):
    """Extract text from a PDF file."""
    try:
        print("Starting PDF text extraction...")
        pdf_reader = PdfReader(io.BytesIO(pdf.read()))
        text = "\n\n".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())
        print(f"Extracted text length: {len(text)} characters")
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {str(e)}")
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def initialize_vector_index(text, api_key):
    """Initialize FAISS vector index from text."""
    try:
        print("Initializing vector index...")
        print(f"Input text length: {len(text)} characters")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=200)
        texts = text_splitter.split_text(text)
        print(f"Split text into {len(texts)} chunks")
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=api_key
        )
        print("Generating embeddings...")
        vector_index = FAISS.from_texts(texts, embeddings).as_retriever()
        print("Vector index initialized successfully")
        return vector_index
    except Exception as e:
        print(f"Error initializing vector index: {str(e)}")
        raise Exception(f"Error initializing vector index: {str(e)}")

def get_response(question, vector_index, api_key):
    """Get response from Gemini model using RAG with rate limit handling."""
    try:
        print(f"Processing question: {question}")
        prompt_template = """
        Answer the question as detailed as possible from the provided context. If the answer is not in the provided context, say, "The answer is not available in the context." Do not provide incorrect information.

        Context:
        {context}

        Question:
        {question}

        Answer:
        """
        prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'question'])
        
        # Try gemini-1.5-flash first (higher free-tier limits)
        try:
            print("Initializing gemini-1.5-flash model...")
            model = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                temperature=0.3,
                google_api_key=api_key
            )
            print("Using gemini-1.5-flash model")
        except Exception as e:
            print(f"Failed to use gemini-1.5-flash: {str(e)}. Falling back to gemini-2.0-flash")
            model = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                temperature=0.3,
                google_api_key=api_key
            )
            print("Using gemini-2.0-flash model")

        # Retrieve relevant documents
        print("Retrieving relevant documents...")
        docs = vector_index.invoke(question)
        print(f"Retrieved {len(docs)} documents")
        
        # Format context for the prompt
        context = "\n".join([doc.page_content for doc in docs])
        print(f"Context length: {len(context)} characters")
        
        # Prepare the prompt
        formatted_prompt = prompt.format(context=context, question=question)
        print(f"Formatted prompt length: {len(formatted_prompt)} characters")
        
        # Retry logic for rate limit errors
        retries = 3
        for attempt in range(retries):
            try:
                print(f"Sending request to Gemini API (attempt {attempt + 1}/{retries})...")
                response = model.invoke(formatted_prompt)
                print("Response generated successfully")
                print(f"Response: {response.content}")
                return response.content
            except ResourceExhausted as e:
                if attempt < retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                    print(f"Rate limit exceeded, retrying in {wait_time} seconds: {str(e)}")
                    time.sleep(wait_time)
                else:
                    print(f"Failed after {retries} attempts: {str(e)}")
                    raise e
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return f"Error generating response: {str(e)}"