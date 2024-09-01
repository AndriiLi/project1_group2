import os
import keras
import streamlit as st
import numpy as np
import pandas as pd
from menu import menu
import pickle
from io import StringIO

WORKING_DIR = os.path.abspath('models')


def getSteps(min_value, max_value, step_value, decimal_count):
    array = np.arange(min_value, max_value, step_value)
    return np.round(array, decimals=decimal_count).tolist()


@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')


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


def load_scaler():
    scaler_path = os.path.join(WORKING_DIR, 'nn_scaller.pkl')
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)

    return scaler


def load_model():
    model_path = os.path.join(WORKING_DIR, 'nn_model.keras')
    return keras.saving.load_model(model_path)


def predict_by_custom_params():
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
            scaler = load_scaler()
            data_scaled = scaler.transform(df)

            model = load_model()

            y_pred = (model.predict(data_scaled)).astype("float32")
            st.subheader(f"Prediction result: {y_pred[0][0] * 100:.2f}%")


def predict_by_dataset():
    st.subheader('Завантажити датасет')
    uploaded_file = st.file_uploader("оберить файл датасету")

    if uploaded_file is not None:

        threshold = st.select_slider(
            "Оберіть значення treshhold",
            options=getSteps(0, 1.01, 0.01, 2),
        )

        run_predict = st.button('Зробити прогноз')

        if run_predict:

            df = pd.read_csv(uploaded_file)
            df = df.dropna()
            df = df.astype(np.float32)

            scaler = load_scaler()
            data_scaled = scaler.transform(df)

            model = load_model()
            predictions = []
            counter_threshold = 0

            for i in range(len(data_scaled)):
                single_record = data_scaled[i].reshape(1, -1)
                prediction = model.predict(single_record)

                if prediction.shape[1] == 1:
                    predict_value = f"{0 if prediction[0][0] is None else float(prediction[0][0] * 100):.2f}"
                else:
                    predict_value = f"{0 if prediction[0][0] is None else float(prediction.argmax() * 100):.2f}"

                if float(predict_value) > float(threshold*100):
                    counter_threshold += 1

                predictions.append(f"{predict_value}%")

            df['Predictoin'] = predictions

            st.subheader(f"Кількість записів в прогнозом більш введеного значеня threshold: {counter_threshold}")

            csv = convert_df(df)
            st.download_button(
                "Скачати датасет з прогнозом",
                csv,
                "file.csv",
                "text/csv",
                key='download-csv'
            )


def show_predict():
    st.header('Cтворити прогноз')
    tab1, tab2 = st.tabs(["По датасету", "По обраним параметрам"])

    with tab1:
        predict_by_dataset()

    with tab2:
        predict_by_custom_params()


menu()
show_predict()
