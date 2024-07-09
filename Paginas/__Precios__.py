from librerias import *
from streamlit_extras.stylable_container import stylable_container as cont


def make_precios_web():
    c1,c2=st.columns(2)
    with c1:
        with cont(key='Inflacion_cont',css_styles="""
                            {
                            background-color:white;
                            padding:5px;
                            border-radius:15px;       
                            border: silver solid 2px;];
                            box-shadow: 0px 0px 13px 10px rgba(255, 255, 255, 0.5)  
                            }    
                            """):
            st.header('Inflación')
    with c2.container(border=False):
        st.header('Componentes del IPC')
    c1,c2=st.columns(2)
    with c1.container(border=False):
        st.header('TC y Brecha')
    with c2.container(border=False):
        st.header('Expectativas de Inflación')
