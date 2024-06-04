from librerias import *

def load_sectpub():
    pass


def make_sect_pub():
    load_sectpub()
    c1,c2=st.columns((0.8,0.2))
    with c1:
        with st.container():
            st.caption('Aca poner déficit fiscal y financiero y para que el usuario elija el ratio sobre PBI, dólares y pesos')
    with c2:
        with st.container():
            st.caption('Link web')
    c1,c2=st.columns(2)
    with c1:
        with st.container():
            st.subheader('Resultado Fiscal')
    with c2:
        with st.container():
            st.subheader('Resultado Financiero')
    c1,c2=st.columns(2)
    with c1:
        with st.container():
            st.subheader('Deuda Pública')
    with c2:
        with st.container():
            st.subheader('Mapa Fiscal Argentino')