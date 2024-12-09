import streamlit as st

def subHeader(text, color='white', divider=False):
    st.markdown(f"<h2 style='color:{color};'>{text}</h1>", unsafe_allow_html=True)
    if divider:
        st.markdown(f"<hr style='border:1px solid {divider};'/>", unsafe_allow_html=True)
