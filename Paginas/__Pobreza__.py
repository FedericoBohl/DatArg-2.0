from Paginas.librerias import *


def make_pobreza_web():
    c1,c2=st.columns(2)
    with c1.container(border=True):
        st.header('Actividad, empleo y desempleo')
    with c2.container(border=True):
        st.header('Indice de salarios')
    c1,c2=st.columns(2)
    with c1.container(border=True):
        st.header('Tasa de pobreza indigencia')
    with c2.container(border=True):
        st.header('Sal Min Vit y Mov & Haber Min Jub')
