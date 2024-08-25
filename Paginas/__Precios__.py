#from Paginas.librerias import *
import streamlit as st
from streamlit import session_state as S
from _globals_ import *
from Paginas.librerias import get_data
from plotly import graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime,timedelta

st.cache_resource(show_spinner=False)
def load_precios(end):
    his_data=pd.read_csv("His Data/his-precios.csv",delimiter=";")
    his_data['Unnamed: 0'] = pd.to_datetime(his_data.iloc[:, 0].values, format='%d/%m/%Y')
    his_data.set_index('Unnamed: 0', inplace=True)
    ids=[
        "145.3_INGNACNAL_DICI_M_15",
        "148.3_INUCLEONAL_DICI_M_19",
        "148.3_IESTACINAL_DICI_M_25",
        "148.3_IREGULANAL_DICI_M_22",
        "146.3_IALIMENNAL_DICI_M_45",
        "146.3_IVIVIENNAL_DICI_M_52",
        "146.3_ISALUDNAL_DICI_M_18",
        "146.3_ITRANSPNAL_DICI_M_23",
        "448.1_NIVEL_GENERAL_0_0_13_46",
        "449.1_NIVEL_GENERAL_0_0_13_97"
        ]
    cols=["IPC","Nucleo","Estacionales","Regulados","Alimentos","Vivienda","Salud",'Transporte',"IPIM","IPIB"]
    data=get_data(ids,start_date="2024-01-01",col_list=cols)
    data.index = pd.to_datetime(data.index, format='%d/%m/%Y')
    his_data.columns=data.columns
    data.reindex(columns=his_data.columns)
    data=pd.concat([his_data,data],axis=0)
    for col in data.columns:
        data[f'{col}-InfM']=data[col].pct_change(1)
        data[f'{col}-InfA']=data[col].pct_change(12)

    ids=[
        "430.1_REM_IPC_NAL_T_M_0_0_25_28",
        "430.1_MEDIANA_IPT_1_M_0_0_31_29",
        "430.1_MEDIANA_IPT_2_M_0_0_31_73",
        "430.1_MEDIANA_IPT_3_M_0_0_31_26",
        "430.1_MEDIANA_IPT_4_M_0_0_31_49",
        "430.1_MEDIANA_IPT_5_M_0_0_31_100",
        "430.1_MEDIANA_IPT_6_M_0_0_31_24",
        "430.1_MEDIANA_IP_12_M_0_0_27_96"
    ]
    cols=['t','t+1','t+2','t+3','t+4','t+5','t+6','t+12']
    rem=get_data(ids,start_date='2024-01-01',col_list=cols)
    date=rem.index[-1]
    rem_t=rem.iloc[-1]
    data={date:rem_t[0]}
    for i in range(1,8):
        data[(date+timedelta(days=31*int(rem_t.index[i][2:])))]=rem_t[i]
    rem=pd.DataFrame(data.values(),index=data.keys(),columns=['REM'])
    
    return data, rem

def plot_inflacion(data,rem,start,end):
    data=data.loc[f"{start}":f"{end}"]
    data.index=data.index.strftime('%b-%Y')
    fig=make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=data.index,y=data["IPC-InfA"]*100,name="Inflación Interanual",marker_color="green"),secondary_y=False)
    fig.add_trace(go.Bar(x=data.index,y=data["IPC-InfM"]*100,name="Inflación Mensual",marker_color=green),secondary_y=True)
    if rem.index[-1].year<=end:
        rem.index=rem.index.strftime('%b-%Y')
        fig.add_trace(go.Bar(x=rem.index[:-1],y=rem['REM'][:-1]*100,name='Infl. Esperada',marker_color='crimson',legendgroup='rem'),secondary_y=False)
        fig.add_trace(go.Bar(x=rem.index[-1],y=rem['REM'][-1]*100,name='Infl. Esperada-IA',marker_color='crimson',showlegend=False,legendgroup='rem'),secondary_y=True)
    #if (2007<S.start_precios[0] and 2015<S.start_precios[0]) or (2007>S.start_precios[0] and 2015>S.start_precios[0]):
    if (start in range (2007,2015)) or (end in range (2007,2015)) or (2007<=end and 2015>=start):
        fig.add_vrect(x0=f"{max(2007,start)}-01", x1=f"{min(2015,end)}-12", 
            fillcolor="gray", opacity=0.25, line_width=0,label=dict(text="Intervención del INDEC",textposition="top center",font=dict(size=14, color='black')))
    fig.update_layout(margin=dict(l=1, r=1, t=75, b=1),height=450,bargap=0.2,legend=dict(
                                        orientation="h",
                                        yanchor="bottom",
                                        y=-0.3,
                                        xanchor="center",
                                        x=0.5,
                                        bordercolor=black,
                                        borderwidth=2
                                    ),
                                    yaxis=dict(title="%-Var. Interanual",showgrid=False, zeroline=True, showline=True),
                                    yaxis2=dict(title='%-Var. Mensual', side='right',showgrid=False, zeroline=True, showline=True)
                                    )
    st.plotly_chart(fig,use_container_width=True)


def make_precios_web():
    precios=S.precios
    rem=S.rem
    c1,c2=st.columns((0.7,0.3),vertical_alignment='center')
    c1,c2=st.columns(2)
    with c1.container(border=False):
        st.subheader("Inflación - IPC(Base 2016=100)$\\text{ }^{1;2}$")
        st.slider(value=[2010,precios.index[-1].year],label="Datos desde-hasta",min_value=1943,max_value=precios.index[-1].year,key="start_precios")
        plot_inflacion(precios,rem,S.start_precios[0],S.start_precios[1])
    with c2.container(border=False):
        st.header('Componentes del IPC')
    c1,c2=st.columns(2)
    with c1.container(border=False):
        st.header('TC y Brecha')
    with c2.container(border=False):
        st.header('Expectativas de Inflación')
