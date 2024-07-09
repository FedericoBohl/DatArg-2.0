from librerias import *


def make_actividad_web():
    c1,c2=st.columns(2)
    with c1.container(border=False):
        st.header('PBI Real')
    with c2.container(border=False):
        st.header('Componentes sobre PBI')
    c1,c2=st.columns(2)
    with c1.container(border=False):
        st.header('Actividad')
        st.caption('''* Emae general\n* Emae campo\n* Emae construcción\n* Etc.''')
    with c2.container(border=False):
        st.header('PBI en USD y PBI per cápita')
