import streamlit as st
from streamlit import session_state as S
from _globals_ import *
from Paginas.librerias import get_data
from plotly import graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime,timedelta
from itertools import zip_longest
import numpy as np

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
    data['IPC']=S.IPC.reindex(data.index)#list(zip_longest(S.IPC, [], fillvalue=None))
    data['TC']=S.TC.reindex(data.index)#list(zip_longest(S.TC, [], fillvalue=None))
    for col in ["Canasta Basica","Linea Indigencia","Linea Pobreza","SalMVM","Haber Jub"]:
        data[f'{col}-real'] = S.IPC[-1]*data[col]/data['IPC']#data.apply(lambda row: row[f'{col}'] / row['IPC'] if row['IPC'] is not None else None, axis=1)
        data[f'{col}-USD'] = data[col]/data['TC']#data.apply(lambda row: row[f'{col}'] / row['TC'] if row['TC'] is not None else None, axis=1)   
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

@st.cache_resource(show_spinner=False)
def plot_empleo(data):
    fig=make_subplots(specs=[[{"secondary_y": True}]]) 
    fig.add_trace(go.Scatter(x=data.index,y=data["actividad"]*100,name="Actividad",marker_color="rgb(220, 20, 60)",fill="tozeroy",fillcolor=red,line=dict(width=3)),secondary_y=False)
    fig.add_trace(go.Scatter(x=data.index,y=data["empleo"]*100,name="Empleo",marker_color="green",line=dict(width=3),fill="tozeroy",fillcolor=green),secondary_y=False)
    fig.add_trace(go.Scatter(x=data.index,y=data["desempleo"]*100,name="Desempleo",marker_color="royalblue",line=dict(width=3,dash="dashdot")),secondary_y=True)
    fig.add_trace(go.Scatter(x=data.index,y=data['sub-total']*100,name='Subempleados',marker_color=black,line=dict(width=2.5)),secondary_y=True)
    fig.add_trace(go.Scatter(x=data.index,y=data['sub-dem']*100,name='Sub-Demandantes',marker_color='violet',line=dict(width=2,dash='dash')),secondary_y=True)
    fig.add_trace(go.Scatter(x=data.index,y=data['sub-Ndem']*100,name='Sub-No Demandantes',marker_color='burlywood',line=dict(width=2,dash='dash')),secondary_y=True)
    fig.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1),barmode='stack',bargap=0,height=450,legend=dict(
                                        orientation="h",
                                        yanchor="bottom",
                                        y=1.05,
                                        xanchor="right",
                                        x=1,
                                    bordercolor=black,
                                    borderwidth=2
                                ),
                                yaxis=dict(title="%-Empleo/Actividad",showgrid=False, zeroline=True, showline=True),
                                yaxis2=dict(title="%-Desempleo/Subocupados",showgrid=True, zeroline=False, showline=True)
                                )
    if S.start_pobreza <=2015:
        fig.add_vrect(x0=f"2015-07",x1=f"2016-04",fillcolor=black, opacity=1, line_width=0,label=dict(textposition="top center",font=dict(size=14, color='black')))
    elif S.start_pobreza==2016:
        fig.add_vrect(x0=f"2016-01",x1=f"2016-04",fillcolor=black, opacity=1, line_width=0,label=dict(textposition="top left",font=dict(size=14, color='black')))
    st.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)

@st.cache_resource(show_spinner=False)
def plot_salarios(data):
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=data.index,y=data['IS Real-Total'],name='Total',marker_color=black,line=dict(width=2)))
    fig.add_trace(go.Scatter(x=data.index,y=data['IS Real-Formal'],name='Sector Formal'))
    fig.add_trace(go.Scatter(x=data.index,y=data['IS Real-Informal'],name='Sector Informal'))
    fig.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1),barmode='stack',bargap=0,height=450,legend=dict(
                                        orientation="h",
                                        yanchor="bottom",
                                        y=1.05,
                                        xanchor="right",
                                        x=1,
                                    bordercolor=black,
                                    borderwidth=2
                                ),
                                yaxis=dict(title="Índice (base Oct 2016=100)",showgrid=True, zeroline=True, showline=True),
                                )
    st.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)
    
@st.cache_resource(show_spinner=False)
def plot_pobreza_indigencia(data):
    fig=go.Figure()
    st.write(data)
    st.write(data.loc[:'II Sem. 2007'])
    fig.add_trace(go.Scatter(x=data.index,y=np.full(len(data.index), np.nan),showlegend=False,name="",line=dict(width=0)))
    fig.add_trace(go.Scatter(x=data.loc[:'I Sem. 2016'].index,y=data.loc[:'I Sem. 2016']["Indigencia"]*100,name="Indigencia",line=dict(width=2.5),fill="tozeroy",legendgroup="Indigencia",showlegend=False,marker_color="#665A48",fillcolor="#D0B8A8",mode="lines"))
    fig.add_trace(go.Scatter(x=data.loc[:'I Sem. 2016'].index,y=data.loc[:'I Sem. 2016']["Pobreza"]*100,name="Pobreza",line=dict(width=2.5),fill="tozeroy",legendgroup="Pobreza",showlegend=False,marker_color="indigo",fillcolor="#BEADFA",mode="lines"))
    fig.add_trace(go.Scatter(x=data.loc['I Sem. 2010':'I Sem. 2016'].index,y=data.loc['I Sem. 2010':'I Sem. 2016']["Pobreza"]*100,name="Pobreza",line=dict(width=2.5,dash="dash"),marker_color="indigo",showlegend=False,legendgroup="Pobreza",mode="lines"))
    fig.add_trace(go.Scatter(x=data.loc['I Sem. 2010':'I Sem. 2016'].index,y=data.loc['I Sem. 2010':'I Sem. 2016']["Indigencia"]*100,name="Indigencia",line=dict(width=2.5,dash="dash"),showlegend=False,legendgroup="Indigencia",marker_color="#665A48",mode="lines"))
    
    fig.add_trace(go.Scatter(x=data.loc['II Sem. 2007':'I Sem. 2010'].index,y=data.loc['II Sem. 2007':'I Sem. 2010']["Pobreza"]*0,name=" ",line=dict(width=0,dash="dash"),marker_color="indigo",showlegend=False,legendgroup="Pobreza",mode="lines"))
    fig.add_trace(go.Scatter(x=data.loc['II Sem. 2007':'I Sem. 2010'].index,y=data.loc['II Sem. 2007':'I Sem. 2010']["Indigencia"]*0,name=" ",line=dict(width=0,dash="dash"),showlegend=False,legendgroup="Indigencia",marker_color="#665A48",mode="lines"))

    
    fig.add_trace(go.Scatter(x=data.loc[:'II Sem. 2007'].index,y=data.loc[:'II Sem. 2007']["Pobreza"]*100,name="Pobreza",line=dict(width=2.5),marker_color="indigo",legendgroup="Pobreza",fillcolor="#BEADFA",fill="tozeroy",mode="lines"))
    fig.add_trace(go.Scatter(x=data.loc[:'II Sem. 2007'].index,y=data.loc[:'II Sem. 2007']["Indigencia"]*100,name="Indigencia",line=dict(width=2.5),fill="tozeroy",legendgroup="Indigencia",marker_color="#665A48",fillcolor="#D0B8A8",mode="lines"))
    fig.add_vrect(x0="II Sem. 2007",x1="II Sem. 2015", opacity=1, line_width=0,label=dict(text="Intervención del INDEC",textposition="top center",font=dict(size=18, color=black)))
    fig.add_vrect(x0="I Sem. 2010",x1="II Sem. 2015",fillcolor="gray", opacity=0.25, line_width=0)
    fig.add_vline(x="II Sem. 2007",line_width=1,col=black)
    fig.add_vline(x="II Sem. 2015",line_width=1,col=black)

    fig.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1),barmode='stack',bargap=0,height=450,legend=dict(
                                        orientation="h",
                                        yanchor="bottom",
                                        y=1.05,
                                        xanchor="right",
                                        x=1,
                                    bordercolor=black,
                                    borderwidth=2
                                ),
                                yaxis=dict(title="% de la población",showgrid=True, zeroline=True, showline=True),
                                )
    st.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)
    st.caption("Entre 2010 y 2015 los datos son estimaciones realizadas por el :blue[**ODSA**]. Al ser estimaciones anuales, el dato se repite para ambos semestres de cada año.")

@st.cache_resource(show_spinner=False)
def plot_ingresos(data:pd.DataFrame):
    data.columns=["Canasta Basica","Linea Indigencia","Linea Pobreza","SalMVM","Haber Jub"]
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=data.index,y=data["SalMVM"],name="",showlegend=False,line=dict(width=0),marker_color=navy))
    if 2007<= S.start_pobreza <=2016:
        fig.add_vrect(x0=f"{S.start_pobreza}-01",x1=f"2016-04",fillcolor=black, opacity=1, line_width=0,label=dict(textposition="top center",font=dict(size=14, color='black')))
    elif 2007> S.start_pobreza:
        fig.add_vrect(x0=f"2007-01",x1=f"2016-04",fillcolor=black, opacity=1, line_width=0,label=dict(textposition="top center",font=dict(size=14, color='black')))
    fig.add_trace(go.Scatter(x=data.index,y=data["Linea Indigencia"],name="Línea de indigencia",fill="tozeroy",fillcolor="#F38BA0",line=dict(width=2),mode="none"))
    fig.add_trace(go.Scatter(x=data.index,y=data["Linea Pobreza"],name="Línea de Pobreza",fill="tozeroy",line=dict(width=2),mode="none"))
    fig.add_trace(go.Scatter(x=data.index,y=data["Canasta Basica"],name="Canasta Básica",fill="tozeroy",fillcolor="#B2B8A3",line=dict(width=2),mode="none"))
    fig.add_trace(go.Scatter(x=data.index,y=data["SalMVM"],name="Salario Mín. Vit. y Mov.",line=dict(width=3),marker_color=navy))
    fig.add_trace(go.Scatter(x=data.index,y=data["Haber Jub"],name="Haber Jubilatorio Mínimo",line=dict(width=3),marker_color="#632626"))

    ult=S.IPC.index[-1]
    fig.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1),barmode='stack',bargap=0,height=450,legend=dict(
                                        orientation="h",
                                        yanchor="bottom",
                                        y=1.05,
                                        xanchor="right",
                                        x=1,
                                    bordercolor=black,
                                    borderwidth=2
                                ),
                                    yaxis=dict(showgrid=False, zeroline=True, showline=True),
                                    )

    if S.metrica_ingresos=='Pesos Corrientes':
        fig['layout']['yaxis']['title']='ARS'
        fig['layout']['yaxis']['type']='log'
    elif S.metrica_ingresos=='Moneda Constante':
        fig['layout']['yaxis']['title']=f"Pesos de {meses_espanol[ult.month]}-{ult.year}"
    else:
        fig['layout']['yaxis']['title']=f"USD-TC Oficial"
    st.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)

def make_pobreza_web():
    salarios=S.salarios
    empleo=S.empleo
    indicesalarios=salarios[['IS Real-Total','IS Real-Formal','IS Real-Informal']]
    indicesalarios.dropna(inplace=True)
    c1,c2=st.columns((0.7,0.3),vertical_alignment='bottom')
    c1.number_input(value=2016,label='Datos desde',min_value=2004,max_value=2024,key="start_pobreza")
    c2.link_button(":blue[**Descargar datos:\nEmpleo y Pobreza**]",url="https://1drv.ms/x/c/56f917c917f2e2f5/EfXi8hfJF_kggFZ2FQAAAAAB010QqFpwX5jKQsspWhva-A?e=Lsp49b",use_container_width=True)
    salarios=salarios.loc[f"{S.start_pobreza}":]
    empleo=empleo.loc[f"{S.start_pobreza}":]
    c1,c2=st.columns(2) 
    with c1.container(border=True):
        st.subheader('Actividad, empleo y desempleo')
        plot_empleo(empleo)
    with c2.container(border=True):
        c21,c22=st.columns(2)
        c21.subheader('Indice de Salarios Reales')
        c22.slider('Datos desde:',min_value=2016,max_value=2024,key='start_IS',value=2020)
        indicesalarios=indicesalarios.loc[f"{S.start_IS}":]
        plot_salarios(indicesalarios)
        st.caption('Índice realizado en base al índice de salarios publicado por el INDEC y el IPC Nacional, tomando de base Octubre del 2016.')
    c1,c2=st.columns(2)
    with c1.container(border=True):
        st.subheader('Tasa de pobreza indigencia')
        plot_pobreza_indigencia(S.pobind)
    with c2.container(border=True):
        st.subheader('Sal Min Vit y Mov & Haber Min Jub')
        st.radio('Datos-Ingresos',label_visibility='collapsed',options=['Pesos Corrientes','Moneda Constante','Dólares'],horizontal=True,key='metrica_ingresos')

        if S.metrica_ingresos=='Pesos Corrientes':
            plot_ingresos(salarios[["Canasta Basica","Linea Indigencia","Linea Pobreza","SalMVM","Haber Jub"]])
        elif S.metrica_ingresos=='Moneda Constante':
            plot_ingresos(salarios[["Canasta Basica-real","Linea Indigencia-real","Linea Pobreza-real","SalMVM-real","Haber Jub-real"]])
        else:
            plot_ingresos(salarios[["Canasta Basica-USD","Linea Indigencia-USD","Linea Pobreza-USD","SalMVM-USD","Haber Jub-USD"]])