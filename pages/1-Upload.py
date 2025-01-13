import fitz
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

def init_page():
    st.set_page_config(
        page_title="Upload PDF(s)",
        page_icon="📃",
    )
    st.sidebar.title("Options")

def init_messages():
    clear_button = st.sidebar.button("Clear DB", key="clear")
    if clear_button and "vectorstore" in st.session_state:
        del st.session_state.vectorstore


def get_pdf_text():
    pdf_file = st.file_uploader(
        label = "Upload a PDF file",
        type="pdf",
    )
    if pdf_file:
        pdf_text = ""
        with st.spinner("Loading PDF..."):
            pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
            for page in pdf_document:
                pdf_text += page.get_text()

        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=500,
            chunk_overlap=0,
        )
        return text_splitter.split_text(pdf_text)
    else:
        return None

def build_vector_store(pdf_text):
    with st.spinner("Saving to vector store..."):
        if 'vectorstore' in st.session_state:
            st.session_state.vectorstore.add_texts(pdf_text)
        else:
            st.session_state.vectorstore = FAISS.from_texts(
                texts=pdf_text,
                embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
            )
            

def page_pdf_upload_and_build_vector_db():
    st.title("PDF Upload")
    pdf_text = get_pdf_text()
    if pdf_text:
        build_vector_store(pdf_text)

def main():
    init_page()
    init_messages()
    page_pdf_upload_and_build_vector_db()

if __name__ == "__main__":
    main()
