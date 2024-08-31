import os
import keras
import streamlit as st
import numpy as np
import pandas as pd
from menu import menu
import pickle

WORKING_DIR = os.path.abspath('models')


def getSteps(min_value, max_value, step_value, decimal_count):
    array = np.arange(min_value, max_value, step_value)
    return np.round(array, decimals=decimal_count).tolist()


def validationFloat(value, name):
    if value is None:
        return
    try:
        if value:
            value = float(value)
            if value < -1 or value > 100:
                st.error(f"{name} must be between -1 and 100.")

    except ValueError:
        st.error("This field must be float. (Ex. 0.5)")


def tab1_predict():
    with st.form(key='input_form'):
        is_tv_subscriber = st.checkbox('Is TV Subscriber')
        is_movie_package_subscriber = st.checkbox('Is Movie Package Subscriber')

        subscription_age = st.text_input('Subscription Age', value=0)
        validationFloat(subscription_age, 'Subscription Age')

        bill_avg = st.text_input('Average Bill', value=0)
        validationFloat(bill_avg, 'Average Bill')

        remaining_contract = st.text_input('Remaining contract', value=0)
        validationFloat(remaining_contract, 'Remaining_contract')

        download_avg = st.text_input('Download avg', value=0)
        validationFloat(download_avg, 'Download avg')

        upload_avg = st.text_input('Upload avg', value=0)
        validationFloat(upload_avg, 'Upload avg')

        download_over_limit = st.text_input('Download Over Limit', value=0)
        validationFloat(download_over_limit, 'Download Over Limit')
        submit_button = st.form_submit_button(label='Submit')
        if submit_button:
            data = [
                [
                    bool(is_tv_subscriber),
                    bool(is_movie_package_subscriber),
                    float(subscription_age),
                    float(bill_avg),
                    float(remaining_contract),
                    float(download_avg),
                    float(upload_avg),
                    float(download_over_limit)
                ]
            ]

            columns = [
                'is_tv_subscriber',
                'is_movie_package_subscriber',
                'subscription_age',
                'bill_avg',
                'remaining_contract',
                'download_avg',
                'upload_avg',
                'download_over_limit'
            ]

            df = pd.DataFrame(data, columns=columns).astype(np.float32)
            scaler_path = os.path.join(WORKING_DIR, 'nn_scaller.pkl')
            with open(scaler_path, 'rb') as f:
                scaler = pickle.load(f)

            data_scaled = scaler.transform(df)

            model_path = os.path.join(WORKING_DIR, 'nn_model.keras')
            model = keras.saving.load_model(model_path)

            y_pred = (model.predict(data_scaled)).astype("float32")
            st.write(f"Prediction result: {y_pred[0][0] * 100:.2f}%")


def show_predict():
    st.header('Cтворити прогноз')
    tab1, tab2 = st.tabs(["По обраним фильтрам", "По датасету"])

    with tab1:

            tab1_predict()

    with tab2:
        st.write('test')


menu()
show_predict()
