import streamlit as st
from Lab_3_RC5_algorithm import *


# сторінка третьої лабораторної
def lab_3():
    st.title("Лабораторна №3 : RC5")

    col1, col2, col3 = st.columns(3)
    with col1:
        w = st.number_input("Введіть бажаний розмір слова у бітах (w)", min_value=16, max_value=64, value=16, step=16)
        if w != 16 and w != 32 and w != 64 :
            st.error('Можливі варіанти рівні лише 16, 32 та 64. Вибрано найменше значення.')
            w = 16

    with col2:
        r = st.number_input("Введіть бажану кількість раундів (r)", min_value=0, max_value=255, value=8)

    with col3:
        b = st.number_input("Введіть бажану кількість октетів у таємному ключі (b)", min_value=0, max_value=255, value=16)

    st.divider()

    key = st.text_input("Ваш таємний ключ:", type="password", value="")

    col1, col2, col3, col4= st.columns([2, 1, 1, 1])

    with col1 :
        uploaded_file = st.file_uploader("Оберіть файл для роботи:")

    if uploaded_file and key:
        if col3.button('Зашифрувати', type="primary"):
            with st.spinner('Шифрування...'):
                result = file_encrypt(w, r, b, key, uploaded_file)
                if result:
                    st.download_button("Завантажити .enc", result,
                                       file_name=f"{uploaded_file.name}.enc")

        if col4.button('Розшифрувати'):
            with st.spinner('Дешифрування...'):
                result = file_decrypt(w, r, b, key, uploaded_file)
                if result:
                    new_name = uploaded_file.name.replace('.enc', '')
                    st.download_button("Завантажити файл", result, file_name=new_name)
