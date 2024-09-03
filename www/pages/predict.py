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

    except ValueError as e:
        st.error("This field must be float. (Ex. 0.5)")


def validationFloatPositive(value, name):
    if value is None:
        return
    try:
        if value:
            value = float(value)
            if value < 0 or value > 100:
                st.error(f"{name} must be between 0 and 100.")

    except ValueError as e:
        st.error("This field must be float. (Ex. 0.5)")

def load_scaler(model_index):
    if model_index == 0:
        scaler_name = f"nn_scaller.pkl"
    else:
        scaler_name = f"nn{model_index}_scaller.pkl"

    scaler_path = os.path.join(WORKING_DIR, scaler_name)

    with open(scaler_path, 'rb') as f:
        return pickle.load(f)


def load_model(model_index):
    if model_index == 0:
        model_name = f"nn_model.keras"
    else:
        model_name = f"nn{model_index}_model.keras"

    model_path = os.path.join(WORKING_DIR, model_name)
    return keras.saving.load_model(model_path)


def predict_by_custom_params(model_index):
    with st.form(key='input_form'):
        is_tv_subscriber = st.checkbox('Is TV Subscriber')
        is_movie_package_subscriber = st.checkbox('Is Movie Package Subscriber')

        subscription_age = st.text_input('Subscription Age', value=0)
        validationFloatPositive(subscription_age, 'Subscription Age')

        bill_avg = st.text_input('Average Bill', value=0)
        validationFloatPositive(bill_avg, 'Average Bill')

        remaining_contract = st.text_input('Remaining contract (-1 if prepaynment)', value=0)
        validationFloat(remaining_contract, 'Remaining_contract')

        download_avg = st.text_input('Download avg', value=0)
        validationFloatPositive(download_avg, 'Download avg')

        upload_avg = st.text_input('Upload avg', value=0)
        validationFloatPositive(upload_avg, 'Upload avg')

        download_over_limit = st.text_input('Download Over Limit', value=0)
        validationFloatPositive(download_over_limit, 'Download Over Limit')
        submit_button = st.form_submit_button(label='Прогнозувати')
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

            scaler = load_scaler(model_index)

            print(scaler)

            data_scaled = scaler.transform(df)
            model = load_model(model_index)

            y_pred = (model.predict(data_scaled)).astype("float32")
            st.subheader(f"Результат прогнозу: {y_pred[0][0] * 100:.2f}%")


def predict_by_dataset(model_index):
    st.subheader('Завантажити датасет')
    uploaded_file = st.file_uploader("оберить файл датасету")

    if uploaded_file is not None:

        threshold = st.select_slider(
            "Оберіть значення порогу",
            options=getSteps(0, 1.01, 0.01, 2),
        )

        run_predict = st.button('Зробити прогноз')

        if run_predict:

            df = pd.read_csv(uploaded_file)
            df = df.dropna()
            df = df.astype(np.float32)

            scaler = load_scaler(model_index)
            data_scaled = scaler.transform(df)

            model = load_model(model_index)
            predictions = []
            counter_threshold = 0

            for i in range(len(data_scaled)):
                single_record = data_scaled[i].reshape(1, -1)
                prediction = model.predict(single_record)

                if prediction.shape[1] == 1:
                    predict_value = f"{0 if prediction[0][0] is None else float(prediction[0][0] * 100):.2f}"
                else:
                    predict_value = f"{0 if prediction[0][0] is None else float(prediction.argmax() * 100):.2f}"

                if float(predict_value) > float(threshold * 100):
                    counter_threshold += 1

                predictions.append(f"{predict_value}%")

            df['Predictoin'] = predictions

            st.subheader(f"Кількість записів з прогнозом більше введеного значення порогу: {counter_threshold}")

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

    model_options = [
        "Модель на основі NN (4 layer 3relu+dropout+sigmoid, optimizer Adam)",
        "Модель на основі NN (4 layer 2relu+sigmoid+early stoping, optimizer Adam, activationFn tahn)"
    ]

    st.header("Оберіть модель:", )
    model_type = st.radio(
        "",
        model_options,
        index=0
    )
    model_index = model_options.index(model_type)
    st.subheader(f"{model_type}")
    tab1, tab2 = st.tabs(["По датасету", "По обраним параметрам"])

    with tab1:
        predict_by_dataset(model_index)

    with tab2:
        predict_by_custom_params(model_index)


hide_streamlit_style = """
         <style>
         [data-testid="stException"] {
             display: none !important;
         }
         </style>
         """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

menu()
show_predict()


