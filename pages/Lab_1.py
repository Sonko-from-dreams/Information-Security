import streamlit as st
from Lab_1_Randomizer import generate_rand_num, analyze, get_period
import pandas as pd
import numpy as np

# функція для отримання даних у вигляді таблиці numpy
def get_data(count) :
    table = pd.DataFrame(np.array(generate_rand_num(count)), columns=['Згенеровані числа'])

    return table

# сторінка першої лабораторної
def lab_1():
    st.title("Лабораторна №1 : ГПВЧ")
    col1, col2 = st.columns([2,3])

    # довжина згенерованої послідовності пвч для визначення пі та похибки
    n = 100000

    with col1:
        period = get_period()
        st.metric(label="Період генерації :", value=f"{period}", border=True)

        column1, column2 = st.columns(2)

        with column1:
            test_array = generate_rand_num(n)
            my_pi, error = analyze(n, test_array)
            st.metric(label="π з алгоритму Лемера :", value=f"{my_pi:.5f}",
                      delta=f"{error:.5f}", delta_color="primary", border=True)

        with column2:
            test_array = np.random.randint(0, 2**31, n)
            my_pi, error = analyze(n, test_array)
            st.metric(label="π з бібліотеки numpy :", value=f"{my_pi:.5f}",
                      delta=f"{error:.5f}", delta_color="primary", border=True)

    with col2:
        with st.form("my_form"):
            number = st.number_input("Введіть число", min_value=1, max_value=int(10e10), value=45, step=1)
            coll1, coll2, coll3 = st.columns([1,2,1])
            with coll2 :
                submitted = st.form_submit_button("Згенерувати послідовність ПВЧ", type="primary")

        if submitted:
            st.session_state.df = get_data(number)
            csv = st.session_state.df.to_csv(index=False).encode('utf-16')
            coll1, coll2, coll3 = st.columns([2,1,2])
            with coll1 :
                st.write("Згенерована послідовність ПВЧ : ")
            with coll3 :
                st.download_button(
                    label="Завантажити результат як CSV",
                    data=csv,
                    file_name=f'pseudorandom_numbers_{number}.csv',
                    mime='text/csv',
                    type="primary"
                )
            st.table(st.session_state.df)
        else :
            st.write("Будь ласка, оберіть потрібну вам кількість та підтвердіть свій вибір!")

