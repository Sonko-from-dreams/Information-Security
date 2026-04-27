import streamlit as st
from Lab_5_DSS import pr_key_for_download, pb_key_for_download, generate_keys, load_private_key_bytes, load_public_key_bytes
from Lab_5_DSS import load_signature_from_hex_file, verify_message, verify_file, sign_message, sign_file, sign_for_download
import io
import zipfile
import base64

def create_zip_archive(priv_key, pub_key, passphrase):
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

def lab_5():
    st.title("Лабораторна №5: Цифровий підпис DSS")

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
        txt = st.text_area("Введіть текст: ")
        if txt:
            input_data = txt.encode()
            type = "text"
            file_name = 'text'

    with tab3:
        uploaded_file = st.file_uploader("Оберіть будь-який файл:")
        if uploaded_file:
            input_data = uploaded_file
            file_name = uploaded_file.name
            type = "file"

    st.divider()



    col1, col2 = st.columns(2)

    if input_data:
        with col1:
            sign = st.file_uploader("Ваш підпис для перевірки : ")
            if st.button('Перевірити', use_container_width=True):
                if sign:
                    signature = load_signature_from_hex_file(sign)
                    data_to_check = None
                    data_to_check = input_data
                    if data_to_check and st.session_state.public_key:
                        try:
                            if type == "text":
                                result = verify_message(st.session_state.public_key, data_to_check, signature)
                            else:
                                result = verify_file(st.session_state.public_key, data_to_check, signature)
                            if result:
                                st.success('Так, повідомлення ваше!')
                            else :
                                st.error('Помилка! Повідомлення не було підписане вами')
                        except Exception as e:
                            st.error(f"Помилка алгоритму: {e}")
                    else :
                        st.warning("Потрібні дані та Публічний ключ. Перевірте, чи обидва є.")
                else :
                    st.error("Потрібен підпис для перевірки.")


        with col2:
            st.caption("Підписання тексту : ")
            if st.button('Підписати', use_container_width=True, type='primary'):
                data_to_sign = None
                if type == "text":
                    data_to_sign = input_data
                    file_name = "text"
                else:
                    data_to_sign = uploaded_file
                if data_to_sign and st.session_state.private_key:
                    try :
                        if type == "text":
                            result = sign_message(st.session_state.private_key, data_to_sign)
                            if result:
                                st.download_button("Завантажити підпис", result.hex(),
                                                   file_name="text_signature.enc")
                            else:
                                st.error(f"Помилка підпису: {e}.")
                        else:
                            result = sign_file(st.session_state.private_key, data_to_sign)
                            if result:
                                st.download_button("Завантажити підпис", sign_for_download(result),
                                                   file_name=f"{file_name}_signature.enc")
                            else:
                                st.error(f"Помилка підпису: {e}.")

                    except Exception as e:
                        st.error(f"Помилка підпису: {e}.")
                else:
                    st.warning("Потрібні дані та Приватний ключ. Перевірте, чи обидва є.")