import streamlit as st
from streamlit_app.pages.users_page import users_page
from streamlit_app.pages.analytics_page import analytics_page
from data_control import DataControl
from session import Session


def initialize_session_state():
    if 'initialize_indicator' not in st.session_state:
        st.session_state['initialize_indicator'] = True

        st.session_state['data_control'] = DataControl()
        st.session_state['session'] = Session()
        st.session_state['user_1'] = ''
        st.session_state['user_2'] = ''
        st.session_state['user_1_df'] = None
        st.session_state['user_2_df'] = None

        st.session_state['text_color'] = st.get_option('theme.textColor')
        print(st.session_state.text_color)


def main():
    st.set_page_config(page_title='Letterboxd user comparison', page_icon='📽️', layout="wide",
                       initial_sidebar_state="auto", menu_items=None)

    st.sidebar.selectbox("Page", ["User selection", "Analytics"], key='current_page')
    if st.session_state.current_page == 'User selection':
        st.sidebar.write('Select two Letterboxd users you want to compare')
    if st.session_state.current_page == 'Analytics':
        st.sidebar.write('Check how similar these users are')

    initialize_session_state()

    page_loader = {'User selection': users_page, 'Analytics': analytics_page}
    page_loader[st.session_state.current_page]()
