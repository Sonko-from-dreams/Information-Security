from pages.Lab_1 import *
from pages.Lab_2 import *
from pages.Lab_3 import *
from pages.Lab_4 import *
from pages.Lab_5 import *

st.set_page_config(layout="wide")

# головна сторінка
def main_page():
    st.title("Головна сторінка")
    st.write("Вітаю на моєму малому сайті із Захисту інформації!")
    st.write("Усі потрібні лабораторні можна переглянути через бічну панель :3")

# усі сторінки
pages = {
    "Мої сторіночки :" : [
        st.Page(main_page, title="Головна сторінка"),
        st.Page(lab_1, title="Лабораторна №1 : ГПВЧ"),
        st.Page(lab_2, title="Лабораторна №2 : MD5"),
        st.Page(lab_3, title="Лабораторна №3 : RC5"),
        st.Page(lab_4, title="Лабораторна №4 : RCA"),
        st.Page(lab_5, title="Лабораторна №5 : DSS")
    ]
}

pg = st.navigation(pages, position="sidebar", expanded=True)

pg.run()