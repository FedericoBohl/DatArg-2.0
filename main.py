import streamlit as st
from streamlit import session_state as S

st.set_page_config(
    page_title="DatArg",
    page_icon="🧉",
    layout="wide",
    initial_sidebar_state="expanded")

if not '__loaded__' in S:
    st.switch_page('pages/login_animation.py')

st.switch_page('pages/app.py')

