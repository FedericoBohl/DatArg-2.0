from librerias import *


def make_precios_web():
    c1,c2=st.columns(2)
    with c1.container(border=True):
        st.header('Inflación')
    with c2.container(border=True):
        st.header('Componentes del IPC')
    c1,c2=st.columns(2)
    with c1.container(border=True):
        st.header('TC y Brecha')
    with c2.container(border=True):
        st.header('Expectativas de Inflación')
