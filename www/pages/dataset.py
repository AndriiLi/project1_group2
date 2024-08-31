import streamlit as st
from pathlib import Path
import json

from menu import menu



DATASET_IMAGES = {
    "Гістограми значень": 'images/histograms_raw.png',
    "Кореляційна Матриця": 'images/corr_matrix.png'
}


def show_dataset():
    st.title("Характеристики датасету")

    with open(Path('./').absolute().parent.joinpath('data/internet_service_churn.csv')) as f:
        st.download_button('Завантажити датасет', f)

    st.text("Розмір датасету")

    with open(Path('').joinpath('reports/summary.json')) as f:
        summary = json.load(f)
        for key, value in summary.items():
            col = st.columns(2)
            with col[0]:
                st.write(key)
            with col[1]:
                st.write(value)


    for name, image in DATASET_IMAGES.items():
        st.write(name)
        st.image(image, width=600)


menu()
show_dataset()
