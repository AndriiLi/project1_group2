import os

import streamlit as st


def show_about():

    parent_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(parent_dir + '/images', "logo.svg")
    st.markdown(
        '''
        Данное приложения является дипломным проектом GoIt  
        Курс:  **Data Science and Machine Learning**  
        проект разработан командой: **Augures**

        '''
    )
    st.image('images/logo.svg', width=200)
