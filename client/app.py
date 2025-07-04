import streamlit as st
from components.upload import render_uploader
from components.history_download import render_history_download
from components.chatUI import render_chat

st.set_page_config(page_title="Docscribe", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <h1 style="text-align: center; margin-top: -40px; color: #2e8bff;">
        Docscribe – Smart PDF Chat Assistant
    </h1>
    <p style="text-align: center; font-size: 1.1rem; color: gray;">
        Upload PDFs. Ask questions. Get document-grounded answers instantly.
    </p>
""", unsafe_allow_html=True)

render_uploader()
render_chat()

render_history_download()