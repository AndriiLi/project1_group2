import streamlit as st
import numpy as np


def getSteps(min_value, max_value, step_value, decimal_count):
    array = np.arange(min_value, max_value, step_value)
    return np.round(array, decimals=decimal_count).tolist()


def validationFloat(value, name):
    if value is None:
        return
    try:
        if value:
            value = float(value)
            if value < 0 or value > 1:
                st.error(f"{name} must be between 0 and 1.")

    except ValueError:
        st.error("This field must be float. (Ex. 0.1)")


def show_predict():
    st.title(f"Cтворити прогноз по обраним")
    st.title(f" фильтрам")

    with st.form(key='input_form'):
        is_tv_subscriber = st.checkbox('Is TV Subscriber')
        is_movie_package_subscriber = st.checkbox('Is Movie Package Subscriber')

        subscription_age = st.text_input('Subscription Age', value=0)
        validationFloat(subscription_age, 'Subscription Age')

        bill_avg = st.text_input('Average Bill', value=0)
        validationFloat(bill_avg, 'Average Bill')

        service_failure_count = st.text_input('Service Failure Count', value=0)
        validationFloat(service_failure_count, 'Service Failure Count')

        download_avg = st.text_input('Average Download Speed', value=0)
        validationFloat(download_avg, 'Average Download Speed')

        upload_avg = st.text_input('Average Upload Speed', value=0)
        validationFloat(upload_avg, 'Average Upload Speed')

        download_over_limit = st.text_input('Download Over Limit', value=0)
        validationFloat(download_over_limit, 'Download Over Limit')

        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        st.write("Form submitted successfully!")
        st.write(f"Is TV Subscriber: {is_tv_subscriber}")
        st.write(f"Is Movie Package Subscriber: {is_movie_package_subscriber}")
        st.write(f"Subscription Age: {subscription_age}")
        st.write(f"Average Bill: {bill_avg}")
        st.write(f"Service Failure Count: {service_failure_count}")
        st.write(f"Average Download Speed: {download_avg}")
        st.write(f"Average Upload Speed: {upload_avg}")
        st.write(f"Download Over Limit: {download_over_limit}")
