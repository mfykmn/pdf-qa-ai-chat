import os
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# models
from langchain_openai import ChatOpenAI

def init_page():
    st.set_page_config(
        page_title="Q&A",
        page_icon="💬",
    )
    st.sidebar.title("Options")

def init_qa_chain():
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
    )
    prompt = ChatPromptTemplate.from_template(
        """
        以下の前提知識を用いて、ユーザーからの質問に答えてください。

        ===
        前提知識
        {context}

        ===
        ユーザーからの質問
        {question}
        """)
    retriever = st.session_state.vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 10},
    )
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain

def page_ask_my_pdf():
    chain = init_qa_chain()

    if query := st.text_input("PDFへの質問を書いてね: ", key="input"):
        st.markdown("### Answer")
        st.write_stream(chain.stream(query))

def main():
    init_page()
    st.title("Q&A")
    if "vectorstore" not in st.session_state:
        st.warning("まずはPDFをアップロードしてね")
    else:
        page_ask_my_pdf()

if __name__ == "__main__":
    main()
