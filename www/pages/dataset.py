import streamlit as st
import os
import json

from menu import menu

DATASET_IMAGES = {
    "Гістограми значень": 'images/histograms_raw.png',
    "Кореляційна Матриця": 'images/corr_matrix.png'
}


def show_dataset():
    st.title("Характеристики вихідного датасету")
    st.subheader("Пояснення колонок:")
    st.markdown(
        '''
        id [int]: id користувача

        is_tv_subscriber [0 or 1]: чи є підписником на телебачення
        
        is_movie_package_subscriber [0 or 1]: чи є підписником на фільми
        
        subscription_age [float]: як довго є клієнтом компанії
        
        bill_avg [int]: середній рахунок
        
        remaining_contract [float]: скільки контракту залишилось
        
        service_failure_count [int]: кількість відмов сервісу
        
        download_avg [float]: середній розмір завантажених даних
        
        upload_avg [float]: середній розмір вивантажених даних
        
        download_over_limit [int]: перевищення ліміту завантажень
        
        churn [0 or 1]: чи покунув користувач компанію
        '''
    )

    with open(os.path.abspath('data/internet_service_churn.csv')) as f:
        st.download_button('Завантажити датасет', f)

    st.text("Розмір датасету")

    with open(os.path.abspath('reports/summary.json')) as f:
        summary = json.load(f)
        for key, value in summary.items():
            col = st.columns(2)
            with col[0]:
                st.write(key)
            with col[1]:
                st.write(value)

    for name, image in DATASET_IMAGES.items():
        st.subheader(name)
        st.image(image, width=600)

    st.subheader("Очистка і заповнення пропущених даних")
    st.markdown(
        '''
        Видалено 381 рядків з відсутніми значеннями download_avg i upload_avg
        
        Відсутні значення remaining_contract замінені на -1 (припущення, що ці клієнти на передплаті і контракт у них вже закінчився)
        
        Колонка service_failure_count не береться до уваги, оскільк не виявлено ніяких кореляцій з churn
        '''
    )


menu()
show_dataset()
