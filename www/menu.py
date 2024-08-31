import os
import streamlit as st


def menu():
    st.sidebar.image('images/logo.svg', width=200)
    st.sidebar.header(' --- Augures Team ---')

    st.sidebar.page_link("pages/home.py", label="Головна")
    st.sidebar.page_link("pages/dataset.py", label="Датасет")
    st.sidebar.page_link("pages/model.py", label="Модель")
    st.sidebar.page_link("pages/predict.py", label="Прогноз")
    st.sidebar.page_link("pages/about.py", label="Про проєкт")


    hide_streamlit_style = """
          <style>
          [data-testid="stSidebarCloseButton"] {
              display: none !important;
          }
    
          [data-testid="stSidebarContent"]:hover  [data-testid="stSidebarCollapseButton"] { display: none;}
          [data-testid="StyledFullScreenButton"] { display: none;}
    
          </style>
          """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
