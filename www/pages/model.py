import streamlit as st
import os


# import tensorflow as tf


def show_model():
    working_dir = os.path.abspath('models')

    model_options = [
        "Логістичну регресія",
        "SVM"
    ]

    modelType = st.radio(
        "Оберіть модель 👇:",
        model_options,
        index=0
    )

    selected_index = model_options.index(modelType)
    st.write(f"Обрана модель: {modelType}")

    match selected_index:
        case 1:
            model_name = ''
            model_history = ''
        case _:
            model_name = ''
            model_history = ''

    if 'button_clicked' not in st.session_state:
        st.session_state.button_clicked = False

    if st.button('Протестити'):
        st.session_state.button_clicked = True

    if st.session_state.button_clicked:
        model_path = os.path.join(working_dir, model_name)
        model_history_path = os.path.join(working_dir, model_history)

        # model = tf.keras.models.load_model(model_path)
