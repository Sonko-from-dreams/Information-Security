import streamlit as st
from Lab_2_MD5_algorithm import *


# сторінка другої лабораторної
def lab_2():
    st.title("Лабораторна №2 : MD5")
    tab1, tab2 = st.tabs(["Текст", "Файл"])

    input_data = None
    mode = None

    with tab1:
        txt = st.text_area("Напишіть текст, який потрібно перевести у хеш:")
        if txt:
            input_data = txt
            mode = "text"

    with tab2:
        uploaded_file = st.file_uploader("Оберіть файл:", type=["pdf", "txt"])
        if uploaded_file :
            input_data = uploaded_file
            mode = "file"

    st.divider()
    cols = st.columns([1, 2, 1])
    with cols[1]:
        submitted = st.button("Згенерувати хеш для повідомлення", type="primary", use_container_width=True)

    st.divider()

    if submitted:
        if not input_data:
            st.error("Будь ласка, введіть текст або завантажте файл")
        else:
            with st.spinner('Обчислення хешу...'):
                try:
                    result = string_hash(input_data) if mode == "text" else file_hash(input_data)
                    col1, col2, col3 = st.columns([1, 2, 1])

                    with col1:
                        st.subheader("Обрахований хеш:")

                    with col2:
                        st.code(result, language="text")

                    with col3:
                        st.download_button(
                            label="Завантажити результат",
                            data=result,
                            file_name="md5_hash.txt",
                            mime="text/plain",
                            use_container_width=True,
                            type="primary"
                        )
                except Exception as e:
                    st.error(f"Помилка при обробці: {e}")