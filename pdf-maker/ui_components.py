import streamlit as st

def sidebar():
    with st.sidebar:
        st.markdown("## 📄 PDF Converter Pro")
        st.caption("Clean • Fast • Unicode-Safe")
        st.divider()

def footer():
    st.divider()
    st.caption("© 2026 PDF Converter Pro | Built with Python & Streamlit")
