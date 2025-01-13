from dotenv import load_dotenv
import streamlit as st


load_dotenv()

def init_page():
    st.set_page_config(
        page_title="PDF Q&A AI Chat",
        page_icon="🤖",
    )

def main():
    init_page()
    st.sidebar.success("メニューから選んでね")

    st.markdown(
        """
        # PDF Q&A AI Chat
        このアプリは、PDFファイルを読み込み、その内容に基づいて質問に答えるAIチャットです。

        - まずは左のメニューから`Upload`ページに遷移してPDFをアップロードしてください。
        - PDFをアップロードしたら、`Q&A`ページに遷移して質問を入力してください。
        """
    )

if __name__ == "__main__":
    main()
