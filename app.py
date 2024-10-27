import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv
import google.generativeai as genai
import os
from PIL import Image
import pytesseract
import base64

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path if necessary

st.set_page_config(page_title="Chat with PDF", page_icon=":books:", layout="wide", initial_sidebar_state="expanded")

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    body {
        font-family: 'Inter', sans-serif;
        background-color: #ffffff;
        color: #333333;
    }
    .main {
        background-color: #ffffff;
        padding: 0 !important;
    }
    .block-container {
        max-width: 100% !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    h1, h2, h3 {
        color: #1a202c;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
        animation: fadeIn 0.5s ease-in-out;
    }
    .chat-message.user {
        background-color: #007bff;
        color: #ffffff;
        align-items: flex-end;
    }
    .chat-message.bot {
        background-color: #f1f3f5;
        color: #000000;
        align-items: flex-start;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    .chat-message .message {
        color: inherit;
    }
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem;
        background-color: #007bff;
        color: #ffffff;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        margin-bottom: 2rem;
        animation: slideDown 0.5s ease-in-out;
    }
    .header-title {
        font-size: 1.5rem;
        font-weight: 600;
    }
    .user-info {
        display: flex;
        align-items: center;
    }
    .user-info span {
        margin-right: 0.5rem;
    }
    .stTextInput > div > div > input {
        background-color: #ffffff;
        color: #333333;
        border: 1px solid #e2e8f0;
        border-radius: 0.375rem;
    }
    iframe {
        border: 1px solid #e2e8f0;
        border-radius: 0.375rem;
        width: 100% !important;
        animation: fadeIn 1s ease-in-out;
    }
    .stSidebar {
        background-color: #f8f9fa;
    }
    .stSidebar [data-testid="stSidebarNav"] {
        background-color: #f8f9fa;
    }
    .stSidebar [data-testid="stSidebarNav"] ::before {
        content: "Upload your PDF or Image";
        margin-left: 20px;
        margin-top: 20px;
        font-size: 1.5em;
        font-weight: bold;
        color: #FF4B4B;
    }
    .css-1offfwp {
        padding-top: 0rem;
    }
    .stButton>button {
        background-color: #007bff;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.3rem;
        font-weight: 600;
        transition: all 0.3s ease;
        animation: pulse 2s infinite;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        transform: scale(1.05);
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes slideDown {
        from { transform: translateY(-20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(0, 123, 255, 0.7);
        }
        70% {
            box-shadow: 0 0 0 10px rgba(0, 123, 255, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(0, 123, 255, 0);
        }
    }
    .animate-charcter {
       text-transform: uppercase;
       background-image: linear-gradient(
         -225deg,
         #231557 0%,
         #44107a 29%,
         #ff1361 67%,
         #fff800 100%
       );
       background-size: auto auto;
       background-clip: border-box;
       background-size: 200% auto;
       color: #fff;
       background-clip: text;
       -webkit-background-clip: text;
       -webkit-text-fill-color: transparent;
       animation: textclip 2s linear infinite;
       display: inline-block;
    }
    @keyframes textclip {
        to {
            background-position: 200% center;
        }
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

st.markdown("""
<div class="header">
    <div class="header-title">
        <span class="animate-charcter">📄 ChatVision</span>
    </div>
    <div class="user-info">
        <span>Welcome</span>
    </div>
</div>
""", unsafe_allow_html=True)

def extract_text_from_image(image):
    try:
        return pytesseract.image_to_string(image)
    except Exception as e:
        st.error(f"Error extracting text from image: {e}")
        return ""

def extract_text_from_pdf(pdf_file):
    try:
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return ""

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_gemini_response(input_text, pdf_context):
   
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Context: {pdf_context}\n\nQuestion: {input_text}\n\nAnswer:"
    response = model.generate_content(prompt)
    return response.text

def main():
   
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hey, how can I help you?"}
        ]
    
    if "current_file" not in st.session_state:
        st.session_state.current_file = None

  
    with st.sidebar:
        uploaded_file = st.file_uploader("Choose a PDF or Image file", type=["pdf", "png", "jpg", "jpeg"], key="file-upload")
    
  
    if uploaded_file and uploaded_file != st.session_state.get('current_file'):
   
        st.session_state.messages = [
            {"role": "assistant", "content": "New file uploaded. How can I help you with this document?"}
        ]
       
        st.session_state.current_file = uploaded_file
      
        if "pdf_context" in st.session_state:
            del st.session_state.pdf_context


    col1, col2 = st.columns([1, 1], gap="small")

    with col1:
        if uploaded_file:
            if uploaded_file.type == "application/pdf":
                pdf_content = uploaded_file.read()
                base64_pdf = base64.b64encode(pdf_content).decode('utf-8')
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" height="600" style="border: none;"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
                
                uploaded_file.seek(0)
                text = extract_text_from_pdf(uploaded_file)
            else:
                st.image(uploaded_file, use_column_width=True)
                image = Image.open(uploaded_file)
                text = extract_text_from_image(image)

            if text:
                with st.sidebar:
                    st.success("Text extracted successfully!")
                    st.text_area("Extracted Text", text, height=150)
                st.session_state.pdf_context = text

    with col2:
        st.markdown("### Chat")
        
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(f'<div style="color: {"#000000" if message["role"] == "assistant" else "#ffffff"};">{message["content"]}</div>', unsafe_allow_html=True)

        if prompt := st.chat_input("Ask about your PDF or Image"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                if "pdf_context" in st.session_state:
                    response = get_gemini_response(prompt, st.session_state.pdf_context)
                else:
                    response = "Please upload a PDF or Image Containing Text first."
                st.markdown(f'<div style="color: #000000;">{response}</div>', unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == '__main__':
    main()
