import os
import streamlit as st
import matplotlib.pyplot as plt
import pickle
import keras
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
            for label, metrics in report.items():
                st.write(f"***Class {label}:***")
                if isinstance(metrics, dict):
                    for metric, value in metrics.items():
                        st.write(f"{metric}: {value}")
                else:
                    st.write(f"{metrics}")

    except AttributeError:
        st.write("Report is not available for this model.")


def show_model():
    working_dir = os.path.abspath('models')

    model_options = [
        "Модель на основі NN",
        "SVM"
    ]

    st.header("Оберіть модель:", )
    model_type = st.radio(
        "",
        model_options,
        index=0
    )

    selected_index = model_options.index(model_type)
    st.write(f"Обрана модель: {model_type}")

    match selected_index:
        case 0:
            model_name = 'nn_model.keras'
            model_history = 'nn_history.pkl'
            model_scaller = 'nn_scaller.pkl'
            model_report = 'nn_report.pkl'
        case _:
            model_name = ''
            model_history = ''
            model_report = ''

    if 'button_clicked' not in st.session_state:
        st.session_state.button_clicked = False

    if st.button('Обрати'):
        st.session_state.button_clicked = True

    if st.session_state.button_clicked:
        # model_path = os.path.join(working_dir, model_name)
        model_history_path = os.path.join(working_dir, model_history)
        model_report_path = os.path.join(working_dir, model_report)

        # model = keras.saving.load_model(model_path)
        display_model_history(model_history_path)
        display_report(model_report_path)


menu()
show_model()
