#from Paginas.librerias import *
import streamlit as st
from streamlit import session_state as S
from _globals_ import *
from Paginas.librerias import get_data
from plotly import graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime,timedelta

@st.cache_resource(show_spinner=False)
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
    precios=data.copy()
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
    data={pd.Timestamp(date.year, date.month, 1): value for date, value in data.items()}
    rem=pd.DataFrame(data.values(),index=data.keys(),columns=['REM'])
    
    return precios, rem

@st.cache_resource(show_spinner=False)
def plot_inflacion(data,rem,start,end):
    rem_IA=[]
    for i in range(len(rem.index)-1):
        prod=1
        ind_t=rem.index[i]
        inf_M=data.loc[pd.Timestamp(ind_t.year-1, ind_t.month, 1):,'IPC-InfM']
        for inf in inf_M[1:]:
            prod*=(1+inf)
        for t in rem.iloc[0:i]['REM']:
            prod*=(1+t)
        rem_IA.append((prod-1)*100)
    rem_IA.append(rem['REM'][-1]*100) 
    data=data.loc[f"{start}":f"{end}"]
    fig=make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=data.index,y=data["IPC-InfA"]*100,name="Inflación Interanual",marker_color="green",mode='lines+markers'),secondary_y=False)
    fig.add_trace(go.Bar(x=data.index,y=data["IPC-InfM"]*100,name="Inflación Mensual",marker_color=green),secondary_y=True)
    if rem.index[0].year<=end:
        fig.add_trace(go.Bar(x=rem.index[:-1],y=rem['REM'][:-1]*100,name='Infl. Esperada',marker_color='crimson',legendgroup='rem'),secondary_y=True)
        fig.add_trace(go.Scatter(x=rem.index,y=rem_IA,name='Infl. Esperada-IA',marker_color='crimson',showlegend=False,legendgroup='rem'),secondary_y=False)
    if (start in range (2007,2015)) or (end in range (2007,2015)) or (2007<=end and 2015>=start):
        fig.add_vrect(x0=f"{max(2007,start)}-01", x1=f"{min(2015,end)}-12", 
            fillcolor="lightslategrey", opacity=0.25, line_width=0,label=dict(text="Intervención del INDEC",textposition="top center",font=dict(size=14, color='black')))
    fig.update_layout(hovermode="x unified", margin=dict(l=1, r=1, t=25, b=1),height=450,bargap=0.2,legend=dict(
                                        orientation="h",
                                        yanchor="bottom",
                                        y=-0.2,
                                        xanchor="center",
                                        x=0.5,
                                        bordercolor=black,
                                        borderwidth=2
                                    ),
                                    yaxis=dict(title="%-Var. Interanual",showgrid=False, zeroline=True, showline=True),
                                    yaxis2=dict(title='%-Var. Mensual', side='right',showgrid=False, zeroline=True, showline=True)
                                    )
    st.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)

@st.cache_resource(show_spinner=False)
def plot_categorias(data:pd.DataFrame,start,end):
    data=data.loc[f"{start}":f"{end}"]
    col=S.col_categoria
    fig=make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=data.index,y=data[f"{col}-InfA"]*100,name="Var. Interanual",marker_color=navy,mode='lines'),secondary_y=False)
    fig.add_trace(go.Bar(x=data.index,y=data[f"{col}-InfM"]*100,name="Var. Mensual",marker_color='cornflowerblue'),secondary_y=True)
    fig.update_layout(hovermode="x unified", margin=dict(l=1, r=1, t=25, b=1),height=450,bargap=0.2,legend=dict(
                                        orientation="h",
                                        yanchor="bottom",
                                        y=-0.2,
                                        xanchor="center",
                                        x=0.5,
                                        bordercolor=black,
                                        borderwidth=2
                                    ),
                                    yaxis=dict(title="%-Var. Interanual",showgrid=False, zeroline=True, showline=True),
                                    yaxis2=dict(title='%-Var. Mensual', side='right',showgrid=False, zeroline=True, showline=True)
                                    )
    st.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)

@st.cache_resource(show_spinner=False)
def make_metrics(precios,rem):
    with st.container(border=True):
        c11,c12,c13,c14=st.columns(4,vertical_alignment='center')
        c11.metric('Inflación Mensual',value=f'{precios['IPC-InfM'][-1]*100:.2f}%',delta=f'{(precios['IPC-InfM'][-1]-precios['IPC-InfM'][-2])*100:.2f} PP',delta_color='inverse')
        c12.metric('Inflación Interanual',value=f'{precios['IPC-InfA'][-1]*100:.2f}%',delta=f'{(precios['IPC-InfA'][-1]-precios['IPC-InfA'][-2])*100:.2f} PP',delta_color='inverse')
        c13.metric('Inflación Núcleo',value=f'{precios['Nucleo-InfM'][-1]*100:.2f}%',delta=f'{(precios['Nucleo-InfM'][-1]-precios['Nucleo-InfM'][-2])*100:.2f} PP',delta_color='inverse')
        t1=pd.Timestamp(precios.index[-1].year,precios.index[-1].month+1,1)
        c14.metric(f'REM para {meses_espanol[t1.month]}',f'{rem['REM'].loc[t1]*100:.2f}%',delta=f'{(rem['REM'].loc[t1]-precios['IPC-InfM'][-1])*100:.2f} PP',delta_color='inverse')
        st.write(precios)
@st.cache_data(show_spinner=False)
def data_selected(categoria_IPC):
    data:pd.DataFrame=S.precios.copy()
    options={'IPC Núcleo':'Nucleo',
            'IPC Estacionales':'Estacionales',
            'IPC Regulados':'Regulados',
            'IPIM':'IPIM',
            'IPIB':'IPIB',
            'Alimentos y bebidas no alcohólicas':'Alimentos',
            'Vivienda, agua, electricidad y otros combustibles':'Vivienda',
            'Salud':'Salud',
            'Transporte':'Transporte'}
    data=data[[options[categoria_IPC],f'{options[categoria_IPC]}-InfM',f'{options[categoria_IPC]}-InfA']]
    data_categoria=data.dropna().copy()
    col_categoria = options[categoria_IPC]
    return data_categoria,col_categoria

def make_precios_web():
    precios=S.precios.copy()
    rem=S.rem.copy()
    c1,c2=st.columns((0.7,0.3),vertical_alignment='center')
    with c1:make_metrics(precios,rem)
    c2.link_button(":blue[**Descargar datos:\nPrecios**]",url="https://1drv.ms/x/c/56f917c917f2e2f5/QfXi8hfJF_kggFZ4FQAAAAAAr3wUsfOZo5CUFA",use_container_width=True)
    c1,c2=st.columns(2,vertical_alignment='bottom')
    with c1.container(border=True):
        st.subheader("Inflación - IPC(Base 2016=100)$\\text{ }^{1;2}$")
        st.slider(value=[2022,precios.index[-1].year],label="Datos desde-hasta",min_value=1943,max_value=precios.index[-1].year,key="start_precios")
        plot_inflacion(precios,rem,S.start_precios[0],S.start_precios[1])
    with c2.container(border=True):
        st.subheader('Componentes y Categorías del IPC')
        c21,c22=st.columns(2,vertical_alignment='bottom')
        c21.selectbox('Indicador',label_visibility='collapsed',options=['IPC Núcleo',
                                                                        'IPC Estacionales',
                                                                        'IPC Regulados',
                                                                        'IPIM',
                                                                        'IPIB',
                                                                        'Alimentos y bebidas no alcohólicas',
                                                                        'Vivienda, agua, electricidad y otros combustibles',
                                                                        'Salud',
                                                                        'Transporte',],key='categoria_IPC')
        S.data_categoria,S.col_categoria=data_selected(S.categoria_IPC)
        c22.slider(value=[2020,S.data_categoria.index[-1].year],label="Datos desde-hasta",min_value=S.data_categoria.index[0].year,max_value=S.data_categoria.index[-1].year,key='start_categorias')
        plot_categorias(S.data_categoria,S.start_categorias[0],S.start_categorias[1])
    st.divider()
    st.caption("$\\text{ }^1$Debido a la intervención del INDEC entre 2007 y 2015(zona marcada en gris), los datos son provisorios, creados a partir del IPC de San Luís y el IPC de CABA.")
    st.caption("$\\text{ }^2$Los datos anteriores a 2016 son el IPC de GBA, empalmados con el reciente IPC nacional con base 2016=100.")

