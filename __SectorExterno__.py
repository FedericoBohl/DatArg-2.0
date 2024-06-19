from librerias import *

def make_sect_ext_web():
    c1,c2=st.columns((0.8,0.2))
    with c1:
        with st.container(border=True):
            c11,c12=st.columns((0.3,0.7))
            with c11: st.radio("Escala de los datos",options=["***Millones de USD***","***% del PBI***"],key="escala_sectext")
            with c12: st.number_input(value=2016,label='Datos desde',min_value=2000,max_value=2024,key="start_sectext")
    with c2:
        st.link_button(":blue[**Descargar datos:\nSector Externo**]",url="https://1drv.ms/x/c/56f917c917f2e2f5/QfXi8hfJF_kggFaNFQAAAAAAHinUdp-mVHJoLA",use_container_width=True)
    c1,c2=st.columns(2)
    with c1.container(border=True):
        st.subheader('Balance de Pagos')
        st.text('Suma Interanual')
    with c2.container(border=True):
        st.subheader('Balance Comercial - ToT + TCR')
        st.caption('El Tipo de Cambio es re-escalado por conveniencia visual con base Enero 2004 = 100.')
    c1,c2=st.columns(2)
    with c1.container(border=True):
        st.subheader('Destino de las Expo/Importaciones')
        c11,c12=st.columns(2)
        c11.number_input('Año',2004,2023,step=1)
        c12.radio('Destino expo/impo',label_visibility='collapsed',options=['Valor (USD)','Porcentaje del Total'])
        ex,im=st.tabs(['Exportaciones','Importaciones'])
    with c2.container(border=True):
        st.subheader('Intercambio Comercial Argentino')
        ex,im=st.tabs(['Exportaciones','Importaciones'])