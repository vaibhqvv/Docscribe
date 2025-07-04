import streamlit as st
from utils.api import upload_pdfs_api

def render_uploader():
    st.sidebar.markdown("""
        <style>
        .glass-box {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(12px);
            border-radius: 20px;
            padding: 1.5rem;
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: #fff;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        }

        .glass-header {
            font-size: 1.3rem;
            font-weight: bold;
            margin-bottom: 1rem;
            color: #00c6ff;
        }

        .upload-icon {
            font-size: 1.8rem;
            margin-right: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)

    st.sidebar.markdown('<div class="glass-header">Upload PDFs</div>', unsafe_allow_html=True)

    uploaded_files = st.sidebar.file_uploader(
        "Select one or more PDF files", type="pdf", accept_multiple_files=True
    )

    if st.sidebar.button("Upload to Database") and uploaded_files:
        with st.sidebar.status("Uploading to Chroma..."):
            response = upload_pdfs_api(uploaded_files)

        if response.status_code == 200:
            st.sidebar.success("Uploaded successfully!")
        else:
            st.sidebar.error(f"Error: {response.text}")

    st.sidebar.markdown("</div>", unsafe_allow_html=True)
