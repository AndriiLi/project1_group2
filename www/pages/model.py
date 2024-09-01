import os
import streamlit as st
import matplotlib.pyplot as plt
import pickle
import pandas as pd
from menu import menu


def plot_training_history(history):
    if not history:
        st.write("Історія тренування недоступна.")
        return
    else:
        st.write("Історія тренування.")

    plt.figure(figsize=(12, 10))

    if 'loss' in history and 'val_loss' in history:
        plt.subplot(2, 1, 1)
        plt.plot(history['loss'], label='Train Loss')
        plt.plot(history['val_loss'], label='Validation Loss')
        plt.title('Функція втрат')
        plt.xlabel('Епоха')
        plt.ylabel('Втрата')
        plt.legend()
    else:
        st.write("Ключі 'loss' або 'val_loss' не знайдені в історії.")

    if 'accuracy' in history and 'val_accuracy' in history:
        plt.subplot(2, 1, 2)  # Размещаем второй график во второй ячейке
        plt.plot(history['accuracy'], label='Train Accuracy')
        plt.plot(history['val_accuracy'], label='Validation Accuracy')
        plt.title('Точність')
        plt.xlabel('Епоха')
        plt.ylabel('Точність')
        plt.legend()
    else:
        st.write("Ключі 'accuracy' або 'val_accuracy' не знайдені в історії.")

    st.pyplot(plt)


def display_model_history(history_file):
    try:
        with open(history_file, 'rb') as file:
            history = pickle.load(file)
            plot_training_history(history)
    except AttributeError:
        st.write("Training history is not available for this model.")


def display_report(report_file):
    try:
        with open(report_file, 'rb') as file:
            report = pickle.load(file)
            report_df = pd.DataFrame(report).transpose()
            st.write("### Звіт по класифікації")
            st.dataframe(report_df)

    except AttributeError:
        st.write("Report is not available for this model.")
    except FileNotFoundError:
        st.write(f"File {report_file} not found.")


def show_model():
    working_dir = os.path.abspath('models')

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

    selected_index = model_options.index(model_type)
    st.subheader(f"{model_type}")
    model_history = ''
    model_report = ''

    match selected_index:
        case 0:
            model_name = 'nn_model.keras'
            model_history = 'nn_history.pkl'
            model_scaller = 'nn_scaller.pkl'
            model_report = 'nn_report.pkl'
        case 1:
            model_name = 'nn1_model.keras'
            model_history = 'nn1_history.pkl'
            model_scaller = 'nn1_scaller.pkl'
            model_report = 'nn1_report.pkl'

    model_history_path = os.path.join(working_dir, model_history)
    model_report_path = os.path.join(working_dir, model_report)
    display_model_history(model_history_path)
    display_report(model_report_path)


menu()
show_model()
