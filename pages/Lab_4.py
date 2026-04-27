import streamlit as st
from Lab_4_RSA_algorithm import pr_key_for_download, load_private_key_bytes, load_public_key_bytes, pb_key_for_download, generate_keys
from Lab_4_RSA_algorithm import encrypt_chunks, decrypt_chunks
import io
import zipfile
import base64

def create_zip_archive(priv_key, pub_key, passphrase):
    # Створюємо буфер у пам'яті
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        # Додаємо приватний ключ
        zf.writestr("private_key.pem", pr_key_for_download(priv_key, passphrase))
        # Додаємо публічний ключ
        zf.writestr("public_key.pem", pb_key_for_download(pub_key))
    return buf.getvalue()

def bytes_to_b64(data):
    return base64.b64encode(data).decode('utf-8')

def b64_to_bytes(b64_str):
    return base64.b64decode(b64_str)

def lab_4():
    st.title("Лабораторна №4: RSA Шифрування")

    if 'private_key' not in st.session_state:
        st.session_state.private_key = None
    if 'public_key' not in st.session_state:
        st.session_state.public_key = None

    tab1, tab2, tab3 = st.tabs(["Ключі", "Текст", "Файл"])

    with tab1:
        passphrase = st.text_input("Ваш пароль для ключа:", type="password")

        st.divider()

        st.markdown("Згенерувати ключі")
        col1, col2 = st.columns(2)
        with col1:
            if st.button('Згенерувати нову пару', type="primary"):
                if not passphrase:
                    st.error("Введіть пароль для захисту приватного ключа!")
                else:
                    pr_k, pb_k = generate_keys()
                    st.session_state.private_key = pr_k
                    st.session_state.public_key = pb_k
                    zip_data = create_zip_archive(
                        st.session_state.private_key,
                        st.session_state.public_key,
                        passphrase
                    )

                    st.download_button(
                        label="Завантажити ключі (ZIP)",
                        data=zip_data,
                        file_name="rsa_keys.zip",
                        mime="application/zip"
                    )
                    with col2:
                        st.success('Ключі згенеровано та збережено в пам\'яті!')
        st.divider()
        st.markdown("Завантажити ключі")
        up_pri = st.file_uploader("Приватний ключ:", type="pem")
        up_pub = st.file_uploader("Публічний ключ:", type="pem")
        if up_pri and up_pub and passphrase:
            if st.button("Активувати завантажені ключі"):
                try:
                    if up_pri and passphrase:
                        st.session_state.private_key = load_private_key_bytes(up_pri.read(), passphrase)
                    if up_pub:
                        st.session_state.public_key = load_public_key_bytes(up_pub.read())
                    st.success("Ключі успішно завантажені!")
                except Exception as e:
                    st.error(f"Помилка: Перевірте пароль або файл ключа. {e}")

    input_data = None
    type = None

    with tab2:
        txt = st.text_area("Введіть текст:")
        if txt:
            input_data = txt.encode()
            type = "text"

    with tab3:
        uploaded_file = st.file_uploader("Оберіть будь-який файл:")
        if uploaded_file:
            input_data = uploaded_file.read()
            file_name = uploaded_file.name
            type = "file"

    st.divider()

    col1, col2 = st.columns(2)

    if input_data:
        with col1:
            if st.button('Зашифрувати', use_container_width=True, type='primary'):
                data_to_enc = None
                if type == "text":
                    data_to_enc = input_data
                else:
                    data_to_enc = uploaded_file
                if data_to_enc and st.session_state.public_key:
                    # if len(input_data) > 190:
                    #     st.error("Текст занадто довгий для чистого RSA. Використовуйте короткі повідомлення.")
                    # else :
                    try:
                        result = encrypt_chunks(input_data, st.session_state.public_key)
                        if type == 'text':
                            st.write("Зашифрований текст:")
                            st.code(bytes_to_b64(result))
                        else :
                            st.download_button("Завантажити зашифрований файл", result, file_name=f"{file_name}.enc")
                    except Exception as e:
                        st.error(f"Помилка шифрування: {e}")
                else:
                    st.warning("Потрібні дані та Публічний ключ. Перевірте, чи обидва є.")

        with col2:
            if st.button('Розшифрувати', use_container_width=True):
                if st.session_state.private_key:
                    try:
                        if type == "text":
                            try:
                                bytes_to_decrypt = b64_to_bytes(input_data)
                            except Exception:
                                raise ValueError("Текст не є валідним Base64 кодом.")
                        else:
                            bytes_to_decrypt = input_data
                        result = decrypt_chunks(bytes_to_decrypt, st.session_state.private_key)

                        if type == 'text':
                            st.text_area("Результат :", result.decode())
                        else :
                            st.download_button("Завантажити розшифрований файл", result,
                                           file_name=f"decrypted_{file_name.replace('.enc', '')}")
                    except Exception as e:
                        st.error(f"Помилка дешифрування: {e}. Можливо, неправильний ключ або пароль.")
                else:
                    st.warning("Потрібні дані та Приватний ключ. Перевірте, чи обидва є.")