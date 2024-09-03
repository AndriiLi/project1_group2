import os

import streamlit as st

from menu import menu


def show_about():
    st.markdown(
        '''
        Цей додаток є **дипломним проєктом для GoIt**  
        Курс:  **Data Science and Machine Learning**  
        Проєкт розроблений командою: **Augures**

        '''
    )
    st.image('images/logo.svg', width=200)

    st.subheader('Структура та ролі команди')

    col1, col2 = st.columns([1, 3])
    with col1:
        st.write("Andrii Li")
        st.write("Hanna Malygina")
        st.write("Egor Zaks")
        st.write("Ihor Lytvynenko")
        st.write("Volodymyr Byba")

    with col2:
        st.markdown("роль: Team lead, Developer (створення та докеризація додатку)")
        st.markdown("роль: Scrum Master, Developer (eda, створення моделей)")
        st.markdown("роль: Developer (створення моделей)")
        st.markdown("роль: Developer (створення моделей)")
        st.markdown("роль: Developer (eda)")


menu()
show_about()
