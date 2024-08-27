import streamlit as st
from streamlit import session_state as S
from _globals_ import *
from Paginas.librerias import get_data
from plotly import graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime,timedelta
from itertools import zip_longest

st.cache_resource(show_spinner=False)
def load_pobreza(end):
    his_data=pd.read_csv("His Data/his-salarios.csv",delimiter=";")
    his_data['Unnamed: 0'] = pd.to_datetime(his_data.iloc[:, 0].values, format='%d/%m/%Y')
    his_data.set_index('Unnamed: 0', inplace=True)
    ids=[
        '150.1_CSTA_BARIA_0_D_26',
        '150.1_LA_INDICIA_0_D_16',
        '150.1_LA_POBREZA_0_D_13',
        '57.1_SMVMM_0_M_34',
        '58.1_MP_0_M_24',
        '149.1_TL_INDIIOS_OCTU_0_21',
        '149.1_TL_REGIADO_OCTU_0_16',
        '149.1_SOR_PRIADO_OCTU_0_28',
        '145.3_INGNACNAL_DICI_M_15'
        ]
    cols=["Canasta Basica","Linea Indigencia","Linea Pobreza","SalMVM","Haber Jub","IS Real-Total","IS Real-Formal","IS Real-Informal",'IPC']
    data=get_data(ids,start_date="2024-01-01",col_list=cols)
    data.index = pd.to_datetime(data.index, format='%d/%m/%Y')
    for col in ["IS Real-Total","IS Real-Formal","IS Real-Informal"]:
        data[col]=data[col]/data['IPC']*100*(100/96.73343191)
    data=pd.concat([his_data,data],axis=0)
    data['IPC']=list(zip_longest(S.IPC, [], fillvalue=None))
    data['TC']=list(zip_longest(S.TC, [], fillvalue=None))
    for col in ["Canasta Basica","Linea Indigencia","Linea Pobreza","SalMVM","Haber Jub"]:
        data[f'{col}-real'] = data.apply(lambda row: row[f'{col}'] / row['IPC'] if row['IPC'] is not None else None, axis=1)
        data[f'{col}-USD'] = data.apply(lambda row: row[f'{col}'] / row['TC'] if row['TC'] is not None else None, axis=1)   
    salarios=data.copy()
    
    his_data=pd.read_csv("His Data/his-mercado laboral.csv",delimiter=";")
    his_data['Unnamed: 0'] = pd.to_datetime(his_data.iloc[:, 0].values, format='%d/%m/%Y')
    his_data.set_index('Unnamed: 0', inplace=True)
    ids=[
        '42.3_EPH_PUNTUATAL_0_M_27',
        '42.3_EPH_PUNTUATAL_0_M_24',
        '42.3_EPH_PUNTUATAL_0_M_30',
        '42.3_EPH_PUNTUATAL_II_0_M_30',
        '42.3_EPH_PUNTUANTE_0_M_41',
        '42.3_EPH_PUNTUANTE_0_M_44'
        ]
    cols=["actividad","empleo","desempleo","sub-total","sub-dem","sub-Ndem"]
    data=get_data(ids,start_date="2024-01-01",col_list=cols)
    data.index = pd.to_datetime(data.index, format='%d/%m/%Y')
    data.reindex(columns=his_data.columns)
    data=pd.concat([his_data,data],axis=0)
    empleo=data.copy()
    
    data=pd.read_csv("His Data/his-pobreza-indigencia.csv",delimiter=";")
    data['Unnamed: 0'] = pd.to_datetime(data.iloc[:, 0].values, format='%d/%m/%Y')
    data.set_index('Unnamed: 0', inplace=True)
    def format_semester(date):
        year = date.year
        semester = "I Sem." if date.month == 1 else "II Sem."
        return f"{semester} {year}"
    # Aplicar la transformación al índice
    data.index = data.index.map(format_semester)

    return salarios, empleo, data


def make_pobreza_web():
    salarios=S.salarios
    empleo=S.empleo
    pobind=S.pobind
    
    c1,c2=st.columns((0.7,0.3),vertical_alignment='center')
    c1.number_input(value=2016,label='Datos desde',min_value=2004,max_value=2024,key="start_pobreza")
    c2.link_button(":blue[**Descargar datos:\nEmpleo y Pobreza**]",url="https://1drv.ms/x/c/56f917c917f2e2f5/EfXi8hfJF_kggFZ2FQAAAAAB010QqFpwX5jKQsspWhva-A?e=Lsp49b",use_container_width=True)
    salarios=salarios.loc[f"{S.start_pobreza}":]
    empleo=empleo.loc[f"{S.start_pobreza}":]
    c1,c2=st.columns(2)
    with c1.container(border=True):
        st.header('Actividad, empleo y desempleo')
        st.write(empleo)
    with c2.container(border=True):
        st.header('Indice de salarios')
        st.write(salarios)
    c1,c2=st.columns(2)
    with c1.container(border=True):
        st.header('Tasa de pobreza indigencia')
        st.write(pobind)
    with c2.container(border=True):
        st.header('Sal Min Vit y Mov & Haber Min Jub')
