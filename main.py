import streamlit as st
from page1 import page_1
from page2 import page_2
from page3 import page_3

st.set_page_config(page_title="Cutting Process Feedback", page_icon=":bar_chart:", layout="wide")
pages = {
    "A1 Cutting Process FB": page_1,
    "GHM Cutting FB": page_2,
    "KEM Cutting FB": page_3,
}


if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "A1 Cutting Process FB"

# Sidebar for navigation
selected_page = st.sidebar.radio(
    "Select a page:",
    list(pages.keys()),
    index=list(pages.keys()).index(st.session_state['current_page'])
)


if st.session_state['current_page'] != selected_page:
    st.session_state['current_page'] = selected_page
    st.experimental_rerun()  

pages[st.session_state['current_page']]()
