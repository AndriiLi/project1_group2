import os

import streamlit as st
from streamlit_navigation_bar import st_navbar

from constants import NAV_MENU

st.set_page_config(initial_sidebar_state="collapsed")

# parent_dir = os.path.dirname(os.path.abspath(__file__))
# logo_path = os.path.join(parent_dir + '/images', "logo.svg")

options = {
    "show_menu": False,
    "show_sidebar": False,
}

page = st_navbar(
    list(NAV_MENU.keys()),
    # logo_path=logo_path,
    options=options,
)

redirect = NAV_MENU.get(page)

if redirect:
    redirect()
